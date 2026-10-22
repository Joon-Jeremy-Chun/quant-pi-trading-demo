# Read the code — one responsibility at a time

[Home](../README.md) · [한국어 시작](START_HERE.ko.md) · [File guide](FILE_GUIDE.md)

## Signal: loading versus calculation

[demo_signal.py](../src/demo_signal.py) has three layers: `load_closes(path)` reads a UTF-8/BOM CSV, `build_demo_signal(closes)` validates and computes, and `main()` parses command-line arguments and prints. The pure calculation accepts at least three finite positive values. It compares the last-three average with the full input average, rounds displayed numbers to four decimal places, and returns a dictionary with `demo_only=True`. The comparison uses unrounded values; display rounding is separate.

한국어: 파일을 읽는 함수와 계산 함수를 나누면 파일 없이 `[10, 10, 10]` 같은 작은 입력으로 검사할 수 있습니다. 출력 문자열 BUY/HOLD를 외부 행동과 혼동하지 마세요. 이 함수는 사전 하나를 반환할 뿐입니다.

## Simulation: decisions versus actions

[demo_backtest.py](../src/demo_backtest.py) uses a `PriceRow` record. `moving_average` takes the last w observations; `run_demo_backtest` validates rows, tracks cash/shares, consumes the previous decision, computes the current decision, and records equity. Its long window defaults to five, unlike the snapshot signal's whole-sample average. [Detailed timeline](BACKTEST.md).

Inputs must have finite positive prices, positive finite initial cash, positive integer windows with short < long, enough rows and strictly increasing unique ISO dates. A pending final decision is reported but never fabricated into a fill after the dataset ends.

## Report: selection versus presentation

[demo_event_alert.py](../src/demo_event_alert.py) loads `CorporateEvent` records, filters an inclusive calendar-date window, sorts by date/symbol, and renders strings. `render_email` and `render_slack` return text; their names describe formatting only. `write_outbox` is the optional file-writing boundary. None of the source URLs is requested. [Date boundaries](event_alert_demo.md).

한국어: “알림”이라는 이름만으로 발송 기능이 있다고 추측하지 않습니다. 선택 결과를 바꾸려면 날짜 필터를, 문장 형태를 바꾸려면 renderer를 수정합니다.

## Dashboard: state versus geometry

[sample_state.json](../examples/dashboard_3d/sample_state.json) defines data. [app.js](../examples/dashboard_3d/app.js) validates it, connects buttons, calculates the chart, and optionally builds 3D shapes. `validateSample` rejects malformed inputs before simulation controls are enabled. `selectAgent`, `advance`, `stopPlayback` and `reset` manage visible state. Dynamic Three.js imports are confined to `buildScene`, so intentional 2D mode skips them.

[demo_dashboard.py](../src/demo_dashboard.py) is a small local static server. Its allowlist contains exactly index.html, styles.css, app.js and sample_state.json. There is no backend trading/report API. The browser and CLI examples share a teaching theme, but no automatic result handoff is implemented.

## Read the tests as examples of questions

- Does an equal snapshot average produce HOLD?
- Can the fifth observation produce a decision without a same-close action?
- Does adding future rows leave earlier events unchanged?
- Are today and the inclusive end date both selected?
- Is an existing unlisted file still rejected by the local server?

[Python checks](../tests/test_classroom.py) use standard-library unittest and temporary fixtures; [JavaScript checks](../tests/test_dashboard_state.cjs) use Node built-ins only. They test the public teaching behavior, not a private model.
