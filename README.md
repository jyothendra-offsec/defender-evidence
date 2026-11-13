# Defender Evidence

Review Defender telemetry around controlled lab tests.

## Quick start

Use Python 3.10 or newer. The CLI runs locally with the standard library. From the repository root, run:

```sh
python3 main.py tests.csv events.csv
```

The sample pairs `T01` with event `1116` one minute later. Event `1117` falls outside the default five-minute window.

## Input and output

| Input | Format | Output or purpose |
| --- | --- | --- |
| Test CSV | `test_id,host,timestamp` | One output row per test |
| Event CSV | `event_id,host,timestamp` | 1116 detection, 1117 action, 5007 configuration change |
| `--minutes` | Nonnegative integer | Inclusive window starting at each test |

Results are JSON on stdout. Redirect to a file when you want to save the review.

## Interpreting results

Hostnames are matched without regard to case. Use consistent short names or FQDNs across both files and include a timezone offset in every timestamp. Time and host matching establish correlation only. Confirm the event details in the original log.

## Troubleshooting

- Use the included fixture first to confirm the command and working directory.
- Check the input path and required fields if the CLI exits with status 2.
- Keep real assessment exports and generated reports in your private workspace.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
```

## Review workflow

A test with an empty matches array should prompt a review of log collection, clock alignment and hostname spelling. Compare the original event details before assigning causation.

## Usage terms

Original material in this revision requires the owner's written permission for modification or redistribution. Earlier MIT releases and third-party licenses retain their terms. See [LICENSE](LICENSE).
