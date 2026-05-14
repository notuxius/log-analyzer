from collections.abc import Iterable

from log_analyzer.models import LogEntry, LogLevel, LogSummary


class LogSummarizer:
    def summarize(self, entries: Iterable[LogEntry]) -> LogSummary:
        total_lines = 0
        debug_count = 0
        info_count = 0
        warning_count = 0
        error_count = 0
        error_messages: list[str] = []

        for log_entry in entries:
            total_lines += 1
            log_entry_level = log_entry.level

            match log_entry_level:
                case LogLevel.DEBUG:
                    debug_count += 1
                case LogLevel.INFO:
                    info_count += 1
                case LogLevel.WARNING:
                    warning_count += 1
                case LogLevel.ERROR:
                    error_count += 1
                    error_messages.append(log_entry.message)

        log_summary: LogSummary = {
            "total_lines": total_lines,
            "debug_count": debug_count,
            "info_count": info_count,
            "warning_count": warning_count,
            "error_count": error_count,
            "error_messages": error_messages,
        }

        return log_summary
