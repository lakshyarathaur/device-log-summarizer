
import argparse
import json
import sys

import matplotlib

matplotlib.use("Agg")  # render to file without needing a display
import matplotlib.pyplot as plt


def main(argv=None):
    parser = argparse.ArgumentParser(description="Plot average temperature per device")
    parser.add_argument("--input", default="summary.json")
    parser.add_argument("--output", default="avg_temperature.png")
    args = parser.parse_args(argv)

    try:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error reading {args.input}: {exc}", file=sys.stderr)
        return 1

    if not data:
        print("No data to plot.", file=sys.stderr)
        return 1

    devices = [d["device_id"] for d in data]
    temps = [d["avg_temperature"] for d in data]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(devices, temps, color="#2f6db5")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    ax.axhline(80.0, color="#c0392b", linestyle="--", linewidth=1, label="Filter threshold (80.0)")

    ax.set_title("Average Temperature per Device")
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.set_ylim(0, max(max(temps), 80.0) * 1.15)
    ax.legend()
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(args.output, dpi=150)
    print(f"Saved chart to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
