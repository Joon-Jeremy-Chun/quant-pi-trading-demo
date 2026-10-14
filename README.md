# Quant Pi Trading Demo

A public, sanitized overview of a Raspberry Pi based quantitative trading pipeline.

This repository is intentionally a demo scaffold. It shows the architecture, data flow, and automation shape without exposing private strategy parameters, production model artifacts, broker credentials, order logs, or live trading code.

## What This Shows

- Daily market data update concept
- Signal generation interface
- Paper-trading style order handoff shape
- Email/reporting workflow concept
- Corporate event alert workflow concept
- Raspberry Pi scheduled runner architecture
- A student 3D dashboard starter with fictional teammates and synthetic data

## What Is Not Included

- Real strategy edge or private model logic
- Real Alpaca keys or account details
- Production signal files
- Real order/tranche books
- Full historical optimization outputs
- Private backtest artifacts

## Repository Layout

```text
docs/
  architecture.md      Public system overview
  event_alert_demo.md  Corporate event alert demo notes
  dashboard_3d.md      3D starter setup and classroom exercises (English / Korean)
  disclaimer.md        Risk and usage notes
examples/
  corporate_events.csv Fake company event calendar
  synthetic_prices.csv Fake sample market data
  dashboard_3d/       Small independent 3D lab; editable mock JSON
src/
  demo_event_alert.py  Toy event alert renderer
  demo_signal.py       Toy signal generator using synthetic data
  demo_dashboard.py    Local server for the student 3D starter
.env.example           Fake environment shape
```

## Quick Demo

### Student 3D dashboard

```bash
python src/demo_dashboard.py
```

Open **http://127.0.0.1:8000/**. On Windows you can also use `py -3 src/demo_dashboard.py`.
No Python packages or API keys are required. The 3D view loads pinned Three.js from a CDN;
internet is needed for 3D, and a 2D fallback remains usable without it.
See the [step-by-step guide and learning exercises](docs/dashboard_3d.md).

### Toy signal and event examples

```bash
python src/demo_signal.py --prices examples/synthetic_prices.csv
```

```bash
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

## License

MIT, unless changed by the repository owner.
