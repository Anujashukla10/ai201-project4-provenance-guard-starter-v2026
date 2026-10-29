#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────

class _LimiterOff:
    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── POST /submit ──────────────────────────────────────────────────────────────

def _reject(creator_id, reason, status, message, **extra):
    """Log a refused request and send back a JSON error."""
    audit.log_rejection(creator_id=creator_id or "unknown", reason=reason, **extra)
    return jsonify({"error": reason, "message": message}), status


@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, score it with two signals, label it, log it.

    In:  {"text": "...", "creator_id": "..."}
    Out: {"content_id", "guess", "confidence", "label",
          "model_score", "style_score", "status"}
    """
    # 1. Must be a JSON object
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _reject("unknown", "bad_request", 400,
                       'Send a JSON object with "text" and "creator_id".')

    text = payload.get("text")
    creator_id = payload.get("creator_id")

    # 2. Validate creator_id and text
    if not isinstance(creator_id, str) or not creator_id.strip():
        return _reject("unknown", "missing_creator_id", 400,
                       'Send a non-empty "creator_id".')

    if not isinstance(text, str) or not text.strip():
        return _reject(creator_id, "missing_or_empty_text", 400,
                       'Send JSON with a non-empty "text".')

    if len(text) > config.MAX_TEXT_CHARS:
        return _reject(creator_id, "text_too_long", 413,
                       f"Text must be under {config.MAX_TEXT_CHARS} characters.",
                       length=len(text))

    # 3. Signal one — the model
    try:
        model_score = detector.model_signal(text)
    except ValueError:
        return _reject(creator_id, "text_too_short", 400,
                       "Please submit at least a few sentences.")
    except detector.DetectorUnavailable as exc:
        return _reject(creator_id, "detector_unavailable", 503, str(exc))

    # 4. Signal two — the style
    style_score = stylometry.style_signal(text)

    # 5. Combine and label
    combined = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined)

    # 6. Log the decision
    content_id = uuid.uuid4().hex[:12]
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined,
        label=label,
        status="decided",
    )

    # 7. Answer
    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "status": "decided",
    }), 200


# ── POST /appeal ──────────────────────────────────────────────────────────────

@app.post("/appeal")
def appeal():
    """
    A writer says we got it wrong.

    In:  {"content_id": "...", "reasoning": "..."}
    Out: {"content_id", "status": "under_review", "message", "original_label"}
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "bad_request",
                        "message": 'Send JSON with "content_id" and "reasoning".'}), 400

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")

    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({"error": "bad_request",
                        "message": 'Send a "content_id".'}), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({"error": "bad_request",
                        "message": "Tell us why you think we got it wrong."}), 400

    # Does this content_id actually exist as a decision?
    history = audit.entries_for(content_id)
    decisions = [e for e in history if e.get("event") is None]
    if not decisions:
        return jsonify({"error": "not_found",
                        "message": f"No submission with content_id {content_id}."}), 404

    original = decisions[0]
    audit.log_appeal(
        content_id=content_id,
        creator_id=original.get("creator_id", "unknown"),
        reasoning=reasoning,
    )

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thank you. Your appeal is recorded and a person will review this piece.",
        "original_label": original.get("label"),
    }), 200


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()