import pytest

from log_analyzer.log_analyzer.log_parser import LogParser
from log_analyzer.log_analyzer.settings import Config


@pytest.fixture
def sample_log_file(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text(
        """1.169.137.128 -  - [29/Jun/2017:03:50:23 +0300] "GET /api/v2/banner/7763463 HTTP/1.1" 200 1018 "-" "Configovod" "-" "1498697422-2118016444-4708-9752774" "712e90144abee9" 0.181
        invalid log line
        1.194.135.240 -  - [29/Jun/2017:03:50:23 +0300] "GET /api/v2/group/7786683/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28 HTTP/1.1" 200 22 "-" "python-requests/2.13.0" "-" "1498697423-3979856266-4708-9752782" "8a7741a54297568b" 0.061"""
    )
    return log_file


@pytest.fixture
def sample_config():
    return Config(
        ERROR_THRESHOLD=1,
    )


@pytest.fixture
def sample_config_threshold():
    return Config(
        ERROR_THRESHOLD=0,
    )


def test_log_parser(sample_log_file, sample_config):
    parser = LogParser(sample_log_file, 3, sample_config)
    parsed_data = list(parser.parse())

    assert len(parsed_data) == 2
    assert parser.unparsable_lines == 1
    assert parser.total_lines == 3

    assert parsed_data[0]["request"] == "GET /api/v2/banner/7763463 HTTP/1.1"
    assert parsed_data[0]["request_time"] == "0.181"


def test_error_threshold_exceeded(sample_log_file, sample_config_threshold):

    parser = LogParser(sample_log_file, 3, sample_config_threshold)

    with pytest.raises(RuntimeError) as exc_info:
        list(parser.parse())

    assert "Error threshold exceeded" in str(exc_info.value)
