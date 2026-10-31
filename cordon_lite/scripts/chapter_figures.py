"""Figures for the CUPUM 2027 chapter (version 5): study area, morning profile, road maps, distance.

    python scripts/chapter_figures.py --out runs/figures/chapter

Writes to --out (PNG, 300 dpi, 16 cm wide to fit an A4 page with 2.54 cm margins):
    fig1_study_area.png     land, TomTom major roads, the simulated road sections, commuter origins and the
                            cordon, with an inset of the city centre and its gates by corridor
    fig2_pipeline.png       one simulated morning: options, cognitive clock, decider (rule or LLM), traffic and
                            memory, with the inputs and outputs of the model
    fig3_time_profile.png   change in commuter car crossings and in road + queue delay per trip by 15-min
                            crossing time, days 6-10 against days 2-5 of each arm, R-clock against H-clock (seed 1)
    fig4_road_change.png    change in vehicle-hours of delay per road section, days 6-10 against days 2-5,
                            06:00-08:00 and 08:00-10:00, R-clock against H-clock (seed 1)
    fig5_distance.png       road delay per car trip and share who drive by route length, before the charge
                            and at the NZ$6 peak, R-clock against H-clock (seed 1)
Reads data/, netlogo7/gis/, the SA2 polygons of prep.sa2_gpkg (land outline only), runs/full_*-clock_s1 and
runs/llm_behaviour/delay_by_departure.csv. Vehicle-hours as in scripts/llm_congestion_report.py.
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import shapefile  # noqa: E402  (pyshp)
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, Normalize  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from matplotlib.patches import Polygon as MplPolygon  # noqa: E402
from shapely import wkb  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import llm_congestion_report as C  # noqa: E402

GIS = ROOT / "netlogo7" / "gis"
SA2_GPKG = ROOT / ".." / ".." / "gtfs-isochrone" / "data" / "sa2" / "auckland_sa2.gpkg"
H_RUN, R_RUN = ROOT / "runs" / "full_H-clock_s1", ROOT / "runs" / "full_R-clock_s1"
WIDTH_IN = 16 / 2.54

# reference palette (dataviz skill, light mode): slot 1 blue = rule, slot 2 orange = LLM
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
RULE, LLM = "#2a78d6", "#eb6834"
LAND, WATER, ROAD = "#f3f2ee", "#ffffff", "#d3d2cc"
DIVERGING = LinearSegmentedColormap.from_list(
    "blue_grey_red", ["#184f95", "#5598e7", "#dcdbd7", "#ec7b7a", "#b3302f"])

plt.rcParams.update({"font.family": "Arial", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 9, "axes.titleweight": "normal",
                     "savefig.dpi": 300, "savefig.facecolor": "white"})


def land_outline():
    con = sqlite3.connect(SA2_GPKG)
    geoms = []
    for (blob,) in con.execute("SELECT geom FROM statistical_area_2_2026_clipped"):
        flags = blob[3]
        env = {0: 0, 1: 32, 2: 48, 3: 48, 4: 64}[(flags >> 1) & 0x07]
        geoms.append(wkb.loads(bytes(blob[8 + env:])))
    return unary_union(geoms)


def draw_polygon(ax, geom, **kw):
    for g in getattr(geom, "geoms", [geom]):
        ax.add_patch(MplPolygon(np.asarray(g.exterior.coords), closed=True, **kw))
        for hole in g.interiors:
            ax.add_patch(MplPolygon(np.asarray(hole.coords), closed=True, facecolor=WATER, edgecolor="none",
                                    zorder=kw.get("zorder", 0)))


def road_shapes() -> tuple[dict, pd.DataFrame]:
    r = shapefile.Reader(str(GIS / "tomtom_major_roads"))
    lines, rows = {}, []
    for sr in r.iterShapeRecords():
        seg, frc = sr.record["segment_id"], sr.record["frc"]
        pts, parts = sr.shape.points, list(sr.shape.parts) + [len(sr.shape.points)]
        lines[seg] = [np.asarray(pts[a:b]) for a, b in zip(parts[:-1], parts[1:])]
        rows.append((seg, frc))
    return lines, pd.DataFrame(rows, columns=["segment_id", "frc"])


def section_lines(lines: dict) -> dict[int, list]:
    out: dict[int, list] = {}
    for sid, seg in pd.read_csv(ROOT / "data" / "section_segments.csv")[["section_id", "segment_id"]].values:
        out.setdefault(int(sid), []).extend(lines.get(seg, []))
    return out


def cordon_polygon():
    r = shapefile.Reader(str(GIS / "cordon"))
    pts = np.asarray(r.shape(0).points)
    return pts


def fig1(out: Path, lines: dict, frc: pd.DataFrame, sec: dict, land) -> None:
    origins = pd.read_csv(ROOT / "data" / "origins.csv")
    gates = pd.read_csv(ROOT / "data" / "gates.csv")
    names = pd.read_csv(ROOT / "data" / "corridors.csv").set_index("corridor_id")["name"].str.split(" \\(").str[0]
    cordon = cordon_polygon()
    used = [ln for s in sec.values() for ln in s]
    xy = np.vstack(used + [origins[["x_nztm", "y_nztm"]].to_numpy()])
    x0, y0 = xy.min(axis=0) - 1500
    x1, y1 = xy.max(axis=0) + 1500
    fig = plt.figure(figsize=(WIDTH_IN, WIDTH_IN * 0.62))
    ax = fig.add_axes([0.0, 0.0, 0.60, 1.0])
    ax2 = fig.add_axes([0.63, 0.34, 0.36, 0.58])
    for a in (ax, ax2):
        a.set_facecolor(WATER)
        draw_polygon(a, land, facecolor=LAND, edgecolor="none", zorder=0)
        a.set_xticks([])
        a.set_yticks([])
        for s in a.spines.values():
            s.set_edgecolor(GRID)
    mw = set(frc.loc[frc["frc"] == 0, "segment_id"])
    allr = [ln for seg, ls in lines.items() if seg not in mw for ln in ls]
    mwy = [ln for seg in mw for ln in lines.get(seg, [])]
    ax.add_collection(LineCollection(allr, colors=ROAD, linewidths=0.25, zorder=1))
    ax.add_collection(LineCollection(mwy, colors="#a9a8a2", linewidths=0.8, zorder=2))
    ax.add_collection(LineCollection(used, colors=RULE, linewidths=0.55, zorder=3))
    w = origins.groupby(["x_nztm", "y_nztm"])["weight"].sum().reset_index()
    ax.scatter(w["x_nztm"], w["y_nztm"], s=np.minimum(0.6 + 0.8 * w["weight"], 10), color=LLM, linewidths=0,
               alpha=0.75, zorder=4)
    ax.add_patch(MplPolygon(cordon, closed=True, facecolor=INK, edgecolor=INK, zorder=5))
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal")
    bx0, by0 = cordon.min(axis=0) - 900
    bx1, by1 = cordon.max(axis=0) + 900
    ax.add_patch(plt.Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fill=False, edgecolor=INK2, linewidth=0.6, zorder=6))
    ax.plot([x0 + 1500, x0 + 6500], [y0 + 1200] * 2, color=INK, linewidth=1.2, zorder=7)
    ax.text(x0 + 4000, y0 + 1700, "5 km", ha="center", va="bottom", color=INK, fontsize=7, zorder=7)
    ax.text(x0 + 1500, y1 - 1300, "a  Study area", fontsize=9, color=INK, va="top", fontweight="bold")
    # inset: the city centre, buildings and gates
    bld = shapefile.Reader(str(GIS / "cbd_buildings"))
    ax2.add_collection(LineCollection(allr + mwy, colors=ROAD, linewidths=0.4, zorder=1))
    ax2.add_collection(LineCollection(used, colors=RULE, linewidths=0.9, zorder=3))
    ax2.add_patch(MplPolygon(cordon, closed=True, facecolor="#e8e7e2", edgecolor=INK, linewidth=1.0, zorder=2))
    for shp in bld.iterShapes():
        ax2.add_patch(MplPolygon(np.asarray(shp.points), closed=True, facecolor="#c9c8c1", edgecolor="none",
                                 zorder=2.5))
    ax2.scatter(gates["x_nztm"], gates["y_nztm"], s=16, facecolor="white", edgecolor=INK, linewidth=0.8, zorder=6)
    offsets = {0: (450, 700), 1: (750, -650), 2: (250, -650), 3: (-650, -650), 4: (-650, 550)}
    for cid, g in gates.groupby("corridor_id"):
        cx, cy = g["x_nztm"].mean(), g["y_nztm"].mean()
        dx, dy = offsets.get(int(cid), (0, 0))
        ax2.annotate(f"{names[cid]}\n({len(g)} gate{'s' if len(g) > 1 else ''})", (cx, cy), (cx + dx, cy + dy),
                     fontsize=6.5, color=INK, ha="center", va="center", zorder=7,
                     bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8),
                     arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.5))
    ax2.set_xlim(bx0, bx1)
    ax2.set_ylim(by0, by1)
    ax2.set_aspect("equal")
    ax2.set_title("b  City centre cordon and its 23 gates", loc="left", fontsize=9, fontweight="bold", color=INK)
    handles = [plt.Line2D([], [], color="#a9a8a2", lw=1.2, label="Motorway"),
               plt.Line2D([], [], color=ROAD, lw=1.2, label="Other major road"),
               plt.Line2D([], [], color=RULE, lw=1.2, label="Simulated road section"),
               plt.Line2D([], [], color=LLM, marker="o", lw=0, markersize=4, label="Commuter origin"),
               plt.Rectangle((0, 0), 1, 1, facecolor=INK, label="Cordon (city centre)")]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.64, 0.02), ncol=1, frameon=False, fontsize=7,
               handlelength=1.6)
    fig.savefig(out / "fig1_study_area.png")
    plt.close(fig)


def fig2(out: Path) -> None:
    """One simulated morning as a loop: options, cognitive clock, decider (rule or LLM), traffic, memory."""
    w, h = 16.0, 7.2                                      # canvas in cm
    fig = plt.figure(figsize=(WIDTH_IN, WIDTH_IN * h / w))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")

    def box(x, y, bw, bh, title, body, fill="#f3f2ee", edge=INK2, title_size=7.5):
        ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0,rounding_size=0.12", facecolor=fill,
                                    edgecolor=edge, linewidth=0.8))
        ax.text(x + 0.15, y + bh - 0.14, title, fontsize=title_size, fontweight="bold", color=INK, va="top")
        ax.text(x + 0.15, y + bh - 0.52, body, fontsize=6.5, color=INK, va="top", linespacing=1.3)

    def arrow(p, q, dashed=False):
        ax.annotate("", q, p, arrowprops=dict(arrowstyle="-|>", color=INK2, linewidth=0.8, shrinkA=0, shrinkB=0,
                                              mutation_scale=7, linestyle=(0, (3, 2)) if dashed else "-"))

    c1, c2, c3, cw = 2.9, 6.5, 10.1, 3.0                  # loop columns and their width
    box(0.1, 3.9, 2.3, 2.3, "Inputs", "Census commuters:\n950 agents,\n1 agent = 20 cars\nroads, counts,\ncongestion index",
        fill="white")
    box(c1, 4.3, cw, 1.9, "1  Today’s options", "each with its delay, queue,\ncharge and arrival, from\nyesterday’s traffic")
    box(c2, 4.3, cw, 1.9, "2  Cognitive clock", "a reason to reconsider?\nnew charge, late arrival,\nPT disrupted, option gone")
    box(c2, 2.5, cw, 1.25, "Repeat the routine", "most mornings,\nno decision needed", title_size=7)
    box(c3, 2.5, cw, 3.7, "3  Decider", "")
    box(c3 + 0.15, 4.55, cw - 0.3, 1.2, "Rule", "lowest generalised cost\n(R-daily, R-clock)",
        fill="#e6f0fb", edge=RULE, title_size=7)
    box(c3 + 0.15, 2.6, cw - 0.3, 1.8, "LLM", "reads the situation in\nwords, returns a routine\nand a reason\n(H-clock)",
        fill="#fdeee7", edge=LLM, title_size=7)
    box(c2, 0.4, c3 + cw - c2, 1.3, "4  Traffic", "road sections with BPR delay,\nmotorway breakdown and gate queues")
    box(c1, 0.4, cw, 1.3, "5  Memory", "delay, lateness and\ncharge paid, every day")
    box(13.6, 0.4, 2.3, 2.1, "Outputs", "car crossings\ndelay per car trip\nvehicle-hours\nreasons for change",
        fill="white")

    arrow((2.4, 5.25), (c1, 5.25))
    arrow((c1 + cw, 5.25), (c2, 5.25))
    arrow((c2 + cw, 5.25), (c3, 5.25))
    ax.text((c2 + cw + c3) / 2, 5.35, "yes", fontsize=6.5, color=INK2, ha="center", va="bottom", style="italic")
    arrow((c2 + cw / 2, 4.3), (c2 + cw / 2, 3.75))
    ax.text(c2 + cw / 2 + 0.1, 4.02, "no", fontsize=6.5, color=INK2, va="center", style="italic")
    arrow((c2 + cw / 2, 2.5), (c2 + cw / 2, 1.7))
    arrow((c3 + cw / 2, 2.5), (c3 + cw / 2, 1.7))
    arrow((c2, 1.05), (c1 + cw, 1.05))
    arrow((c1 + cw / 2, 1.7), (c1 + cw / 2, 4.3))
    ax.text(c1 + cw / 2 + 0.1, 3.0, "next\nmorning", fontsize=6.5, color=INK2, va="center", style="italic")
    arrow((c3 + cw, 1.05), (13.6, 1.05))
    # R-daily skips the clock: the rule decides for every agent every morning
    ax.plot([c1 + cw / 2, c1 + cw / 2, c3 + cw / 2], [6.2, 6.75, 6.75], color=INK2, linewidth=0.8,
            linestyle=(0, (3, 2)))
    arrow((c3 + cw / 2, 6.75), (c3 + cw / 2, 6.2), dashed=True)
    ax.text((c1 + c3 + cw) / 2, 6.85, "R-daily skips the clock and decides every morning", fontsize=6.5, color=INK2,
            ha="center", va="bottom", style="italic")
    fig.savefig(out / "fig2_pipeline.png")
    plt.close(fig)


def fig3(out: Path) -> None:
    """Change against each arm's own base (days 6-10 minus days 2-5), so the rule and the LLM share one zero line."""
    d = pd.read_csv(ROOT / "runs" / "llm_behaviour" / "delay_by_departure.csv")
    d = d[d["scenario"] == "NZ6_s1"]
    w = d.pivot_table(index="gate_bin", columns=["arm", "period"], values=["car_entries", "road_plus_queue_per_trip"])
    w.index = pd.to_timedelta(w.index + ":00").total_seconds() / 3600
    w = w[(w.index >= 6.25) & (w.index < 10)].sort_index()
    fig, axes = plt.subplots(2, 1, figsize=(WIDTH_IN, WIDTH_IN * 0.62), sharex=True)
    for ax, col, ylab in ((axes[0], "car_entries", "Change in car crossings\nper 15 min (cars)"),
                          (axes[1], "road_plus_queue_per_trip", "Change in road delay + gate\nqueue per car trip (min)")):
        ax.axvspan(8, 9, color="#f0efec", zorder=0)
        ax.axhline(0, color=INK2, linewidth=0.8, zorder=2)
        for arm, colour, dx, label in (("R-clock", RULE, -0.0575, "Rule (R-clock)"),
                                       ("H-clock", LLM, 0.0575, "LLM (H-clock)")):
            before, charge = w[(col, arm, "before")], w[(col, arm, "charge")]
            # a bin without cars has no crossings but no delay per trip either
            ch = (charge.fillna(0) - before.fillna(0)) * 20 if col == "car_entries" else charge - before
            ax.bar(w.index + 0.125 + dx, ch, width=0.105, color=colour, edgecolor="white", linewidth=0.6,
                   label=label, zorder=3)
        ax.set_ylabel(ylab)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].text(8.5, 0.97, "Peak charge NZ$6", transform=axes[0].get_xaxis_transform(), ha="center", va="top",
                 fontsize=6.5, color=INK2)
    axes[1].set_xlim(6.2, 10)
    axes[1].set_xticks([6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10],
                       ["06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"])
    axes[1].set_xlabel("Time of crossing the cordon (15-min bins)")
    axes[0].set_title("a  More or fewer cars than before the charge", loc="left", fontweight="bold")
    axes[1].set_title("b  Longer or shorter delay per car trip than before the charge", loc="left", fontweight="bold")
    axes[0].set_ylim(-1400, 700)
    axes[0].text(7.02, 560, "Rule: drivers leave earlier,\na new peak before 07:30", fontsize=6.5, color=INK,
                 va="center")
    axes[0].text(6.27, -480, "LLM: fewer cars before 08:00 as well", fontsize=6.5, color=INK, va="center")
    axes[1].text(6.27, -4.0, "Rule: longer delays for the cars\nthat now cross before 07:30", fontsize=6.5,
                 color=INK, va="center")
    axes[1].text(9.27, -5.0, "Both: 5 to 7 min shorter\naround 08:30", fontsize=6.5, color=INK, va="center")
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=2, frameon=False, fontsize=7, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=1.2)
    fig.savefig(out / "fig3_time_profile.png")
    plt.close(fig)


def fig4(out: Path, sec: dict, land) -> None:
    regions = C.section_table()
    win = {"06:00–08:00": ("06:00-07:00", "07:00-08:00"), "08:00–10:00": ("08:00-09:00", "09:00-10:00")}
    vals = {}
    for arm, run in (("Rule (R-clock)", R_RUN), ("LLM (H-clock)", H_RUN)):
        los = C.road_delay(run, regions)
        for w, bins in win.items():
            y = los[los["bin"].isin(bins)].groupby(["section_id", "period"])["veh_h"].sum().unstack("period")
            vals[(arm, w)] = (y["charge"] - y["before"]).fillna(0)
    mwy = pd.read_csv(ROOT / "data" / "road_sections.csv").set_index("section_id")["mwy"]
    used = [ln for s in sec.values() for ln in s]
    xy = np.vstack(used)
    x0, y0 = xy.min(axis=0) - 800
    x1, y1 = xy.max(axis=0) + 800
    lim = 6.0
    norm = Normalize(-lim, lim)
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_IN, WIDTH_IN * 1.12))
    labels = {  # name: (point on the road, label position), NZTM
        "Northern Motorway": ((1755851, 5926601), (1762500, 5929000)),
        "Northwestern Motorway": ((1749479, 5919502), (1745500, 5924500)),
        "Southern Motorway": ((1764210, 5912357), (1769000, 5915500)),
        "SH20": ((1759758, 5909069), (1752500, 5906500)),
        "Dominion Rd": ((1755602, 5915823), (1749000, 5913500)),
        "Tamaki Dr": ((1763462, 5920096), (1766500, 5924000))}
    for i, w in enumerate(win):
        for j, arm in enumerate(("Rule (R-clock)", "LLM (H-clock)")):
            ax = axes[i, j]
            ax.set_facecolor(WATER)
            draw_polygon(ax, land, facecolor=LAND, edgecolor="none", zorder=0)
            v = vals[(arm, w)]
            order = v.abs().sort_values().index      # largest changes drawn on top
            segs, cols, lws = [], [], []
            for sid in order:
                for ln in sec.get(int(sid), []):
                    segs.append(ln)
                    cols.append(DIVERGING(norm(np.clip(v[sid], -lim, lim))))
                    lws.append(1.5 if mwy.get(sid, 0) == 1 else 0.7)
            ax.add_collection(LineCollection(segs, colors=cols, linewidths=lws, zorder=2))
            ax.set_xlim(x0, x1)
            ax.set_ylim(y0, y1)
            ax.set_aspect("equal")
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(GRID)
            ax.set_title(f"{'abcd'[2 * i + j]}  {arm}, {w}", loc="left", fontweight="bold")
            up, down = v[v > 0].sum(), v[v < 0].sum()
            ax.text(0.02, 0.02, f"Delay added {up:,.0f} veh-h\nDelay removed {-down:,.0f} veh-h",
                    transform=ax.transAxes, fontsize=6.5, color=INK, va="bottom",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.5))
            if i == 0 and j == 0:
                for name, (pt, at) in labels.items():
                    ax.annotate(name, pt, at, fontsize=6, color=INK, ha="center", va="center", zorder=5,
                                bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=0.6),
                                arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.5))
    cax = fig.add_axes([0.25, 0.065, 0.5, 0.014])
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=DIVERGING), cax=cax, orientation="horizontal",
                      extend="both")
    cb.set_label("Change in vehicle-hours of delay per section, days 6–10 against days 2–5 (all vehicles)",
                 fontsize=7, color=INK)
    cb.ax.tick_params(labelsize=7)
    cb.outline.set_edgecolor(GRID)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.12, wspace=0.03, hspace=0.08)
    fig.savefig(out / "fig4_road_change.png")
    plt.close(fig)


def fig5(out: Path) -> None:
    rows = []
    for arm, run in (("Rule (R-clock)", R_RUN), ("LLM (H-clock)", H_RUN)):
        o = pd.read_csv(run / "outcomes.csv")
        km = pd.read_csv(run / "personas.csv").set_index("agent_id")["path_km"]
        o["band"] = pd.cut(o["agent_id"].map(km), [0, 10, 20, 1e9], labels=["0–10 km", "10–20 km", "20+ km"],
                           right=False)
        for cond, sel in (("Before the charge (days 2–5)", o["day"].between(2, 5)),
                          ("NZ$6 peak (days 6–10)", o["day"].between(6, 10))):
            x = o[sel]
            for band, g in x.groupby("band", observed=True):
                cars = g[g["mode"] == "CAR"]
                rows.append((arm, cond, band, cars["road_delay_min"].mean(), 100 * (g["mode"] == "CAR").mean()))
    t = pd.DataFrame(rows, columns=["arm", "cond", "band", "road", "share"])
    t.to_csv(out / "fig5_distance.csv", index=False, lineterminator="\n")
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_IN, WIDTH_IN * 0.72), sharey="row")
    colours = {"Before the charge (days 2–5)": "#c9c8c1", "NZ$6 peak (days 6–10)": RULE}
    bands = ["0–10 km", "10–20 km", "20+ km"]
    for j, arm in enumerate(("Rule (R-clock)", "LLM (H-clock)")):
        for i, (col, ylab) in enumerate((("road", "Road delay per car trip (min)"),
                                         ("share", "Commuters who drive (%)"))):
            ax = axes[i, j]
            for k, cond in enumerate(colours):
                y = t[(t["arm"] == arm) & (t["cond"] == cond)].set_index("band").reindex(bands)[col]
                xs = np.arange(3) + (k - 0.5) * 0.36
                ax.bar(xs, y, width=0.34, color=colours[cond], edgecolor="#8a8984" if k == 0 else "none",
                       linewidth=0.6, label=cond, zorder=2)
                for xx, yy in zip(xs, y):
                    ax.text(xx, yy, f"{yy:.1f}" if col == "road" else f"{yy:.0f}", ha="center", va="bottom",
                            fontsize=6, color=INK2)
            ax.set_xticks(range(3), bands)
            ax.grid(axis="y", color=GRID, linewidth=0.6)
            ax.set_axisbelow(True)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            if j == 0:
                ax.set_ylabel(ylab)
            if i == 0:
                ax.set_title(arm, fontsize=9)
            if i == 1:
                ax.set_xlabel("Route length to the city centre")
    axes[1, 0].set_ylim(0, 100)
    h, lab = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, lab, loc="upper center", ncol=2, frameon=False, fontsize=7, bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out / "fig5_distance.png")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="runs/figures/chapter")
    ap.add_argument("--only", nargs="*", default=["1", "2", "3", "4", "5"])
    args = ap.parse_args()
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    need_map = {"1", "4"} & set(args.only)
    if need_map:
        land = land_outline()
        lines, frc = road_shapes()
        sec = section_lines(lines)
    if "1" in args.only:
        fig1(out, lines, frc, sec, land)
    if "2" in args.only:
        fig2(out)
    if "3" in args.only:
        fig3(out)
    if "4" in args.only:
        fig4(out, sec, land)
    if "5" in args.only:
        fig5(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
