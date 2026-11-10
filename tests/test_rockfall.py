import numpy as np
import pandas as pd
import pytest
from scipy import stats

from ds_toolbox import rockfall as rf


def test_energy_is_half_m_v_squared_in_kj():
    assert rf.energy_kj(2000, 10) == pytest.approx(100.0)


def test_simulation_has_the_right_rate_and_order():
    zones = rf.true_zones()
    ev = rf.simulate(zones, minutes=rf.MIN_PER_YEAR * 20, seed=1)
    assert ev["minute"].is_monotonic_increasing
    per_year = ev.groupby("zone").size() / 20
    for z in zones:
        assert per_year[z.name] == pytest.approx(z.rate_per_year(), rel=0.1)


def _events(rows):
    return pd.DataFrame(rows, columns=["minute", "mass", "speed"]).assign(
        zone="z", energy=lambda d: rf.energy_kj(d["mass"], d["speed"]))


def test_net_rules():
    nine = 9 * 60                                         # 09:00 on day 0
    ev = _events([
        (nine, 2500, 10),                                 # 125 kJ: held, net now 2500 kg
        (nine + 10, 1500, 30),                            # 675 kJ into a full net: breaks through
        (nine + 20, 3000, 30),                            # 1350 kJ: always breaks through
        (nine + 1440, 1500, 30),                          # next day after 08:00: net was emptied
    ])
    assert rf.through_net(ev).tolist() == [False, True, True, False]


def test_analytic_probability_matches_monte_carlo():
    mass, speed = stats.expon(scale=400), stats.norm(30, 4)
    rng = np.random.default_rng(0)
    m, v = mass.rvs(size=400_000, random_state=rng), speed.rvs(size=400_000, random_state=rng)
    mc = (rf.energy_kj(m, v) >= 500).mean()
    assert rf.p_energy_at_least(mass, speed, 500) == pytest.approx(mc, rel=0.03)


def test_breach_rate_grows_with_the_full_net_share():
    zones = rf.true_zones()
    assert rf.breach_rate_analytic(zones, 0.5) > rf.breach_rate_analytic(zones, 0.0) > 0


def test_fitting_recovers_a_known_family():
    rng = np.random.default_rng(2)
    m = stats.lognorm(s=0.8, scale=300).rvs(size=4000, random_state=rng)
    fit = rf.fit_mass(m, "lognormal")
    assert fit.median() == pytest.approx(300, rel=0.05)
    for fam in ("gamma", "weibull", "exponential"):
        assert rf.fit_mass(m, fam).mean() > 0
    season = pd.DataFrame({"zone": "a", "mass": m[:90], "speed": rng.normal(9, 2, 90)})
    z = rf.fit_zone(season, "a", "exponential", minutes=90 * 1440)
    assert z.rate_per_year() == pytest.approx(365.25, rel=1e-6)


def test_estimate_and_season():
    zones = rf.true_zones()
    est = rf.estimate_breach_rate(zones, years=3000, seed=1)
    assert 0.008 < est < 0.03                         # the truth is about 0.016 a year
    s = rf.season(days=90, seed=2019)
    assert set(s["zone"]) == {"zone 1", "zone 2"} and s["time"].is_monotonic_increasing
    assert s["time"].min() >= pd.Timestamp("2019-01-01") and s["time"].max() < pd.Timestamp("2019-04-01")
