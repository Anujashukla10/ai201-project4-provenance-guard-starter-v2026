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
MAX_TEXT_CHARS = 20000

# Unit 8, improvement 2 (stretch): refuse text with fewer than this many real
# words before the signals see it. 0 = off (the "before" and "after" runs).
MIN_WORDS = 0


# ─── Scoring ─────────────────────────────────────────────────────────────────

WEIGHT_MODEL_SIGNAL = 0.6
WEIGHT_STYLE_SIGNAL = 0.4
DISAGREEMENT_GAP = 0.5


# ─── Thresholds ──────────────────────────────────────────────────────────────
#   score < HUMAN_THRESHOLD          -> high-confidence human
#   HUMAN_THRESHOLD <= score < AI    -> unsure
#   score >= AI_THRESHOLD            -> high-confidence AI

HUMAN_THRESHOLD = 0.31
AI_THRESHOLD = 0.78


# ─── Rate limiting (UNIT 8) ──────────────────────────────────────────────────

RATE_LIMITING_ENABLED = True
RATE_LIMIT_PER_MINUTE = 10
RATE_LIMIT_PER_DAY = 200
RATE_LIMIT_STORAGE = "memory://"


# ─── Paths ───────────────────────────────────────────────────────────────────

LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "audit.jsonl"
RESULTS_DIR = ROOT / "results"