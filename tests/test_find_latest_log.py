from datetime import datetime

import pytest

from app.log_utils import find_latest_log


@pytest.fixture
def setup_log_dir(tmp_path):
    log1 = tmp_path / "nginx-access-ui.log-20231127.gz"
    log2 = tmp_path / "nginx-access-ui.log-20231128.gz"
    log1.touch()
    log2.touch()
    return tmp_path


def test_find_latest_log(setup_log_dir):
    latest_log = find_latest_log(setup_log_dir)
    assert latest_log is not None
    assert latest_log.filename.endswith("nginx-access-ui.log-20231128.gz")
    assert latest_log.date == datetime(2023, 11, 28)
