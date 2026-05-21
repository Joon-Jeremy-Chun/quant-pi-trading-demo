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
  disclaimer.md        Risk and usage notes
examples/
  corporate_events.csv Fake company event calendar
  synthetic_prices.csv Fake sample market data
src/
  demo_event_alert.py  Toy event alert renderer
  demo_signal.py       Toy signal generator using synthetic data
.env.example           Fake environment shape
```

## Quick Demo

```bash
python src/demo_signal.py --prices examples/synthetic_prices.csv
```

```bash
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

## License

MIT, unless changed by the repository owner.
