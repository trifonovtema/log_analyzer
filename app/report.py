import json
import os
from string import Template
from typing import Iterable, Iterator

import structlog

from app.log_processing import process_log_data
from app.settings import Config

logger = structlog.get_logger(__name__)


def generate_report(
    log_entry: Iterator[dict[str, str]], report_path: str, config: Config
) -> None:
    report_data = process_log_data(log_entry, config.REPORT_SIZE)
    logger.info("Report Size", report_size=len(report_data))
    render_report(report_data, report_path)
    logger.info("Report successfully generated", report_path=report_path)


def render_report(report_data, output_path, template_path="./app/report_template.html"):
    try:
        with open(template_path, "r", encoding="utf-8") as template_file:
            template_content = template_file.read()
        template = Template(template_content)
        report_html = template.safe_substitute(table_json=json.dumps(report_data))

        temp_path = f"{output_path}.incomplete"

        with open(temp_path, "w", encoding="utf-8") as output_file:
            output_file.write(report_html)

        os.rename(temp_path, output_path)
        logger.info("Report saved", report_path=output_path)

    except Exception as e:
        logger.error(
            "Failed to render report",
            error=str(e),
            report_path=output_path,
            exc_info=True,
        )
        raise
