# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely accused

Of 10 pieces I wrote myself (each at least 100 words), at most 1 receives the
high-confidence AI label, in each of 3 separate trials.

**Why this target:** On a writing site, a wrong accusation costs a real person
their reputation, while a missed AI piece costs the site much less. My first
signal (GPT-2 predictability) is known to score plain, simple writing as
machine-like, so I want a hard ceiling on how often my own plain writing gets
accused. 1 in 10 is the most I would accept if it were my work being judged.

---

## 2. Clearly AI and clearly human text are far apart

The instructor's clearly_ai sample scores at least 0.30 higher than the
clearly_human sample on the combined confidence score, and the borderline
sample scores between them, in all 3 trials.

**Why this target:** If my two signals can't separate the obvious cases by a
wide margin, then my thresholds at 0.40 and 0.70 are meaningless. A gap of
0.30 is wide enough that the two ends can land in different labels.

---

## 3. All three labels are reachable

Across a set of 10 texts (the 3 instructor samples plus 7 of my own chosen to
span plain, formal, casual and AI-edited writing), each of the three labels —
high-confidence human, unsure, high-confidence AI — appears at least once.

**Why this target:** A label that can never appear is dead code that hides a
gap in my score ranges. My combining rule clamps disagreeing signals into the
unsure band, which could starve the other two labels, so I need to check that
both ends are still reachable.

---

## 4. Every appeal is recorded and changes status

For 5 out of 5 appeals sent with a real content_id, POST /appeal returns 200
with status "under_review", and GET /log shows a new appeal entry for that
content_id after the original decision. An appeal with a made-up content_id
returns 404 in 3 of 3 attempts and does not add an appeal entry.

**Why this target:** The appeal is the only thing standing between a wrong
accusation and nothing. If it ever silently fails, the writer believes they
have been heard when they have not, so the target is 100%, not "most".

---

## 5. Bad input never crashes the service

Each of these returns a 4xx status with a JSON error message, never a 500:
missing "text", empty "text", "text": null, a body that is not JSON, text
under 3 tokens, and text over 20,000 characters. Each one also writes a
"rejected" entry to logs/audit.jsonl. Target: 6 of 6 cases, in 3 of 3 trials.

**Why this target:** A crash looks like a broken site to an honest writer and
an opportunity to an attacker. Rejections are also logged, because an attack
that only shows up as an absence can't be diagnosed.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
