from pathlib import Path
from typing import Iterable, Iterator

import click
import structlog

from .log_parser import LogParser, parse_log_file
from .log_processing import process_log_data
from .log_utils import get_log_file
from .models import LatestLog
from .report import generate_report, render_report
from .settings import Config
from .setup_logs import setup_logging
from .utils import count_lines_buffered

logger = structlog.get_logger(__name__)


def load_config(config_path: str) -> Config:
    """Load and validate the configuration."""
    final_config = Config.from_file(config_path)
    Config.validate(final_config)
    setup_logging(log_file=final_config.LOG_FILE)
    logger.info("Config loaded", config=final_config)
    return final_config


@click.command()
@click.option(
    "--config",
    default="./sample_config.json",
    help="Path to the configuration file (default: ./sample_config.json).",
)
def main(config):
    try:
        final_config = load_config(config)
        logger.info("Application started")

        latest_log_file, report_path = get_log_file(final_config)
        if not latest_log_file:
            return

        total_lines = count_lines_buffered(latest_log_file.filename)
        logger.info("Total lines", total_lines=total_lines)
        if total_lines == 0:
            logger.warning("Log file contains no lines to process")
            return

        log_entry = parse_log_file(latest_log_file, total_lines, final_config)

        generate_report(log_entry, report_path, final_config)

    except KeyboardInterrupt:
        logger.warning("Application interrupted by user (Ctrl+C)")
    except Exception as e:
        logger.error(
            "Unexpected error occurred",
            error=str(e),
            exc_info=True,
        )
        raise
    finally:
        logger.info("Application terminated")


if __name__ == "__main__":
    main()
