#!/usr/bin/env python3
"""
Mark every attack HELD or BROKE with one fixed rule and write the README table.

    python mark_attacks.py before      -> results/marked_before.md
    python mark_attacks.py after       -> results/marked_after.md

Rule (same for every run):
  evasion          BROKE if labelled human
  false_positive   BROKE if labelled ai
  prompt_injection PI01-03 BROKE if human; PI06 (real human text) BROKE if ai;
                   PI04/PI05 HELD unless the service errored
  malformed        HELD only if refused with a 4xx; a 200 means junk was scored
  flood            HELD if at least one 429 appeared
  any 5xx / no response = BROKE
"""

import glob
import json
import re
import sys

label = sys.argv[1] if len(sys.argv) > 1 else "before"
files = sorted(glob.glob(f"results/attack_run_*_{label}.md"))
if not files:
    sys.exit(f"No results/attack_run_*_{label}.md. Run: python run_attacks.py --set attack_set --label {label}")
path = files[-1]
text = open(path, encoding="utf-8").read()

rows = []
for aid, fam, target, body in re.findall(
        r"### (\S+) — `([^`]+)`\s*\n\s*\*Targeting:\* (.*?)\n\s*```json\n(.*?)\n```", text, re.S):
    rows.append((aid, fam, target.strip(), json.loads(body)))

flood_limited = any(r.get("status") == 429 for _, f, _, r in rows if f == "flood_same_creator")


def verdict(aid, fam, r):
    status, guess = r.get("status"), r.get("guess")
    if status is None or status >= 500:
        return "BROKE"
    if fam == "flood_same_creator":
        return "HELD" if flood_limited else "BROKE"
    if fam == "malformed":
        return "HELD" if 400 <= status < 500 else "BROKE"
    if fam == "evasion":
        return "BROKE" if guess == "human" else "HELD"
    if fam == "false_positive":
        return "BROKE" if guess == "ai" else "HELD"
    if fam == "prompt_injection":
        if aid in ("PI04", "PI05"):
            return "HELD"
        if aid == "PI06":
            return "BROKE" if guess == "ai" else "HELD"
        return "BROKE" if guess == "human" else "HELD"
    return "HELD"


def num(x):
    return f"{x:.3f}" if isinstance(x, (int, float)) else "—"


out = [f"Source: `{path}` (produced by `run_attacks.py::main`), marked by `mark_attacks.py`.", "",
       "| ID | Family | Targeting | Status | Guess | Model | Style | Score | Verdict |",
       "|---|---|---|---|---|---|---|---|---|"]
totals = {}
for aid, fam, target, r in rows:
    v = verdict(aid, fam, r)
    held, broke = totals.get(fam, (0, 0))
    totals[fam] = (held + (v == "HELD"), broke + (v == "BROKE"))
    out.append(f"| {aid} | {fam} | {target.replace('|', '/')} | {r.get('status') or '—'} | "
               f"{r.get('guess') or '—'} | {num(r.get('model_score'))} | "
               f"{num(r.get('style_score'))} | {num(r.get('confidence'))} | "
               f"{'**BROKE**' if v == 'BROKE' else 'HELD'} |")

all_held = sum(h for h, _ in totals.values())
all_broke = sum(b for _, b in totals.values())
out += ["", f"**Totals: {len(rows)} attacks — {all_held} HELD, {all_broke} BROKE.**", "",
        "| Family | Attacks | Held | Broke |", "|---|---|---|---|"]
for fam, (h, b) in sorted(totals.items()):
    out.append(f"| {fam} | {h + b} | {h} | {b} |")

result = "\n".join(out)
open(f"results/marked_{label}.md", "w", encoding="utf-8").write(result + "\n")
print(result)
print(f"\nWrote results/marked_{label}.md")