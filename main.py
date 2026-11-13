"""Pair authorized test timestamps with Defender operational log evidence."""
import argparse
import csv
import json
from datetime import datetime, timedelta

EVENTS = {"1116": "detection", "1117": "action", "5007": "configuration-change"}


def timestamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.utcoffset() is None:
        raise ValueError("Timestamp requires a timezone offset")
    return result


def load(path, required):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing CSV columns: {', '.join(sorted(missing))}")
        return list(reader)


def correlate(tests, events, window):
    indexed = sorted([(timestamp(row["timestamp"]), row) for row in events
                      if row["event_id"] in EVENTS], key=lambda pair: pair[0])
    result = []
    for test in tests:
        start = timestamp(test["timestamp"])
        matches = [dict(timestamp=event["timestamp"], event_id=event["event_id"],
                        category=EVENTS[event["event_id"]])
                   for when, event in indexed
                   if event["host"].casefold() == test["host"].casefold()
                   and start <= when <= start + window]
        result.append(dict(test=test["test_id"], host=test["host"], matches=matches))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tests")
    parser.add_argument("events")
    parser.add_argument("--minutes", type=int, default=5)
    args = parser.parse_args()
    if args.minutes < 0:
        parser.error("--minutes must be nonnegative")
    print(json.dumps(correlate(load(args.tests, {"test_id", "host", "timestamp"}),
                               load(args.events, {"event_id", "host", "timestamp"}),
                               timedelta(minutes=args.minutes)), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError, csv.Error) as exc:
        import sys

        print(f"Invalid input: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
