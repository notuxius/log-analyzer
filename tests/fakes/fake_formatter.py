from log_analyzer.models import LogSummary


class FakeFormatter:
    def format(self, summary: LogSummary) -> str:
        return f"Processed {summary['total_lines']} entries"
