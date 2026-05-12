import re

from log_analyzer.exceptions import InvalidLogLevelError
from log_analyzer.models import LogEntry, LogLevel


class LogParser:
    LOG_PATTERN = re.compile(
        r"^(?P<date>\d{4}-\d{2}-\d{2}) "
        r"(?P<time>\d{2}:\d{2}:\d{2}) "
        r"(?P<level>[A-Za-z]+) "
        r"(?P<message>.*)$"
    )

    def parse(self, line: str) -> LogEntry | None:
        match = self.LOG_PATTERN.match(line)

        if match is None:
            return None

        date_part = match.group("date")
        time_part = match.group("time")
        level_part = match.group("level")
        message_part = match.group("message")
        timestamp = f"{date_part} {time_part}"

        try:
            level = LogLevel(level_part)
        except ValueError as error:
            raise InvalidLogLevelError(
                f"Invalid log message level: {level_part}"
            ) from error

        if not message_part.strip():
            return None

        log_entry: LogEntry = {
            "timestamp": timestamp,
            "level": level,
            "message": message_part,
        }

        return log_entry
