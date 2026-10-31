"""How sound is the LLM's reasoning? Checks of the H-clock answers against the facts it was given and the rule.

    python scripts/llm_reasoning_check.py --out runs/llm_behaviour \
        --pair NZ6_s1=full_H-clock_s1,full_R-clock_s1 --pair NZ18_s1=full_H-clock_s1_peak18,full_R-clock_s1_peak18

Each --pair is LABEL=H_RUN,R_RUN (folders in runs/, same seed and settings). Writes to --out:
    reasoning_check.csv     per scenario: answers, invalid replies and fallbacks; the share of charge-day answers
                            that take the option the rule's generalised cost ranks first (H-clock and R-clock);
                            agreement of the two arms on the charge day; facts quoted in the LLM's words that
                            can be traced to its message; trial reviews that kept the arrangement
    charge_day_agreement.csv  per scenario: what the LLM answered on the charge day (keep, retime, PT, WFH)
                            against what the rule chose for the same commuter
    reasoning_check.md      both tables
Quoted facts: every NZ$ amount in the LLM's words must equal, within NZ$0.50 or 5%, an amount in its message,
a sum of two or three of them, a difference of two, or five times one (a week); every clock time (hh:mm) must
be within 5 min of a time in the message. Reads run folders only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CHARGE_DAY_DEFAULT = 6
MONEY = re.compile(r"(?:NZ)?\$\s?(\d+(?:\.\d+)?)")
CLOCK = re.compile(r"\b(\d{1,2}):(\d{2})\b")


def calls(run: Path) -> pd.DataFrame:
    rows = [json.loads(x) for x in (run / "llm_calls.jsonl").read_text(encoding="utf-8").splitlines()]
    c = pd.DataFrame(rows)
    return pd.concat([c.drop(columns="parsed"), pd.json_normalize(c["parsed"])], axis=1)


def derivable(prompt: str) -> set[float]:
    p = sorted({float(v) for v in MONEY.findall(prompt)})
    d = set(p) | {5 * a for a in p}
    d |= {a + b for a, b in itertools.combinations(p, 2)} | {abs(a - b) for a, b in itertools.combinations(p, 2)}
    d |= {a + b + c for a, b, c in itertools.combinations(p, 3)}
    return d


def traced(value: float, pool: set[float]) -> bool:
    return any(abs(value - q) <= max(0.5, 0.05 * q) for q in pool)


def quoted_facts(c: pd.DataFrame) -> dict:
    money_n = money_ok = clock_n = clock_ok = 0
    for words, prompt in zip(c["in_my_words"].fillna(""), c["user"]):
        pool = derivable(prompt)
        for v in MONEY.findall(words):
            money_n += 1
            money_ok += traced(float(v), pool)
        times = {int(h) * 60 + int(m) for h, m in CLOCK.findall(prompt)}
        for h, m in CLOCK.findall(words):
            clock_n += 1
            clock_ok += any(abs(int(h) * 60 + int(m) - t) <= 5 for t in times)
    return {"money_quoted": money_n, "money_traced_pct": 100 * money_ok / max(money_n, 1),
            "clock_quoted": clock_n, "clock_traced_pct": 100 * clock_ok / max(clock_n, 1)}


def response(d: pd.DataFrame, day: int, ids) -> pd.Series:
    """keep / retime / PT / WFH on ``day`` against the commuter's option of the day before."""
    now = d[d["day"] == day].set_index("agent_id").reindex(ids)
    before = d[d["day"] == day - 1].set_index("agent_id").reindex(ids)
    out = now["mode"].map({"PT": "PT", "WFH": "WFH"})
    car = now["mode"] == "CAR"
    out[car] = (now["option_id"][car] == before["option_id"][car]).map({True: "keep", False: "retime"})
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
    rows, agree = [], []
    for spec in args.pair:
        label, runs = spec.split("=", 1)
        h_run, r_run = (ROOT / "runs" / x for x in runs.split(","))
        c = calls(h_run)
        hd, rd = pd.read_csv(h_run / "decisions.csv"), pd.read_csv(r_run / "decisions.csv")
        meta = json.loads((h_run / "summary.json").read_text(encoding="utf-8"))["meta"]["llm"]
        asked = hd[(hd["day"] == cd) & (hd["decider"] == "llm")]
        woken = rd[(rd["day"] == cd) & (rd["decider"] == "rule")]
        ids = asked["agent_id"].tolist()
        h_resp, r_resp = response(hd, cd, ids), response(rd, cd, ids)
        t = pd.crosstab(h_resp.rename("LLM"), r_resp.rename("rule"))
        for llm_choice, r in t.iterrows():
            agree.append({"scenario": label, "LLM": llm_choice, **r.to_dict()})
        reviews = c[c["triggers"].map(len).eq(0) & (c["day"] > cd)]
        rows.append({"scenario": label, "llm_answers": meta["n_contexts"], "invalid": meta["n_invalid"],
                     "fallbacks": meta["n_fallback"], "refusals": meta["n_refusals"],
                     "charge_day_asked": len(asked),
                     "llm_takes_gc_best_pct": 100 * (asked["rank_of_choice_by_gc"] == 1).mean(),
                     "rule_takes_gc_best_pct": 100 * (woken["rank_of_choice_by_gc"] == 1).mean(),
                     "same_response_as_rule_pct": 100 * (h_resp == r_resp).mean(),
                     "llm_pt_where_rule_drives": int(((h_resp == "PT") & r_resp.isin(["keep", "retime"])).sum()),
                     "rule_pt_where_llm_drives": int(((r_resp == "PT") & h_resp.isin(["keep", "retime"])).sum()),
                     "rule_retimes": int((r_resp == "retime").sum()), "llm_retimes": int((h_resp == "retime").sum()),
                     **quoted_facts(c),
                     "reviews": len(reviews), "reviews_kept_pct": 100 * (reviews["what_i_do"] == "keep_as_is").mean()})
    s, a = pd.DataFrame(rows).round(1), pd.DataFrame(agree).fillna(0)
    s.to_csv(out / "reasoning_check.csv", index=False, lineterminator="\n")
    a.to_csv(out / "charge_day_agreement.csv", index=False, lineterminator="\n")
    md = ["# Checks of the LLM's reasoning (H-clock)", "", s.T.to_string(), "",
          "## Charge-day answer (rows: LLM) against the rule's choice for the same commuter (columns)", "",
          a.to_string(index=False), ""]
    (out / "reasoning_check.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
