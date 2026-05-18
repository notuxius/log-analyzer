from pathlib import Path

from log_analyzer.config import AppConfig
from log_analyzer.formatter import FormatterFactory
from log_analyzer.loader import LogLoader
from log_analyzer.logger import AppLogger
from log_analyzer.processor import LogProcessor
from log_analyzer.protocols import Formatter, Saver
from log_analyzer.saver import ReportSaver
from log_analyzer.summarizer import LogSummarizer


class AppContainer:
    def __init__(self, config: AppConfig, logger: AppLogger) -> None:
        self.config = config
        self.logger = logger

    def create_formatter(self) -> Formatter:
        return FormatterFactory.create(self.config.format_type)

    def create_processor(self) -> LogProcessor:
        return LogProcessor(
            loader=self.create_loader(),
            summarizer=self.create_summarizer(),
            formatter=self.create_formatter(),
        )

    def create_loader(self) -> LogLoader:
        return LogLoader(self.config.input_path, logger=self.logger)

    def create_summarizer(self) -> LogSummarizer:
        return LogSummarizer()

    def create_saver(self) -> Saver:
        return ReportSaver(self.config.output_path)

    def run(self) -> tuple[str, Path]:
        processor = self.create_processor()
        report = processor.process()
        saver = self.create_saver()
        path = saver.save(report)
        return report, path
