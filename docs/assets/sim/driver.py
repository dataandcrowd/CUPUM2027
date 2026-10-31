"""Browser driver: runs the unmodified cordonlite package inside Pyodide and returns one JSON document.

run_web(settings_json, on_day) calls cordonlite.run.simulate, the function the command line uses. Nothing
here changes the model: settings become the same overrides that `--set` gives on the command line.
"""

import hashlib
import json
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd

from cordonlite.config import load_config
from cordonlite.run import resolve_capacity_scale, simulate

ROOT = Path("/home/pyodide/cordon_lite")
MODE = {"CAR": 0, "PT": 1, "WFH": 2}


def fingerprint(rows):
    """Hash of (agent, day, mode, departure, gate exit), the same function as scripts/build_docs_site.py."""
    h = hashlib.sha256()
    for r in rows:
        h.update(("%d,%d,%s,%d,%d;" % r).encode())
    return h.hexdigest()[:16]


def run_web(settings_json, on_day=None):
    s = json.loads(settings_json)
    overrides = dict(s.get("overrides", {}))
    overrides["run.arm"] = s["arm"]
    overrides["run.seed"] = int(s["seed"])
    overrides["run.traits"] = s.get("traits", "on")
    overrides["fees.peak_fee"] = float(s["peak_fee"])
    cfg = load_config(ROOT / "config.toml", overrides)
    t0 = time.perf_counter()
    scale, source = resolve_capacity_scale(cfg, None, warn=False)
    import builtins
    real_print = builtins.print

    def spy(*a, **k):                       # simulate(progress=True) prints one line per day
        line = " ".join(str(x) for x in a)
        if on_day is not None and line.startswith("day "):
            on_day(int(line.split()[1]))

    builtins.print = spy
    try:
        with tempfile.TemporaryDirectory() as d:
            res = simulate(cfg, Path(d), scale, progress=True)
    finally:
        builtins.print = real_print
    out = pd.DataFrame(res.outcomes).sort_values(["day", "agent_id"], kind="stable")
    n, days = len(res.personas), int(cfg.run.n_days)

    def col(name, fill=-1):
        v = pd.to_numeric(out[name], errors="coerce").fillna(fill).to_numpy(dtype=np.int64)
        return [v[i * n:(i + 1) * n].tolist() for i in range(days)]

    mode = out["mode"].map(MODE).to_numpy(dtype=np.int64)
    fp = fingerprint(zip(out["agent_id"].astype(int), out["day"].astype(int), out["mode"],
                         pd.to_numeric(out["depart_min"], errors="coerce").fillna(-1).astype(int),
                         pd.to_numeric(out["gate_exit_min"], errors="coerce").fillna(-1).astype(int)))
    dec = pd.DataFrame(res.decisions)
    woken = dec[dec["decider"] == "rule"].groupby("day").size().reindex(range(1, days + 1), fill_value=0).tolist()
    return json.dumps({
        "settings": s, "seconds": round(time.perf_counter() - t0, 1), "capacity_scale": scale, "source": source,
        "fingerprint": fp, "days": res.days, "woken": woken,
        "disruption_corridor": res.disruption_corridor,
        "mode": [mode[i * n:(i + 1) * n].tolist() for i in range(days)],
        "depart": col("depart_min"), "gate_arrive": col("gate_arrive_min"), "gate_exit": col("gate_exit_min"),
        "arrive": col("arrive_min"), "road": col("road_delay_min", 0), "queue": col("queue_delay_min", 0),
    })
