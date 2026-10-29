"""
Signal two: the style signal.

Measures the text AS TEXT — its shape — without understanding a word.

    sentence_length_spread   stdev / mean of sentence lengths (higher = human)
    type_token_ratio         unique / total over first 100 words (higher = human)
    punctuation_density      non-full-stop punctuation per word (higher = human)

All three point "higher = more human", so each is flipped and scaled to 0-1
before combining, giving a final score where HIGHER = MORE LIKELY AI.

Blind spot: this signal cannot read. Typos, chopped-up sentences, or a pasted
quotation change the shape without changing the substance.

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# Punctuation that varies between writers. Full stops are left out on purpose —
# everybody uses them.
PUNCT = ",;:—–-()!?\""

# Scaling points (where each measure maps to 0 or 1). Tuned on the instructor's
# three samples; see README.
SPREAD_HUMAN_AT = 0.6     # coefficient of variation >= 0.6 -> fully human
TTR_HUMAN_AT = 0.80       # TTR >= 0.80 -> fully human
TTR_AI_AT = 0.55          # TTR <= 0.55 -> fully AI
PUNCT_HUMAN_AT = 0.15     # >= 0.15 punctuation marks per word -> fully human

W_SPREAD = 0.4
W_TTR = 0.3
W_PUNCT = 0.3


def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence lengths (stdev / mean).
    Higher = lumpier sentences = more human.
    Fewer than 2 sentences -> 0.0 (no spread can be measured).
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words / total words, over the first 100 words only, so long and
    short texts are comparable. Higher = more varied vocabulary = more human.
    """
    w = words(text)[:100]
    if not w:
        return 0.0
    return round(len(set(w)) / len(w), 4)


def punctuation_density(text: str) -> float:
    """
    Count of commas, semicolons, colons, dashes, brackets, ! ? and quotes,
    per word. Higher = more human.
    """
    w = words(text)
    if not w:
        return 0.0
    count = sum(text.count(c) for c in PUNCT)
    return round(count / len(w), 4)


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. HIGHER MEANS MORE LIKELY AI.

    Each measure is flipped (because each one is 'higher = human') and scaled
    to 0-1, then combined: 0.4 spread + 0.3 TTR + 0.3 punctuation.
    """
    spread_ai = _clamp(1 - sentence_length_spread(text) / SPREAD_HUMAN_AT)
    ttr_ai = _clamp((TTR_HUMAN_AT - type_token_ratio(text)) / (TTR_HUMAN_AT - TTR_AI_AT))
    punct_ai = _clamp(1 - punctuation_density(text) / PUNCT_HUMAN_AT)

    score = W_SPREAD * spread_ai + W_TTR * ttr_ai + W_PUNCT * punct_ai
    return round(_clamp(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")