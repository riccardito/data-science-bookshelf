"""`make demo`: run the four challenges offline and print each one's number.

Every challenge notebook is executed in a fresh kernel, from its own folder, exactly as CI runs it --
no key, no network, the recorded answers replayed. Then the headline of each `results.json`.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
CHALLENGES = [
    ("swiss-forecast", "shelves/05-statistical-learning/21-time-series/challenge/swiss-forecast.ipynb"),
    ("qr-bill-reader", "shelves/07-deep-learning/27-dl-vision-signals/challenge/qr-bill-reader.ipynb"),
    ("photo-compress", "shelves/01-foundations/01-linear-algebra/challenge/photo-compress.ipynb"),
    ("rockfall", "shelves/01-foundations/03-probability/challenge/rockfall.ipynb"),
]


def headline(name: str, r: dict) -> str:
    if name == "swiss-forecast":
        res = r["results"]
        base = res[r["baseline"]]["mae_mw"]
        best = min(res, key=lambda m: res[m]["mae_mw"])
        return f"day-ahead MAE {res[best]['mae_mw']:.2f} MW ({best}) against {base:.2f} MW for {r['baseline']}"
    if name == "qr-bill-reader":
        q = r["by_reader_and_quality"]["combined, check digits enforced"]
        return (f"fields read: {q['2']:.0%} on a handheld photo, {q['3']:.0%} on a blurred one "
                f"(QR alone {r['by_reader_and_quality']['QR code alone']['3']:.0%})")
    if name == "photo-compress":
        k = {row["image"]: row["rank for PSNR 30 dB"] for row in r["results"]}
        return "rank for 30 dB: " + ", ".join(f"{img} {rank}" for img, rank in k.items())
    s = r["over_seasons"]
    return (f"true {r['true_breach_rate_per_year']:.4f} breaches/yr; one season, true family within 2x "
            f"{s['gamma']['within_2x']:.0%} of the time, lognormal median {s['lognormal']['median']:.0f}x")


def main() -> int:
    for name, rel in CHALLENGES:
        path = ROOT / rel
        start = time.time()
        nb = nbformat.read(path, as_version=4)
        NotebookClient(nb, timeout=900, kernel_name="python3",
                       resources={"metadata": {"path": str(path.parent)}}).execute()
        result = json.loads((path.parent / "results.json").read_text(encoding="utf-8"))
        print(f"{name:15s} {headline(name, result)}   [{time.time() - start:.0f} s]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
