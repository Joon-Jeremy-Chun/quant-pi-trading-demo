import argparse
import csv
from pathlib import Path


def load_closes(path: Path) -> list[float]:
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return [float(row["close"]) for row in rows]


def build_demo_signal(closes: list[float]) -> dict[str, object]:
    if len(closes) < 3:
        raise ValueError("Need at least three prices for the demo signal")

    short_avg = sum(closes[-3:]) / 3
    long_avg = sum(closes) / len(closes)
    signal = "BUY" if short_avg > long_avg else "HOLD"

    return {
        "signal": signal,
        "short_average": round(short_avg, 4),
        "long_average": round(long_avg, 4),
        "demo_only": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a toy signal from synthetic prices.")
    parser.add_argument("--prices", type=Path, required=True)
    args = parser.parse_args()

    result = build_demo_signal(load_closes(args.prices))
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
