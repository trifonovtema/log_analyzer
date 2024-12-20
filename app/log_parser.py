import gzip
import re
from pathlib import Path
from typing import Iterator

import structlog
from tqdm import tqdm

from app.models import LatestLog
from app.settings import Config

logger = structlog.getLogger(name=__name__)


def parse_log_file(
    latest_log_file: LatestLog, total_lines: int, config: Config
) -> Iterator[dict[str, str]]:
    logger.info(
        "Start parsing log file",
        latest_log_filename=latest_log_file.filename,
    )
    try:
        log_parser = LogParser(Path(latest_log_file.path), total_lines, config)
        log_entry = log_parser.parse()
        logger.info(
            "Log file successfully processed",
            latest_log_filename=latest_log_file.filename,
        )
        return log_entry
    except OSError as e:
        logger.error(
            "File operation failed",
            error=str(e),
            file_path=latest_log_file.path,
            exc_info=True,
        )
        raise
    except Exception as e:
        logger.error(
            "Unexpected error during log parsing",
            error=str(e),
            exc_info=True,
        )
        raise


class LogParser:
    LOG_PATTERN = re.compile(
        r"(?P<remote_addr>[\d\.]+)\s+"
        r"(?P<remote_user>-|\S+)\s+"
        r"(?P<http_x_real_ip>[\d\.]+|-)\s+"
        r"\[(?P<time_local>[^\]]+)\]\s+"
        r'"(?P<request>[^"]+)"\s+'
        r"(?P<status>\d+)\s+"
        r"(?P<body_bytes_sent>\d+|-)\s+"
        r'"(?P<http_referer>[^"]*|-)"\s+'
        r'"(?P<http_user_agent>[^"]*|-)"\s+'
        r'"(?P<http_x_forwarded_for>[^"]*|-)"\s+'
        r'"(?P<http_x_request_id>[^"]*|-)"\s+'
        r'"(?P<http_x_rb_user>[^"]*|-)"\s+'
        r"(?P<request_time>[\d\.]+)"
    )

    def __init__(self, filepath: Path, total_lines: int, final_config: Config):
        self.filepath = filepath
        self.unparsable_lines = 0
        self.total_lines = total_lines
        self.config = final_config
        self.file_opener = self.get_file_opener()

    def check_thresholds(self):
        error_ratio = self.unparsable_lines / self.total_lines
        logger.debug("Error ratio", error_ratio=error_ratio)
        if error_ratio > self.config.ERROR_THRESHOLD:
            logger.error(
                "Error threshold exceeded",
                unparsable_lines=self.unparsable_lines,
                total_lines=self.total_lines,
                error_ratio=error_ratio,
                error_threshold=self.config.ERROR_THRESHOLD,
            )
            raise RuntimeError(
                f"Error threshold exceeded: {error_ratio:.2%} (threshold: {self.config.ERROR_THRESHOLD:.2%})"
            )
        return True

    def get_file_opener(self):
        try:
            return (
                gzip.open(self.filepath, "rt", encoding="utf-8")
                if self.filepath.suffix == ".gz"
                else open(self.filepath, "r", encoding="utf-8")
            )
        except OSError as e:
            logger.error(
                "Failed to open log file",
                error=str(e),
                file_path=str(self.filepath),
                exc_info=True,
            )
            raise

    def parse(self) -> Iterator[dict[str, str]]:
        try:
            with self.file_opener as log_file:
                with tqdm(
                    total=self.total_lines,
                    desc="Processing log file",
                    unit="lines",
                ) as progress_bar:
                    for line in log_file:
                        progress_bar.update(1)
                        if not line.strip():
                            continue
                        match = self.LOG_PATTERN.match(line.strip())
                        if not match:
                            self.unparsable_lines += 1
                            logger.debug("Unparsable line", line=line.strip())
                            self.check_thresholds()
                            continue
                        parsed = match.groupdict()
                        if parsed.get("request") == "0":
                            self.unparsable_lines += 1
                            logger.debug("Invalid request detected", request="0")
                            self.check_thresholds()
                            continue
                        yield parsed

        except Exception as e:
            logger.error(
                "Error occurred during log file parsing",
                error=str(e),
                file_path=str(self.filepath),
                exc_info=True,
            )
            raise
