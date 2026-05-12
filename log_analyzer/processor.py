from log_analyzer.protocols import Formatter, Loader, Summarizer


class LogProcessor:
    def __init__(
        self, loader: Loader, summarizer: Summarizer, formatter: Formatter
    ) -> None:
        self.loader = loader
        self.summarizer = summarizer
        self.formatter = formatter

    def process(self) -> str:
        entries = self.loader.load()
        summary = self.summarizer.summarize(entries)
        return self.formatter.format(summary)
