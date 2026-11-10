#!/usr/bin/env python3
"""
Pull ten audit-log entries for the README from an attack run's log extract.

    python extract_entries.py before   -> results/ten_entries_before.json
"""

import json
import sys

label = sys.argv[1] if len(sys.argv) > 1 else "before"
entries = json.load(open(f"results/audit_extract_{label}.json", encoding="utf-8"))["entries"]

WANTED = [
    "attacker_FP03",   # non-native speaker, real human writing
    "attacker_FP05",   # technical docs, real human writing
    "attacker_FP01",   # plain human writing
    "attacker_EV01",   # AI text with typos
    "attacker_PI02",   # fake SYSTEM message
    "attacker_MF06",   # emoji only
    "attacker_MF03",   # control characters
    "attacker_PI05",   # tries to inject fields into the log
    "attacker_EV10",   # repeated stanza
]

picked = []
for creator in WANTED:
    matches = [e for e in entries if e.get("creator_id") == creator]
    if matches:
        picked.append(matches[-1])

rejected = [e for e in entries
            if e.get("creator_id") == "attacker_flood" and e.get("event") == "rejected"]
if rejected:
    picked.append(rejected[-1])

out = json.dumps(picked, indent=2, ensure_ascii=False)
open(f"results/ten_entries_{label}.json", "w", encoding="utf-8").write(out + "\n")
print(out)
print(f"\nWrote results/ten_entries_{label}.json ({len(picked)} entries)")