"""The models a real model has to beat before its number means anything.

Each forecaster has the ``(history, horizon) -> array`` shape ``evaluation.backtest`` expects.
"""

from __future__ import annotations

from collections import Counter

import numpy as np
import pandas as pd


def _values(history) -> np.ndarray:
    v = np.asarray(history, dtype=float)
    if v.size == 0:
        raise ValueError("empty history")
    return v


def naive(history, horizon: int) -> np.ndarray:
    """Tomorrow is today: the last value, repeated."""
    return np.full(horizon, _values(history)[-1])


def mean(history, horizon: int) -> np.ndarray:
    return np.full(horizon, _values(history).mean())


def drift(history, horizon: int) -> np.ndarray:
    """The straight line through the first and the last value, extended."""
    v = _values(history)
    if v.size == 1:
        return np.full(horizon, v[0])
    slope = (v[-1] - v[0]) / (v.size - 1)
    return v[-1] + slope * np.arange(1, horizon + 1)


def seasonal_naive(season: int):
    """A forecaster that repeats the last full season: this Monday is last Monday."""
    if season < 1:
        raise ValueError("season must be >= 1")

    def forecast(history, horizon: int) -> np.ndarray:
        v = _values(history)
        if v.size < season:
            raise ValueError("history shorter than one season")
        last = v[-season:]
        return np.resize(last, horizon)

    forecast.__name__ = f"seasonal_naive_{season}"
    return forecast


def majority_class(y_train) -> object:
    """The classification baseline: the most common label."""
    labels = list(pd.Series(y_train).dropna())
    if not labels:
        raise ValueError("no labels")
    return Counter(labels).most_common(1)[0][0]
