from rich.console import Console
from rich.panel import Panel


class AppConsole:
    def __init__(self) -> None:
        self.console = Console()

    def print_report(self, report: str) -> None:
        self.console.print(
            Panel(
                report,
                title="Log Report",
                border_style="green",
            )
        )
