# Classroom maintenance — 2026-10-21

[Home](../README.md) · [Validation](VALIDATION.md)

| Area | Observation | Change |
| --- | --- | --- |
| Backtest | A rule used the current close and acted at that same close | Previous decision processed at next observation's close; timing fields exposed |
| Backtest | HOLD also meant closing an existing toy position | Simulation's target-cash label is now FLAT; snapshot HOLD remains descriptive |
| Input | Invalid prices/cash/dates and helper-window values could yield misleading arithmetic | Positive finite values, ordered dates and integer windows checked |
| Date helper | Negative window was rejected only in CLI | Pure date filter now enforces the same contract |
| Local server | Root-directory boundary existed, but arbitrary files inside the dashboard directory could be served | Exactly four public assets allowed; GET/HEAD boundary and headers tested |
| Fixture provenance | Invented calendar used real company/ticker names | Fully fictional DEMO-A…E names and example URLs |
| Documentation | README omitted the backtest, architecture implied unimplemented operations | Actual entry points, local behavior and independent inputs documented |
| Student support | Limited walkthrough, expected outputs and exercises | EN/KR start paths, explanations, boundary exercises, answer notes and instructor plan |

No private code, strategy data, device-access information or operational artifacts were consulted. The existing 3D scene/state implementation was preserved. Screenshots were produced from that public synthetic scene in a fresh local browser profile and reviewed before publication.

Old backtest numbers differ because the declared time convention changed. This is a software correctness lesson, not a performance improvement claim. The three CLI examples, source tests, JS checks and browser behavior are recorded in [verification](VALIDATION.md). The original local working folder is preserved in a separate checkout.
