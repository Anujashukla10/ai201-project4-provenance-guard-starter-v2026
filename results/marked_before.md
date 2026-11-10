Source: `results\attack_run_2026-11-10_1635_before.md` (produced by `run_attacks.py::main`), marked by `mark_attacks.py`.

| ID | Family | Targeting | Status | Guess | Model | Style | Score | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.164 | 0.499 | 0.298 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.594 | 0.212 | 0.441 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.253 | 0.501 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | ai | 0.611 | 0.468 | 0.554 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.321 | 0.167 | 0.260 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.295 | 0.462 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.432 | 0.525 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 0.511 | 0.352 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.280 | 0.535 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.979 | 0.737 | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | ai | 0.618 | 0.476 | 0.561 | **BROKE** |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.739 | 0.621 | 0.692 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.805 | 0.574 | 0.713 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.833 | 0.426 | 0.670 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.800 | 0.715 | 0.766 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | ai | 0.881 | 0.401 | 0.689 | **BROKE** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | ai | 0.882 | 0.532 | 0.742 | **BROKE** |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.322 | 0.411 | 0.358 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.463 | 0.300 | 0.398 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.204 | 0.211 | 0.207 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.362 | 0.501 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.279 | 0.411 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.086 | 0.418 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.452 | 0.516 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | unsure | 0.000 | 0.700 | 0.320 | **BROKE** |
| MF04 | malformed | text is only punctuation | 200 | unsure | 0.011 | 1.000 | 0.407 | **BROKE** |
| MF05 | malformed | text is a very long single word | 200 | ai | 0.998 | 0.700 | 0.879 | **BROKE** |
| MF06 | malformed | text is emoji only | 200 | ai | 0.997 | 1.000 | 0.998 | **BROKE** |
| MF07 | malformed | text is right-to-left script | 200 | ai | 0.906 | 1.000 | 0.944 | **BROKE** |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | — | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | — | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | — | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | — | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | unsure | 0.029 | 0.700 | 0.320 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | — | — | HELD |

**Totals: 56 attacks — 41 HELD, 15 BROKE.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 8 | 2 |
| false_positive | 8 | 1 | 7 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 15 | 5 |
| prompt_injection | 6 | 5 | 1 |
