"""A rockfall slope with a protection net -- a seeded world with a known truth.

The model follows the FHNW probability challenge "Steinschlag" (autumn 2019; report in
``riccardito/FHNW-Projects``): rocks fall from two zones of a slope into one net above a road.
Each rock has a mass and a speed, so an energy ``E = 0.5 m v^2`` (kJ). The net is emptied every
day at 08:00. A rock of 1000 kJ or more breaks through; a rock of 500 to 1000 kJ breaks through
only if the net already holds 2000 kg or more.

**Where the parameters come from.** Zone 1's mass (gamma) and speed (normal) are fitted to the
68 observations the report prints; its time between rocks is the mean gap of those observations.
The report chose a lognormal for the masses, and on those 68 rocks a lognormal fits a little
better (AIC 1011.5 against 1015.6) -- but its tail puts a 13-tonne rock at 4 in 10 000 where the
gamma puts it at 1 in 10 billion. The truth here is the gamma, chosen on purpose: the two families
agree on every rock the data holds and disagree exactly where the risk is.
Zone 2's time between rocks is the report's own fit (lognormal, minutes). Zone 2's masses and
speeds are not in the report, so they are *chosen* -- an exponential mass and a normal speed whose
means make the whole model reproduce the report's result, about 0.016 rocks through the net a year.
The truth here is therefore invented on purpose: it is what lets a challenge measure how close an
estimate from one season of data comes to it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import integrate, stats

MIN_PER_YEAR = 365.25 * 24 * 60
BREAK_KJ, WEAK_KJ, NET_CAPACITY_KG, CLEAR_HOUR = 1000.0, 500.0, 2000.0, 8


@dataclass(frozen=True)
class Zone:
    name: str
    gap: stats.rv_continuous       # minutes between rocks
    mass: stats.rv_continuous      # kg
    speed: stats.rv_continuous     # m/s

    def rate_per_year(self) -> float:
        return MIN_PER_YEAR / float(self.gap.mean())


def true_zones() -> tuple[Zone, Zone]:
    """The two zones of the seeded world (see the module docstring for each parameter's source)."""
    zone1 = Zone("zone 1", gap=stats.expon(scale=1830.0),
                 mass=stats.gamma(a=1.1405, scale=551.19), speed=stats.norm(8.788, 1.975))
    zone2 = Zone("zone 2", gap=stats.lognorm(s=0.86983, scale=np.exp(7.965341)),
                 mass=stats.expon(scale=ZONE2_MASS_MEAN), speed=stats.norm(37.0, 5.0))
    return zone1, zone2


ZONE2_MASS_MEAN = 115.0   # kg -- calibrated so the whole model gives the report's ~0.016 a year
                          # (400 000 simulated years: 0.0154 at 114 kg, 0.0171 at 116 kg)


def energy_kj(mass, speed):
    return 0.5 * np.asarray(mass) * np.asarray(speed) ** 2 / 1000.0


def simulate(zones, minutes: float, seed: int = 0) -> pd.DataFrame:
    """Every rock that falls in ``minutes``, both zones, in time order."""
    rng = np.random.default_rng(seed)
    parts = []
    for z in zones:
        n = int(minutes / float(z.gap.mean()) * 1.2 + 50)
        times = np.cumsum(z.gap.rvs(size=n, random_state=rng))
        while times[-1] < minutes:                                  # rare: draw more
            times = np.concatenate([times, times[-1] + np.cumsum(z.gap.rvs(size=n, random_state=rng))])
        times = times[times < minutes]
        k = len(times)
        mass = z.mass.rvs(size=k, random_state=rng)
        speed = np.clip(z.speed.rvs(size=k, random_state=rng), 0, None)
        parts.append(pd.DataFrame({"minute": times, "zone": z.name, "mass": mass, "speed": speed}))
    ev = pd.concat(parts).sort_values("minute", ignore_index=True)
    ev["energy"] = energy_kj(ev["mass"], ev["speed"])
    return ev


def through_net(events: pd.DataFrame) -> np.ndarray:
    """Which rocks break through, given the net's load since the last 08:00 clearing."""
    day = np.floor((events["minute"].to_numpy() - CLEAR_HOUR * 60) / 1440.0)
    energy, mass = events["energy"].to_numpy(), events["mass"].to_numpy()
    strong = energy >= BREAK_KJ
    held = np.where(strong, 0.0, mass)                    # a rock that breaks through adds nothing
    load_before = pd.Series(held).groupby(day).cumsum().to_numpy() - held
    weak = (energy >= WEAK_KJ) & (energy < BREAK_KJ) & (load_before >= NET_CAPACITY_KG)
    return strong | weak


def p_energy_at_least(mass_dist, speed_dist, kj: float) -> float:
    """P(0.5 m v^2 >= kj) for independent mass and speed: one integral over the speed."""
    def integrand(v):
        return mass_dist.sf(2000.0 * kj / max(v, 1e-9) ** 2) * speed_dist.pdf(v)

    lo, hi = max(0.0, speed_dist.ppf(1e-9)), speed_dist.ppf(1 - 1e-9)
    value, _ = integrate.quad(integrand, lo, hi, limit=200)
    return float(value)


def breach_rate_analytic(zones, net_full_share: float = 0.0) -> float:
    """Rocks through the net per year: every 1000 kJ rock, plus the 500-1000 kJ rocks that arrive
    while the net is full (``net_full_share`` = the share of rocks that meet a full net)."""
    total = 0.0
    for z in zones:
        strong = p_energy_at_least(z.mass, z.speed, BREAK_KJ)
        weak = p_energy_at_least(z.mass, z.speed, WEAK_KJ) - strong
        total += z.rate_per_year() * (strong + net_full_share * weak)
    return total


def fit_mass(masses, family: str) -> stats.rv_continuous:
    """A mass distribution fitted by maximum likelihood, the location fixed at 0."""
    m = np.asarray(masses, dtype=float)
    m = m[m > 0]
    dist = {"lognormal": stats.lognorm, "gamma": stats.gamma, "weibull": stats.weibull_min,
            "exponential": stats.expon}[family]
    params = dist.fit(m, floc=0)
    return dist(*params)


def fit_zone(season: pd.DataFrame, zone: str, family: str, minutes: float) -> Zone:
    """A zone estimated from one season: Poisson timing, a fitted mass family, a normal speed."""
    s = season[season["zone"] == zone]
    gap = stats.expon(scale=minutes / max(len(s), 1))
    mu, sd = stats.norm.fit(s["speed"])
    return Zone(zone, gap=gap, mass=fit_mass(s["mass"], family), speed=stats.norm(mu, sd))


def estimate_breach_rate(zones, years: int = 2000, seed: int = 0) -> float:
    """Rocks through the net per year under ``zones``: the 1000 kJ rocks exactly, the 500-1000 kJ
    rocks through the share of them that meet a full net, simulated over ``years``."""
    ev = simulate(zones, MIN_PER_YEAR * years, seed=seed)
    weak = ((ev["energy"] >= WEAK_KJ) & (ev["energy"] < BREAK_KJ)).to_numpy()
    full_share = float(through_net(ev)[weak].mean()) if weak.any() else 0.0
    return breach_rate_analytic(zones, net_full_share=full_share)


def season(days: int = 90, seed: int = 2019) -> pd.DataFrame:
    """One observed season of the seeded world -- the shape of the course's January-March record."""
    ev = simulate(true_zones(), minutes=days * 1440.0, seed=seed)
    start = pd.Timestamp("2019-01-01")
    ev.insert(0, "time", start + pd.to_timedelta(ev["minute"].round(), unit="min"))
    return ev.drop(columns="minute").round({"mass": 0, "speed": 1, "energy": 3})
