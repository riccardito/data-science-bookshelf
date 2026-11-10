"""Public data in, offline by default.

A chapter never needs the network: it reads a committed sample from ``data/samples/``. The
full series comes from the publisher on request, through a disk cache, so a second run is
offline too. opendata.swiss is a CKAN portal; ``opendata_resources`` lists a dataset's files
through its ``package_show`` action.
"""

from __future__ import annotations

import hashlib
import io as _io
import os
from collections.abc import Callable
from pathlib import Path

import pandas as pd
import requests

OPENDATA_API = "https://opendata.swiss/api/3/action/package_show"

Fetcher = Callable[[str], bytes]


def repo_root(start: Path | None = None) -> Path:
    """The bookshelf's root: the nearest parent holding ``data/samples``."""
    here = (start or Path.cwd()).resolve()
    for p in (here, *here.parents):
        if (p / "data" / "samples").is_dir():
            return p
    raise FileNotFoundError("no data/samples above " + str(here))


def samples_dir(start: Path | None = None) -> Path:
    return repo_root(start) / "data" / "samples"


def load_sample(name: str, start: Path | None = None, **read_kw) -> pd.DataFrame:
    """Read ``data/samples/<name>`` -- CSV (also gzipped) or Parquet -- from anywhere in the repo."""
    path = samples_dir(start) / name
    if not path.exists():
        raise FileNotFoundError(f"no sample {name!r} in {path.parent}")
    if path.suffix == ".parquet":
        return pd.read_parquet(path, **read_kw)
    return pd.read_csv(path, **read_kw)


def cache_dir() -> Path:
    """``$DS_TOOLBOX_CACHE``, else ``~/.cache/ds_toolbox``."""
    d = Path(os.environ.get("DS_TOOLBOX_CACHE", Path.home() / ".cache" / "ds_toolbox"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def http_get(url: str, timeout: float = 60.0) -> bytes:
    resp = requests.get(url, timeout=timeout, headers={"User-Agent": "ds-toolbox/0.1 (data-science-bookshelf)"})
    resp.raise_for_status()
    return resp.content


def fetch(url: str, *, refresh: bool = False, fetcher: Fetcher = http_get) -> bytes:
    """The bytes behind ``url``, from the disk cache when present."""
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    path = cache_dir() / key
    if path.exists() and not refresh:
        return path.read_bytes()
    data = fetcher(url)
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)
    return data


def fetch_csv(url: str, *, refresh: bool = False, fetcher: Fetcher = http_get, **read_kw) -> pd.DataFrame:
    return pd.read_csv(_io.BytesIO(fetch(url, refresh=refresh, fetcher=fetcher)), **read_kw)


def opendata_resources(dataset_id: str, *, fetcher: Fetcher = http_get) -> list[dict]:
    """The files of an opendata.swiss dataset: ``name``, ``format`` and ``url`` per resource."""
    import json

    raw = fetch(f"{OPENDATA_API}?id={dataset_id}", fetcher=fetcher)
    payload = json.loads(raw)
    if not payload.get("success"):
        raise LookupError(f"opendata.swiss has no dataset {dataset_id!r}")
    out = []
    for r in payload["result"].get("resources", []):
        name = r.get("name")
        if isinstance(name, dict):  # the portal stores titles per language
            name = name.get("en") or name.get("de") or next(iter(name.values()), "")
        out.append({"name": name or "", "format": (r.get("format") or "").upper(), "url": r.get("url", "")})
    return out
