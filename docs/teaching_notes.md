# Teaching Notes

This repository is a small public teaching scaffold. It is meant to help students see how an automated trading project can be organized without exposing private research, live broker code, real model artifacts, or real order history.

## Learning Goals

- Separate data loading, signal generation, backtesting, and reporting.
- Understand why reproducible inputs matter.
- Practice using synthetic data before touching real market data.
- Learn the difference between a software demo and a deployable trading system.
- Discuss operational safeguards such as dry runs, logs, and credential isolation.

## Suggested Class Flow

1. Run the toy signal script.

```bash
python src/demo_signal.py --prices examples/synthetic_prices.csv
```

2. Run the toy backtest script.

```bash
python src/demo_backtest.py --prices examples/synthetic_prices.csv
```

3. Ask students to inspect the daily events and explain when the demo strategy enters or exits.

4. Change the moving-average windows.

```bash
python src/demo_backtest.py --prices examples/synthetic_prices.csv --short-window 2 --long-window 4
```

5. Discuss why this does not prove a real trading edge.

## Discussion Questions

- What assumptions are hidden inside a backtest?
- Why should a project use synthetic data for public examples?
- What logs would you want before trusting an automated system?
- Why should credentials and production outputs never be committed?
- How would you design a dry-run mode before sending real orders?

## What Students Can Extend

- Add more synthetic price rows.
- Export the daily backtest events to a CSV file.
- Add a maximum-position rule.
- Add transaction costs.
- Add a simple HTML or text report.
- Write tests for the moving-average and backtest functions.

## What This Demo Intentionally Omits

- Real strategy parameters.
- Real broker API calls.
- Real account identifiers or credentials.
- Production model selection logic.
- Live order books, tranche ledgers, or private execution logs.
- Any claim that the toy signal has investment value.

## Instructor Note

Keep the framing clear: this repo teaches software structure, reproducibility, and risk awareness. It should not be presented as a profitable strategy or as a live trading template.
