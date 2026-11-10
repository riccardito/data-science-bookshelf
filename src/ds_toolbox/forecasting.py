"""Day-ahead forecasting on a local-day grid (``features.to_local_days``).

The task: at local midnight, forecast the 24 hours of the coming day. Everything a model sees
must have been known at that midnight -- the grid makes that easy to state: a feature for day
``d`` may only come from rows ``d-1`` and earlier.

Two models share this module. ``day_ahead_table`` builds the tabular features a gradient-boosted
model needs. ``DayAheadCNN`` is a small temporal convolutional network that reads the last week
hour by hour and predicts a *correction* to "the same day last week" -- learning the residual of
a strong baseline is easier than learning the level from scratch. torch is imported lazily: the
rest of the toolbox does not need it.
"""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from . import features as ft


def day_calendar(dates: pd.DatetimeIndex, holidays: Iterable | None = None) -> pd.DataFrame:
    """Per day: weekday one-hot, a holiday flag, and a smooth day of the year."""
    days = set(holidays or ())
    doy = dates.day_of_year.to_numpy()
    out = pd.DataFrame({f"wd{k}": (dates.day_of_week == k).astype(float) for k in range(7)}, index=dates)
    out["holiday"] = np.fromiter((d.date() in days for d in dates), dtype=float, count=len(dates))
    out["doy_sin"] = np.sin(2 * np.pi * doy / 365.25)
    out["doy_cos"] = np.cos(2 * np.pi * doy / 365.25)
    return out


def day_ahead_table(grid: pd.DataFrame, holidays: Iterable | None = None) -> tuple[pd.DataFrame, pd.Series]:
    """One row per (day, hour) with features known at the previous midnight; ``y`` the load."""
    y = ft.from_local_days(grid).rename("load")
    lags = ft.lag_features(y, [24, 48, 168, 336], min_lag=24, prefix="load")
    per_day = pd.DataFrame({
        "yesterday_mean": grid.mean(axis=1).shift(1),
        "yesterday_last_hour": grid[23].shift(1),
        "last_week_mean": grid.mean(axis=1).shift(7),
    })
    day_of_row = y.index.normalize()
    daily = per_day.reindex(day_of_row).set_axis(y.index)
    cal = ft.calendar_features(pd.DatetimeIndex(y.index), tz=None, holidays=holidays)
    X = pd.concat([lags, daily, cal], axis=1)
    ok = X.notna().all(axis=1)
    return X[ok], y[ok]


def cnn_windows(grid: pd.DataFrame, holidays: Iterable | None = None) -> dict[str, np.ndarray]:
    """For every day with a full week before it: the past 168 hours, the day's calendar, the
    same day last week (the base the network corrects) and the target 24 hours."""
    values = grid.to_numpy(dtype=np.float32)
    cal = day_calendar(grid.index, holidays).to_numpy(dtype=np.float32)
    idx = np.arange(7, len(grid))
    past = np.stack([values[i - 7:i].reshape(-1) for i in idx])
    return {"past": past, "cal": cal[idx], "base": values[idx - 7], "y": values[idx],
            "dates": grid.index[idx].to_numpy()}


def _torch():
    import torch
    from torch import nn

    return torch, nn


def build_cnn(n_cal: int = 10, channels: int = 16):
    """Dilated 1-D convolutions over the week, then a dense head that also sees the calendar."""
    torch, nn = _torch()

    class DayAheadCNN(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv = nn.Sequential(
                nn.Conv1d(1, channels, 7, padding=3), nn.ReLU(),
                nn.Conv1d(channels, channels, 7, padding=6, dilation=2), nn.ReLU(),
                nn.Conv1d(channels, channels, 7, padding=12, dilation=4), nn.ReLU(),
                nn.AvgPool1d(4),
            )
            self.head = nn.Sequential(nn.Linear(channels * 42 + n_cal, 64), nn.ReLU(), nn.Linear(64, 24))
            # start as the baseline: the correction is zero until training finds one
            nn.init.zeros_(self.head[-1].weight)
            nn.init.zeros_(self.head[-1].bias)

        def forward(self, past, cal):
            z = self.conv(past.unsqueeze(1)).flatten(1)
            return self.head(torch.cat([z, cal], dim=1))

    return DayAheadCNN()


class CNNForecaster:
    """Fit/predict wrapper around ``build_cnn``.

    The network learns the *residual* ``y - base`` in its own units: the inputs are standardised
    by the training load, the target by the residual's standard deviation. Without that, the
    correction the network must find is a fraction of a percent of the level and drowns in the
    optimiser's step size. Early stopping keeps the best epoch on a validation tail.
    """

    def __init__(self, epochs: int = 80, batch: int = 64, lr: float = 1e-3, val_days: int = 180,
                 patience: int = 12, seed: int = 0):
        self.epochs, self.batch, self.lr, self.val_days = epochs, batch, lr, val_days
        self.patience, self.seed = patience, seed
        self.history: list[tuple[float, float]] = []

    def _inputs(self, w):
        torch, _ = _torch()
        return (torch.tensor((w["past"] - self.mu) / self.sd), torch.tensor(w["cal"]))

    def fit(self, w: dict[str, np.ndarray]) -> CNNForecaster:
        torch, nn = _torch()
        torch.manual_seed(self.seed)
        rng = np.random.default_rng(self.seed)
        n_tr = len(w["y"]) - self.val_days
        if n_tr < self.batch:
            raise ValueError("too few days to train")
        self.mu, self.sd = float(w["y"][:n_tr].mean()), float(w["y"][:n_tr].std())
        self.res_sd = float((w["y"][:n_tr] - w["base"][:n_tr]).std())
        past, cal = self._inputs(w)
        target = torch.tensor((w["y"] - w["base"]) / self.res_sd, dtype=torch.float32)
        self.net = build_cnn(n_cal=cal.shape[1])
        opt = torch.optim.Adam(self.net.parameters(), lr=self.lr)
        loss_fn = nn.L1Loss()
        best, best_state, wait = np.inf, None, 0
        for _ in range(self.epochs):
            self.net.train()
            order = rng.permutation(n_tr)
            for start in range(0, n_tr, self.batch):
                b = torch.as_tensor(order[start:start + self.batch])
                opt.zero_grad()
                loss = loss_fn(self.net(past[b], cal[b]), target[b])
                loss.backward()
                opt.step()
            self.net.eval()
            with torch.no_grad():
                tr = loss_fn(self.net(past[:n_tr], cal[:n_tr]), target[:n_tr]).item()
                va = loss_fn(self.net(past[n_tr:], cal[n_tr:]), target[n_tr:]).item()
            self.history.append((tr, va))
            if va < best - 1e-5:
                best, wait = va, 0
                best_state = {k: v.clone() for k, v in self.net.state_dict().items()}
            else:
                wait += 1
                if wait >= self.patience:
                    break
        self.net.load_state_dict(best_state)
        return self

    def predict(self, w: dict[str, np.ndarray]) -> np.ndarray:
        torch, _ = _torch()
        past, cal = self._inputs(w)
        self.net.eval()
        with torch.no_grad():
            return w["base"] + self.net(past, cal).numpy() * self.res_sd
