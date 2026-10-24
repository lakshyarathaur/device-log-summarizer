
import argparse
import csv
import json
import math
import sys
from collections import defaultdict

REQUIRED_COLUMNS = {"device_id", "status", "temperature"}


def read_rows(path):
    """Yield (device_id, status, temperature) from valid rows; skip bad ones.

    Returns (rows, skipped_count). Raises FileNotFoundError / ValueError for
    file-level problems so main() can report them cleanly.
    """
    rows, skipped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty")
        missing = REQUIRED_COLUMNS - {c.strip() for c in reader.fieldnames}
        if missing:
            raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
        for row in reader:
            device = (row.get("device_id") or "").strip()
            status = (row.get("status") or "").strip().upper()
            try:
                temp = float(row.get("temperature"))
            except (TypeError, ValueError):
                skipped += 1
                continue
            if not device or math.isnan(temp) or math.isinf(temp):
                skipped += 1
                continue
            rows.append((device, status, temp))
    return rows, skipped


def aggregate(rows):
    """Group by device_id -> total records, mean temperature, ERROR count."""
    groups = defaultdict(list)
    for device, status, temp in rows:
        groups[device].append((status, temp))

    results = []
    for device in sorted(groups):
        records = groups[device]
        temps = [t for _, t in records]
        results.append({
            "device_id": device,
            "total_records": len(records),
            "avg_temperature": round(sum(temps) / len(temps), 2),
            "error_count": sum(1 for s, _ in records if s == "ERROR"),
        })
    return results


def filter_hot_devices(results, max_avg_temp):
    """Drop devices whose average temperature is above the threshold."""
    return [r for r in results if r["avg_temperature"] <= max_avg_temp]


def print_table(results):
    header = f"{'Device':<10}{'Records':>9}{'Avg Temp':>10}{'Errors':>8}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['device_id']:<10}{r['total_records']:>9}"
              f"{r['avg_temperature']:>10.2f}{r['error_count']:>8}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Device Log Summarizer")
    parser.add_argument("--input", default="device_telemetry.csv")
    parser.add_argument("--output", default="summary.json")
    parser.add_argument("--max-avg-temp", type=float, default=80.0)
    args = parser.parse_args(argv)

    try:
        rows, skipped = read_rows(args.input)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}", file=sys.stderr)
        return 1
    except (ValueError, csv.Error, UnicodeDecodeError) as exc:
        print(f"Error reading {args.input}: {exc}", file=sys.stderr)
        return 1

    if skipped:
        print(f"Warning: skipped {skipped} malformed row(s).", file=sys.stderr)

    results = filter_hot_devices(aggregate(rows), args.max_avg_temp)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
    except OSError as exc:
        print(f"Error writing {args.output}: {exc}", file=sys.stderr)
        return 1

    if results:
        print_table(results)
    else:
        print("No devices at or below the temperature threshold.")
    print(f"\nSaved {len(results)} device(s) to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
