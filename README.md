# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

1. A writing site sends `POST /submit` with JSON: `text` and `creator_id`.
2. `app.py::submit` checks the input. A body that isn't a JSON object, a
   missing `creator_id`, missing/empty/null `text`, or text too short to score
   gets a 400; text over 20,000 characters gets a 413. Every refusal returns a
   JSON error and is logged as `rejected`.
3. **Signal one** (`detector.py::model_signal`) runs GPT-2 on my own machine
   and measures how predictable the text is, as a 0–1 score (higher = more AI).
4. **Signal two** (`stylometry.py::style_signal`) measures the shape of the
   text — sentence-length spread, vocabulary variety, punctuation — as a 0–1
   score (higher = more AI).
5. `scoring.py::combine_signals` merges the two into one confidence score.
6. `scoring.py::score_to_label` turns that score into one of three
   plain-English labels.
7. The decision (both signal scores, combined score, guess, label, status
   `decided`) is written to `logs/audit.jsonl` and returned with a
   `content_id`. If the writer disagrees, `POST /appeal` with that
   `content_id` records their reasoning next to the original decision and
   moves the item to `under_review`.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** Perplexity under GPT-2 — how predictable each next word
is — squashed onto 0–1 so low perplexity (very predictable) gives a high,
AI-like score. Lives in `detector.py::model_signal`.

**Why that might differ between human and AI writing:** A language model
writes by repeatedly choosing a likely next word, so its output is easy for
another model to predict. People make odder, more specific choices.

**What it can't see:** Who actually wrote the text. It rewards common words
in short, plain sentences, so second-language writers, younger writers and
anyone writing plainly score as machine-like. My test confirmed this: a
plain, simply written test paragraph about cooking
(`samples/plain_human.json`) got model_score 0.8801 — higher than the
instructor's clearly-AI sample (0.7544). In the other direction, ornate AI
text full of rare words can score as human.

### Signal two — the style signal

**What it measures:** Three shape measures, each flipped so higher = more AI
and scaled to 0–1 (`stylometry.py::style_signal`):
- sentence-length spread: stdev ÷ mean of sentence lengths (fully human at ≥ 0.6)
- type-token ratio over the first 100 words (fully human at ≥ 0.80, fully AI at ≤ 0.55)
- punctuation density: commas, dashes, semicolons, colons, brackets, quotes,
  ! and ? per word (fully human at ≥ 0.15)

Combined as 0.4 × spread + 0.3 × TTR + 0.3 × punctuation.

**Why that might differ between human and AI writing:** Generated prose
tends toward even, mid-length sentences and plain punctuation. Human writing
is lumpier — a two-word sentence next to a forty-word one, dashes, asides.
Tested from the terminal: the AI opening scored 0.5699 (spread 0.12,
punctuation 0.02); the human opening scored 0.021 (spread 1.03, punctuation
0.14).

**What it can't see:** Meaning — it cannot read. Typos, chopping sentences
up, adding dashes or pasting a quotation all move it without changing who
wrote the text. It also mis-reads formal AI prose: that text uses varied
vocabulary (TTR 0.976 on the AI opening), which this signal treats as human.

### The combining rule

**The rule:** A weighted average of the two signals, with the model signal
counting more because it at least reads the words, while the style signal
only sees shape and is cheap to fool. If the two signals disagree by 0.5 or
more, the result is clamped into the unsure band, because two methods
contradicting each other is real uncertainty, and I would rather say "unsure"
than accuse a writer on one signal alone.

**The numbers:** model weight 0.6, style weight 0.4, disagreement gap 0.5,
human threshold 0.31, AI threshold 0.55 (all in `config.py`, as of unit 7 —
unit 8's improvement raised the AI threshold to 0.78; see The Improvement).

I started at gap 0.4, human 0.40, AI 0.70. On the first run the AI label was
unreachable: the clearly-AI sample was clamped into "unsure". So I widened the
gap to 0.5 and lowered the AI threshold to 0.55. Then nothing landed in
"unsure" (both human samples were under 0.40), so I lowered the human
threshold to 0.31. Lowering the AI threshold has a cost: it makes plain human
writing more likely to be accused (see below).

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
On the instructor's clearly-AI sample, model_score was 0.7544 but style_score
was only 0.316 — a gap of 0.44. The style signal under-read it because formal
AI prose has varied vocabulary. With my original gap of 0.4, the rule clamped
it into "unsure" (0.41–0.69), and with the original AI threshold of 0.70 the
AI label could never be reached. With the gap at 0.5 the weighted average
stands: 0.6 × 0.7544 + 0.4 × 0.316 = 0.579, which is now labelled
high-confidence AI.

**A false positive I found:** a plain, simply written test paragraph about
cooking scored 0.7583 and was labelled high-confidence AI. Both signals
agreed (model 0.8801, style 0.5757): short sentences of common words are
predictable to GPT-2 and evenly sized to stylometry, so the disagreement rule
couldn't protect it. This is the false positive I'd least want to explain to
a writer, and it is the item I appealed in the Sample Run.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.31 | We think this was written by a person. |
| unsure | 0.31 – 0.55 | We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation — our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal. |
| high-confidence AI | 0.55 – 1.00 | This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it. |

All three were reached: borderline → human (0.298), clearly_human → unsure
(0.3248), clearly_ai → AI (0.579).

*(Unit 8 update: after my improvement the ranges are human 0.00–0.31, unsure
0.31–0.78, AI 0.78–1.00. The label text is unchanged.)*

**Why I worded the "unsure" one this way:** The person reading it may have
written every word, and my first signal is known to flag plain writing. So
the label says outright that it is not an accusation, explains that the
system is often unsure with clear, simple writing, and points to the appeal
so the writer has something to do next. Even the AI label admits automated
checks can be wrong, because a false positive is the expensive mistake here.

---

## Sample Run

**A submission** — a plain, simply written paragraph (in the style of a
second-language or beginner writer), which my system labelled AI. This is the
false positive I then appealed:

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d "@samples/plain_human.json"
```

```json
{
  "confidence": 0.7583,
  "content_id": "aae86d89808a",
  "guess": "ai",
  "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "model_score": 0.8801,
  "status": "decided",
  "style_score": 0.5757
}
```

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d "@samples/appeal.json"
```

```json
{
  "content_id": "aae86d89808a",
  "message": "Thank you. Your appeal is recorded and a person will review this piece.",
  "original_label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.298,
      "content_id": "cfa35f9529af",
      "creator_id": "demo_instructor",
      "guess": "human",
      "label": "We think this was written by a person.",
      "model_score": 0.3489,
      "status": "decided",
      "style_score": 0.2216,
      "timestamp": "2026-10-29T01:44:54+00:00"
    },
    {
      "combined_score": 0.3248,
      "content_id": "31f5e4fc27d5",
      "creator_id": "demo_instructor",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
      "model_score": 0.4445,
      "status": "decided",
      "style_score": 0.1452,
      "timestamp": "2026-10-29T01:49:31+00:00"
    },
    {
      "content_id": "aae86d89808a",
      "creator_id": "anuja_test",
      "event": "appeal",
      "reasoning": "I wrote this myself. It is simple because I write in plain English on purpose. I can share my drafts.",
      "status": "under_review",
      "timestamp": "2026-10-29T01:49:33+00:00"
    }
  ]
}
```

The original decision for `aae86d89808a` stays in the log unchanged (the log
is append-only); the appeal entry sits after it with status `under_review`.

A bad-input check from the same session — empty text is refused, not crashed:

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d "@samples/empty.json"
```

```json
{
  "error": "missing_or_empty_text",
  "message": "Send JSON with a non-empty \"text\"."
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Why `pip install -r requirements.txt` failed with "No
  matching distribution found for torch" on my Windows machine.
- *What came back:* A way to check whether my Python was 32-bit or ARM, and
  a suggestion to rebuild the virtual environment on 64-bit Python 3.12 and
  install torch from the PyTorch CPU index.
- *What I changed:* I deleted my Python 3.13 venv, rebuilt it on 3.12,
  installed CPU torch first, and `test.py` then passed 8 of 8.

**Moment 2**

- *What I asked for:* Code for the stylometry measures, a combining rule, and
  a starting draft of the five criteria.
- *What came back:* The three measures with scaling constants, a 0.6/0.4
  weighted average with a disagreement clamp, thresholds of 0.40/0.70, draft
  criteria, and a plain-writing test paragraph (`samples/plain_human.json`)
  to probe Signal 1's blind spot.
- *What I changed:* When I ran the real samples, the AI label was unreachable
  and nothing landed in "unsure", so I retuned the disagreement gap
  (0.4 → 0.5) and both thresholds (AI 0.70 → 0.55, human 0.40 → 0.31) based
  on the actual scores. Running the plain-writing paragraph exposed a false
  positive the defaults had hidden, which I documented and appealed.

**Moment 3 (unit 8)**

- *What I asked for:* Help testing the service: scripts to run my appeal and
  bad-input criteria three times, to mark every attack held or broke with one
  fixed rule, and to turn the eval output into the run-log table; then help
  diagnosing the failures.
- *What came back:* `criteria_extra.py`, `mark_attacks.py`,
  `summarize_eval.py`, `extract_entries.py`, and a proposed stage and
  mechanism for each failure, based on my real scores.
- *What I changed:* I checked each diagnosis against the numbers in my
  results files, chose the AI-threshold change as my first improvement
  because my worst outcome (FP03) pointed at it, chose the word-minimum as my
  second because MF03–MF07 pointed at the route, and recorded honestly that my
  criterion 1 test pieces were shorter than the criterion says.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

## Unit 8 stretch features (declared before building)

I am attempting all three stretch features:

1. **Per-creator rate limits** — limits keyed to `creator_id`, falling back to
   the caller's address only when no creator_id is sent.
2. **A second measured improvement** — a second change from my diagnosis, with
   a third attack run and run log (`--label after2`) in the same format.
3. **Three attacks on someone else's system** — three inputs I send to a
   classmate's Provenance Guard, with what each one did.

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day (`config.py`; applied to
`app.py::submit` with `@limiter.limit`).

**Why those numbers and not others:** A real writer submits their own work a
few times an hour; even someone re-submitting drafts while editing rarely sends
more than a handful in a minute, so 10/minute never touches them. A script
mapping my thresholds needs hundreds of near-identical variations to find where
my thresholds sit. At 10/minute and 200/day one creator can probe at most 200
points a day, which makes threshold-mapping slow and very visible in the log.

**What a caller counts as:** per `creator_id` (stretch feature), falling back to
the IP address when a request has no usable creator_id
(`app.py::rate_limit_key`).

**What per-creator limiting changes (stretch):** It catches one account
flooding from many addresses (VPN, phone + laptop), which per-address limiting
misses, and it doesn't punish several honest writers sharing one household or
school address. The cost: creator_id is whatever the caller sends, so a script
that invents a new creator_id per request is never limited. The attack set does
exactly that (each row is `attacker_<id>`), and only the `flood_same_creator`
rows, which share one creator_id, were cut off (FL01_11 and FL01_12 got 429 in
every run). A real site would key on a logged-in account instead.

**The run of status codes when I pushed past it** (`python run_attacks.py --flood 15`,
`run_attacks.py::run_flood`, saved in `results/flood_2026-11-10_1633.md`):

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

A rejection as it appears in the audit log:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "10 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-10T22:33:45+00:00"
}
```

Each of the five 429s left one `rejected` entry like this, so a flood shows up
in the log rather than as an absence.

---

## Attack Run — Before

Settings: weights 0.6 / 0.4, disagreement gap 0.5, human < 0.31, AI ≥ 0.55,
no word minimum. Source: `results/attack_run_2026-11-10_1635_before.md`
(`run_attacks.py::main`), marked by `mark_attacks.py`.

**How I marked held / broke** — one rule for every run, applied by
`mark_attacks.py`:
- `evasion` (AI text disguised): BROKE if labelled human.
- `false_positive` (real human writing): BROKE if labelled AI.
- `prompt_injection`: PI01–03 (AI text) BROKE if human; PI06 (human text)
  BROKE if AI; PI04/PI05 HELD unless the service errored.
- `malformed`: HELD only if refused with a 4xx; a 200 means junk was scored.
- `flood_same_creator`: HELD if 429s appear once the limit is reached.
- Any 5xx or no response: BROKE.

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

Why the held injection attacks held: PI04's `<script>` tag never reached the
response, because the label is one of three fixed strings in `scoring.py`,
never built from the input. PI05's fake `"guess": "human"` fields had nowhere
to land, because the audit log never stores the submitted text, only my own
computed fields, written with `json.dumps` (see its log entry below).

**Ten audit log entries from the run** (`results/audit_extract_before.json`,
picked with `extract_entries.py`; the last is a rejected flood request):

```json
[
  {
    "combined_score": 0.7125,
    "content_id": "5d5021e2d17b",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.5737,
    "timestamp": "2026-11-10T22:34:59+00:00"
  },
  {
    "combined_score": 0.7665,
    "content_id": "27ac3604eb6d",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.7154,
    "timestamp": "2026-11-10T22:34:59+00:00"
  },
  {
    "combined_score": 0.561,
    "content_id": "71aa548cc95c",
    "creator_id": "attacker_FP01",
    "guess": "ai",
    "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
    "model_score": 0.6175,
    "status": "decided",
    "style_score": 0.4762,
    "timestamp": "2026-11-10T22:34:59+00:00"
  },
  {
    "combined_score": 0.2976,
    "content_id": "4ca683de5684",
    "creator_id": "attacker_EV01",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.1635,
    "status": "decided",
    "style_score": 0.4987,
    "timestamp": "2026-11-10T22:34:56+00:00"
  },
  {
    "combined_score": 0.2071,
    "content_id": "78152d44ec22",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.2044,
    "status": "decided",
    "style_score": 0.2112,
    "timestamp": "2026-11-10T22:35:00+00:00"
  },
  {
    "combined_score": 0.9981,
    "content_id": "3806847628ef",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 1.0,
    "timestamp": "2026-11-10T22:35:02+00:00"
  },
  {
    "combined_score": 0.32,
    "content_id": "a22d5ac6f26d",
    "creator_id": "attacker_MF03",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
    "model_score": 0.0,
    "status": "decided",
    "style_score": 0.7,
    "timestamp": "2026-11-10T22:35:01+00:00"
  },
  {
    "combined_score": 0.4183,
    "content_id": "8a09a1bb47bd",
    "creator_id": "attacker_PI05",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or with help from an AI tool. This is not an accusation \u2014 our checks are often unsure, especially with clear, simple writing. If you'd like a person to look at it, you can appeal.",
    "model_score": 0.6401,
    "status": "decided",
    "style_score": 0.0857,
    "timestamp": "2026-11-10T22:35:01+00:00"
  },
  {
    "combined_score": 0.8825,
    "content_id": "4100d145c399",
    "creator_id": "attacker_EV10",
    "guess": "ai",
    "label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
    "model_score": 0.9792,
    "status": "decided",
    "style_score": 0.7374,
    "timestamp": "2026-11-10T22:34:58+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "status": "rejected",
    "timestamp": "2026-11-10T22:35:03+00:00"
  }
]
```

**The single worst outcome:** **FP03**, a non-native English speaker writing
carefully about their first month in a new country, was told "This piece shows
strong signs of being written by an AI tool" (combined 0.7125, model 0.805).
That is the person with the least room to argue back, accused because they
chose simple, safe vocabulary — exactly what signal one reads as
"predictable". MF06 scored higher (0.998 AI for a string of emoji), but
nobody's reputation rides on an emoji string; FP03's does.

---

## Run Log and Verdicts

Five criteria from `criteria.md`, three trials each, before any fix. Sources:
`results/run_2026-11-10_1636_before.md` (`run_eval.py::main`, criteria 1–3)
and `results/criteria_4_5_2026-11-10_1637_before.md`
(`criteria_extra.py::main`, criteria 4–5), summarised by `summarize_eval.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10, every trial | 3/10 | 3/10 | 3/10 | **MISSED** |
| 2. Clearly AI vs clearly human score spread | gap ≥ 0.30 and borderline between, every trial | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | **MISSED** |
| 3. All three labels reachable | 3 of 3 labels, every trial | 3/3 | 3/3 | 3/3 | MET |
| 4. Every appeal recorded and changes status | 5/5 real and 3/3 fake → 404, every trial | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | MET |
| 5. Bad input never crashes | 6/6 → 4xx + rejected log entry, every trial | 6/6 | 6/6 | 6/6 | MET |

All three trials came out identical. That's expected, because neither signal
has any randomness, so the repeats show the results hold rather than turned up
once.

**How I reached each verdict:** a target counts as MET only if it held in all
three trials; one bad trial is a MISS. I revised no criteria.

**Note on criterion 1's test data:** my criterion says pieces of at least 100
words, but most of the ten pieces I used are shorter (5–60 words). I've kept
the result rather than quietly changing the criterion. Short pieces make the
problem worse, not better (see diagnosis), so a longer set would be a fairer
test, not an easier one.

**Real output from one trial** (trial 1 of the before run; excerpts, exactly
as returned).

Criterion 1 — the three of my pieces labelled AI
(`results/run_2026-11-10_1636_before.md`, `run_eval.py::main`):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.8645,
    "model_score": 0.8275,
    "style_score": 0.92,
    "sent": "sometimes some classes are really hard for some and easy for other, an"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6082,
    "model_score": 0.5997,
    "style_score": 0.6209,
    "sent": "Hello Professor, I wanted to let you know that I had missed the assign"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.7517,
    "model_score": 0.7177,
    "style_score": 0.8028,
    "sent": "Python is a simple language which is not too hard but for new learners"
  }
]
```

Criterion 2 — clearly_ai, clearly_human, borderline (same file):

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.579, "model_score": 0.7544, "style_score": 0.316,
   "sent": "The importance of effective time management cannot be overstated in to"},
  {"status": 200, "guess": "unsure", "confidence": 0.3248, "model_score": 0.4445, "style_score": 0.1452,
   "sent": "I didn't sleep. Not properly, anyway \u2014 I lay there listening to the bo"},
  {"status": 200, "guess": "human", "confidence": 0.298, "model_score": 0.3489, "style_score": 0.2216,
   "sent": "Time management matters more than people admit, especially now that wo"}
]
```

Criterion 3 — the label coverage run reached all three labels; its first
three results were ai (0.579), unsure (0.3248) and human (0.298), the same
texts as above, and my piece "sometimes some classes…" also got ai (0.8645).

Criterion 4 — one real appeal and one fake id, trial 1
(`results/criteria_4_5_2026-11-10_1637_before.md`, `criteria_extra.py::criterion_4`):

```json
[
  {
    "case": "real appeal 1",
    "content_id": "fb26ce54cd2d",
    "status": 200,
    "response": {
      "content_id": "fb26ce54cd2d",
      "message": "Thank you. Your appeal is recorded and a person will review this piece.",
      "original_label": "This piece shows strong signs of being written by an AI tool. Automated checks can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
      "status": "under_review"
    },
    "log_events_for_id": ["decision", "appeal"],
    "pass": true
  },
  {
    "case": "fake id 1",
    "content_id": "fake_before_t1_1",
    "status": 404,
    "response": {
      "error": "not_found",
      "message": "No submission with content_id fake_before_t1_1."
    },
    "log_entries_for_id": 0,
    "pass": true
  }
]
```

Criterion 5 — all six bad inputs, trial 1 (`criteria_extra.py::criterion_5`):

```json
[
  {"case": "missing text", "status": 400, "response": {"error": "missing_or_empty_text"}, "rejected_entries_added": 1, "pass": true},
  {"case": "empty text", "status": 400, "response": {"error": "missing_or_empty_text"}, "rejected_entries_added": 1, "pass": true},
  {"case": "null text", "status": 400, "response": {"error": "missing_or_empty_text"}, "rejected_entries_added": 1, "pass": true},
  {"case": "not JSON", "status": 400, "response": {"error": "bad_request"}, "rejected_entries_added": 1, "pass": true},
  {"case": "too short", "status": 400, "response": {"error": "text_too_short"}, "rejected_entries_added": 1, "pass": true},
  {"case": "over 20,000", "status": 413, "response": {"error": "text_too_long"}, "rejected_entries_added": 1, "pass": true}
]
```

(The full responses, including each `message`, are in the results file.)

### Diagnoses

My service has five stages: the route, signal one (GPT-2 predictability),
signal two (stylometry), the combining rule, and the label mapping.

**Pattern: one cause behind most failures.** Signal one gives a high AI score
to any plain, predictable writing, and in unit 7 I lowered the AI threshold
to 0.55. Those two together explain all 7 false positives and criterion 1.
That is one problem, not eight.

**False positives FP01–FP07 (7 broke) — stage: signal one, then the label
mapping.** Every one is plain, formal, templated or repetitive human writing:
a camping trip, a committee report, a non-native speaker, a rubric essay,
setup instructions, a cover letter, deliberate repetition. GPT-2 finds all of
these easy to predict, so model_score ran 0.62–0.88. Signal two agreed
(0.40–0.72) because these texts have even sentence lengths and few commas or
dashes, so the disagreement clamp never fired. Combined scores of 0.561–0.767
all cleared my 0.55 AI threshold. The mechanism is that predictability is not
authorship, and my threshold was low enough to turn "predictable" into an
accusation.

**Criterion 1 (MISSED, 3/10 in every trial) — stage: signal one plus signal
two, then the label mapping.** Three of my ten pieces were labelled AI, with
identical scores in all three trials:
- "sometimes some classes are really hard for some and easy for other…" —
  model 0.828, style 0.920, combined 0.865
- my email to a professor asking for an extension — model 0.600, style 0.621,
  combined 0.608
- "Python is a simple language which is not too hard…" — model 0.718, style
  0.803, combined 0.752

The mechanism has two parts. Signal one: all three use common, everyday
words in a predictable order, and the email follows a standard polite
template, so GPT-2 can guess each next word. Signal two: the first and third
are a single sentence, so `stylometry.py::sentence_length_spread` returns 0,
which signal two reads as maximally AI-like (40% of its score). The first one
also repeats "some" and "hard", which lowers vocabulary variety. Both signals
agreed, so the disagreement clamp never fired, and all three cleared my 0.55
AI threshold.

**Criterion 2 (MISSED) — stage: signal one (ordering) and signal two (gap).**
clearly_ai scored 0.579 and clearly_human 0.3248: a gap of 0.254, short of
0.30. Signal two compresses the gap because formal AI prose uses varied
vocabulary (type-token ratio near 1.0), which my style measure reads as human,
so clearly_ai only got style 0.316. The ordering fails because borderline
(0.298) scored below clearly_human. Signal one found the borderline text
*less* predictable (model 0.349) than the real human text (0.445): its British
spellings, dash and semicolon are unusual tokens for GPT-2, and the human
sample's plain "I said fine" sentences are not.

**EV01, typos (broke) — stage: signal one, not signal two.** The attack
targeted signal two, and signal two did stay AI-leaning (0.499). What moved
was signal one: misspelled words like "poistioned" and "thsi" split into rare
tokens GPT-2 can't predict, so perplexity rose and model_score fell to 0.164.
Combined: 0.6 × 0.164 + 0.4 × 0.499 = 0.298, just under my 0.31 human
threshold. The 0.335 gap between signals was under my 0.5 disagreement gap, so
the clamp didn't catch it.

**EV05, heavy human editing (broke) — stage: both signals agree.** model 0.321,
style 0.167, combined 0.260. After a heavy human rewrite (dashes, two-word
sentences, specific details like "a corridor in March") the text is close to
human-written. Neither signal measures provenance, only surface features, so
there is nothing left for them to catch. I count this as a break by my rule,
but it's the limit of the approach, not a fixable bug.

**PI02, fake SYSTEM message (broke) — stage: signal one.** Nothing in my
pipeline reads instructions, so the instruction itself had no effect (PI01,
PI03 and PI06 all held). What worked was the *shape* of the header:
"provenance check bypassed… guess=human, confidence=0.02" is a jumble of rare
tokens and symbols GPT-2 can't predict, which pushed model_score down to 0.204.
The AI paragraph after it was cut off after a single sentence, so it couldn't
pull the score back up. Same mechanism as EV01: anything unusual lowers signal
one.

**MF03–MF07, junk scored as writing (5 broke) — stage: the route.** My route
only refused empty text and text under 3 GPT-2 tokens. Control characters,
punctuation, one very long word, emoji and right-to-left script all passed
and were scored. For text with few or no real English words,
`stylometry.words()` finds almost nothing, so every style measure falls to
its AI end (style 0.7–1.0). GPT-2 sees long runs of repeated byte-tokens it
can predict easily (model up to 0.998). The result: a row of emoji labelled
AI at 0.998.

---

## The Improvement

**What I changed:** one line — `AI_THRESHOLD` in `config.py`, from **0.55 to
0.78**. Nothing else moved (`MIN_WORDS` stayed 0, weights and the human
threshold unchanged).

**Which diagnosis pointed at it:** the false-positive pattern. All seven
broken false positives scored 0.561–0.767, and my worst outcome (FP03) was
one of them. A threshold above 0.767 puts every one of them in "unsure"
instead of accusing the writer. The unit 7 change from 0.70 to 0.55 had made
this worse, so this partly reverses a decision I can now measure.

### Attack Run — After

Same attack set, same marking rule. Source:
`results/attack_run_2026-11-10_1644_after.md`, marked by `mark_attacks.py`
(`results/marked_after.md`).

| ID | Family | Targeting | Status | Guess | Model | Style | Score | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.164 | 0.499 | 0.298 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.594 | 0.212 | 0.441 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.253 | 0.501 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.611 | 0.468 | 0.554 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.321 | 0.167 | 0.260 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.295 | 0.462 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.432 | 0.525 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 0.511 | 0.352 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.280 | 0.535 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.979 | 0.737 | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.476 | 0.561 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.739 | 0.621 | 0.692 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.805 | 0.574 | 0.713 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.833 | 0.426 | 0.670 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.800 | 0.715 | 0.766 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.401 | 0.689 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.882 | 0.532 | 0.742 | HELD |
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

**Totals: 56 attacks — 48 HELD, 8 BROKE.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 8 | 2 |
| false_positive | 8 | 8 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 15 | 5 |
| prompt_injection | 6 | 5 | 1 |

### Run Log — After

Sources: `results/run_2026-11-10_1645_after.md` (`run_eval.py::main`) and
`results/criteria_4_5_2026-11-10_1646_after.md` (`criteria_extra.py::main`),
summarised by `summarize_eval.py` (`results/runlog_after.md`).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10, every trial | 1/10 | 1/10 | 1/10 | MET |
| 2. Clearly AI vs clearly human score spread | gap ≥ 0.30 and borderline between, every trial | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | **MISSED** |
| 3. All three labels reachable | 3 of 3 labels, every trial | 3/3 | 3/3 | 3/3 | MET |
| 4. Every appeal recorded and changes status | 5/5 real and 3/3 fake → 404, every trial | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | MET |
| 5. Bad input never crashes | 6/6 → 4xx + rejected log entry, every trial | 6/6 | 6/6 | 6/6 | MET |

### Before vs after, side by side

| | Before | After improvement 1 |
|---|---|---|
| Attacks broke | 15 | 8 |
| false_positive broke | 7 | 0 |
| Criteria met | 3 of 5 | 4 of 5 |
| Criterion 1 (my writing called AI) | 3/10 MISSED | 1/10 MET |

**Did it help, and how do I know:** Yes, for the problem it targeted. The
false_positive family went from 7 broke to 0 (compare the two tables above):
all seven now get the "unsure" label, which says outright it is not an
accusation and points to the appeal. FP03, my worst outcome, is now unsure.
Criterion 1 went from 3/10 to 1/10 in every trial: my email (0.608) and my
Python piece (0.752) moved to unsure, and only "sometimes some classes…"
(0.865) is still labelled AI, which meets my "at most 1" target.

**The cost is real.** Ordinary AI writing no longer gets the AI label.
clearly_ai (0.579) and EV04 (0.554) dropped to "unsure", so only extreme
cases (EV10 at 0.882 and the junk inputs) are still called AI. I traded
detection strength for fewer wrong accusations. Criterion 3 is still MET,
but honestly: in the label-coverage run the *only* AI label now comes from
one of my own human pieces (0.865), not from AI text. So "all three labels
are reachable" now holds partly because of a false positive.

Criterion 2 didn't change, because the scores themselves didn't move, only
the labels. The evasion and injection breaks (EV01, EV05, PI02) are at the
human end, which this change didn't touch, and the junk inputs (MF03–MF07)
were still scored. That pointed at my second improvement.

### Second improvement (stretch)

**What I changed:** one setting — `MIN_WORDS` in `config.py`, from **0 to
5**. The route (`app.py::submit`) now refuses text with fewer than 5 real
words with a 400 and a logged `not_enough_words` rejection, before either
signal runs. The AI threshold stays at 0.78 from improvement 1; nothing else
moved.

**Which diagnosis pointed at it:** MF03–MF07. The route let non-text through,
and both signals then scored it at their AI end.

#### Attack Run — After 2

Source: `results/attack_run_2026-11-10_1652_after2.md`, marked by
`mark_attacks.py` (`results/marked_after2.md`).

| ID | Family | Targeting | Status | Guess | Model | Style | Score | Verdict |
|---|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | human | 0.164 | 0.499 | 0.298 | **BROKE** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure | 0.594 | 0.212 | 0.441 | HELD |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.666 | 0.253 | 0.501 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.611 | 0.468 | 0.554 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.321 | 0.167 | 0.260 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.573 | 0.295 | 0.462 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | 0.586 | 0.432 | 0.525 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | 0.245 | 0.511 | 0.352 | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.704 | 0.280 | 0.535 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.979 | 0.737 | 0.882 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.618 | 0.476 | 0.561 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | 0.739 | 0.621 | 0.692 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | 0.805 | 0.574 | 0.713 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | 0.833 | 0.426 | 0.670 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | 0.800 | 0.715 | 0.766 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.881 | 0.401 | 0.689 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.882 | 0.532 | 0.742 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.322 | 0.411 | 0.358 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.463 | 0.300 | 0.398 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.204 | 0.211 | 0.207 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.594 | 0.362 | 0.501 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.500 | 0.279 | 0.411 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.640 | 0.086 | 0.418 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.558 | 0.452 | 0.516 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | — | — | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | — | — | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | — | — | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | — | — | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | — | — | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | — | — | — | — | HELD |
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

**Totals: 56 attacks — 53 HELD, 3 BROKE.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 8 | 2 |
| false_positive | 8 | 8 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 20 | 0 |
| prompt_injection | 6 | 5 | 1 |

#### Run Log — After 2

Sources: `results/run_2026-11-10_1654_after2.md` (`run_eval.py::main`) and
`results/criteria_4_5_2026-11-10_1655_after2.md` (`criteria_extra.py::main`),
summarised by `summarize_eval.py` (`results/runlog_after2.md`).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10, every trial | 1/10 | 1/10 | 1/10 | MET |
| 2. Clearly AI vs clearly human score spread | gap ≥ 0.30 and borderline between, every trial | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | **MISSED** |
| 3. All three labels reachable | 3 of 3 labels, every trial | 3/3 | 3/3 | 3/3 | MET |
| 4. Every appeal recorded and changes status | 5/5 real and 3/3 fake → 404, every trial | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | MET |
| 5. Bad input never crashes | 6/6 → 4xx + rejected log entry, every trial | 6/6 | 6/6 | 6/6 | MET |

### All three runs, side by side

| | Before | After 1 (AI threshold 0.78) | After 2 (+ min 5 words) |
|---|---|---|---|
| Attacks HELD / BROKE | 41 / 15 | 48 / 8 | 53 / 3 |
| false_positive broke | 7 | 0 | 0 |
| malformed broke | 5 | 5 | 0 |
| evasion broke | 2 | 2 | 2 |
| prompt_injection broke | 1 | 1 | 1 |
| Criteria met | 3 of 5 | 4 of 5 | 4 of 5 |

**Did it help, and how do I know:** Yes. The malformed family went from 5
broke to 0: control characters, punctuation, the single long word, emoji and
right-to-left script are all now refused with a 400 instead of being scored
(MF03–MF07 changed from 200 to 400 in the table). Nothing else changed: every
other attack and every criterion result is identical to After 1, because
every other input has at least 5 words. Criterion 5 still passes 6/6; its
"too short" case ("Hi") is now refused by the word check instead of the token
check, but it's still a 400 with a logged rejection.

**The cost:** my word counter (`stylometry.words()`) only recognises Latin
letters and digits. So a writer using Arabic, Hebrew, Chinese and other
scripts is now told to "submit at least 5 words" even though they did.
Before, they were wrongly accused (MF07 scored 0.944 AI); now they're wrongly
refused. Refused is less harmful than accused, but it's still a wrong answer
for a real person.

---

## What's Still Broken

- **EV01 (typos) and PI02 (rare-token header) still pass as human.** Both
  work by adding tokens GPT-2 can't predict, which drags signal one down.
  Next fix: score signal one on the median per-sentence perplexity instead of
  the whole text, so a few odd words can't drag the score, or spell-correct
  before scoring. I stopped because each is a new signal design that needs its
  own calibration run, and the unit allows only measured, one-at-a-time
  changes.
- **EV05 (heavily human-edited AI) passes as human.** I wouldn't try to fix
  this. After a real human rewrite there's little machine fingerprint left,
  and chasing it would raise false positives on genuine writers.
- **Criterion 2 is still missed.** Neither improvement moved any scores, only
  labels and the route. Fixing it means changing what signal two measures
  (formal AI vocabulary reads as human to it) or reweighting toward signal
  one. I'd test a style weight of 0.3 next, but that would shift every score
  and needs its own before/after run.
- **The AI label is now rare.** With the threshold at 0.78, ordinary AI text
  (clearly_ai, EV04) lands in "unsure". A third signal that measures
  something other than predictability, such as phrases repeated across the
  text, could restore confident AI calls without lowering the threshold
  again.
- **One of my own pieces is still called AI** ("sometimes some classes…",
  0.865): a single repetitive sentence maxes out both signals. A minimum
  length for a confident AI call (for example, at least 3 sentences before
  the AI label is allowed) would stop single-sentence accusations.
- **Non-Latin writing is refused.** The word counter needs to count words in
  any script, not just a–z.

**The trade I'd make if this ran for real:** I'd keep the high AI threshold
and accept that more AI text gets through as "unsure", because a wrong
accusation lands on a real writer — most often a second-language or plain
writer like FP03 — while a missed AI piece costs the site and its readers
much less. The people who pay are readers and honest writers competing with
undetected AI text, and I think that cost is smaller and more spread out than
the cost of calling one real person a cheat.

---

## Stretch: three attacks on someone else's system

Not completed. I declared this stretch feature but didn't get to run my
three attacks against a classmate's service before the deadline, so I'm not
claiming it.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**