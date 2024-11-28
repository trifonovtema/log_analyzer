import json
import os
from dataclasses import dataclass

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class Config:
    LOG_DIR: str = "/log_analyzer/logs"
    REPORT_DIR: str = "/log_analyzer/reports"
    REPORT_SIZE: int = 1000
    ERROR_THRESHOLD: float = 0.1
    LOG_FILE: str | None = "/log_analyzer/output_logs/log_analyzer.log"

    @classmethod
    def from_file(cls, filepath: str) -> "Config":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found at {filepath}")

        with open(filepath, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse JSON config file at {filepath}: {e}")

        return cls(**data)

    @classmethod
    def validate(cls, config: "Config"):
        if not os.path.isdir(config.REPORT_DIR):
            raise ValueError(f"Report directory does not exist: {config.REPORT_DIR}")
        if config.REPORT_SIZE <= 0:
            raise ValueError("Report size must be a positive integer")
        if not (0 <= config.ERROR_THRESHOLD <= 1):
            raise ValueError("Error threshold must be between 0 and 1")
