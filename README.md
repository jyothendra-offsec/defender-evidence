# Defender Evidence

Correlate exported Defender events with lab tests by hostname and time window. Time proximity alone does not establish causation.

Requires Python 3.10+. Run from the repo root with the synthetic examples.

```bash
python3 main.py tests.csv events.csv
```

The CLI prints JSON. Use the included examples as input schema references.
