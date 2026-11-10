import datetime as dt

import numpy as np
import pandas as pd
import pytest

from ds_toolbox import features as ft


def _hourly(n=48):
    idx = pd.date_range("2024-03-30 00:00", periods=n, freq="h", tz="UTC")
    return pd.Series(np.arange(n, dtype=float), index=idx, name="load")


def test_lags_shift_and_name():
    y = _hourly(10)
    f = ft.lag_features(y, [2, 1])
    assert list(f.columns) == ["load_lag1", "load_lag2"]
    assert f["load_lag2"].iloc[5] == 3.0 and np.isnan(f["load_lag1"].iloc[0])


def test_a_lag_shorter_than_the_lead_time_is_refused():
    with pytest.raises(ValueError, match="future"):
        ft.lag_features(_hourly(), [23, 24], min_lag=24)
    with pytest.raises(ValueError, match="no lags"):
        ft.lag_features(_hourly(), [])


def test_rolling_mean_ends_before_the_lead_time():
    y = _hourly(10)
    f = ft.rolling_mean_features(y, [3], min_lag=2, prefix="x")
    # at t=6 the window is y[2..4] -> mean 3
    assert f["x_mean3"].iloc[6] == pytest.approx(3.0)


def test_calendar_is_local_time_and_flags_holidays():
    # 2024-03-31 is the spring DST switch in Zurich and Easter Sunday
    idx = pd.date_range("2024-03-30 22:00", periods=4, freq="h", tz="UTC")
    f = ft.calendar_features(idx, holidays={dt.date(2024, 3, 31)})
    assert list(f["hour"]) == [23, 0, 1, 3]  # 02:00 local does not exist that night
    assert list(f["holiday"]) == [0, 1, 1, 1]
    assert f["weekend_or_holiday"].all()
    naive = ft.calendar_features(pd.date_range("2024-01-01", periods=2, freq="D"), tz=None)
    assert list(naive["weekday"]) == [0, 1]


def test_swiss_holidays_for_zurich():
    days = ft.swiss_holidays([2024])
    assert dt.date(2024, 12, 25) in days and dt.date(2024, 8, 1) in days


def test_local_days_mend_both_dst_nights():
    idx = pd.date_range("2024-03-29 23:00", "2024-11-01 22:00", freq="h", tz="UTC")
    y = pd.Series(1.0, index=idx)
    grid = ft.to_local_days(y)
    assert grid.shape[1] == 24 and not grid.isna().any().any()
    assert grid.index[0] == pd.Timestamp("2024-03-30") and grid.index[-1] == pd.Timestamp("2024-11-01")
    # spring: 02:00 never happened -> interpolated; autumn: 02:00 twice -> averaged
    y2 = pd.Series(np.arange(len(idx), dtype=float), index=idx)
    g2 = ft.to_local_days(y2)
    spring = g2.loc["2024-03-31"]
    assert spring[2] == pytest.approx((spring[1] + spring[3]) / 2)
    autumn = g2.loc["2024-10-27"]
    assert autumn[3] - autumn[2] == pytest.approx(1.5)  # 02:00 is the mean of two consecutive hours
    long = ft.from_local_days(g2.iloc[:2])
    assert len(long) == 48 and long.index[25] == pd.Timestamp("2024-03-31 01:00")


def test_local_days_need_an_aware_index():
    with pytest.raises(ValueError, match="aware"):
        ft.to_local_days(pd.Series([1.0], index=pd.date_range("2024-01-01", periods=1, freq="h")))
