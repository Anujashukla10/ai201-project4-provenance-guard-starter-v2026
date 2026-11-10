#!/usr/bin/env python3
"""
Criteria 4 (appeal path) and 5 (bad input), three trials each.

run_eval.py can only send JSON bodies to /submit, so it can't test an appeal
(which needs a content_id from an earlier submission) or a body that isn't
JSON at all. This script does both and writes results/criteria_4_5_<label>.md.

    python criteria_extra.py --label before
"""

import argparse
import datetime as dt
import json

import requests

import config

URL = f"http://{config.HOST}:{config.PORT}"

SAMPLE = (
    "The importance of effective time management cannot be overstated in today's "
    "fast-paced work environment. Professionals who develop strong organizational "
    "habits are better positioned to meet deadlines and reduce stress."
)


def log_entries():
    return requests.get(f"{URL}/log", timeout=30).json()["entries"]


def rejected_count():
    return sum(1 for e in log_entries() if e.get("event") == "rejected")


def criterion_4(trial, tag):
    """5 real appeals: 200 + under_review + appeal entry after the decision.
    3 fake content_ids: 404 and nothing logged."""
    detail, real_ok, fake_ok = [], 0, 0

    for i in range(1, 6):
        sub = requests.post(f"{URL}/submit", timeout=90,
                            json={"text": SAMPLE, "creator_id": f"c4_{tag}_t{trial}_{i}"})
        cid = sub.json().get("content_id")
        resp = requests.post(f"{URL}/appeal", timeout=30,
                             json={"content_id": cid, "reasoning": "I wrote this myself."})
        body = resp.json()
        events = [e.get("event") or "decision"
                  for e in log_entries() if e.get("content_id") == cid]
        ok = (resp.status_code == 200
              and body.get("status") == "under_review"
              and events[:1] == ["decision"]
              and "appeal" in events[1:])
        real_ok += ok
        detail.append({"case": f"real appeal {i}", "content_id": cid,
                       "status": resp.status_code, "response": body,
                       "log_events_for_id": events, "pass": ok})

    for k in range(1, 4):
        fake = f"fake_{tag}_t{trial}_{k}"
        resp = requests.post(f"{URL}/appeal", timeout=30,
                             json={"content_id": fake, "reasoning": "test"})
        logged = [e for e in log_entries() if e.get("content_id") == fake]
        ok = resp.status_code == 404 and not logged
        fake_ok += ok
        detail.append({"case": f"fake id {k}", "content_id": fake,
                       "status": resp.status_code, "response": resp.json(),
                       "log_entries_for_id": len(logged), "pass": ok})

    return f"{real_ok}/5 real, {fake_ok}/3 fake", detail


def criterion_5(trial, tag):
    """Six bad inputs: 4xx (not 429) with a JSON error, plus one 'rejected' log entry."""
    c = f"c5_{tag}_t{trial}"
    cases = [
        ("missing text", {"json": {"creator_id": f"{c}_missing"}}),
        ("empty text",   {"json": {"text": "", "creator_id": f"{c}_empty"}}),
        ("null text",    {"json": {"text": None, "creator_id": f"{c}_null"}}),
        ("not JSON",     {"data": "this is not json",
                          "headers": {"Content-Type": "application/json"}}),
        ("too short",    {"json": {"text": "Hi", "creator_id": f"{c}_short"}}),
        ("over 20,000",  {"json": {"text": "word " * 5000, "creator_id": f"{c}_huge"}}),
    ]
    detail, passed = [], 0
    for name, kwargs in cases:
        before = rejected_count()
        resp = requests.post(f"{URL}/submit", timeout=90, **kwargs)
        try:
            body = resp.json()
        except ValueError:
            body = {"not_json_response": resp.text[:200]}
        after = rejected_count()
        ok = (400 <= resp.status_code < 500 and resp.status_code != 429
              and "error" in body and after == before + 1)
        passed += ok
        detail.append({"case": name, "status": resp.status_code, "response": body,
                       "rejected_entries_added": after - before, "pass": ok})
    return f"{passed}/6", detail


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="run")
    parser.add_argument("--trials", type=int, default=3)
    args = parser.parse_args()
    tag = args.label

    results = {4: [], 5: []}
    for trial in range(1, args.trials + 1):
        for number, fn in ((4, criterion_4), (5, criterion_5)):
            summary, detail = fn(trial, tag)
            results[number].append((summary, detail))
            print(f"criterion {number}, trial {trial}: {summary}")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"criteria_4_5_{stamp}_{tag}.md"
    lines = [f"# Criteria 4 and 5 — {tag}", "",
             "- Produced by: `criteria_extra.py::main`", ""]
    for number in (4, 5):
        lines.append(f"- Criterion {number}: " + " | ".join(s for s, _ in results[number]))
    for number in (4, 5):
        for trial, (summary, detail) in enumerate(results[number], 1):
            lines += ["", f"## Criterion {number}, trial {trial}: {summary}", "",
                      "```json", json.dumps(detail, indent=2), "```"]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()