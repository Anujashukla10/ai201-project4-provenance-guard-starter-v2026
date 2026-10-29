"""
Turning two numbers into one, and one number into something a person can read.

combine_signals:  0.6 x model + 0.4 x style. If the two signals disagree by
                  0.4 or more, the result is clamped into the "unsure" band.
score_to_label:   three plain-English labels, thresholds in config.py.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0-1 signals (higher = more AI) into one 0-1 score.

    Rule:
      1. Weighted average: WEIGHT_MODEL_SIGNAL (0.6) x model
                         + WEIGHT_STYLE_SIGNAL (0.4) x style.
      2. Disagreement rule: if |model - style| >= DISAGREEMENT_GAP (0.4), the
         signals are contradicting each other, so the score is clamped into
         the unsure band. We would rather say "unsure" than accuse a writer
         on the strength of one signal.
    """
    score = (config.WEIGHT_MODEL_SIGNAL * model_score
             + config.WEIGHT_STYLE_SIGNAL * style_score)

    if abs(model_score - style_score) >= config.DISAGREEMENT_GAP:
        low = config.HUMAN_THRESHOLD + 0.01
        high = config.AI_THRESHOLD - 0.01
        score = min(max(score, low), high)

    return round(max(0.0, min(1.0, score)), 4)


LABEL_AI = (
    "This piece shows strong signs of being written by an AI tool. "
    "Automated checks can be wrong. If you wrote it yourself, you can "
    "appeal and a person will review it."
)

LABEL_HUMAN = "We think this was written by a person."

LABEL_UNSURE = (
    "We can't tell whether this was written by a person or with help from "
    "an AI tool. This is not an accusation — our checks are often unsure, "
    "especially with clear, simple writing. If you'd like a person to look "
    "at it, you can appeal."
)


def score_to_label(score: float) -> tuple[str, str]:
    """Turn a score into (guess, label_text)."""
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score < config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def label_ranges() -> list[tuple[str, str]]:
    """The score range each label covers."""
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]


if __name__ == "__main__":
    for name, rng in label_ranges():
        print(f"{name:<24} {rng}")