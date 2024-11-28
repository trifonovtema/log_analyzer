import os
import re
from datetime import datetime
from pathlib import Path

import structlog

from app.models import LatestLog
from app.settings import Config

logger = structlog.get_logger(__name__)

LOG_NAME_PATTERN = r"nginx-access-ui\.log-(\d{8})(\.gz)?$"


def find_latest_log(log_dir: str) -> LatestLog | None:
    log_pattern = re.compile(LOG_NAME_PATTERN)
    latest_log = None
    for filename in os.listdir(log_dir):
        match = log_pattern.match(filename)
        if match:
            log_date = datetime.strptime(match.group(1), "%Y%m%d")
            log_path = os.path.join(log_dir, filename)
            if latest_log is None or log_date > latest_log.date:
                latest_log = LatestLog(
                    filename=log_path, date=log_date, path=Path(log_path)
                )
    if latest_log is None:
        logger.info(
            "No log found for",
            log_name_pattern=LOG_NAME_PATTERN,
        )
    else:
        logger.info(
            "Latest log file found",
            latest_log_file=latest_log.path,
        )
    return latest_log


def get_log_file(config: Config):
    latest_log_file = find_latest_log(config.LOG_DIR)
    if not latest_log_file:
        logger.info("No log files found", log_dir=config.LOG_DIR)
        return None, None

    report_name = f"report-{latest_log_file.date.strftime('%Y.%m.%d')}.html"
    report_path = os.path.join(config.REPORT_DIR, report_name)

    if os.path.exists(report_path):
        logger.info(
            "Report for the last date already exists",
            report_path=report_path,
        )
        return None, None

    return latest_log_file, report_path
