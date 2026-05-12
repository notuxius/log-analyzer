from pathlib import Path

from log_analyzer.config import AppConfig
from log_analyzer.formatters import FormatterFactory
from log_analyzer.loader import LogLoader
from log_analyzer.processor import LogProcessor
from log_analyzer.protocols import Formatter, Saver
from log_analyzer.saver import ReportSaver
from log_analyzer.summarizer import LogSummarizer


class AppContainer:
    def __init__(self, config: AppConfig) -> None:
        self.config = config

    def create_formatter(self) -> Formatter:
        return FormatterFactory.create(self.config.format_type)

    def create_processor(self) -> LogProcessor:
        return LogProcessor(
            loader=LogLoader(self.config.input_path),
            summarizer=LogSummarizer(),
            formatter=self.create_formatter(),
        )

    def create_saver(self) -> Saver:
        return ReportSaver(self.config.output_path)

    def run(self) -> tuple[str, Path]:
        processor = self.create_processor()
        report = processor.process()
        saver = self.create_saver()
        path = saver.save(report)
        return report, path
