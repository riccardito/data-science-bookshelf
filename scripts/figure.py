"""`make figure`: docs/results.png -- one panel per challenge, drawn from the committed results.json."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ds_toolbox import viz  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def load(rel: str) -> dict:
    return json.loads((ROOT / rel / "challenge" / "results.json").read_text(encoding="utf-8"))


def main() -> None:
    viz.use_style()
    fc = load("shelves/05-statistical-learning/21-time-series")
    qr = load("shelves/07-deep-learning/27-dl-vision-signals")
    pc = load("shelves/01-foundations/01-linear-algebra")
    rf = load("shelves/01-foundations/03-probability")
    fig, axes = plt.subplots(2, 2, figsize=(12, 7.5))

    ax = axes[0, 0]
    res = fc["results"]
    names = sorted(res, key=lambda m: res[m]["mae_mw"])
    colours = ["0.6" if n == fc["baseline"] else viz.PALETTE[0] for n in names]
    bars = ax.barh(names, [res[n]["mae_mw"] for n in names], color=colours)
    ax.bar_label(bars, fmt="%.2f", padding=3)
    ax.invert_yaxis()
    ax.set(xlabel="MAE, MW", title="Time Series · swiss-forecast\nday-ahead, Zurich's electricity, a test year")

    ax = axes[0, 1]
    levels = ["0", "1", "2", "3", "4"]
    for reader, colour in [("QR code alone", viz.PALETTE[5]), ("OCR + rules", viz.PALETTE[1]),
                           ("combined, check digits enforced", viz.PALETTE[0])]:
        ax.plot(range(5), [qr["by_reader_and_quality"][reader][k] * 100 for k in levels], marker="o",
                label=reader, color=colour)
    ax.set(xticks=range(5), xticklabels=["scan", "good", "handheld", "blurred", "unreadable"],
           ylabel="fields read correctly, %", ylim=(-3, 103),
           title="Images & Signals · qr-bill-reader\nfive payment fields per photo quality")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    rows = pc["results"]
    x = np.arange(len(rows))
    ax.bar(x - 0.2, [r["rank for 95 % energy"] for r in rows], 0.4, label="95 % of the energy", color="0.6")
    b = ax.bar(x + 0.2, [r["rank for PSNR 30 dB"] for r in rows], 0.4, label="PSNR 30 dB", color=viz.PALETTE[0])
    ax.bar_label(b, padding=2)
    ax.set(xticks=x, xticklabels=[r["image"] for r in rows], ylabel="rank of the SVD",
           title="Linear Algebra · photo-compress\nhow many singular values an image needs")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    fams = ["lognormal", "gamma", "weibull", "exponential", "AIC's pick"]
    s = rf["over_seasons"]
    med = np.array([s[f]["median"] for f in fams])
    lo, hi = np.array([s[f]["p05"] for f in fams]), np.array([s[f]["p95"] for f in fams])
    ax.errorbar(range(len(fams)), med, yerr=[med - lo, hi - med], fmt="o", capsize=5, color=viz.PALETTE[0])
    ax.axhline(1, color=viz.PALETTE[3], lw=1.5)
    ax.axhspan(0.5, 2, color=viz.PALETTE[3], alpha=0.1)
    ax.set(yscale="log", xticks=range(len(fams)), xticklabels=fams, ylabel="estimate / truth",
           title="Probability · rockfall\nbreach rate from one season, 100 seasons")
    ax.tick_params(axis="x", labelsize=8)

    fig.tight_layout()
    out = ROOT / "docs" / "results.png"
    out.parent.mkdir(exist_ok=True)
    fig.savefig(out, dpi=110)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
