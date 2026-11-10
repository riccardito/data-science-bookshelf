"""Features for models of data ordered in time.

The rule this module enforces: a feature for time ``t`` may only use what was known when the
forecast was made. ``lag_features`` therefore takes the forecast lead time explicitly and
refuses lags shorter than it -- a day-ahead model may look 24 hours back, never 23.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


def lag_features(y: pd.Series, lags: Iterable[int], *, min_lag: int = 1,
                 prefix: str | None = None) -> pd.DataFrame:
    """One column per lag: ``y`` shifted by ``lag`` steps. ``min_lag`` is the forecast lead time."""
    lags = sorted(set(lags))
    if not lags:
        raise ValueError("no lags")
    if lags[0] < min_lag:
        raise ValueError(f"lag {lags[0]} is shorter than the lead time {min_lag}: it would use the future")
    name = prefix or (y.name or "y")
    return pd.DataFrame({f"{name}_lag{k}": y.shift(k) for k in lags}, index=y.index)


def rolling_mean_features(y: pd.Series, windows: Iterable[int], *, min_lag: int = 1,
                          prefix: str | None = None) -> pd.DataFrame:
    """The mean of the ``w`` values ending ``min_lag`` steps before ``t``."""
    name = prefix or (y.name or "y")
    past = y.shift(min_lag)
    return pd.DataFrame({f"{name}_mean{w}": past.rolling(w).mean() for w in windows}, index=y.index)


def calendar_features(index: pd.DatetimeIndex, *, tz: str | None = "Europe/Zurich",
                      holidays: Iterable | None = None) -> pd.DataFrame:
    """Hour, weekday, month, a smooth day-of-year, and a holiday flag -- in local time.

    Electricity follows the clock on the wall, not UTC, so an aware index is converted to
    ``tz`` first. ``holidays`` is any collection of dates (``datetime.date``).
    """
    local = index.tz_convert(tz) if (tz and index.tz is not None) else index
    doy = local.day_of_year.to_numpy()
    out = pd.DataFrame({
        "hour": local.hour,
        "weekday": local.day_of_week,
        "month": local.month,
        "doy_sin": np.sin(2 * np.pi * doy / 365.25),
        "doy_cos": np.cos(2 * np.pi * doy / 365.25),
    }, index=index)
    days = set(holidays or ())
    out["holiday"] = np.fromiter((d in days for d in local.date), dtype=bool, count=len(local)).astype(int)
    out["weekend_or_holiday"] = ((out["weekday"] >= 5) | (out["holiday"] == 1)).astype(int)
    return out


def swiss_holidays(years: Iterable[int], canton: str = "ZH") -> set:
    """Public holidays of a canton, from the ``holidays`` package."""
    import holidays as hol

    return set(hol.Switzerland(subdiv=canton, years=list(years)).keys())


def to_local_days(y: pd.Series, tz: str = "Europe/Zurich") -> pd.DataFrame:
    """An hourly UTC series as a grid: one row per local day, one column per wall-clock hour 0-23.

    The two nights a year that break the grid are mended the same way every time: the hour that
    happens twice in October is averaged, the hour that never happens in March is interpolated.
    Days at the ends that are not complete are dropped.
    """
    if y.index.tz is None:
        raise ValueError("the series needs a time-zone-aware index")
    local = y.tz_convert(tz)
    frame = pd.DataFrame({"date": local.index.date, "hour": local.index.hour, "v": local.to_numpy()})
    counts = frame.groupby("date").size()
    grid = frame.groupby(["date", "hour"])["v"].mean().unstack("hour").reindex(columns=range(24))
    grid = grid.interpolate(axis=1, limit_area="inside")
    complete = counts.index[counts >= 23]
    grid = grid.loc[grid.index.isin(complete)].dropna()
    grid.index = pd.DatetimeIndex(pd.to_datetime(grid.index), name="date")
    grid.columns.name = "hour"
    return grid


def from_local_days(grid: pd.DataFrame) -> pd.Series:
    """The inverse view: the grid as one long series indexed by local wall-clock time."""
    long = grid.stack()
    idx = long.index.get_level_values(0) + pd.to_timedelta(long.index.get_level_values(1), unit="h")
    return pd.Series(long.to_numpy(), index=pd.DatetimeIndex(idx, name="local_time"))
