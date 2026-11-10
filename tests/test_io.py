import json

import pandas as pd
import pytest

from ds_toolbox import io


@pytest.fixture(autouse=True)
def _cache(tmp_path, monkeypatch):
    monkeypatch.setenv("DS_TOOLBOX_CACHE", str(tmp_path / "cache"))


def test_fetch_caches_the_first_answer():
    calls = []

    def fake(url):
        calls.append(url)
        return b"a,b\n1,2\n"

    assert io.fetch("https://x/y.csv", fetcher=fake) == b"a,b\n1,2\n"
    io.fetch("https://x/y.csv", fetcher=fake)
    assert calls == ["https://x/y.csv"]
    io.fetch("https://x/y.csv", fetcher=fake, refresh=True)
    assert len(calls) == 2


def test_fetch_csv_reads_a_frame():
    df = io.fetch_csv("https://x/z.csv", fetcher=lambda u: b"a,b\n1,2\n3,4\n")
    assert list(df.columns) == ["a", "b"] and len(df) == 2


def test_opendata_resources_picks_a_language_for_the_name():
    payload = {"success": True, "result": {"resources": [
        {"name": {"de": "Verbrauch", "en": "Consumption"}, "format": "csv", "url": "https://x/c.csv"},
        {"name": "plain", "format": None, "url": "https://x/p.json"},
    ]}}
    res = io.opendata_resources("some-id", fetcher=lambda u: json.dumps(payload).encode())
    assert res == [{"name": "Consumption", "format": "CSV", "url": "https://x/c.csv"},
                   {"name": "plain", "format": "", "url": "https://x/p.json"}]


def test_opendata_unknown_dataset():
    with pytest.raises(LookupError):
        io.opendata_resources("nope", fetcher=lambda u: b'{"success": false}')


def test_load_sample_finds_the_repo_from_a_subfolder(tmp_path):
    (tmp_path / "data" / "samples").mkdir(parents=True)
    pd.DataFrame({"x": [1, 2]}).to_csv(tmp_path / "data" / "samples" / "s.csv", index=False)
    deep = tmp_path / "shelves" / "01" / "book"
    deep.mkdir(parents=True)
    assert io.load_sample("s.csv", start=deep)["x"].tolist() == [1, 2]
    with pytest.raises(FileNotFoundError, match="no sample"):
        io.load_sample("missing.csv", start=deep)


def test_repo_root_outside_a_repo(tmp_path):
    with pytest.raises(FileNotFoundError):
        io.repo_root(tmp_path)


def test_http_get_sends_a_user_agent(monkeypatch):
    seen = {}

    class Resp:
        content = b"ok"

        def raise_for_status(self):
            pass

    def fake_get(url, timeout, headers):
        seen.update(url=url, ua=headers["User-Agent"])
        return Resp()

    monkeypatch.setattr(io.requests, "get", fake_get)
    assert io.http_get("https://x") == b"ok"
    assert seen["ua"].startswith("ds-toolbox/")
