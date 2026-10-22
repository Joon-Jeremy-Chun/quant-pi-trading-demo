# Invented event calendar → local report

[Home](../README.md) · [한국어 시작](START_HERE.ko.md) · [Source](../src/demo_event_alert.py)

This lesson reads a local calendar, selects a date range, sorts records and renders two text formats. All five company identifiers and dates are invented. `example.com` source fields are inert teaching references, not downloaded evidence.

## Data contract

| CSV column | Meaning |
| --- | --- |
| symbol | Fictional DEMO-A through DEMO-E identifiers |
| event_date | YYYY-MM-DD calendar date |
| event_type | Invented update/review/note category |
| title | Plain-text classroom description |
| source_url | Reserved example URL, not fetched |

`load_events` strips text and uppercases symbols. `upcoming_events(events, today, lookahead_days)` accepts a non-negative window and selects `today <= event_date <= today + lookahead_days`. Both endpoints are included, so 14 days spans day 0 through day 14, not 14 trading sessions. Records are sorted by date and symbol.

## Fixed-date run and expected selection

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

The end date is June 4. The selected records are May 28 DEMO-A, May 29 DEMO-B, June 1 DEMO-C, June 3 DEMO-D. June 12 DEMO-E is excluded. Omitting `--today` uses the computer's actual local date and can produce an empty result; this is expected for old sample dates.

## Output boundary

`render_email` returns a formatted string. `render_slack` returns another string. Nothing is delivered, and no recipients, webhook or credentials are needed. With an empty list the renderer explains that no events were found.

```console
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14 --outbox outputs/classroom
```

This optional argument creates a local directory and writes email_message.txt and slack_message.txt, replacing those preview files if they exist. No other external side effect is implemented. A duplicate-notification ledger would be a new lesson; it does not exist here.

한국어: 날짜를 고정한 뒤 경계일 포함 여부를 직접 확인하세요. “메일 형식”과 “메일 발송”은 다른 기능입니다. 다음 확장 과제는 [실습](LABS.ko.md)에 있고, 실제 발송 연동은 수업 범위에 포함하지 않습니다.
