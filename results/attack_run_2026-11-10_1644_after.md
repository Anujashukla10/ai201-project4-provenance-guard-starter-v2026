# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 16:44
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `168284f12e87` | human | 0.298 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `df7deda67b30` | unsure | 0.441 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `43442771fe9c` | unsure | 0.501 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `bbd7ad23f3e7` | unsure | 0.554 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e3b7cd3a8b6a` | human | 0.260 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `23dc2a426bdc` | unsure | 0.462 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `206841c80b98` | unsure | 0.525 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `ac8960226c36` | unsure | 0.352 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `44bf0056bd8e` | unsure | 0.535 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5ae94b832396` | ai | 0.882 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `fa28cac3af5b` | unsure | 0.561 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `e883b539b8cf` | unsure | 0.692 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `86923af5a71d` | unsure | 0.713 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `b0857ba0b275` | unsure | 0.670 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `9cbe48a10895` | unsure | 0.766 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c18c59119550` | unsure | 0.689 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `05e7d1283985` | unsure | 0.742 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `2860c31f52cb` | unsure | 0.358 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `4c996549f4ee` | unsure | 0.398 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `1883a7a9d003` | human | 0.207 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a7094bb7f467` | unsure | 0.501 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `18858237b022` | unsure | 0.411 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `6a8bc11653ef` | unsure | 0.418 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `a87db2e1deaa` | unsure | 0.516 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `298d4695d557` | unsure | 0.320 |  |
| MF04 | malformed | text is only punctuation | 200 | `835ba942bb86` | unsure | 0.407 |  |
| MF05 | malformed | text is a very long single word | 200 | `652710b443bc` | ai | 0.879 |  |
| MF06 | malformed | text is emoji only | 200 | `6a2afc858768` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `662aa6bab659` | ai | 0.944 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `76c5c6e41d11` | unsure | 0.320 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d6836193492d` | unsure | 0.320 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `492553da04b1` | unsure | 0.320 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d2d0edccb619` | unsure | 0.320 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ee4022592327` | unsure | 0.320 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `50cbe4a2e14e` | unsure | 0.320 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `87063deca779` | unsure | 0.320 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4489e5b99655` | unsure | 0.320 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `736aa795e2e4` | unsure | 0.320 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `61e7de39e40f` | unsure | 0.320 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "168284f12e87",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2976,
  "model_score": 0.1635,
  "style_score": 0.4987,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "df7deda67b30",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4414,
  "model_score": 0.5943,
  "style_score": 0.212,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "43442771fe9c",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5011,
  "model_score": 0.6662,
  "style_score": 0.2534,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "bbd7ad23f3e7",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.554,
  "model_score": 0.6114,
  "style_score": 0.4678,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e3b7cd3a8b6a",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2596,
  "model_score": 0.3212,
  "style_score": 0.1672,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "23dc2a426bdc",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4615,
  "model_score": 0.5727,
  "style_score": 0.2948,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "206841c80b98",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5246,
  "model_score": 0.5862,
  "style_score": 0.4322,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "ac8960226c36",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3517,
  "model_score": 0.2452,
  "style_score": 0.5115,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "44bf0056bd8e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5346,
  "model_score": 0.7042,
  "style_score": 0.2801,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "5ae94b832396",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8825,
  "model_score": 0.9792,
  "style_score": 0.7374,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "fa28cac3af5b",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.561,
  "model_score": 0.6175,
  "style_score": 0.4762,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "e883b539b8cf",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6915,
  "model_score": 0.7387,
  "style_score": 0.6208,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "86923af5a71d",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7125,
  "model_score": 0.8051,
  "style_score": 0.5737,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "b0857ba0b275",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6702,
  "model_score": 0.8329,
  "style_score": 0.4261,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "9cbe48a10895",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7665,
  "model_score": 0.8005,
  "style_score": 0.7154,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c18c59119550",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6894,
  "model_score": 0.8814,
  "style_score": 0.4014,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "05e7d1283985",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.7418,
  "model_score": 0.8816,
  "style_score": 0.5322,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "2860c31f52cb",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.3579,
  "model_score": 0.3223,
  "style_score": 0.4113,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "4c996549f4ee",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3975,
  "model_score": 0.4625,
  "style_score": 0.3,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "1883a7a9d003",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2071,
  "model_score": 0.2044,
  "style_score": 0.2112,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a7094bb7f467",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5015,
  "model_score": 0.5943,
  "style_score": 0.3623,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "18858237b022",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4114,
  "model_score": 0.4998,
  "style_score": 0.2787,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "6a8bc11653ef",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4183,
  "model_score": 0.6401,
  "style_score": 0.0857,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "a87db2e1deaa",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5157,
  "model_score": 0.5583,
  "style_score": 0.4517,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "298d4695d557",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "835ba942bb86",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.4067,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "652710b443bc",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8786,
  "model_score": 0.9976,
  "style_score": 0.7,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "6a2afc858768",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9981,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "662aa6bab659",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9438,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "76c5c6e41d11",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "d6836193492d",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "492553da04b1",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d2d0edccb619",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "ee4022592327",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "50cbe4a2e14e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "87063deca779",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "4489e5b99655",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "736aa795e2e4",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "61e7de39e40f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.32,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
