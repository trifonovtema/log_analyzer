import logging
from logging.handlers import RotatingFileHandler

import structlog


def setup_logging(log_file=None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=(
            [RotatingFileHandler(log_file, maxBytes=10**6, backupCount=3)]
            if log_file
            else [logging.StreamHandler()]
        ),
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
