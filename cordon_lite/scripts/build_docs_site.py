"""Build the data behind the website in ../docs: python scripts/build_docs_site.py

Writes, under ../docs/assets:
    sim/model.zip          the cordonlite package, config.toml and the prep outputs that the browser run reads
    data/map.json          land, cordon, gates, background roads and the simulated road sections
    data/agents.json       the 950 commuters of seed 1, their routes and the day-6 state of the cost explorer
    data/run_<key>.json    stored runs of seed 1 (mode, departure, gate times, reasons), replayed on the site
    data/site.json         fee table, run fingerprints, parameter table and the LLM tallies
    data/cost_check.json   generalised costs from options.build_options; model.html recomputes them in JavaScript
                           on load and reports the largest difference (the cost explorer's self-check)

Reads data/, netlogo7/gis/, runs/ and the SA2 polygons of prep.sa2_gpkg (land outline only). Nothing here
changes the model; the site's numbers come from the stored runs named in RUNS.
"""

from __future__ import annotations

import collections
import hashlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cordonlite import fees as feesmod  # noqa: E402
from cordonlite import run as runmod  # noqa: E402
from cordonlite.config import load_config  # noqa: E402

DOCS = ROOT.parent / "docs" / "assets"
DATA = DOCS / "data"
MODEL_FILES = ["config.toml"] + [f"cordonlite/{m}.py" for m in (
    "__init__", "clock", "config", "engine", "fees", "memory", "options", "persona", "roads", "rules", "run",
    "types")] + [f"data/{f}" for f in ("origins.csv", "corridors.csv", "road_sections.csv", "origin_sections.csv",
                                       "road_profile.csv", "road_meta.json", "calibration.json")]
# site key -> stored run (seed 1, NZ$6 peak; _pt = PT disruption on days 3 and 8)
RUNS = {"rclock": "full_R-clock_s1", "hclock": "full_H-clock_s1", "rdaily": "R-daily_mock_py_s1",
        "rclock_pt": "full_R-clock_s1_pt3_pt8", "hclock_pt": "full_H-clock_s1_pt3_pt8",
        "rdaily_pt": "R-daily_mock_py_s1_pt3_pt8"}
GRID_M = 10          # map coordinates are whole units of 10 m from the map origin
MODE = {"CAR": 0, "PT": 1, "WFH": 2}


def write_json(name: str, obj) -> None:
    p = DATA / name
    p.write_text(json.dumps(obj, separators=(",", ":"), allow_nan=False), encoding="utf-8")
    print(f"{p.name:24s} {p.stat().st_size / 1024:8.0f} KB")


def fingerprint(df: pd.DataFrame) -> str:
    """Hash of (agent, day, mode, departure, gate exit), the same function as docs/assets/sim/driver.py."""
    h = hashlib.sha256()
    df = df.sort_values(["day", "agent_id"], kind="stable")
    for r in zip(df["agent_id"], df["day"], df["mode"],
                 pd.to_numeric(df["depart_min"], errors="coerce").fillna(-1).astype(int),
                 pd.to_numeric(df["gate_exit_min"], errors="coerce").fillna(-1).astype(int)):
        h.update(("%d,%d,%s,%d,%d;" % (int(r[0]), int(r[1]), r[2], r[3], r[4])).encode())
    return h.hexdigest()[:16]


def build_model_zip() -> None:
    with zipfile.ZipFile(DOCS / "sim" / "model.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in MODEL_FILES:
            z.write(ROOT / f, f)
    print(f"model.zip                {(DOCS / 'sim' / 'model.zip').stat().st_size / 1024:8.0f} KB")


def chain(lines: list[list[tuple[float, float]]]) -> list[tuple[float, float]]:
    """Join a section's segments end to end, flipping a segment whose far end meets the chain."""
    def gap(p, q):
        return abs(p[0] - q[0]) + abs(p[1] - q[1])

    out = list(lines[0])
    for i, ln in enumerate(lines[1:]):
        ends = [(gap(out[-1], ln[0]), 0), (gap(out[-1], ln[-1]), 1), (gap(out[0], ln[0]), 2), (gap(out[0], ln[-1]), 3)]
        k = min(ends)[1] if i == 0 else min(ends[:2])[1]
        if k == 1:
            ln = ln[::-1]
        elif k == 2:
            out = out[::-1]
        elif k == 3:
            out, ln = out[::-1], ln[::-1]
        out += ln
    return out


def build_map(routes: pd.DataFrame, cfg) -> tuple[dict, dict[int, np.ndarray]]:
    """map.json; section polylines point in the direction of travel."""
    shp = gpd.read_file(ROOT / "netlogo7/gis/tomtom_major_roads.shp")
    seg_col = next(c for c in shp.columns if c.lower().startswith("newseg") or c == "segment_id")
    geom = {s: list(g.coords) if g.geom_type == "LineString" else list(g.geoms[0].coords)
            for s, g in zip(shp[seg_col], shp.geometry)}
    secseg = pd.read_csv(ROOT / "data/section_segments.csv")
    used = sorted(routes["section_id"].unique())
    raw: dict[int, list] = {}
    for sid, g in secseg[secseg["section_id"].isin(used)].groupby("section_id"):
        raw[int(sid)] = chain([[tuple(p[:2]) for p in geom[s]] for s in g.sort_values("seq")["segment_id"]])
    # orient each section so that it ends where the next section of a route begins
    votes: dict[int, int] = collections.Counter()
    for _, g in routes.groupby("agent_id"):
        ids = g.sort_values("seq")["section_id"].tolist()
        for a, b in zip(ids, ids[1:]):
            pa, pb = raw[a], raw[b]
            d_fwd = min(abs(pa[-1][0] - q[0]) + abs(pa[-1][1] - q[1]) for q in (pb[0], pb[-1]))
            d_rev = min(abs(pa[0][0] - q[0]) + abs(pa[0][1] - q[1]) for q in (pb[0], pb[-1]))
            votes[a] += 1 if d_fwd <= d_rev else -1
    x0, y0 = 1730000.0, 5880000.0

    def enc(coords) -> list[int]:
        out: list[int] = []
        for x, y in coords:
            out += [int(round((x - x0) / GRID_M)), int(round((y - y0) / GRID_M))]
        return out

    sections, sec_xy = {}, {}
    for sid, pts in raw.items():
        if votes[sid] < 0:
            pts = pts[::-1]
        ls = LineString(pts).simplify(12.0)
        sections[str(sid)] = enc(ls.coords)
        sec_xy[sid] = np.asarray(ls.coords)
    cordon = gpd.read_file(ROOT / "data/cordon.geojson").to_crs(2193)
    bbox = [1737000.0, 5887000.0, 1781000.0, 5947000.0]
    land = gpd.read_file(cfg.resolve_path(cfg.prep.sa2_gpkg)).to_crs(2193)
    land = gpd.GeoSeries([unary_union(land.geometry)], crs=2193).clip(bbox).simplify(70.0).iloc[0]
    polys = [land] if land.geom_type == "Polygon" else [g for g in land.geoms if g.area > 3e5]
    bg = {"motorway": [], "major": []}
    for frc, g in zip(shp["frc"] if "frc" in shp else shp["FRC"], shp.geometry):
        if int(frc) > 2 or g.geom_type != "LineString":
            continue
        s = g.simplify(40.0)
        if s.length > 150:
            bg["motorway" if int(frc) == 0 else "major"].append(enc(list(s.coords)))
    gates = pd.read_csv(ROOT / "data/gates.csv")
    corridors = pd.read_csv(ROOT / "data/corridors.csv")
    cg = unary_union(cordon.geometry)
    out = {
        "origin": [x0, y0], "grid_m": GRID_M,
        "bbox": enc([bbox[:2], bbox[2:]]),
        "land": [enc(p.exterior.coords) for p in polys],
        "cordon": [enc(p.exterior.coords) for p in (cg.geoms if cg.geom_type == "MultiPolygon" else [cg])],
        "roads": bg, "sections": sections,
        "gates": [{"c": int(g.corridor_id), "name": g.streetName, "xy": enc([(g.x_nztm, g.y_nztm)])}
                  for g in gates.itertuples()],
        "corridors": [{"id": int(c.corridor_id), "name": str(c.name).split(" (")[0]} for c in corridors.itertuples()],
    }
    write_json("map.json", out)
    return out, sec_xy


def capture_state(cfg, run_dir: Path) -> dict:
    """Run R-clock and keep what options.build_options saw on day 6, with its options, for the cost explorer."""
    keep: dict[int, dict] = {}
    real = runmod.build_options

    def spy(p, mem, today, params, c, disc, wtt=True):
        o = real(p, mem, today, params, c, disc, wtt=wtt)
        if today.day == 6 and p.agent_id not in keep:
            keep[p.agent_id] = {"standing": mem.standing_option_id, "ref_fee": mem.ref_fee,
                                "ema": mem.delay_ratio_ema, "standing_depart": mem.standing_depart_min,
                                "today": today, "gc": {x.option_id: x.gc for x in o},
                                "fee": {x.option_id: x.fee for x in o}}
        return o

    runmod.build_options = spy
    try:
        scale, _ = runmod.resolve_capacity_scale(cfg, None)
        res = runmod.simulate(cfg, run_dir, scale)
    finally:
        runmod.build_options = real
    return {"keep": keep, "personas": res.personas}


def build_agents(cfg, personas_df: pd.DataFrame, routes: pd.DataFrame, mp: dict, sec_xy: dict) -> None:
    with tempfile.TemporaryDirectory() as d:
        st = capture_state(cfg, Path(d))
    keep = st["keep"]
    t = cfg.time
    grid = runmod.departure_grid(cfg)
    today = keep[0]["today"]
    ffm = pd.read_csv(ROOT / "data/road_sections.csv").set_index("section_id")["ff_min"]
    cols = {}
    for c in ("origin_id", "corridor_id", "fftt_to_gate_min", "fftt_gate_to_dest_min", "vot", "archetype", "tstar_min",
              "sched_mult", "parking_cost", "pt_time_min", "pt_fare", "H", "F", "P", "S", "fuel_cost", "wtp_fee",
              "path_km", "x_nztm", "y_nztm", "activity"):
        cols[c] = [round(float(x), 8) if isinstance(x, (float, np.floating)) and np.isfinite(x) else
                   (None if isinstance(x, (float, np.floating)) else (x if isinstance(x, str) else int(x)))
                   for x in personas_df[c]]
    for c in ("fixed_start", "must_drive", "pt_allowed", "wfh_allowed", "company_car", "early_shift_ok"):
        cols[c] = [int(x) for x in personas_df[c]]
    rt = [g.sort_values("seq")["section_id"].astype(int).tolist() for _, g in routes.groupby("agent_id")]
    rff = [[round(float(ffm[s]), 3) for s in r] for r in rt]
    i0 = t.sim_start_min
    road = [[round(float(today.public_road[a][m - i0]), 7) for m in grid] for a in range(len(rt))]
    cost = {
        "grid": grid,
        "pub_delay": {str(k): [[x, round(y, 7)] for x, y in v] for k, v in today.public_delay.items()},
        "road": road,
        "standing": [keep[a]["standing"] for a in range(len(rt))],
        "ref_fee": [round(keep[a]["ref_fee"], 8) for a in range(len(rt))],
        "ema": [round(keep[a]["ema"], 8) for a in range(len(rt))],
        "standing_depart": [keep[a]["standing_depart"] for a in range(len(rt))],
        "opts": [list(keep[a]["gc"].keys()) for a in range(len(rt))],
    }
    write_json("agents.json", {"cols": cols, "routes": rt, "route_ff": rff, "cost": cost})
    write_json("cost_check.json", {"gc": [keep[a]["gc"] for a in range(len(rt))],
                                   "fee": [keep[a]["fee"] for a in range(len(rt))]})


def build_run(key: str, folder: str) -> dict:
    d = ROOT / "runs" / folder
    o = pd.read_csv(d / "outcomes.csv").sort_values(["day", "agent_id"], kind="stable")
    dec = pd.read_csv(d / "decisions.csv", keep_default_na=False)
    n = int(o["agent_id"].max()) + 1
    days = int(o["day"].max())

    def col(name):
        v = pd.to_numeric(o[name], errors="coerce").fillna(-1).to_numpy(dtype=np.int64)
        return [v[i * n:(i + 1) * n].tolist() for i in range(days)]

    summ = json.loads((d / "summary.json").read_text())
    log = {}
    if (d / "plan_log.jsonl").exists():
        for ln in (d / "plan_log.jsonl").read_text().splitlines():
            r = json.loads(ln)
            log[(r["agent_id"], r["day"])] = r
    # a decision worth showing: every rule or LLM answer after day 1 (R-daily would be 9,000 rows of template)
    keep_rows = []
    if not folder.startswith("R-daily"):
        for r in dec[(dec["decider"].isin(["rule", "llm"])) & (dec["day"] > 1)].itertuples():
            row = [int(r.agent_id), int(r.day), r.decider, r.option_id, r.triggers, r.reason]
            p = log.get((int(r.agent_id), int(r.day)))
            if p is not None:
                row.append({"h": p.get("handler"), "s": p.get("strategy"), "tag": p.get("reason_tag") or p.get("main_reason"),
                            "backup": (p.get("plan") or {}).get("if_bus_disrupted")})
            keep_rows.append(row)
    days_kept = [{k: x[k] for k in ("day", "cars", "pt", "wfh", "mean_road_delay", "mean_queue_delay", "calls",
                                    "revenue", "wtt_no_car")} for x in summ["days"]]
    bcalls = collections.Counter()
    for x in summ["days"]:
        bcalls.update(x["calls"])
    handler = collections.Counter()
    if log:
        for (a, dd), r in log.items():
            handler[(dd, r.get("handler"))] += 1
    backups = [[a, dd] for (a, dd), r in log.items() if r.get("handler") in ("backup", "back_up", "back-up")]
    out = {
        "key": key, "run": folder, "arm": summ["meta"]["arm"], "fingerprint": fingerprint(o),
        "disruption_corridor": summ["meta"].get("pt_disruption_corridor"),
        "mode": [o["mode"].map(MODE).to_numpy()[i * n:(i + 1) * n].tolist() for i in range(days)],
        "depart": col("depart_min"), "gate_arrive": col("gate_arrive_min"), "gate_exit": col("gate_exit_min"),
        "arrive": col("arrive_min"), "road": col("road_delay_min"), "queue": col("queue_delay_min"),
        "fee": [[round(float(x), 2) for x in o["fee_paid"].to_numpy()[i * n:(i + 1) * n]] for i in range(days)],
        "late": [[int(round(x)) for x in pd.to_numeric(o["late_min"], errors="coerce").fillna(0).to_numpy()[i * n:(i + 1) * n]]
                 for i in range(days)],
        "pt_hit": [[int(x) for x in o["pt_disrupted"].to_numpy()[i * n:(i + 1) * n]] for i in range(days)],
        "early": [[int(x) for x in o["early_shift"].fillna(False).astype(bool).to_numpy()[i * n:(i + 1) * n]]
                  for i in range(days)],
        "decisions": keep_rows, "days": days_kept, "calls": dict(bcalls), "backups": backups,
        "handlers": sorted({str(h) for (_, h) in handler}),
    }
    write_json(f"run_{key}.json", out)
    return out


def fingerprints() -> dict:
    """Fingerprints of the stored rule runs a browser run can repeat, by arm|seed|peak|traits|pt."""
    out = {}
    specs = [(a, s, 6, "on", 0) for a in ("R-clock", "R-daily") for s in (1, 2, 3)]
    specs += [(a, 1, p, "on", 0) for a in ("R-clock", "R-daily") for p in (0, 3, 12, 18, 30)]
    specs += [("R-clock", 1, 6, "off", 0)]
    specs += [(a, 1, p, "on", 1) for a in ("R-clock", "R-daily") for p in (6, 18)]
    for arm, seed, peak, traits, pt in specs:
        name = f"{arm}_mock_py_s{seed}" + (f"_peak{peak}" if peak != 6 else "") + ("_traitsoff" if traits == "off" else "")
        name += "_pt3_pt8" if pt else ""
        p = ROOT / "runs" / name / "outcomes.csv"
        if p.exists():
            out[f"{arm}|{seed}|{peak}|{traits}|{pt}"] = {"run": name, "fp": fingerprint(pd.read_csv(p))}
    return out


def build_site(cfg) -> None:
    c = cfg
    table = feesmod.fee_table_from_config(cfg)
    params = [
        ("Run", "run.n_agents", c.run.n_agents, "Commuters simulated, 5% of the 19,000 charged morning entries"),
        ("Run", "run.n_days", c.run.n_days, "Weekday mornings"),
        ("Run", "fees.fee_start_day", c.fees.fee_start_day, "First charged day"),
        ("Run", "fees.peak_fee", c.fees.peak_fee, "Peak charge, NZ$ per entry"),
        ("Time", "time.sim_start_min", c.time.sim_start_min, "Engine clock start (05:30)"),
        ("Time", "time.depart_step_min", c.time.depart_step_min, "Departure grid, minutes"),
        ("Time", "time.retime_offsets_min", list(c.time.retime_offsets_min), "Car options around the standing departure"),
        ("Costs", "persona.vot_mu", c.persona.vot_mu, "ln VoT mean; the median VoT is exp(2.3) = NZ$9.97/h"),
        ("Costs", "persona.vot_sigma", c.persona.vot_sigma, "ln VoT standard deviation"),
        ("Costs", "costs.beta_ratio", c.costs.beta_ratio, "Early arrival cost / VoT (Small 1982)"),
        ("Costs", "costs.gamma_ratio", c.costs.gamma_ratio, "Late arrival cost / VoT (Small 1982)"),
        ("Costs", "costs.pt_fare", c.costs.pt_fare, "PT round trip, NZ$"),
        ("Costs", "costs.pt_ratio_default", c.costs.pt_ratio_default, "PT in-vehicle time / free-flow car time"),
        ("Costs", "costs.pt_access_min", c.costs.pt_access_min, "Walk and wait added to PT time, minutes"),
        ("Costs", "costs.fuel_cost_per_km", c.costs.fuel_cost_per_km, "Fuel, NZ$/km, round trip"),
        ("Costs", "costs.early_shift_cost", c.costs.early_shift_cost, "Inconvenience of the 07:00 to 15:00 day, NZ$, x phi(F)"),
        ("Calibrated", "costs.pt_attitude_penalty", c.costs.pt_attitude_penalty, "PT attitude penalty, NZ$ (a fitted residual)"),
        ("Calibrated", "costs.wfh_cost", c.costs.wfh_cost, "WFH cost k_WFH, NZ$, x phi(F)"),
        ("Calibrated", "wtt.beta0", c.wtt.beta0, "Price sensitivity of the willingness to pay"),
        ("Calibrated", "road k", json.loads((ROOT / "data/road_meta.json").read_text()).get("k"), "Road capacity = k x directional ADT"),
        ("Clock", "clock.late_tolerance_by_F", list(c.clock.late_tolerance_by_F), "T3 tolerance, minutes, by F level"),
        ("Clock", "clock.sustained_rel", c.clock.sustained_rel, "T5 relative gap"),
        ("Clock", "clock.sustained_days", c.clock.sustained_days, "T5 consecutive car days"),
        ("Clock", "traits.kappa_h_disc_factor", c.traits.kappa_h_disc_factor, "Habit cost multiplier on T1, T4, T6"),
        ("Rule", "rules.sigma_rule", c.rules.sigma_rule, "Gumbel noise scale, NZ$"),
        ("Roads", "road.bpr_alpha", c.road.bpr_alpha, "BPR alpha"),
        ("Roads", "road.bpr_beta", c.road.bpr_beta, "BPR power"),
        ("Roads", "road.speed_floor", c.road.speed_floor, "Lowest speed, share of free flow"),
        ("Roads", "road.flow_window_min", c.road.flow_window_min, "Commuter flow window, minutes"),
        ("Roads", "road.mwy_jam_speed", c.road.mwy_jam_speed, "Motorway speed in breakdown, share of free flow"),
        ("Roads", "road.mwy_capacity_drop", c.road.mwy_capacity_drop, "Default capacity drop in breakdown"),
        ("Gates", "engine.calib_target_peak_delay_min", c.engine.calib_target_peak_delay_min, "Peak 15-min delay target, minutes"),
        ("Gates", "engine.rush_window_min", c.engine.rush_window_min, "Corridor agents / this = base capacity"),
        ("LLM", "llm.model", c.llm.model, "Model behind H-clock"),
        ("LLM", "llm.effort", c.llm.effort, "Effort"),
    ]
    tr = c.traits
    write_json("site.json", {
        "fee_table": [round(x, 4) for x in table],
        "fingerprints": fingerprints(),
        "params": [{"group": g, "key": k, "value": v, "note": n} for g, k, v, n in params],
        "traits": {"kappa_h": list(tr.kappa_h), "phi": list(tr.phi), "omega": list(tr.omega), "eta": list(tr.eta),
                   "shares_H": list(tr.shares_H), "shares_F": list(tr.shares_F), "shares_P": list(tr.shares_P),
                   "shares_S": list(tr.shares_S), "disc": tr.kappa_h_disc_factor},
        "costs": {"beta": c.costs.beta_ratio, "gamma": c.costs.gamma_ratio, "pap": c.costs.pt_attitude_penalty,
                  "wfh": c.costs.wfh_cost, "early_start": c.costs.early_start_min, "early_cost": c.costs.early_shift_cost,
                  "headway": c.costs.pt_headway_min, "bin": c.costs.delay_bin_min},
        "time": {"earliest": c.time.depart_earliest_min, "latest": c.time.depart_latest_min, "step": c.time.depart_step_min,
                 "offsets": list(c.time.retime_offsets_min), "anchors": list(c.time.anchor_offsets_min),
                 "buffer": c.time.initial_buffer_min},
        "sigma_rule": c.rules.sigma_rule,
    })


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    cfg = load_config(ROOT / "config.toml")
    build_model_zip()
    base = ROOT / "runs" / RUNS["rclock"]
    routes = pd.read_csv(base / "agent_routes.csv")
    personas = pd.read_csv(base / "personas.csv")
    mp, sec_xy = build_map(routes, cfg)
    build_agents(cfg, personas, routes, mp, sec_xy)
    for k, f in RUNS.items():
        build_run(k, f)
    build_site(cfg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
