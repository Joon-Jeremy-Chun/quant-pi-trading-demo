import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PriceRow:
    date: str
    close: float


def load_prices(path: Path) -> list[PriceRow]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    return [PriceRow(date=row["date"], close=float(row["close"])) for row in rows]


def moving_average(values: list[float], window: int) -> float | None:
    if len(values) < window:
        return None
    return sum(values[-window:]) / window


def run_demo_backtest(
    prices: list[PriceRow],
    short_window: int,
    long_window: int,
    initial_cash: float,
) -> dict[str, object]:
    if short_window <= 0 or long_window <= 0:
        raise ValueError("Windows must be positive")
    if short_window >= long_window:
        raise ValueError("Use short_window < long_window for this toy demo")
    if len(prices) < long_window:
        raise ValueError("Not enough rows for the requested long window")

    cash = initial_cash
    shares = 0.0
    events: list[dict[str, object]] = []
    closes: list[float] = []

    for row in prices:
        closes.append(row.close)
        short_ma = moving_average(closes, short_window)
        long_ma = moving_average(closes, long_window)
        if short_ma is None or long_ma is None:
            signal = "WAIT"
        else:
            signal = "BUY" if short_ma > long_ma else "HOLD"

        if signal == "BUY" and shares == 0.0:
            shares = cash / row.close
            cash = 0.0
            action = "ENTER"
        elif signal == "HOLD" and shares > 0.0:
            cash = shares * row.close
            shares = 0.0
            action = "EXIT"
        else:
            action = "NONE"

        equity = cash + shares * row.close
        events.append(
            {
                "date": row.date,
                "close": round(row.close, 4),
                "signal": signal,
                "action": action,
                "shares": round(shares, 6),
                "cash": round(cash, 2),
                "equity": round(equity, 2),
            }
        )

    final_equity = float(events[-1]["equity"])
    buy_hold_shares = initial_cash / prices[0].close
    buy_hold_equity = buy_hold_shares * prices[-1].close

    return {
        "demo_only": True,
        "initial_cash": round(initial_cash, 2),
        "final_equity": round(final_equity, 2),
        "total_return_pct": round((final_equity / initial_cash - 1.0) * 100.0, 2),
        "buy_hold_equity": round(buy_hold_equity, 2),
        "buy_hold_return_pct": round((buy_hold_equity / initial_cash - 1.0) * 100.0, 2),
        "events": events,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a toy moving-average backtest on synthetic prices.")
    parser.add_argument("--prices", type=Path, required=True)
    parser.add_argument("--short-window", type=int, default=3)
    parser.add_argument("--long-window", type=int, default=5)
    parser.add_argument("--initial-cash", type=float, default=10_000.0)
    args = parser.parse_args()

    result = run_demo_backtest(
        load_prices(args.prices),
        short_window=args.short_window,
        long_window=args.long_window,
        initial_cash=args.initial_cash,
    )

    print("Demo backtest summary")
    print("=====================")
    for key in ["demo_only", "initial_cash", "final_equity", "total_return_pct", "buy_hold_equity", "buy_hold_return_pct"]:
        print(f"{key}: {result[key]}")

    print("\nDaily events")
    for event in result["events"]:
        print(
            f"{event['date']} close={event['close']} signal={event['signal']} "
            f"action={event['action']} equity={event['equity']}"
        )


if __name__ == "__main__":
    main()
