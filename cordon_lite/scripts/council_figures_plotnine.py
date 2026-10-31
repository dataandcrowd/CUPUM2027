"""Council slide charts in plotnine (Arial): R-clock, seed 1. The slide carries the headline, so no chart titles.

Writes PNGs to runs/figures/council_deck/. Run from cordon_lite/:  python scripts/council_figures_plotnine.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from plotnine import (aes, annotate, coord_flip, element_blank, element_line, element_rect, element_text, facet_wrap,
                      geom_col, geom_errorbar, geom_step, geom_text, ggplot, labs, position_dodge,
                      scale_color_manual, scale_fill_manual, scale_x_continuous, scale_y_continuous, theme,
                      theme_minimal)

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
OUT = RUNS / "figures" / "council_deck"
OUT.mkdir(parents=True, exist_ok=True)

BEFORE = "#2a78d6"
AFTER = "#eb6834"
AFTER_LIGHT = "#f2a98a"
INK = "#1c1b1a"
INK2 = "#52514e"
GRID = "#e4e3df"
BG = "#fbfbf8"
W, H, DPI = 11, 4.6, 300

BASE = theme_minimal(base_size=15, base_family="Arial") + theme(
    plot_background=element_rect(fill=BG, color=BG),
    panel_background=element_rect(fill=BG, color=BG),
    panel_grid_major_x=element_blank(),
    panel_grid_minor=element_blank(),
    panel_grid_major_y=element_line(color=GRID, size=0.6),
    axis_line_x=element_line(color=INK2, size=0.8),
    axis_text=element_text(color=INK2, size=14),
    axis_title=element_text(color=INK2, size=14),
    legend_position="top",
    legend_title=element_blank(),
    legend_text=element_text(color=INK, size=14),
    strip_text=element_text(color=INK, size=15, ha="left"),
)


def save(p, name):
    p.save(OUT / name, width=W, height=H, dpi=DPI, verbose=False)


def fee_table():
    f = pd.read_csv(RUNS / "figures" / "fee_response.csv")
    return f[(f.arm == "R-clock") & (f.seed == 1)].sort_values("peak_fee").reset_index(drop=True)


# 1. Peak hour empties, early shoulder fills
def fig_peak_shift():
    o = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "outcomes.csv")
    car = o[o["mode"] == "CAR"]
    bins = np.arange(360, 616, 15)
    rows = []
    for day, lab in [(5, "Before the charge"), (10, "With the charge")]:
        h, _ = np.histogram(car.loc[car.day == day, "gate_exit_min"], bins)
        h = np.append(h, h[-1])  # close the last step
        rows.append(pd.DataFrame({"minute": bins, "cars": h, "run": lab}))
    d = pd.concat(rows)
    ymax = d.cars.max() * 1.15
    ticks = list(range(360, 616, 30))
    p = (ggplot(d, aes("minute", "cars", color="run"))
         + annotate("rect", xmin=480, xmax=540, ymin=0, ymax=ymax, fill=AFTER, alpha=0.09)
         + annotate("text", x=510, y=ymax * 0.95, label="NZ$6 peak charge", color=AFTER, size=13,
                    fontweight="bold", family="Arial")
         + geom_step(size=1.6, direction="hv")
         + scale_color_manual(values=[BEFORE, AFTER])
         + scale_x_continuous(breaks=ticks, labels=[f"{t // 60:02d}:{t % 60:02d}" for t in ticks],
                              limits=(360, 615), expand=(0, 0))
         + scale_y_continuous(limits=(0, ymax), expand=(0, 0))
         + labs(x="Time the car crosses into the city centre", y="Cars per 15 minutes")
         + BASE)
    save(p, "1_peak_shift.png")


# 2. Diminishing returns: cars vs delay, one facet each (free y, not a dual axis)
def fig_diminishing():
    f = fee_table()
    lab = ["None" if v == 0 else f"${v:.0f}" for v in f.peak_fee]
    tone = ["none" if v == 0 else ("six" if v == 6 else "other") for v in f.peak_fee]
    a = pd.DataFrame({"fee": lab, "value": f.car_crossings_per_day, "tone": tone,
                      "panel": "Cars crossing the cordon per day", "txt": [f"{v:.0f}" for v in f.car_crossings_per_day]})
    b = pd.DataFrame({"fee": lab, "value": f.mean_road_delay, "tone": tone,
                      "panel": "Road delay per car (min)", "txt": [f"{v:.1f}" for v in f.mean_road_delay]})
    d = pd.concat([a, b])
    d["fee"] = pd.Categorical(d.fee, categories=lab, ordered=True)
    d["panel"] = pd.Categorical(d.panel, categories=[a.panel[0], b.panel[0]], ordered=True)
    d["y_lab"] = d.value + d.groupby("panel", observed=True).value.transform("max") * 0.04
    p = (ggplot(d, aes("fee", "value", fill="tone"))
         + geom_col(width=0.64, show_legend=False)
         + geom_text(aes(y="y_lab", label="txt"), va="bottom", size=13, color=INK, family="Arial")
         + facet_wrap("panel", scales="free_y")
         + scale_fill_manual(values={"none": INK2, "six": AFTER, "other": AFTER_LIGHT})
         + scale_y_continuous(expand=(0, 0, 0.14, 0))
         + labs(x="Peak charge (NZ$)", y="")
         + BASE + theme(subplots_adjust={"wspace": 0.18}))
    save(p, "2_diminishing_returns.png")


# 3. Local streets gain, motorway does not
def fig_roads():
    f = fee_table().set_index("peak_fee")
    rows = []
    for fee, run in [(0.0, "No charge"), (6.0, "NZ$6 charge")]:
        rows.append({"road": "Motorways", "run": run, "pct": 100 * f.loc[fee, "los_ef_speed_share_mwy"]})
        rows.append({"road": "Non-motorway roads", "run": run, "pct": 100 * f.loc[fee, "congested_at_share_other"]})
    d = pd.DataFrame(rows)
    d["road"] = pd.Categorical(d.road, categories=["Motorways", "Non-motorway roads"], ordered=True)
    d["run"] = pd.Categorical(d.run, categories=["No charge", "NZ$6 charge"], ordered=True)
    d["txt"] = d.pct.map(lambda v: f"{v:.1f}%")
    dodge = position_dodge(width=0.74)
    p = (ggplot(d, aes("road", "pct", fill="run"))
         + geom_col(position=dodge, width=0.7)
         + geom_text(aes(y="pct + 2.5", label="txt"), position=dodge, va="bottom", size=15,
                     fontweight="bold", color=INK, family="Arial")
         + scale_fill_manual(values=[BEFORE, AFTER])
         + scale_y_continuous(limits=(0, 100), breaks=[0, 25, 50, 75, 100], expand=(0, 0))
         + labs(x="", y="Vehicle-km in congested flow, 07:00-09:00 (%)")
         + BASE + theme(axis_text_x=element_text(size=16, color=INK)))
    save(p, "3_roads.png")


# 4. Who changes
def fig_who():
    w = pd.read_csv(RUNS / "figures" / "who_adapts_R-clock.csv")
    q = w[w.group == "vot_quintile"].sort_values("level")
    labels = ["Lowest 20%", "2nd", "3rd", "4th", "Highest 20%", "Work vehicle"]
    d = pd.DataFrame({
        "group": labels,
        "pct": list(100 * q.left_car_share) + [0.0],
        "lo": list(100 * q.ci_low) + [np.nan],
        "hi": list(100 * q.ci_high) + [np.nan],
        "tone": ["vot"] * 5 + ["fixed"],
    })
    d["group"] = pd.Categorical(d.group, categories=labels, ordered=True)
    d["txt"] = [f"{v:.0f}%" for v in d.pct[:5]] + ["0%, no alternative"]
    d["y_lab"] = d.hi.fillna(0) + 1.2
    p = (ggplot(d, aes("group", "pct", fill="tone"))
         + geom_col(width=0.64, show_legend=False)
         + geom_errorbar(aes(ymin="lo", ymax="hi"), width=0.18, color=INK2, size=0.6, na_rm=True)
         + geom_text(aes(y="y_lab", label="txt"), va="bottom", size=14, fontweight="bold", color=INK,
                     family="Arial")
         + scale_fill_manual(values={"vot": AFTER, "fixed": INK2})
         + scale_y_continuous(limits=(0, 52), expand=(0, 0))
         + labs(x="Value of time, lowest to highest fifth of commuters", y="Drivers who left the car (%)")
         + BASE)
    save(p, "4_who_changes.png")


# 5. Why drivers switched to PT on the charge day: factors named in the decision reason
def fig_reasons():
    d = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "decisions.csv")
    o = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "outcomes.csv")
    car5 = set(o[(o.day == 5) & (o["mode"] == "CAR")].agent_id)
    pt = d[(d.day == 6) & (d["mode"] == "PT") & d.agent_id.isin(car5) & (d.decider == "rule")]
    f = pt.factors.fillna("").str.split(";")
    n = len(pt)
    names = [("other", "Parking or fuel"), ("fee", "The charge"), ("travel_time", "Travel time"),
             ("arrival_time", "Arrival time")]
    r = pd.DataFrame({"factor": [lab for _, lab in names],
                      "pct": [100 * f.map(lambda s, k=k: k in s).sum() / n for k, _ in names]})
    r["factor"] = pd.Categorical(r.factor, categories=[lab for _, lab in names][::-1], ordered=True)
    r["tone"] = ["key", "key", "other", "other"]
    r["txt"] = r.pct.map(lambda v: f"{v:.0f}%")
    p = (ggplot(r, aes("factor", "pct", fill="tone"))
         + geom_col(width=0.62, show_legend=False)
         + geom_text(aes(y="pct + 1.5", label="txt"), ha="left", size=16, fontweight="bold", color=INK,
                     family="Arial")
         + coord_flip()
         + scale_fill_manual(values={"key": AFTER, "other": AFTER_LIGHT})
         + scale_y_continuous(limits=(0, 100), expand=(0, 0))
         + labs(x="", y=f"Share of the {n} drivers who switched to PT on the charge day (%)")
         + BASE + theme(axis_text_y=element_text(size=17, color=INK), panel_grid_major_y=element_blank(),
                        panel_grid_major_x=element_line(color=GRID, size=0.6), axis_line_x=element_blank()))
    save(p, "5_reasons.png")


# 6. PT openness
def fig_pt_open():
    w = pd.read_csv(RUNS / "figures" / "who_adapts_R-clock.csv")
    q = w[w.group == "P"].sort_values("level")
    labels = ["Least open", "2", "3", "4", "Most open"]
    d = pd.DataFrame({"level": labels, "pct": 100 * q.left_car_share.to_numpy(),
                      "lo": 100 * q.ci_low.to_numpy(), "hi": 100 * q.ci_high.to_numpy()})
    d["level"] = pd.Categorical(d.level, categories=labels, ordered=True)
    d["txt"] = d.pct.map(lambda v: f"{v:.0f}%")
    p = (ggplot(d, aes("level", "pct"))
         + geom_col(width=0.62, fill=BEFORE)
         + geom_errorbar(aes(ymin="lo", ymax="hi"), width=0.18, color=INK2, size=0.6)
         + geom_text(aes(y="hi + 1.2", label="txt"), va="bottom", size=14, fontweight="bold", color=INK,
                     family="Arial")
         + scale_y_continuous(limits=(0, 55), expand=(0, 0))
         + labs(x="Openness to public transport (five levels)", y="Drivers who left the car (%)")
         + BASE)
    save(p, "6_pt_openness.png")


# 7. Decisions per day: decide every morning vs decision clock
def fig_calls():
    rows = []
    for run, lab in [("R-daily_mock_py_s1", "Decide every morning"), ("R-clock_mock_py_s1", "Decision clock")]:
        d = pd.read_csv(RUNS / run / "decisions.csv")
        c = d[d.decider == "rule"].groupby("day").size().reindex(range(1, 11), fill_value=0)
        rows.append(pd.DataFrame({"day": c.index.astype(str), "n": c.to_numpy(), "run": lab}))
    d = pd.concat(rows)
    d["day"] = pd.Categorical(d.day, categories=[str(i) for i in range(1, 11)], ordered=True)
    d["run"] = pd.Categorical(d.run, categories=["Decide every morning", "Decision clock"], ordered=True)
    clock = d[d.run == "Decision clock"].copy()
    clock["txt"] = clock.n.astype(str)
    dodge = position_dodge(width=0.8)
    p = (ggplot(d, aes("day", "n", fill="run"))
         + geom_col(position=dodge, width=0.76)
         + annotate("rect", xmin=5.5, xmax=10.5, ymin=0, ymax=1080, fill=AFTER, alpha=0.07)
         + annotate("text", x=8, y=1040, label="Charge in place", color=AFTER, size=13, fontweight="bold",
                    family="Arial")
         + geom_text(aes(x="day", y="n + 20", label="txt"), data=clock, nudge_x=0.2, va="bottom", size=12,
                     color=INK, family="Arial", inherit_aes=False)
         + scale_fill_manual(values=["#b9b6ae", AFTER])
         + scale_y_continuous(limits=(0, 1080), expand=(0, 0))
         + labs(x="Day", y="Commuters making a fresh decision")
         + BASE)
    save(p, "7_decisions_per_day.png")



# 8. Where each corridor's drivers live (2023 Census OD): map coloured by corridor + corridor shares
CORRIDORS = {  # corridor_id -> (entry, where its drivers mostly live), from data/origins.csv joined to SA2s
    4: ("Harbour Bridge", "North Shore"),
    3: ("inner-west ramps", "Inner and west Auckland"),
    1: ("Parnell", "Remuera and east Auckland"),
    2: ("Southern Motorway", "Epsom and south Auckland"),
    0: ("the waterfront", "Eastern bays"),
}
CORRIDOR_COLORS = {4: "#2a78d6", 3: "#eb6834", 1: "#1baf7a", 2: "#eda100", 0: "#4a3aa7"}
SA2_GPKG = ROOT / ".." / ".." / "gtfs-isochrone" / "data" / "sa2" / "auckland_sa2.gpkg"


def _corridor_sa2():
    import geopandas as gpd
    sa2 = gpd.read_file(SA2_GPKG)[["SA22026_V1_00", "geometry"]].rename(columns={"SA22026_V1_00": "code"})
    o = pd.read_csv(ROOT / "data" / "origins.csv")
    og = gpd.GeoDataFrame(o, geometry=gpd.points_from_xy(o.x_nztm, o.y_nztm), crs=2193)
    j = gpd.sjoin(og, sa2, predicate="within", how="inner")
    w = j.groupby(["code", "corridor_id"]).weight.sum().reset_index()
    dom = w.sort_values("weight").groupby("code").tail(1).set_index("code").corridor_id
    od = pd.read_csv(ROOT / "data" / "od_sa2.csv", dtype={"sa2_code": str}).set_index("sa2_code").drivers_to_cordon
    sa2["corridor"] = sa2.code.map(dom)
    sa2["drivers"] = sa2.code.map(od).fillna(0)
    shares = o.groupby("corridor_id").weight.sum() / o.weight.sum()
    return sa2, shares


def fig_corridor_map():
    import geopandas as gpd
    from plotnine import coord_fixed, geom_map, scale_alpha_continuous
    sa2, _ = _corridor_sa2()
    cordon = gpd.read_file(ROOT / "data" / "cordon.geojson").to_crs(2193)
    cx, cy = cordon.geometry.union_all().centroid.coords[0]
    r = 21000
    box = sa2.cx[cx - r:cx + r, cy - r:cy + r].copy()
    box["geometry"] = box.geometry.clip_by_rect(cx - r, cy - r, cx + r, cy + r)
    box = box[~box.geometry.is_empty]
    has = box[box.corridor.notna()].copy()
    has["corridor"] = pd.Categorical(has.corridor.astype(int).astype(str), categories=[str(k) for k in CORRIDORS])
    has["dens"] = np.log1p(has.drivers)
    labels = pd.DataFrame([  # area names placed at representative SA2 points, NZTM
        ("North Shore", cx - 1500, cy + 11000), ("Eastern bays", cx + 7500, cy - 1200),
        ("Remuera", cx + 3600, cy - 4200), ("Epsom, Onehunga", cx - 600, cy - 9000),
        ("Grey Lynn,\nPt Chevalier", cx - 6300, cy - 2400), ("West Auckland", cx - 15000, cy + 1500),
        ("East Auckland", cx + 15500, cy - 9500), ("South Auckland", cx + 4000, cy - 14500),
        ("City centre", cx + 300, cy + 1900)], columns=["label", "x", "y"])
    p = (ggplot()
         + geom_map(box, fill="#ecebe6", color=BG, size=0.15)
         + geom_map(has, aes(fill="corridor", alpha="dens"), color=BG, size=0.15)
         + geom_map(cordon, fill=INK, color=INK)
         + geom_text(aes("x", "y", label="label"), data=labels, size=12, fontweight="bold", color=INK,
                     family="Arial")
         + scale_fill_manual(values={str(k): v for k, v in CORRIDOR_COLORS.items()}, guide=None)
         + scale_alpha_continuous(range=(0.35, 1.0), guide=None)
         + coord_fixed(xlim=(cx - r, cx + r), ylim=(cy - r, cy + r), expand=False)
         + BASE + theme(axis_text=element_blank(), axis_title=element_blank(), axis_line_x=element_blank(),
                        panel_grid_major_y=element_blank()))
    p.save(OUT / "8_corridor_map.png", width=6.4, height=6.4, dpi=DPI, verbose=False)


def fig_corridor_shares():
    _, shares = _corridor_sa2()
    n = len(CORRIDORS)
    d = pd.DataFrame([{"k": str(k), "x": n - i, "label": f"{h}, via {e}", "pct": 100 * shares[k]}
                      for i, (k, (e, h)) in enumerate(CORRIDORS.items())])
    d["txt"] = d.pct.map(lambda v: f"{v:.0f}%")
    p = (ggplot(d, aes("x", "pct", fill="k"))
         + geom_col(width=0.42, show_legend=False)
         + geom_text(aes(x="x + 0.24", y=0, label="label"), ha="left", va="bottom", size=14, color=INK,
                     family="Arial")
         + geom_text(aes(y="pct + 0.6", label="txt"), ha="left", size=14, fontweight="bold", color=INK,
                     family="Arial")
         + coord_flip()
         + scale_fill_manual(values={str(k): v for k, v in CORRIDOR_COLORS.items()})
         + scale_y_continuous(limits=(0, 42), expand=(0, 0))
         + scale_x_continuous(limits=(0.6, n + 0.75), expand=(0, 0))
         + labs(x="", y="")
         + BASE + theme(axis_text=element_blank(), panel_grid_major_y=element_blank(),
                        panel_grid_major_x=element_blank(), axis_line_x=element_blank()))
    p.save(OUT / "9_corridor_shares.png", width=7.0, height=3.4, dpi=DPI, verbose=False)

# 10. Mode share by day: the step on the charge day, then it holds
def fig_mode_by_day():
    o = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "outcomes.csv")
    m = o.groupby("day")["mode"].value_counts(normalize=True).rename("share").reset_index()
    names = {"CAR": "Car", "PT": "Public transport", "WFH": "Work from home"}
    m["mode"] = pd.Categorical(m["mode"].map(names), categories=["Work from home", "Public transport", "Car"],
                               ordered=True)
    m["day"] = pd.Categorical(m.day.astype(str), categories=[str(i) for i in range(1, 11)], ordered=True)
    m["pct"] = 100 * m.share
    lab = m[m.day.isin(["5", "10"]) & (m["mode"] != "Work from home")].copy()
    lab["txt"] = lab.pct.map(lambda v: f"{v:.0f}%")
    lab["y"] = np.where(lab["mode"] == "Car", lab.pct / 2, 100 - lab.pct / 2)
    p = (ggplot(m, aes("day", "pct", fill="mode"))
         + geom_col(width=0.78)
         + geom_text(aes("day", "y", label="txt"), data=lab, size=14, fontweight="bold", color="#fbfbf8",
                     family="Arial", inherit_aes=False)
         + annotate("text", x=8, y=106, label="Charge in place", color=AFTER, size=13, fontweight="bold",
                    family="Arial")
         + annotate("segment", x=5.6, xend=10.4, y=102, yend=102, color=AFTER, size=1.2)
         + scale_fill_manual(values={"Car": INK2, "Public transport": BEFORE, "Work from home": "#1baf7a"})
         + scale_y_continuous(limits=(0, 110), breaks=[0, 25, 50, 75, 100], expand=(0, 0))
         + labs(x="Day", y="Share of commuters (%)")
         + BASE + theme(legend_position="bottom"))
    p.save(OUT / "10_mode_by_day.png", width=6.6, height=4.6, dpi=DPI, verbose=False)


# 11. Delay by departure time: where the time is saved
def fig_delay_by_departure():
    o = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "outcomes.csv")
    c = o[(o["mode"] == "CAR") & (o.day >= 2)].copy()
    c["delay"] = c.road_delay_min + c.queue_delay_min
    c["bin"] = (c.depart_min // 15) * 15
    c["run"] = np.where(c.day <= 5, "No charge (days 2-5)", "NZ$6 charge (days 6-10)")
    d = c.groupby(["bin", "run"]).agg(delay=("delay", "mean"), n=("delay", "size")).reset_index()
    d = d[(d.n >= 20) & d.bin.between(375, 585)]
    rows = []
    for run, g in d.groupby("run"):  # step outline closed at the last bin
        g = g.sort_values("bin")
        rows.append(pd.concat([g, g.tail(1).assign(bin=g.bin.iloc[-1] + 15)]))
    d = pd.concat(rows)
    d["run"] = pd.Categorical(d.run, categories=["No charge (days 2-5)", "NZ$6 charge (days 6-10)"], ordered=True)
    ticks = list(range(390, 601, 30))
    p = (ggplot(d, aes("bin", "delay", color="run"))
         + annotate("rect", xmin=465, xmax=525, ymin=0, ymax=14, fill=AFTER, alpha=0.08)
         + geom_step(size=1.6, direction="hv")
         + scale_color_manual(values=[BEFORE, AFTER])
         + scale_x_continuous(breaks=ticks, labels=[f"{t // 60:02d}:{t % 60:02d}" for t in ticks],
                              limits=(375, 600), expand=(0, 0))
         + scale_y_continuous(limits=(0, 14), breaks=[0, 4, 8, 12], expand=(0, 0))
         + labs(x="Departure time from home", y="Delay per car (min)")
         + BASE + theme(legend_position="bottom"))
    p.save(OUT / "11_delay_by_departure.png", width=6.6, height=4.6, dpi=DPI, verbose=False)


if __name__ == "__main__":
    fig_peak_shift()
    fig_diminishing()
    fig_roads()
    fig_who()
    fig_reasons()
    fig_pt_open()
    fig_calls()
    fig_corridor_map()
    fig_corridor_shares()
    fig_mode_by_day()
    fig_delay_by_departure()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
