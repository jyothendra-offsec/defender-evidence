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


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


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
    print(json.dumps(correlate(load(args.tests), load(args.events),
                               timedelta(minutes=args.minutes)), indent=2))


if __name__ == "__main__":
    main()
