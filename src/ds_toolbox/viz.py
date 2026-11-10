"""One plotting style for the whole shelf.

The palette is colour-blind safe (Okabe-Ito). ``use_style()`` is the first line of every
chapter that draws.
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]


def use_style() -> None:
    mpl.rcParams.update({
        "figure.figsize": (9, 4),
        "figure.dpi": 100,
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.titleweight": "bold",
        "axes.titlesize": 12,
        "legend.frameon": False,
        "font.size": 10,
    })


def plot_forecast(history, actual, forecasts: dict[str, np.ndarray], ax=None, title: str = ""):
    """History in grey, the truth in black, each forecast in its own colour."""
    ax = ax or plt.gca()
    ax.plot(history.index, history.to_numpy(), color="0.6", lw=1, label="history")
    ax.plot(actual.index, actual.to_numpy(), color="black", lw=1.5, label="actual")
    for (name, pred), colour in zip(forecasts.items(), PALETTE, strict=False):
        ax.plot(actual.index, np.asarray(pred), color=colour, lw=1.5, ls="--", label=name)
    ax.set_title(title)
    ax.legend()
    return ax


def bar_scores(scores: dict[str, float], baseline: str | None = None, ax=None, title: str = "",
               unit: str = ""):
    """One bar per model; the baseline's bar in grey, its value as a dotted line."""
    ax = ax or plt.gca()
    names = list(scores)
    colours = ["0.6" if n == baseline else PALETTE[0] for n in names]
    bars = ax.bar(names, [scores[n] for n in names], color=colours)
    ax.bar_label(bars, fmt="%.3g")
    if baseline is not None:
        ax.axhline(scores[baseline], color="0.4", ls=":", lw=1)
    ax.set_ylabel(unit)
    ax.set_title(title)
    return ax
