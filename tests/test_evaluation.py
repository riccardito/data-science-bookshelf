import numpy as np
import pandas as pd
import pytest

from ds_toolbox import baselines
from ds_toolbox import evaluation as ev


def test_point_metrics_on_a_known_case():
    y, p = [1.0, 2.0, 4.0], [2.0, 2.0, 2.0]
    assert ev.mae(y, p) == pytest.approx(1.0)
    assert ev.rmse(y, p) == pytest.approx(np.sqrt(5 / 3))
    assert ev.mape(y, p) == pytest.approx((100 + 0 + 50) / 3)


def test_metrics_refuse_bad_input():
    with pytest.raises(ValueError, match="shape"):
        ev.mae([1, 2], [1])
    with pytest.raises(ValueError, match="empty"):
        ev.rmse([], [])
    with pytest.raises(ValueError, match="undefined"):
        ev.mape([0, 1], [1, 1])


def test_mase_is_one_for_the_seasonal_naive_on_a_repeating_trend():
    train = np.arange(20.0)
    # the naive step on a unit-slope line is off by exactly the in-sample scale
    assert ev.mase([20.0, 21.0], [19.0, 20.0], train) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="longer"):
        ev.mase([1.0], [1.0], [1.0], season=1)
    with pytest.raises(ValueError, match="constant"):
        ev.mase([1.0], [1.0], [3.0, 3.0, 3.0])


def test_skill_against_the_baseline():
    assert ev.skill(5.0, 10.0) == pytest.approx(0.5)
    assert ev.skill(12.0, 10.0) < 0
    with pytest.raises(ValueError):
        ev.skill(1.0, 0.0)


def test_splits_never_look_ahead_and_tile_the_tail():
    splits = list(ev.expanding_window_splits(10, initial=4, horizon=2))
    assert [(s.train.stop, s.test.start, s.test.stop) for s in splits] == [(4, 4, 6), (6, 6, 8), (8, 8, 10)]
    for s in splits:
        assert s.train.stop == s.test.start
    assert len(list(ev.expanding_window_splits(10, 4, 2, step=1))) == 5


def test_splits_refuse_impossible_requests():
    with pytest.raises(ValueError, match="short"):
        list(ev.expanding_window_splits(5, 4, 2))
    with pytest.raises(ValueError, match=">= 1"):
        list(ev.expanding_window_splits(5, 0, 2))


def test_backtest_scores_each_fold():
    idx = pd.date_range("2024-01-01", periods=12, freq="D")
    y = pd.Series(np.tile([1.0, 2.0, 3.0], 4), index=idx)
    out = ev.backtest(y, baselines.seasonal_naive(3), initial=6, horizon=3)
    assert list(out["fold"]) == [0, 1]
    assert np.allclose(out["score"], 0.0)  # a perfectly periodic series
    assert out.loc[0, "test_start"] == idx[6]


def test_bootstrap_ci_brackets_the_estimate():
    est, lo, hi = ev.bootstrap_ci(np.arange(100.0), n_boot=500, seed=1)
    assert lo < est < hi
    assert est == pytest.approx(49.5)
    with pytest.raises(ValueError):
        ev.bootstrap_ci([1.0])
