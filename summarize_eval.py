#!/usr/bin/env python3
"""
Build the five-row run log (three trials, MET/MISSED) from the eval outputs.

    python summarize_eval.py before   -> results/runlog_before.md

Reads the newest results/run_*_<label>.md (run_eval.py, criteria 1-3) and
results/criteria_4_5_*_<label>.md (criteria_extra.py, criteria 4-5).
"""

import glob
import json
import re
import sys

label = sys.argv[1] if len(sys.argv) > 1 else "before"


def newest(pattern):
    files = sorted(glob.glob(pattern))
    if not files:
        sys.exit(f"Missing {pattern}. Run the eval for --label {label} first.")
    return files[-1]


run_path = newest(f"results/run_*_{label}.md")
extra_path = newest(f"results/criteria_4_5_*_{label}.md")

run = open(run_path, encoding="utf-8").read()
scen = {}
for section in re.split(r"^### ", run, flags=re.M)[1:]:
    name = section.splitlines()[0].strip()
    scen[name] = [json.loads(b) for b in re.findall(r"```json\n(.*?)\n```", section, re.S)]

rows, notes = [], []

# 1 — my own writing called AI: at most 1 of 10, every trial
c1 = [sum(1 for r in t if r.get("guess") == "ai") for t in scen["my own writing"]]
rows.append(("1. My own writing labelled high-confidence AI", "≤ 1 of 10, every trial",
             [f"{n}/10" for n in c1], all(n <= 1 for n in c1)))
for i, r in enumerate(scen["my own writing"][0], 1):
    if r.get("guess") == "ai":
        notes.append(f"Criterion 1, piece {i} labelled AI: model {r.get('model_score')}, "
                     f"style {r.get('style_score')}, combined {r.get('confidence')} — \"{r.get('sent')}\"")

# 2 — clearly_ai at least 0.30 above clearly_human, borderline between them
c2_cells, c2_ok = [], []
for t in scen["score spread"]:
    ai, hu, bl = (t[0].get("confidence"), t[1].get("confidence"), t[2].get("confidence"))
    gap = ai - hu
    between = min(ai, hu) < bl < max(ai, hu)
    c2_cells.append(f"gap {gap:.3f}; borderline {bl:.3f} {'between' if between else 'NOT between'}")
    c2_ok.append(gap >= 0.30 and between)
rows.append(("2. Clearly AI vs clearly human score spread",
             "gap ≥ 0.30 and borderline between, every trial", c2_cells, all(c2_ok)))
t0 = scen["score spread"][0]
notes.append("Criterion 2 scores (trial 1): " + "; ".join(
    f"{n} model {r.get('model_score')} style {r.get('style_score')} combined {r.get('confidence')}"
    for n, r in zip(("clearly_ai", "clearly_human", "borderline"), t0)))

# 3 — all three labels appear
c3 = [len({r.get("guess") for r in t} & {"ai", "unsure", "human"}) for t in scen["label coverage"]]
rows.append(("3. All three labels reachable", "3 of 3 labels, every trial",
             [f"{n}/3" for n in c3], all(n == 3 for n in c3)))

# 4 and 5 — from criteria_extra.py
extra = open(extra_path, encoding="utf-8").read()
c4 = re.search(r"- Criterion 4: (.*)", extra).group(1).split(" | ")
c5 = re.search(r"- Criterion 5: (.*)", extra).group(1).split(" | ")
rows.append(("4. Every appeal recorded and changes status", "5/5 real and 3/3 fake → 404, every trial",
             c4, all(c == "5/5 real, 3/3 fake" for c in c4)))
rows.append(("5. Bad input never crashes", "6/6 → 4xx + rejected log entry, every trial",
             c5, all(c == "6/6" for c in c5)))

out = [f"Sources: `{run_path}` (`run_eval.py::main`) and `{extra_path}` "
       f"(`criteria_extra.py::main`), summarised by `summarize_eval.py`.", "",
       "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
       "|---|---|---|---|---|---|"]
for name, target, cells, ok in rows:
    out.append(f"| {name} | {target} | {' | '.join(cells)} | {'MET' if ok else '**MISSED**'} |")
out += [""] + [f"- {n}" for n in notes]

result = "\n".join(out)
open(f"results/runlog_{label}.md", "w", encoding="utf-8").write(result + "\n")
print(result)
print(f"\nWrote results/runlog_{label}.md")