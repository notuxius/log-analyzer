import argparse
import logging
from pathlib import Path

from log_analyzer.config import AppConfig
from log_analyzer.container import AppContainer

APP_NAME = "log-analyzer"
__version__ = "1.0.0"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze logs and generate a report.")
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
        choices=["txt", "json"],
        help="Output format: text or json.",
    )
    parser.add_argument(
        "--print-report",
        action="store_true",
        help="Print report to console.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {__version__}",
    )
    return parser.parse_args()


def main() -> int:
    configure_logging()

    try:
        args = parse_args()
        input_path = Path(args.input)
        output_path = Path(args.output)

        if not output_path.suffix:
            output_path = output_path.with_suffix(f".{args.format}")

        config = AppConfig(
            input_path=input_path, output_path=output_path, format_type=args.format
        )

        container = AppContainer(config)

        log_report, saved_path = container.run()

        if args.print_report:
            print(log_report)
            print()

        logging.info("Report saved to: %s", saved_path)
        return 0
    except (FileNotFoundError, ValueError) as error:
        logging.error("%s", error)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
