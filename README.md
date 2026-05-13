# Log Analyzer

[![Tests](https://github.com/notuxius/log-analyzer/actions/workflows/python-tests.yml/badge.svg)](https://github.com/notuxius/log-analyzer/actions/workflows/tests.yml)

A modular Python CLI application for analyzing log files and generating formatted reports.

The project demonstrates modern Python development practices including:
- dependency injection
- protocol-oriented architecture
- dataclass models
- streaming file processing
- structured logging
- unit and integration testing
- type checking and linting

---

# Features

- Parse log files using regex-based parsing
- Generate TXT or JSON reports
- Stream log files lazily using iterators
- Detect malformed log entries
- Validate log levels
- Configurable CLI interface
- JSON configuration support
- Structured logging
- Dependency injection with protocols
- Fully tested architecture
- 100% test coverage

---

# Architecture

The application is separated into focused components:

```text
LogLoader
    Reads log files lazily line-by-line

LogParser
    Parses raw log lines into LogEntry objects

LogSummarizer
    Aggregates log statistics and error messages

Formatter
    Generates report output (TXT or JSON)

ReportSaver
    Saves reports to disk

AppContainer
    Wires application dependencies together
```

The project follows:
- Single Responsibility Principle (SRP)
- Dependency Injection (DI)
- Protocol-oriented design

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd log_analyzer-project
```

Install dependencies using uv:

```bash
uv sync
```

---

# Usage

## Analyze a log file

```bash
uv run log-analyzer --input logs/sample.txt
```

## Generate JSON report

```bash
uv run log-analyzer \
    --input logs/sample.txt \
    --format json
```

## Print report to console

```bash
uv run log-analyzer \
    --input logs/sample.txt \
    --print-report
```

## Use configuration file

```bash
uv run log-analyzer --config config.json
```

## Enable debug logging

```bash
uv run log-analyzer \
    --input logs/sample.txt \
    --verbose
```

---

# Example Input

```text
2026-04-10 10:00:00 INFO Application started
2026-04-10 10:01:00 WARNING High memory usage
2026-04-10 10:02:00 ERROR Database connection failed
```

---

# Example TXT Output

```text
Total lines: 3
INFO: 1
WARNING: 1
ERROR: 1
Error messages:
- Database connection failed
```

---

# Example JSON Output

```json
{
    "total_lines": 3,
    "info_count": 1,
    "warning_count": 1,
    "error_count": 1,
    "error_messages": [
        "Database connection failed"
    ]
}
```

---

# Running Tests

Run all tests:

```bash
uv run pytest -v
```

Run tests with coverage:

```bash
uv run pytest -v --cov=log_analyzer --cov-report=term-missing
```

---

# Code Quality

Linting:

```bash
uv run ruff check .
```

Formatting:

```bash
uv run black .
```

---

# Technologies Used

- Python 3.11
- pytest
- pytest-cov
- Ruff
- Black
- uv

---

# Future Improvements

Possible future enhancements:

- CSV formatter
- HTML formatter
- Async log processing
- Plugin formatter system
- Compressed log support
- Rich terminal UI
- Parallel processing
- Real-time log monitoring
