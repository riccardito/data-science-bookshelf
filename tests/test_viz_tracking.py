import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from ds_toolbox import tracking, viz  # noqa: E402


def test_style_and_plots_draw():
    viz.use_style()
    assert matplotlib.rcParams["axes.spines.top"] is False
    idx = pd.date_range("2024-01-01", periods=6, freq="D")
    hist, act = pd.Series(np.arange(4.0), idx[:4]), pd.Series([4.0, 5.0], idx[4:])
    fig, (a, b) = plt.subplots(1, 2)
    viz.plot_forecast(hist, act, {"naive": [3.0, 3.0]}, ax=a, title="t")
    assert len(a.lines) == 3
    viz.bar_scores({"base": 2.0, "model": 1.0}, baseline="base", ax=b, unit="MAE")
    assert len(b.patches) == 2 and len(b.lines) == 1
    plt.close(fig)


def test_json_runs_round_trip(tmp_path):
    p = tracking.log_run("exp", {"k": 3}, {"mae": 1.5}, root=tmp_path, use_mlflow=False)
    tracking.log_run("exp", {"k": 4}, {"mae": 1.2}, root=tmp_path, use_mlflow=False)
    assert p.exists()
    runs = tracking.load_runs("exp", root=tmp_path)
    assert [r["params"]["k"] for r in runs] == [3, 4]
    assert runs[1]["metrics"]["mae"] == 1.2


def test_mlflow_detection_is_a_bool():
    assert isinstance(tracking.mlflow_available(), bool)


def test_mlflow_branch_with_a_fake_module(tmp_path, monkeypatch):
    import sys
    import types

    calls = {}

    class Run:
        def __init__(self):
            self.info = types.SimpleNamespace(run_id="r1")

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    fake = types.SimpleNamespace(
        set_tracking_uri=lambda u: calls.setdefault("uri", u),
        set_experiment=lambda e: calls.setdefault("exp", e),
        start_run=Run,
        log_params=lambda p: calls.setdefault("params", p),
        log_metrics=lambda m: calls.setdefault("metrics", m),
    )
    monkeypatch.setitem(sys.modules, "mlflow", fake)
    assert tracking.mlflow_available()
    assert tracking.log_run("exp", {"k": 1}, {"mae": 2}, root=tmp_path) == "r1"
    assert calls["uri"].startswith("file:") and calls["metrics"] == {"mae": 2.0}
