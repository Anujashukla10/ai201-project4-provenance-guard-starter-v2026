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
human threshold 0.31, AI threshold 0.55 (all in `config.py`).

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
      "creator_id": "x_test",
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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**

**What a caller counts as:**

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After



**Did it help, and how do I know:**



---

## What's Still Broken



**The trade I'd make if this ran for real:**



---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**