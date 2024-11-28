from pathlib import Path

import structlog

logger = structlog.getLogger(__name__)


def count_lines_buffered(filepath: str, buffer_size: int = 1024 * 1024) -> int:
    with open(filepath, "r", encoding="utf-8") as file:
        buffer = file.read(buffer_size)
        lines = 0
        while buffer:
            lines += buffer.count("\n")
            buffer = file.read(buffer_size)
        return lines


def ensure_directory_exists(directory: str):
    try:
        logger.info(f"Creating/checking directory: {directory}")
        Path(directory).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(
            "Failed to create directory",
            directory=directory,
            error=str(e),
            exc_info=True,
        )
        raise RuntimeError(f"Failed to create directory {directory}: {e}")
