Sources: `results\run_2026-11-10_1636_before.md` (`run_eval.py::main`) and `results\criteria_4_5_2026-11-10_1637_before.md` (`criteria_extra.py::main`), summarised by `summarize_eval.py`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled high-confidence AI | ≤ 1 of 10, every trial | 3/10 | 3/10 | 3/10 | **MISSED** |
| 2. Clearly AI vs clearly human score spread | gap ≥ 0.30 and borderline between, every trial | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | gap 0.254; borderline 0.298 NOT between | **MISSED** |
| 3. All three labels reachable | 3 of 3 labels, every trial | 3/3 | 3/3 | 3/3 | MET |
| 4. Every appeal recorded and changes status | 5/5 real and 3/3 fake → 404, every trial | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | 5/5 real, 3/3 fake | MET |
| 5. Bad input never crashes | 6/6 → 4xx + rejected log entry, every trial | 6/6 | 6/6 | 6/6 | MET |

- Criterion 1, piece 1 labelled AI: model 0.8275, style 0.92, combined 0.8645 — "sometimes some classes are really hard for some and easy for other, an"
- Criterion 1, piece 3 labelled AI: model 0.5997, style 0.6209, combined 0.6082 — "Hello Professor, I wanted to let you know that I had missed the assign"
- Criterion 1, piece 9 labelled AI: model 0.7177, style 0.8028, combined 0.7517 — "Python is a simple language which is not too hard but for new learners"
- Criterion 2 scores (trial 1): clearly_ai model 0.7544 style 0.316 combined 0.579; clearly_human model 0.4445 style 0.1452 combined 0.3248; borderline model 0.3489 style 0.2216 combined 0.298
