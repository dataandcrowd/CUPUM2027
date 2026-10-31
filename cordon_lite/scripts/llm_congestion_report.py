"""Where and when the charge relieves congestion: H-clock (LLM) against R-clock (rule).

    python scripts/llm_congestion_report.py --out runs/llm_behaviour \
        --pair NZ6_s1=full_H-clock_s1,full_R-clock_s1 --pair NZ6_s2=full_H-clock_s2,full_R-clock_s2

Each --pair is LABEL=H_RUN,R_RUN (folders in runs/, same seed and settings). Before = days 2 to the day before
the charge, charge = the charge day to the last day; every value is a daily mean over those days. Writes to --out:
    congestion_summary.csv      per run: commuter mode shares, car crossings in the peak-charge hour (gate exit
                                08:00-09:00) and outside it, delays of the commuters' car trips, and vehicle-hours
                                of delay of all vehicles on the simulated roads, 06:00-10:00
    congestion_by_corridor.csv  per run and entry corridor: car trips, road delay and gate queue per trip
    congestion_by_home.csv      per run and home area (compass sector and crow-fly distance from the destination):
                                commuters, who left the car among the base drivers, delay per remaining car trip
    congestion_by_region.csv    per run and road region (roads.LOS_REGIONS): vehicle-hours of delay, mean V/C
    congestion_by_street.csv    per run and street: vehicle-hours of delay and delay per car 07:00-09:00
    congestion_by_street_hour.csv  per run, street and hour bin 06:00-10:00: vehicle-hours of delay, to find
                                where delay grows in one hour although it falls over the morning
    delay_by_departure.csv      per run and 15-min crossing (gate exit) bin: car entries and road + queue delay per trip
    congestion.md               the main tables side by side
Vehicle-hours come from road_los.csv: flow = vc_mean x cap_vph per hour bin, delay per vehicle =
ff_min x (1 / speed_factor_mean - 1), summed over the four hour bins 06:00-10:00 (hour means, so an
approximation; the same for both arms). Reads run folders only.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cordonlite.roads import LOS_REGIONS, los_region_of  # noqa: E402

CHARGE_DAY_DEFAULT = 6
DEST_XY = (1757409.0, 5920504.0)          # destination node, data/prep_report.md
PEAK = (480, 540)                         # gate minute of the peak charge, 08:00-09:00
HOUR_BINS = ("06:00-07:00", "07:00-08:00", "08:00-09:00", "09:00-10:00")
SECTORS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
DIST_BANDS = [0, 5, 10, 15, 20, 30, 1e9]
DIST_LABELS = ["0-5 km", "5-10 km", "10-15 km", "15-20 km", "20-30 km", "30+ km"]


def periods(o: pd.DataFrame, cd: int) -> dict[str, pd.DataFrame]:
    return {"before": o[(o["day"] >= 2) & (o["day"] < cd)], "charge": o[o["day"] >= cd]}


def home_areas(p: pd.DataFrame) -> pd.DataFrame:
    dx, dy = p["x_nztm"] - DEST_XY[0], p["y_nztm"] - DEST_XY[1]
    ang = np.degrees(np.arctan2(dy, dx)) % 360
    out = pd.DataFrame(index=p.index)
    out["sector"] = [SECTORS[int(((a + 22.5) % 360) // 45)] for a in ang]
    out["distance"] = pd.cut(np.hypot(dx, dy) / 1000, DIST_BANDS, labels=DIST_LABELS, right=False).astype(str)
    return out


def section_table() -> pd.DataFrame:
    s = pd.read_csv(ROOT / "data" / "road_sections.csv")
    s["region"] = [LOS_REGIONS[los_region_of(n if isinstance(n, str) else "", x, y)]
                   for n, x, y in zip(s["street_name"], s["x_mid"], s["y_mid"])]
    return s.set_index("section_id")[["region"]]


def road_delay(run: Path, regions: pd.DataFrame) -> pd.DataFrame:
    """Vehicle-hours of delay and V/C per section, hour bin and period (d2-5 / d6-10)."""
    los = pd.read_csv(run / "road_los.csv")
    sec = pd.read_csv(run / "road_sections.csv").set_index("section_id")[["ff_min", "cap_vph"]]
    los = los.join(sec, on="section_id").join(regions, on="section_id")
    los["flow_vph"] = los["vc_mean"] * los["cap_vph"]
    los["delay_min"] = los["ff_min"] * (1 / los["speed_factor_mean"].clip(lower=1e-6) - 1)
    los["veh_h"] = los["flow_vph"] * los["delay_min"] / 60
    los["period"] = los["period"].map({"d2-5": "before", "d6-10": "charge"})
    return los


def summary_row(label: str, arm: str, run: Path, o: pd.DataFrame, los: pd.DataFrame, cd: int) -> dict:
    row = {"scenario": label, "arm": arm, "run": run.name}
    n_agents = o["agent_id"].nunique()
    for tag, x in periods(o, cd).items():
        n = x["day"].nunique()
        cars = x[x["mode"] == "CAR"]
        peak = cars["gate_exit_min"].between(PEAK[0], PEAK[1] - 1e-9)
        row.update({f"car_share_{tag}": len(cars) / n / n_agents, f"pt_share_{tag}": (x["mode"] == "PT").sum() / n / n_agents,
                    f"wfh_share_{tag}": (x["mode"] == "WFH").sum() / n / n_agents,
                    f"cars_peak_hour_{tag}": peak.sum() / n, f"cars_other_hours_{tag}": (~peak).sum() / n,
                    f"road_delay_per_car_{tag}": cars["road_delay_min"].mean(),
                    f"queue_per_car_{tag}": cars["queue_delay_min"].mean(),
                    f"door_to_door_{tag}": cars["travel_min"].mean(),
                    f"late_share_of_car_trips_{tag}": (cars["late_min"] > 5).mean()})
        y = los[(los["period"] == tag) & los["bin"].isin(HOUR_BINS)]
        row[f"veh_h_all_roads_{tag}"] = y["veh_h"].sum()
        row[f"veh_h_motorway_{tag}"] = y.loc[y["mwy"] == 1, "veh_h"].sum()
        row[f"veh_h_other_roads_{tag}"] = y.loc[y["mwy"] == 0, "veh_h"].sum()
    for k in ("cars_peak_hour", "cars_other_hours", "veh_h_all_roads", "veh_h_motorway", "veh_h_other_roads"):
        row[f"{k}_change_pct"] = 100 * (row[f"{k}_charge"] / row[f"{k}_before"] - 1)
    return row


def by_corridor(label: str, arm: str, o: pd.DataFrame, names: dict, cd: int) -> list[dict]:
    rows = []
    for cid, g in o.groupby("corridor_id"):
        r = {"scenario": label, "arm": arm, "corridor": names.get(int(cid), str(cid)).split(" (")[0]}
        for tag, x in periods(g, cd).items():
            cars = x[x["mode"] == "CAR"]
            r.update({f"car_trips_{tag}": len(cars) / x["day"].nunique(),
                      f"road_delay_per_trip_{tag}": cars["road_delay_min"].mean(),
                      f"queue_per_trip_{tag}": cars["queue_delay_min"].mean()})
        r["delay_per_trip_change_min"] = (r["road_delay_per_trip_charge"] + r["queue_per_trip_charge"]
                                          - r["road_delay_per_trip_before"] - r["queue_per_trip_before"])
        rows.append(r)
    return rows


def by_home(label: str, arm: str, o: pd.DataFrame, areas: pd.DataFrame, cd: int) -> list[dict]:
    w = o.pivot(index="agent_id", columns="day", values="mode")
    base = w[[d for d in w.columns if 2 <= d < cd]].eq("CAR").all(axis=1)
    last = w[w.columns.max()]
    rows = []
    for kind in ("sector", "distance"):
        for level, ids in areas.groupby(kind).groups.items():
            g = o[o["agent_id"].isin(ids)]
            b = base.reindex(ids).fillna(False)
            r = {"scenario": label, "arm": arm, "grouping": kind, "area": level, "commuters": len(ids),
                 "base_drivers": int(b.sum()),
                 "left_car_share": float((last.reindex(ids)[b] != "CAR").mean()) if b.any() else math.nan,
                 "to_pt_share": float((last.reindex(ids)[b] == "PT").mean()) if b.any() else math.nan,
                 "to_wfh_share": float((last.reindex(ids)[b] == "WFH").mean()) if b.any() else math.nan}
            for tag, x in periods(g, cd).items():
                cars = x[x["mode"] == "CAR"]
                r[f"car_trips_{tag}"] = len(cars) / x["day"].nunique()
                r[f"delay_per_trip_{tag}"] = (cars["road_delay_min"] + cars["queue_delay_min"]).mean()
            r["delay_per_trip_change_min"] = r["delay_per_trip_charge"] - r["delay_per_trip_before"]
            rows.append(r)
    return rows


def by_region(label: str, arm: str, los: pd.DataFrame) -> list[dict]:
    rows = []
    for reg, g in los.groupby("region"):
        r = {"scenario": label, "arm": arm, "region": reg,
             "km": g.drop_duplicates("section_id")["km"].sum()}
        for tag in ("before", "charge"):
            y = g[(g["period"] == tag) & g["bin"].isin(HOUR_BINS)]
            z = g[(g["period"] == tag) & (g["bin"] == "07:00-09:00")]
            r[f"veh_h_{tag}"] = y["veh_h"].sum()
            r[f"vc_mean_0709_{tag}"] = np.average(z["vc_mean"], weights=z["km"])
        r["veh_h_change"] = r["veh_h_charge"] - r["veh_h_before"]
        r["veh_h_change_pct"] = 100 * r["veh_h_change"] / r["veh_h_before"]
        rows.append(r)
    return rows


def by_street(label: str, arm: str, los: pd.DataFrame) -> list[dict]:
    rows = []
    for (street, mwy), g in los.groupby(["street_name", "mwy"]):
        r = {"scenario": label, "arm": arm, "street": street, "motorway": int(mwy),
             "km": g.drop_duplicates("section_id")["km"].sum()}
        for tag in ("before", "charge"):
            y = g[(g["period"] == tag) & g["bin"].isin(HOUR_BINS)]
            z = g[(g["period"] == tag) & g["bin"].isin(("07:00-08:00", "08:00-09:00"))]
            r[f"veh_h_{tag}"] = y["veh_h"].sum()
            # delay of a car driving every simulated section of the street, 07:00-09:00, weighted by flow
            per_sec = z.groupby("section_id").apply(
                lambda s: np.average(s["delay_min"], weights=s["flow_vph"]) if s["flow_vph"].sum() > 0 else 0.0,
                include_groups=False)
            r[f"delay_per_car_0709_{tag}"] = per_sec.sum()
        r["veh_h_change"] = r["veh_h_charge"] - r["veh_h_before"]
        rows.append(r)
    return rows


def by_street_hour(label: str, arm: str, los: pd.DataFrame) -> pd.DataFrame:
    y = (los[los["bin"].isin(HOUR_BINS)].groupby(["street_name", "mwy", "bin", "period"])["veh_h"].sum()
         .unstack("period").reset_index())
    y = y.rename(columns={"street_name": "street", "mwy": "motorway", "before": "veh_h_before",
                          "charge": "veh_h_charge"})
    y["veh_h_change"] = y["veh_h_charge"] - y["veh_h_before"]
    y.insert(0, "arm", arm)
    y.insert(0, "scenario", label)
    return y


def by_departure(label: str, arm: str, o: pd.DataFrame, cd: int) -> list[dict]:
    rows = []
    for tag, x in periods(o, cd).items():
        cars = x[x["mode"] == "CAR"].copy()
        n = x["day"].nunique()
        cars["bin"] = (cars["gate_exit_min"] // 15 * 15).astype(int)
        for b, g in cars.groupby("bin"):
            rows.append({"scenario": label, "arm": arm, "period": tag,
                         "gate_bin": f"{b // 60:02d}:{b % 60:02d}", "car_entries": len(g) / n,
                         "road_plus_queue_per_trip": (g["road_delay_min"] + g["queue_delay_min"]).mean()})
    return rows


def md_table(df: pd.DataFrame, cols: list[str], fmt: dict | None = None) -> list[str]:
    fmt = fmt or {}
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(fmt.get(c, "{}").format(r[c]) if not isinstance(r[c], str) else r[c]
                                     for c in cols) + " |")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pair", action="append", required=True, help="LABEL=H_RUN,R_RUN")
    ap.add_argument("--out", default="runs/llm_behaviour")
    ap.add_argument("--charge-day", type=int, default=CHARGE_DAY_DEFAULT)
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    cd = args.charge_day
    regions = section_table()
    summ, corr, home, reg, street, street_hour, dep = [], [], [], [], [], [], []
    for spec in args.pair:
        label, runs = spec.split("=", 1)
        for arm, name in zip(("H-clock", "R-clock"), runs.split(",")):
            run = ROOT / "runs" / name
            o = pd.read_csv(run / "outcomes.csv")
            p = pd.read_csv(run / "personas.csv").set_index("agent_id")
            names = {int(c): n for c, n in pd.read_csv(run / "corridors.csv")[["corridor_id", "name"]].values}
            los = road_delay(run, regions)
            summ.append(summary_row(label, arm, run, o, los, cd))
            corr += by_corridor(label, arm, o, names, cd)
            home += by_home(label, arm, o, home_areas(p), cd)
            reg += by_region(label, arm, los)
            street += by_street(label, arm, los)
            street_hour.append(by_street_hour(label, arm, los))
            dep += by_departure(label, arm, o, cd)
    frames = {"congestion_summary": pd.DataFrame(summ), "congestion_by_corridor": pd.DataFrame(corr),
              "congestion_by_home": pd.DataFrame(home), "congestion_by_region": pd.DataFrame(reg),
              "congestion_by_street": pd.DataFrame(street), "congestion_by_street_hour": pd.concat(street_hour),
              "delay_by_departure": pd.DataFrame(dep)}
    for name, df in frames.items():
        df.round(4).to_csv(out / f"{name}.csv", index=False, lineterminator="\n")

    md = ["# Where and when the charge relieves congestion: rule (R-clock) and LLM (H-clock)", "",
          f"Before = days 2-{cd - 1}, charge = days {cd}-10; daily means. Vehicle-hours: all vehicles on the "
          "simulated roads (background traffic and commuters), 06:00-10:00, from road_los.csv hour means.", ""]
    s = frames["congestion_summary"]
    for c in ("car_share", "pt_share", "wfh_share", "road_delay_per_car", "queue_per_car", "door_to_door"):
        s[c] = s[f"{c}_before"].map("{:.3f}".format) + " -> " + s[f"{c}_charge"].map("{:.3f}".format)
    md += ["## Summary", ""] + md_table(s, ["scenario", "arm", "car_share", "pt_share", "wfh_share",
                                          "cars_peak_hour_change_pct", "cars_other_hours_change_pct",
                                          "road_delay_per_car", "queue_per_car", "veh_h_all_roads_before",
                                          "veh_h_all_roads_change_pct", "veh_h_motorway_change_pct",
                                          "veh_h_other_roads_change_pct"],
                                       {c: "{:.1f}" for c in s.columns}) + [""]
    for name, cols in (("congestion_by_region", ["scenario", "arm", "region", "km", "veh_h_before", "veh_h_change",
                                                 "veh_h_change_pct", "vc_mean_0709_before", "vc_mean_0709_charge"]),
                       ("congestion_by_corridor", ["scenario", "arm", "corridor", "car_trips_before", "car_trips_charge",
                                                   "road_delay_per_trip_before", "road_delay_per_trip_charge",
                                                   "queue_per_trip_before", "queue_per_trip_charge",
                                                   "delay_per_trip_change_min"])):
        md += [f"## {name.replace('congestion_', '').replace('_', ' ')}", ""]
        md += md_table(frames[name], cols, {c: "{:.2f}" for c in cols}) + [""]
    h = frames["congestion_by_home"]
    md += ["## by home area", ""] + md_table(h, ["scenario", "arm", "grouping", "area", "commuters", "base_drivers",
                                                 "left_car_share", "to_pt_share", "delay_per_trip_before",
                                                 "delay_per_trip_charge", "delay_per_trip_change_min"],
                                             {c: "{:.2f}" for c in h.columns}) + [""]
    st = frames["congestion_by_street"]
    st = st[st["veh_h_before"] >= 40]
    md += ["## streets with the largest change (at least 40 vehicle-hours of delay before the charge)", ""]
    for (label, arm), g in st.groupby(["scenario", "arm"], sort=False):
        md += [f"### {label}, {arm}", ""] + md_table(g.sort_values("veh_h_change").head(12),
            ["street", "km", "veh_h_before", "veh_h_change", "delay_per_car_0709_before",
             "delay_per_car_0709_charge"], {c: "{:.2f}" for c in g.columns}) + [""]
    sh = frames["congestion_by_street_hour"]
    md += ["## street-hours where delay grew by more than 1 vehicle-hour", ""]
    md += md_table(sh[sh["veh_h_change"] > 1].sort_values(["scenario", "arm", "veh_h_change"],
                                                            ascending=[True, True, False]),
                   ["scenario", "arm", "street", "bin", "veh_h_before", "veh_h_change"],
                   {"veh_h_before": "{:.1f}", "veh_h_change": "{:.1f}"}) + [""]
    (out / "congestion.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
