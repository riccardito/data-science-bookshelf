"""A run log: MLflow when it is installed, plain JSON when it is not.

A challenge logs its parameters and its number through ``log_run``. With the ``tracking``
extra installed the run lands in a local MLflow store (``mlruns/``, browse it with
``mlflow ui``); without it, one JSON file per run lands in ``runs/``. Either way the call is the
same, so a chapter never branches on what is installed.
"""

from __future__ import annotations

import json
import time
from pathlib import Path


def mlflow_available() -> bool:
    try:
        import mlflow  # noqa: F401
    except ImportError:
        return False
    return True


def log_run(experiment: str, params: dict, metrics: dict, *, root: Path | str = ".",
            use_mlflow: bool | None = None) -> Path | str:
    """Record one run; returns the JSON path, or the MLflow run id."""
    use_mlflow = mlflow_available() if use_mlflow is None else use_mlflow
    if use_mlflow:
        import mlflow

        mlflow.set_tracking_uri((Path(root) / "mlruns").resolve().as_uri())
        mlflow.set_experiment(experiment)
        with mlflow.start_run() as run:
            mlflow.log_params(params)
            mlflow.log_metrics({k: float(v) for k, v in metrics.items()})
            return run.info.run_id
    out = Path(root) / "runs" / experiment
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    path = out / f"{stamp}-{len(list(out.glob('*.json'))):03d}.json"
    path.write_text(json.dumps({"experiment": experiment, "params": params,
                                "metrics": {k: float(v) for k, v in metrics.items()}},
                               indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_runs(experiment: str, root: Path | str = ".") -> list[dict]:
    """The JSON runs of an experiment, oldest first."""
    d = Path(root) / "runs" / experiment
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json"))]
