"""Simple slide figures for a council audience: R-clock, seed 1, one message per figure.

Writes PNGs to runs/figures/council/. Run from cordon_lite/:  python scripts/council_figures.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
OUT = RUNS / "figures" / "council"
OUT.mkdir(parents=True, exist_ok=True)

BEFORE = "#2a78d6"   # no charge
AFTER = "#eb6834"    # with charge
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.parse_math": False,
    "font.size": 15,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "figure.facecolor": "white",
    "savefig.dpi": 200,
})


def title(fig, headline, sub):
    fig.text(0.04, 0.95, headline, fontsize=24, weight="bold", color=INK, va="top")
    fig.text(0.04, 0.875, sub, fontsize=15, color=INK2, va="top")


def footer(fig, text="Cordon-Lite simulation, rule-based commuters with a decision clock (R-clock), 950 commuters, seed 1."):
    fig.text(0.04, 0.025, text, fontsize=10.5, color=INK2)


def hhmm(m):
    return f"{int(m // 60):02d}:{int(m % 60):02d}"


# 1. Where the cars go: peak hour emptied, early shoulder fills ---------------------------------
def fig_peak_shift():
    o = pd.read_csv(RUNS / "R-clock_mock_py_s1" / "outcomes.csv")
    car = o[o["mode"] == "CAR"]
    bins = np.arange(360, 616, 15)
    h5, _ = np.histogram(car.loc[car.day == 5, "gate_exit_min"], bins)
    h10, _ = np.histogram(car.loc[car.day == 10, "gate_exit_min"], bins)
    peak = lambda d: ((car.day == d) & car.gate_exit_min.between(480, 539)).sum()
    early = lambda d: ((car.day == d) & (car.gate_exit_min < 450)).sum()
    p5, p10, e5, e10 = peak(5), peak(10), early(5), early(10)

    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.78, bottom=0.13)
    title(fig, f"The peak hour empties: {100 * (p5 - p10) / p5:.0f}% fewer cars from 08:00 to 09:00",
          f"Some drivers switch to PT, others leave earlier. Before 07:30, crossings rise {100 * (e10 - e5) / e5:+.0f}%.")
    ax.axvspan(480, 540, color=AFTER, alpha=0.08, lw=0)
    ax.text(510, max(h5.max(), h10.max()) * 1.08, "NZ$6 peak charge", ha="center", color=AFTER, fontsize=13, weight="bold")
    ax.stairs(h5, bins, color=BEFORE, lw=3, label=f"Before the charge ({(car.day == 5).sum()} cars)")
    ax.stairs(h10, bins, color=AFTER, lw=3, label=f"With the charge ({(car.day == 10).sum()} cars)")
    ax.set_xlim(360, 615)
    ax.set_ylim(0, max(h5.max(), h10.max()) * 1.18)
    ticks = np.arange(360, 616, 30)
    ax.set_xticks(ticks, [hhmm(t) for t in ticks])
    ax.set_xlabel("Time the car crosses into the city centre")
    ax.set_ylabel("Cars per 15 minutes")
    ax.legend(loc="upper left", frameon=False)
    footer(fig, "Cordon-Lite, R-clock, 950 commuters, seed 1. Day 5 (no charge) vs day 10 (charge NZ$4 off-peak, NZ$6 08:00-09:00).")
    fig.savefig(OUT / "1_peak_shift.png")
    plt.close(fig)


# 2. Diminishing returns: more charge removes more cars, but the roads barely improve -----------
def fig_diminishing():
    f = pd.read_csv(RUNS / "figures" / "fee_response.csv")
    f = f[(f.arm == "R-clock") & (f.seed == 1)].sort_values("peak_fee")
    x = np.arange(len(f))
    labels = [f"${p:.0f}" if p else "None" for p in f.peak_fee]
    hi = list(f.peak_fee).index(6.0)

    fig, (a, b) = plt.subplots(1, 2, figsize=(13.33, 7.5))
    fig.subplots_adjust(left=0.07, right=0.97, top=0.74, bottom=0.17, wspace=0.28)
    i12 = list(f.peak_fee).index(12.0)
    c12, c30 = f.car_crossings_per_day.iloc[i12], f.car_crossings_per_day.iloc[-1]
    d12, d30 = f.mean_road_delay.iloc[i12], f.mean_road_delay.iloc[-1]
    title(fig, "Beyond NZ$12, a higher charge removes cars, not delay",
          f"From NZ$12 to NZ$30, another {c12 - c30:.0f} cars a day stay off the road, "
          f"but delay per car falls only {d12 - d30:.1f} min.")
    cols = [INK2 if p == 0 else (AFTER if p == 6 else "#f2a98a") for p in f.peak_fee]
    a.text(i12 + 1.5, f.car_crossings_per_day.max() * 1.08, "more cars removed", ha="center", fontsize=12, color=INK2)
    b.text(i12 + 1.5, f.mean_road_delay.max() * 1.08, "delay flattens", ha="center", fontsize=12, color=INK2)
    for ax, col, ttl, fmt in [(a, "car_crossings_per_day", "Cars crossing the cordon per day", "{:.0f}"),
                              (b, "mean_road_delay", "Road delay per car before the cordon (min)", "{:.1f}")]:
        v = f[col].to_numpy()
        ax.bar(x, v, width=0.62, color=cols, edgecolor="white", linewidth=2)
        for i, y in enumerate(v):
            ax.text(i, y + v.max() * 0.02, fmt.format(y), ha="center", va="bottom", fontsize=14, color=INK)
        ax.set_xticks(x, labels)
        ax.set_xlabel("Peak charge (NZ$)")
        ax.set_title(ttl, loc="left", fontsize=16, color=INK, pad=12)
        ax.set_ylim(0, v.max() * 1.15)
    for ax in (a, b):
        ax.axvspan(i12 - 0.45, len(x) - 0.55, color=GRID, alpha=0.45, lw=0, zorder=0)
    footer(fig, "Cordon-Lite, R-clock, seed 1, days 6-10. Behaviour is calibrated at NZ$6. Other charge levels are extrapolations.")
    fig.savefig(OUT / "2_diminishing_returns.png")
    plt.close(fig)


# 3. Local roads gain, the motorway does not ---------------------------------------------------
def fig_roads():
    f = pd.read_csv(RUNS / "figures" / "fee_response.csv")
    f = f[(f.arm == "R-clock") & (f.seed == 1)].set_index("peak_fee")
    mw = 100 * f.loc[[0.0, 6.0], "los_ef_speed_share_mwy"].to_numpy()
    lo = 100 * f.loc[[0.0, 6.0], "congested_at_share_other"].to_numpy()

    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.76, bottom=0.14)
    title(fig, "Local streets get the relief. The motorway does not",
          f"Congested traffic, 07:00-09:00: city streets {lo[0]:.0f}% to {lo[1]:.0f}%, motorway {mw[0]:.0f}% to {mw[1]:.0f}%.")
    x = np.array([0, 1])
    w = 0.34
    for k, (vals, lab, colr) in enumerate([((mw[0], lo[0]), "No charge", BEFORE), ((mw[1], lo[1]), "NZ$6 charge", AFTER)]):
        xs = x + (k - 0.5) * (w + 0.02)
        ax.bar(xs, vals, width=w, color=colr, label=lab)
        for xi, v in zip(xs, vals):
            ax.text(xi, v + 1.5, f"{v:.0f}%", ha="center", fontsize=17, weight="bold", color=INK)
    ax.text(1, max(lo) + 12, f"{100 * (lo[1] - lo[0]) / lo[0]:.0f}%", ha="center", fontsize=22, weight="bold", color=AFTER)
    ax.text(0, mw[0] + 10, f"{100 * (mw[1] - mw[0]) / mw[0]:.0f}%", ha="center", fontsize=22, weight="bold", color=INK2)
    ax.set_xticks(x, ["Motorway approaches", "City streets"])
    ax.set_ylabel("Share of traffic that is congested (%)")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, loc="upper right")
    footer(fig, "Cordon-Lite, R-clock, seed 1, days 6-10 vs the same days without a charge. Motorway: below 40% of free-flow "
                "speed. Streets: below 50% (Auckland Transport definition).")
    fig.savefig(OUT / "3_roads.png")
    plt.close(fig)


# 4. Who changes: drivers with less money/time value change most; some cannot change at all ----
def fig_who():
    w = pd.read_csv(RUNS / "figures" / "who_adapts_R-clock.csv")
    q = w[w.group == "vot_quintile"].sort_values("level")
    wv = w[(w.group == "archetype") & w.structural_zero].iloc[0]

    fig, ax = plt.subplots(figsize=(13.33, 7.5))
    fig.subplots_adjust(left=0.08, right=0.97, top=0.76, bottom=0.19)
    lo, hi = q.left_car_share.iloc[0], q.left_car_share.iloc[-1]
    title(fig, f"Those who value time least change most: {100 * lo:.0f}% vs {100 * hi:.0f}%",
          f"Share of drivers who left the car under the NZ$6 charge. "
          f"The {int(wv.n_car_base)} work-vehicle drivers have no alternative.")
    labels = ["Lowest\n20%", "2nd", "3rd", "4th", "Highest\n20%", "Work\nvehicle"]
    vals = list(q.left_car_share) + [0.0]
    lows = list(q.ci_low) + [0.0]
    highs = list(q.ci_high) + [0.0]
    x = np.arange(len(vals))
    cols = [AFTER] * 5 + [INK2]
    ax.bar(x, [100 * v for v in vals], width=0.62, color=cols)
    ax.errorbar(x[:5], [100 * v for v in vals[:5]],
                yerr=[[100 * (v - l) for v, l in zip(vals[:5], lows[:5])], [100 * (h - v) for v, h in zip(vals[:5], highs[:5])]],
                fmt="none", ecolor=INK2, elinewidth=1.2, capsize=5)
    for i, v in enumerate(vals[:5]):
        ax.text(i + 0.33, 100 * v + 0.8, f"{100 * v:.0f}%", ha="left", fontsize=15, weight="bold", color=INK)
    ax.text(5, 1.5, "0%\ncannot switch", ha="center", fontsize=12, color=INK2)
    ax.axvline(4.5, color=GRID, lw=1.5)
    ax.set_xticks(x, labels)
    ax.set_xlabel("Value of time (lowest to highest fifth of commuters)")
    ax.set_ylabel("Drivers who left the car (%)")
    ax.set_ylim(0, 50)
    footer(fig, "Cordon-Lite, R-clock, seed 1. Drivers on days 2-5 who did not drive on days 6-10. Bars show 95% intervals. "
                "The gradient is partly built into the model.")
    fig.savefig(OUT / "4_who_changes.png")
    plt.close(fig)


if __name__ == "__main__":
    fig_peak_shift()
    fig_diminishing()
    fig_roads()
    fig_who()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
