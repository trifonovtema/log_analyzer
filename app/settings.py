import json
import os
from dataclasses import dataclass

import structlog

from app.utils import ensure_directory_exists

logger = structlog.get_logger(__name__)


@dataclass
class Config:
    LOG_DIR: str = "/app/logs"
    REPORT_DIR: str = "/app/reports"
    REPORT_SIZE: int = 1000
    ERROR_THRESHOLD: float = 0.1
    LOG_FILE: str | None = "/app/output_logs/app.log"

    @classmethod
    def from_file(cls, filepath: str) -> "Config":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found at {filepath}")

        with open(filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Failed to parse JSON config file at {filepath}: {e}",
                )

        return cls(**data)

    @classmethod
    def validate(cls, config: "Config"):
        if not os.path.isdir(config.LOG_DIR):
            logger.error(
                "Log directory does not exist",
                log_rid=config.LOG_DIR,
            )
            raise ValueError(f"Log directory does not exist: {config.LOG_DIR}")
        if not os.path.isdir(config.REPORT_DIR):
            try:
                ensure_directory_exists(config.REPORT_DIR)
            except Exception as e:
                logger.error(
                    "Report directory does not exist",
                    report_dir=config.REPORT_DIR,
                    error=e,
                )
                raise ValueError(
                    f"Report directory does not exist: {config.REPORT_DIR}"
                )
        if config.REPORT_SIZE <= 0:
            logger.error(
                "Report size must be a positive integer", report_size=config.REPORT_SIZE
            )
            raise ValueError("Report size must be a positive integer")
        if config.LOG_FILE and not os.path.isdir(
            os.path.dirname(config.LOG_FILE),
        ):
            try:
                ensure_directory_exists(os.path.dirname(config.LOG_FILE))
            except Exception as e:
                logger.error(
                    "Log file directory does not exist",
                    log_file_dir=os.path.dirname(config.LOG_FILE),
                    exc_info=True,
                    error=e,
                )
                raise ValueError(
                    f"Log file directory does not exist: {os.path.dirname(config.LOG_FILE)}",
                )
        if not (0 <= config.ERROR_THRESHOLD <= 1):
            logger.error(
                "Error threshold must be between 0 and 1",
                error_threshold=config.ERROR_THRESHOLD,
            )
            raise ValueError("Error threshold must be between 0 and 1")
