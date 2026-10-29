"""
Settings for Provenance Guard.

Everything you're likely to change lives here, at the top, on purpose.
"""

import os
from pathlib import Path

ROOT = Path(__file__).parent


# ─── The service ─────────────────────────────────────────────────────────────

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("AI201_DEBUG", "1") == "1" and HOST in ("127.0.0.1", "localhost")


# ─── The local model ─────────────────────────────────────────────────────────

DETECTOR_MODEL = os.getenv("AI201_DETECTOR_MODEL", "gpt2")
DETECTOR_MAX_TOKENS = 400


# ─── Input limits ────────────────────────────────────────────────────────────
# Anything longer is refused with a 413 before the model runs.
MAX_TEXT_CHARS = 20000


# ─── Scoring (Milestone 4) ───────────────────────────────────────────────────
# Weighted average. The model signal counts more because it reads the words;
# the style signal only sees shape and is cheap to fool.

WEIGHT_MODEL_SIGNAL = 0.6
WEIGHT_STYLE_SIGNAL = 0.4

# If the two signals differ by this much or more, the combined score is pulled
# into the "unsure" band. Two methods disagreeing IS uncertainty.
DISAGREEMENT_GAP = 0.4


# ─── Thresholds (Milestone 5) ────────────────────────────────────────────────
#   score < HUMAN_THRESHOLD          -> high-confidence human
#   HUMAN_THRESHOLD <= score < AI    -> unsure
#   score >= AI_THRESHOLD            -> high-confidence AI
#
# AI_THRESHOLD is set high on purpose: fewer wrong accusations, at the cost of
# letting more AI text land in "unsure".

HUMAN_THRESHOLD = 0.40
AI_THRESHOLD = 0.70


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────

RATE_LIMITING_ENABLED = os.getenv("AI201_RATE_LIMITS", "0") == "1"
RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"