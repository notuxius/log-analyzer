import argparse

from log_analyzer.config import AppConfig
from log_analyzer.config_loader import ConfigLoader
from log_analyzer.constants import APP_NAME, APP_VERSION
from log_analyzer.container import AppContainer
from log_analyzer.exceptions import LogAnalyzerError
from log_analyzer.logger import AppLogger


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze logs and generate a report.")
    parser.add_argument(
        "--config",
        help="Path to JSON config file.",
    )
    parser.add_argument(
        "--input",
        default="logs/sample.txt",
        help="Path to input log file.",
    )
    parser.add_argument(
        "--output",
        default="reports/log_report",
        help="Path to output report file.",
    )
    parser.add_argument(
        "--format",
        default="txt",
        choices=["txt", "json", "csv"],
        help="Output format: text or json.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        type=str.upper,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational logs.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose debug logging.",
    )
    parser.add_argument(
        "--print-report",
        action="store_true",
        help="Print report to console.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.quiet:
        log_level = "ERROR"
    elif args.verbose:
        log_level = "DEBUG"
    else:
        log_level = args.log_level

    logger = AppLogger(log_level)
    logger.debug("Starting log analysis")

    try:
        if args.config:
            config = ConfigLoader(args.config).load()
        else:
            config = AppConfig.create(
                input_path=args.input, output_path=args.output, format_type=args.format
            )

        container = AppContainer(config, logger)

        log_report, saved_path = container.run()

        if args.print_report:
            print(log_report)
            print()

        logger.info("Report saved to: %s", saved_path)
        return 0
    except LogAnalyzerError as error:
        logger.error("%s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
