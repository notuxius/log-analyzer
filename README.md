# Log Analyzer

[![Tests](https://github.com/notuxius/log-analyzer/actions/workflows/python-tests.yml/badge.svg)](https://github.com/notuxius/log-analyzer/actions/workflows/python-tests.yml)

CLI tool to analyze log files and generate text or JSON reports.

---

## Features

- Parse log files with INFO, WARNING, and ERROR levels
- Generate text or JSON reports
- Save reports to file
- Optional console output
- Configurable log level (DEBUG, INFO, WARNING, ERROR)
- Streaming log processing (memory efficient)
- Tested with pytest
- CI with Ruff, Black, and coverage

---

## Installation

For local development:

```bash
uv sync
```

---

## Usage

### Basic example

```bash
uv run log-analyzer \
  --input logs/sample.txt \
  --output reports/log_report \
  --format txt \
  --log-level INFO \
  --print-report
```

---

### JSON output

```bash
uv run log-analyzer \
  --input logs/sample.txt \
  --format json
```

---

### Logging levels

```bash
uv run log-analyzer --log-level DEBUG
uv run log-analyzer --log-level INFO
uv run log-analyzer --log-level WARNING
uv run log-analyzer --log-level ERROR
```

---

### Help

```bash
uv run log-analyzer --help
```

---

## Development

Run checks locally:

```bash
uv run ruff check .
uv run black --check .
uv run pytest -v --cov=log_analyzer --cov-report=term-missing
```

---

## Architecture

```text
main.py        -> CLI entry point
config.py      -> app configuration and validation
container.py   -> dependency wiring (DI container)
logger.py      -> logging wrapper
analyzer.py    -> core logic (loader, summarizer, formatter)
models.py      -> typed data structures
```

---

## Example Output

```text
Total lines: 8
INFO: 4
WARNING: 2
ERROR: 2
Error messages:
- Database connection failed
- Timeout while calling external API
```

---

## License

MIT
