"""No private product name on the shelf -- the check runs in CI, not from memory.

The names are never written here: ``PRIVATE_SHA256`` holds the SHA-256 of each lower-cased
word (the same list `agora-method` publishes), and every word of every tracked text file is
hashed and compared. Exit 1 on a hit, naming the file and line but not the word.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

PRIVATE_SHA256 = frozenset({
    "a1328c633b67e3f8b8e261c8684d0cc54944b4a97b467af24a612ff65b7d1937",
    "8653057a4b57183ce71278ca80dbd82a61196fa182652f4cba355614b768d063",
    "f24c4023f4c6acd0f155e105203241f37f25d252fdda1ce2dde5902f29fa13fa",
    "f7d6e4bf52a3b96bc6607d937c1d04ea9f1142dbeb6a03a6dfdd5eba9a0a3807",
    "5e891eca12ac778b30bb82add5a4434764fef6f5a9cb92fd70c0d106943cf766",
    "6d6ca7bc23eb151cf2b97d7c589c980555e564c4de33db09a1722471be73b882",
    "7f31e7109b78eb0ab0f9c33f5092557641368faed092a294465ae02c696eda0d",
})
WORD = re.compile(r"[A-Za-z][A-Za-z0-9]*")
TEXT = {".md", ".py", ".ipynb", ".toml", ".yml", ".yaml", ".txt", ".csv", ".json", ".cfg", ""}


def hits(lines: Iterable[str], private: frozenset[str] = PRIVATE_SHA256) -> list[int]:
    """1-based numbers of the lines carrying a private word."""
    out = []
    for n, line in enumerate(lines, 1):
        if any(hashlib.sha256(w.lower().encode()).hexdigest() in private for w in WORD.findall(line)):
            out.append(n)
    return out


def notebook_lines(path: Path) -> list[str]:
    """A notebook is checked cell by cell -- sources AND text outputs (images are skipped)."""
    nb = json.loads(path.read_text(encoding="utf-8"))
    lines = []
    for cell in nb.get("cells", []):
        lines += "".join(cell.get("source", [])).splitlines()
        for o in cell.get("outputs", []):
            lines += "".join(o.get("text", [])).splitlines()
            for mime, v in o.get("data", {}).items():
                # an image is base64: its letters are noise, and a short token can match by chance
                if mime.startswith("image/"):
                    continue
                if isinstance(v, list | str):
                    lines += "".join(v).splitlines()
    return lines


def tracked_files(root: Path) -> list[Path]:
    out = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True).stdout
    return [root / p for p in out.splitlines() if Path(p).suffix in TEXT]


def main(root: Path = Path(".")) -> int:
    bad = 0
    for path in tracked_files(root):
        if path.name == "check_private_terms.py" or not path.exists():
            continue
        try:
            lines = notebook_lines(path) if path.suffix == ".ipynb" else \
                path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        for n in hits(lines):
            print(f"{path.relative_to(root)}:{n}: a private term")
            bad += 1
    print(f"private terms: {bad} hit(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
