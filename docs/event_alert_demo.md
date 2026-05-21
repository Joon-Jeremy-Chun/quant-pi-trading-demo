# Corporate Event Alert Demo

This note describes a public, sanitized version of a corporate-event alert workflow.

The private system may search real data sources, detect relevant company announcement dates, and notify operators through email or Slack. This public demo keeps only the teachable shape of that workflow:

1. Read a small event calendar.
2. Filter events inside a lookahead window.
3. Render an email-style report.
4. Render a Slack-style message.
5. Optionally write both messages to a local outbox folder.

No real API keys, webhooks, broker data, private event sources, or production recipient lists are included.

## Run The Demo

```bash
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14
```

To write message previews:

```bash
python src/demo_event_alert.py --calendar examples/corporate_events.csv --today 2026-05-21 --lookahead-days 14 --outbox examples/outbox
```

The generated files are:

```text
examples/outbox/email_message.txt
examples/outbox/slack_message.txt
```

## Production Concepts To Discuss

- Data source reliability: real event dates should come from a source with timestamps and references.
- Time zones: event dates, market sessions, and scheduled jobs should be explicit.
- Idempotency: a live system should track what it already sent so it does not spam recipients.
- Recipient routing: different strategy groups may need different email and Slack audiences.
- Secrets: SMTP passwords, Slack webhooks, and API tokens belong in environment variables, not Git.
- Audit logs: each notification should leave a small append-only record of what was sent and why.

## Suggested Student Extensions

- Add a `sent_alerts.csv` ledger to prevent duplicate alerts.
- Add a severity field such as `low`, `medium`, or `high`.
- Add symbol filtering from the command line.
- Render Markdown instead of plain text.
- Write a unit test for the date-window filter.
