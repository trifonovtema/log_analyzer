import click
import structlog

from app.log_parser import parse_log_file
from app.log_utils import get_log_file
from app.report import generate_report
from app.settings import Config
from app.setup_logs import setup_logging, setup_temporary_logging
from app.utils import count_lines_buffered

setup_temporary_logging()
logger = structlog.get_logger(__name__)


def load_config(config_path: str) -> Config:
    """Load and validate the configuration."""
    logger.info("Config loading started")
    final_config = Config.from_file(config_path)
    logger.info("Loaded config", config=final_config)
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
    finally:
        logger.info("Application terminated")


if __name__ == "__main__":
    main()
