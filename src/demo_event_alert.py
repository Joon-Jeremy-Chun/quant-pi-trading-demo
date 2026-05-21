import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


@dataclass(frozen=True)
class CorporateEvent:
    symbol: str
    event_date: date
    event_type: str
    title: str
    source_url: str


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def load_events(path: Path) -> list[CorporateEvent]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    events: list[CorporateEvent] = []
    for row in rows:
        events.append(
            CorporateEvent(
                symbol=row["symbol"].strip().upper(),
                event_date=parse_date(row["event_date"]),
                event_type=row["event_type"].strip(),
                title=row["title"].strip(),
                source_url=row["source_url"].strip(),
            )
        )
    return events


def upcoming_events(events: list[CorporateEvent], today: date, lookahead_days: int) -> list[CorporateEvent]:
    end_date = today + timedelta(days=lookahead_days)
    return sorted(
        [event for event in events if today <= event.event_date <= end_date],
        key=lambda event: (event.event_date, event.symbol),
    )


def render_email(events: list[CorporateEvent], today: date, lookahead_days: int) -> str:
    lines = [
        "Corporate Event Watch Demo",
        "==========================",
        f"Run date: {today.isoformat()}",
        f"Window: next {lookahead_days} calendar days",
        "",
    ]
    if not events:
        lines.append("No events found in the demo window.")
        return "\n".join(lines)

    for event in events:
        days_until = (event.event_date - today).days
        lines.append(
            f"- {event.event_date.isoformat()} ({days_until}d): "
            f"{event.symbol} [{event.event_type}] {event.title}"
        )
        lines.append(f"  source: {event.source_url}")
    return "\n".join(lines)


def render_slack(events: list[CorporateEvent], today: date, lookahead_days: int) -> str:
    if not events:
        return f"Corporate Event Watch Demo: no events in the next {lookahead_days} days from {today.isoformat()}."

    header = f"Corporate Event Watch Demo ({today.isoformat()}, next {lookahead_days} days)"
    bullets = []
    for event in events:
        days_until = (event.event_date - today).days
        bullets.append(f"* {event.symbol}: {event.event_date.isoformat()} in {days_until}d - {event.title}")
    return header + "\n" + "\n".join(bullets)


def write_outbox(outbox: Path, email_body: str, slack_body: str) -> None:
    outbox.mkdir(parents=True, exist_ok=True)
    (outbox / "email_message.txt").write_text(email_body + "\n", encoding="utf-8")
    (outbox / "slack_message.txt").write_text(slack_body + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Demo corporate-event alert renderer using a sanitized local calendar CSV."
    )
    parser.add_argument("--calendar", type=Path, required=True, help="CSV with demo corporate events.")
    parser.add_argument("--today", type=parse_date, default=date.today(), help="Run date in YYYY-MM-DD format.")
    parser.add_argument("--lookahead-days", type=int, default=14)
    parser.add_argument("--outbox", type=Path, default=None, help="Optional folder for rendered demo messages.")
    args = parser.parse_args()

    if args.lookahead_days < 0:
        raise ValueError("lookahead-days must be non-negative")

    selected = upcoming_events(load_events(args.calendar), args.today, args.lookahead_days)
    email_body = render_email(selected, args.today, args.lookahead_days)
    slack_body = render_slack(selected, args.today, args.lookahead_days)

    print(email_body)
    print("\n--- Slack Preview ---")
    print(slack_body)

    if args.outbox:
        write_outbox(args.outbox, email_body, slack_body)
        print(f"\nWrote demo outbox to {args.outbox}")


if __name__ == "__main__":
    main()
