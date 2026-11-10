import datetime as dt

import numpy as np
import pandas as pd
import pytest

from ds_toolbox import forecasting as fc


def _grid(days=120, seed=0):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=days, freq="D")
    hours = np.arange(24)
    weekly = np.where(dates.day_of_week >= 5, -20.0, 0.0)[:, None]
    daily = 30 * np.sin(2 * np.pi * (hours - 6) / 24)[None, :]
    values = 300 + weekly + daily + rng.normal(0, 2, size=(days, 24))
    return pd.DataFrame(values, index=pd.DatetimeIndex(dates, name="date"), columns=hours)


def test_calendar_one_hot_and_holiday():
    dates = pd.date_range("2024-12-23", periods=3, freq="D")
    cal = fc.day_calendar(dates, holidays={dt.date(2024, 12, 25)})
    assert cal.filter(like="wd").sum(axis=1).tolist() == [1.0, 1.0, 1.0]
    assert cal["wd0"].iloc[0] == 1.0 and cal["holiday"].tolist() == [0.0, 0.0, 1.0]


def test_table_uses_only_the_previous_days():
    grid = _grid(30)
    X, y = fc.day_ahead_table(grid)
    assert len(X) == len(y) == (30 - 14) * 24       # the 336-hour lag needs two weeks
    first = X.index[0]
    day = first.normalize()
    prev = grid.loc[day - pd.Timedelta(days=1)]
    assert X.loc[first, "yesterday_mean"] == pytest.approx(prev.mean())
    assert X.loc[first, "yesterday_last_hour"] == pytest.approx(prev[23])
    assert X.loc[first, "load_lag24"] == pytest.approx(prev[first.hour])


def test_windows_line_up():
    grid = _grid(20)
    w = fc.cnn_windows(grid)
    assert w["past"].shape == (13, 168) and w["y"].shape == (13, 24) and w["cal"].shape == (13, 10)
    assert np.allclose(w["base"][0], grid.iloc[0].to_numpy())      # day 7's base is day 0
    assert np.allclose(w["past"][0][-24:], grid.iloc[6].to_numpy())  # the week ends the day before


def test_the_cnn_learns_to_beat_last_week():
    pytest.importorskip("torch")
    # a load that grows 1 MW a day: "the same day last week" is always ~7 MW too low, and a
    # network that learns anything at all learns to add it back
    grid = _grid(200) + np.arange(200)[:, None] * 1.0
    w = fc.cnn_windows(grid)
    n = len(w["y"])
    train = {k: v[: n - 30] for k, v in w.items()}
    test = {k: v[n - 30:] for k, v in w.items()}
    model = fc.CNNForecaster(epochs=60, val_days=30, patience=60).fit(train)
    pred = model.predict(test)
    assert pred.shape == (30, 24)
    cnn_mae = np.abs(pred - test["y"]).mean()
    base_mae = np.abs(test["base"] - test["y"]).mean()
    assert cnn_mae < 0.6 * base_mae
    assert len(model.history) >= 1


def test_too_few_days_refused():
    pytest.importorskip("torch")
    w = fc.cnn_windows(_grid(40))
    with pytest.raises(ValueError, match="too few"):
        fc.CNNForecaster(val_days=30).fit(w)
