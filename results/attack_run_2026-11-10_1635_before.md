# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 16:35
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `4ca683de5684` | human | 0.298 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b16197c962be` | unsure | 0.441 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8d8f071d58c8` | unsure | 0.501 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `d3bb9ad558fa` | ai | 0.554 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c11055d18b8a` | human | 0.260 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `3876acb8ab3a` | unsure | 0.462 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `dbc136b0090e` | unsure | 0.525 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `d3d65d0fe480` | unsure | 0.352 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `882cec838406` | unsure | 0.535 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `4100d145c399` | ai | 0.882 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `71aa548cc95c` | ai | 0.561 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `6e486c083539` | ai | 0.692 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `5d5021e2d17b` | ai | 0.713 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `33e589b9d10c` | ai | 0.670 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `27ac3604eb6d` | ai | 0.766 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `1de715450f2e` | ai | 0.689 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ec106ce84996` | ai | 0.742 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `34195f964f6e` | unsure | 0.358 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `f253c9c7bbe2` | unsure | 0.398 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `78152d44ec22` | human | 0.207 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `361201730cd0` | unsure | 0.501 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `8f392df39937` | unsure | 0.411 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `8a09a1bb47bd` | unsure | 0.418 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `564c767c627e` | unsure | 0.516 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `a22d5ac6f26d` | unsure | 0.320 |  |
| MF04 | malformed | text is only punctuation | 200 | `9390b8312219` | unsure | 0.407 |  |
| MF05 | malformed | text is a very long single word | 200 | `558af1516d8e` | ai | 0.879 |  |
| MF06 | malformed | text is emoji only | 200 | `3806847628ef` | ai | 0.998 |  |
| MF07 | malformed | text is right-to-left script | 200 | `485b672ed407` | ai | 0.944 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `38017ae6922a` | unsure | 0.320 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8d61dff95025` | unsure | 0.320 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `de411143ee94` | unsure | 0.320 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fb1f871a414c` | unsure | 0.320 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9350fa5ab4c1` | unsure | 0.320 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e9fb168535d1` | unsure | 0.320 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c38f58971cfb` | unsure | 0.320 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d39c9a928de7` | unsure | 0.320 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9c3733ed198a` | unsure | 0.320 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5937d86e29e9` | unsure | 0.320 |  |
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
  "content_id": "4ca683de5684",
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
  "content_id": "b16197c962be",
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
  "content_id": "8d8f071d58c8",
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
  "content_id": "d3bb9ad558fa",
  "creator_id": "attacker_EV04",
  "guess": "ai",
  "confidence": 0.554,
  "model_score": 0.6114,
  "style_score": 0.4678,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "c11055d18b8a",
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
  "content_id": "3876acb8ab3a",
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
  "content_id": "dbc136b0090e",
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
  "content_id": "d3d65d0fe480",
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
  "content_id": "882cec838406",
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
  "content_id": "4100d145c399",
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
  "content_id": "71aa548cc95c",
  "creator_id": "attacker_FP01",
  "guess": "ai",
  "confidence": 0.561,
  "model_score": 0.6175,
  "style_score": 0.4762,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "6e486c083539",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6915,
  "model_score": 0.7387,
  "style_score": 0.6208,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "5d5021e2d17b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7125,
  "model_score": 0.8051,
  "style_score": 0.5737,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "33e589b9d10c",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6702,
  "model_score": 0.8329,
  "style_score": 0.4261,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "27ac3604eb6d",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7665,
  "model_score": 0.8005,
  "style_score": 0.7154,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "1de715450f2e",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6894,
  "model_score": 0.8814,
  "style_score": 0.4014,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "ec106ce84996",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7418,
  "model_score": 0.8816,
  "style_score": 0.5322,
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "34195f964f6e",
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
  "content_id": "f253c9c7bbe2",
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
  "content_id": "78152d44ec22",
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
  "content_id": "361201730cd0",
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
  "content_id": "8f392df39937",
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
  "content_id": "8a09a1bb47bd",
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
  "content_id": "564c767c627e",
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
  "content_id": "a22d5ac6f26d",
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
  "content_id": "9390b8312219",
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
  "content_id": "558af1516d8e",
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
  "content_id": "3806847628ef",
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
  "content_id": "485b672ed407",
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
  "content_id": "38017ae6922a",
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
  "content_id": "8d61dff95025",
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
  "content_id": "de411143ee94",
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
  "content_id": "fb1f871a414c",
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
  "content_id": "9350fa5ab4c1",
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
  "content_id": "e9fb168535d1",
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
  "content_id": "c38f58971cfb",
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
  "content_id": "d39c9a928de7",
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
  "content_id": "9c3733ed198a",
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
  "content_id": "5937d86e29e9",
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
