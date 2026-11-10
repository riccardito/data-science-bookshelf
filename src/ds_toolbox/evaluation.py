"""Measuring a model honestly.

Two rules run through the whole shelf. A score means something only next to a baseline (see
``baselines``). And on data ordered in time, a model is only ever tested on the future of what
it was fitted on -- ``expanding_window_splits`` and ``backtest`` enforce that.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass

import numpy as np
import pandas as pd


def _arrays(y_true, y_pred) -> tuple[np.ndarray, np.ndarray]:
    a, b = np.asarray(y_true, dtype=float), np.asarray(y_pred, dtype=float)
    if a.shape != b.shape:
        raise ValueError(f"shape mismatch: {a.shape} vs {b.shape}")
    if a.size == 0:
        raise ValueError("empty input")
    return a, b


def mae(y_true, y_pred) -> float:
    a, b = _arrays(y_true, y_pred)
    return float(np.mean(np.abs(a - b)))


def rmse(y_true, y_pred) -> float:
    a, b = _arrays(y_true, y_pred)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def mape(y_true, y_pred) -> float:
    """Mean absolute percentage error, in percent. Undefined where the truth is 0."""
    a, b = _arrays(y_true, y_pred)
    if np.any(a == 0):
        raise ValueError("MAPE is undefined where y_true == 0")
    return float(np.mean(np.abs((a - b) / a)) * 100)


def mase(y_true, y_pred, y_train, season: int = 1) -> float:
    """MAE scaled by the in-sample MAE of the seasonal-naive forecast: below 1 beats it."""
    a, b = _arrays(y_true, y_pred)
    train = np.asarray(y_train, dtype=float)
    if train.size <= season:
        raise ValueError("y_train must be longer than the season")
    scale = np.mean(np.abs(train[season:] - train[:-season]))
    if scale == 0:
        raise ValueError("the training series is constant at this season")
    return float(np.mean(np.abs(a - b)) / scale)


def skill(score: float, baseline_score: float) -> float:
    """1 - score / baseline: 0 is no better than the baseline, 1 is perfect, negative is worse."""
    if baseline_score == 0:
        raise ValueError("baseline score is 0")
    return 1.0 - score / baseline_score


@dataclass(frozen=True)
class Split:
    train: slice
    test: slice


def expanding_window_splits(n: int, initial: int, horizon: int, step: int | None = None) -> Iterator[Split]:
    """Folds over a series of length ``n``: train on ``[0, end)``, test on ``[end, end + horizon)``.

    The first fold trains on ``initial`` points; each later fold moves ``end`` on by ``step``
    (default: ``horizon``, so test windows tile without overlap). A test window never reaches
    past the series.
    """
    if min(initial, horizon) < 1:
        raise ValueError("initial and horizon must be >= 1")
    step = step or horizon
    end = initial
    if end + horizon > n:
        raise ValueError("series too short for one fold")
    while end + horizon <= n:
        yield Split(slice(0, end), slice(end, end + horizon))
        end += step


Forecaster = Callable[[pd.Series, int], np.ndarray]


def backtest(y: pd.Series, forecaster: Forecaster, initial: int, horizon: int, step: int | None = None,
             metric: Callable = mae) -> pd.DataFrame:
    """Refit ``forecaster(history, horizon)`` on every fold; one row per fold with its score."""
    rows = []
    for k, s in enumerate(expanding_window_splits(len(y), initial, horizon, step)):
        hist, fut = y.iloc[s.train], y.iloc[s.test]
        pred = np.asarray(forecaster(hist, horizon), dtype=float)
        rows.append({"fold": k, "train_end": hist.index[-1], "test_start": fut.index[0],
                     "test_end": fut.index[-1], "score": metric(fut.to_numpy(), pred)})
    return pd.DataFrame(rows)


def bootstrap_ci(values, stat: Callable = np.mean, n_boot: int = 2000, level: float = 0.95,
                 seed: int = 0) -> tuple[float, float, float]:
    """``(estimate, low, high)`` -- the percentile bootstrap interval of ``stat``."""
    x = np.asarray(values, dtype=float)
    if x.size < 2:
        raise ValueError("need at least two values")
    rng = np.random.default_rng(seed)
    boots = np.array([stat(rng.choice(x, size=x.size, replace=True)) for _ in range(n_boot)])
    alpha = (1 - level) / 2
    return float(stat(x)), float(np.quantile(boots, alpha)), float(np.quantile(boots, 1 - alpha))
