# File guide

[Home](../README.md) · [Architecture](architecture.md)

| File | Responsibility | Local effects |
| --- | --- | --- |
| [demo_signal.py](../src/demo_signal.py) | CSV → toy snapshot dictionary | Prints values |
| [demo_backtest.py](../src/demo_backtest.py) | Time-ordered invented simulation | Prints events/summary |
| [demo_event_alert.py](../src/demo_event_alert.py) | Calendar filter and text renderers | Prints; optional local outbox |
| [demo_dashboard.py](../src/demo_dashboard.py) | Loopback static server | Serves four allowlisted assets |
| [Price CSV](../examples/synthetic_prices.csv) | Ten invented observations | Input only |
| [Event CSV](../examples/corporate_events.csv) | Five invented calendar records | Input only |
| [Dashboard state](../examples/dashboard_3d/sample_state.json) | Fictional roles, 12 prices and scripted steps | Browser input only |
| [HTML](../examples/dashboard_3d/index.html) / [CSS](../examples/dashboard_3d/styles.css) / [JS](../examples/dashboard_3d/app.js) | UI structure, appearance and behavior | Local UI; optional pinned 3D imports |
| [Python tests](../tests/test_classroom.py) | 22 focused behavior checks | Temporary fixtures and loopback server |
| [JS tests](../tests/test_dashboard_state.cjs) | Nine sample-contract cases | No network or package dependencies |
| [Documentation validator](../tools/validate_documentation.py) | Source/links/fences/SVG checks | Read-only |
| [Publication checker](../tools/check_publication.py) | Public text and optional public-history review | Read-only |
| [Reference runner](../tools/verify_classroom.py) | Repeat fixture checks and save evidence | Writes docs/validation artifacts |

`.env.example` is an unused illustrative shape. `hello-from-claude.md` is a preserved historical greeting, not part of the lesson. Original public file names remain stable.
