import json
import sys
import textwrap

from log_analyzer.main import main


def test_main_success(tmp_path, capsys, monkeypatch):
    log_file = tmp_path / "log.txt"
    log_file.write_text(
        "\n".join(
            [
                "2026-04-26 09:00:00 DEBUG Application initialized",
                "2026-04-26 09:00:00 INFO Application started",
                "2026-04-26 09:01:12 INFO Loaded configuration",
                "2026-04-26 09:03:45 WARNING Disk usage above 80 percent",
                "2026-04-26 09:05:10 ERROR Database connection failed",
                "2026-04-26 09:06:20 INFO Retrying database connection",
                "2026-04-26 09:07:34 WARNING External API response was slow",
                "2026-04-26 09:08:02 ERROR Timeout while calling external API",
                "2026-04-26 09:10:00 INFO Report generation completed",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(log_file),
            "--output",
            str(tmp_path / "report"),
            "--print-report",
        ],
    )

    return_code = main()

    assert return_code == 0

    output_file = tmp_path / "report.txt"
    assert output_file.exists()

    captured = capsys.readouterr()
    expected_report = textwrap.dedent("""\
        Total lines: 9
        DEBUG: 1
        INFO: 4
        WARNING: 2
        ERROR: 2
        Error messages:
        - Database connection failed
        - Timeout while calling external API
        """).strip()

    assert "Total lines: 9" in captured.out
    assert "DEBUG: 1" in captured.out
    assert "INFO: 4" in captured.out
    assert "ERROR: 2" in captured.out
    assert "Database connection failed" in captured.out
    assert "Timeout while calling external API" in captured.out
    assert output_file.read_text(encoding="utf-8") == expected_report


def test_main_success_json_format(tmp_path, monkeypatch):
    log_file = tmp_path / "log.txt"
    output_base = tmp_path / "report"

    log_file.write_text(
        "2026-04-10 10:00:00 ERROR Something failed",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(log_file),
            "--output",
            str(output_base),
            "--format",
            "json",
        ],
    )

    return_code = main()

    assert return_code == 0

    output_file = tmp_path / "report.json"
    assert output_file.exists()

    content = json.loads(output_file.read_text(encoding="utf-8"))
    assert content["total_lines"] == 1
    assert content["error_count"] == 1
    assert content["error_messages"] == ["Something failed"]


def test_main_success_with_config_file(tmp_path, monkeypatch):
    log_file = tmp_path / "log.txt"
    output_file = tmp_path / "report.txt"
    config_file = tmp_path / "config.json"

    log_file.write_text(
        "2026-04-10 10:00:00 ERROR Something failed",
        encoding="utf-8",
    )

    config_file.write_text(
        json.dumps(
            {
                "input_path": str(log_file),
                "output_path": str(output_file),
                "format_type": "txt",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--config",
            str(config_file),
        ],
    )

    return_code = main()

    assert return_code == 0
    assert output_file.exists()
    assert "ERROR: 1" in output_file.read_text(encoding="utf-8")


def test_main_quiet_suppresses_info_logs(tmp_path, capsys, monkeypatch):
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "2026-04-10 10:00:00 INFO Application started",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(log_file),
            "--output",
            str(tmp_path / "report"),
            "--quiet",
        ],
    )

    return_code = main()
    captured = capsys.readouterr()

    assert return_code == 0
    assert "Report saved to" not in captured.err


def test_main_debug_shows_debug_logs(tmp_path, capsys, monkeypatch):
    log_file = tmp_path / "log.txt"

    log_file.write_text(
        "2026-04-10 10:00:00 INFO Application started",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(log_file),
            "--output",
            str(tmp_path / "report"),
            "--verbose",
        ],
    )

    return_code = main()
    captured = capsys.readouterr()

    assert return_code == 0
    assert "Starting log analysis" in captured.err


def test_main_returns_error_for_missing_input_file(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "log-analyzer",
            "--input",
            str(tmp_path / "missing.txt"),
            "--output",
            str(tmp_path / "report"),
            "--print-report",
        ],
    )

    return_code = main()
    captured = capsys.readouterr()

    assert return_code == 1
    assert not (tmp_path / "report.txt").exists()
    assert captured.out.strip() == ""
    assert "doesn't exist" in captured.err
