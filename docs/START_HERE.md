# Start here — a local software lab

[Home](../README.md) · [한국어 상세 안내](START_HERE.ko.md) · [Exercises and answers](LABS.ko.md)

## 1. Prepare a copy

Use Python 3.10+ and a browser. Check `python --version` (Windows alternative: `py -3 --version`). Download ZIP from GitHub and extract it, or clone the public repository:

```console
git clone https://github.com/Joon-Jeremy-Chun/quant-pi-trading-demo.git
cd quant-pi-trading-demo
```

Open a terminal in the folder containing README.md, src and examples. Do not open a private work folder. There is no dependency installation, account setup or environment-file step for these lessons.

## 2. Run one deterministic calculation

```console
python src/demo_signal.py --prices examples/synthetic_prices.csv
```

Expected values: `signal: BUY`, `short_average: 102.6333`, `long_average: 101.51`, `demo_only: True`. The short average uses the last three of ten invented observations; the long average uses all ten. A label is descriptive program output; it does not submit anything. Equality produces HOLD. [Read the functions](CODE_WALKTHROUGH.md).

## 3. Trace a simulation

```console
python src/demo_backtest.py --prices examples/synthetic_prices.csv
```

Read the daily events before the summary. On January 8 the fifth observation produces BUY but performs no action. On January 9 that earlier decision is processed at 101.20. The default toy run ends at equity 10187.75 and return 1.88% from 10000 fictitious units. The separate first-observation buy-and-hold illustration ends at 10310.00. These are fixture checks, not measured market performance; they start exposure at different times. [Timing and assumptions](BACKTEST.md).

## 4. Render an invented event report

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

The inclusive window selects DEMO-A through DEMO-D, and excludes DEMO-E. Names/dates are invented and `example.com` references are not fetched. Email-style and Slack-style headings are text previews; nothing is sent. Optional local files:

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14 --outbox outputs/classroom
```

This creates `outputs/classroom/email_message.txt` and `slack_message.txt`, overwriting those same preview filenames on another run. Keep your own work in separate filenames. [Report guide](event_alert_demo.md).

## 5. Explore the dashboard

```console
python src/demo_dashboard.py
```

Open http://127.0.0.1:8000/ on the same computer. Select teammates, advance Next step, play/pause and reset. Press Ctrl+C in the terminal to stop the server. The page's state comes from examples/dashboard_3d/sample_state.json, not the CLI reports.

The 3D path downloads pinned Three.js modules from jsDelivr. To avoid those requests, open http://127.0.0.1:8000/?view=2d. No Raspberry Pi, remote machine, login or paid service is used. [Dashboard guide](dashboard_3d.md).

## 6. Check and explain

Run `python -m unittest discover -s tests -v`. Then complete [the exercises](LABS.ko.md), comparing with [answers](SOLUTIONS.ko.md) after your own attempt. A useful submission includes the command, expected result, one changed input, an explanation and a boundary test. [Teaching plan](teaching_notes.md).

For common errors, see the [troubleshooting table](START_HERE.ko.md). The local server serves only the four classroom assets, and should stay local. [Public boundary](PUBLIC_BOUNDARY.md).
