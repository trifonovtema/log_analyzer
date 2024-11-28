import pytest

from log_analyzer.log_analyzer.report import render_report


@pytest.fixture
def report_template(tmp_path):
    template = tmp_path / "report_template.html"
    template.write_text("<html><body>${table_json}</body></html>")
    return template


@pytest.fixture
def output_report_path(tmp_path):
    return tmp_path / "report.html"


def test_render_report(report_template, output_report_path):
    report_data = [
        {"url": "/url1", "count": 10, "time_sum": 12.34},
        {"url": "/url2", "count": 5, "time_sum": 7.89},
    ]
    render_report(report_data, output_report_path, template_path=report_template)

    # Проверяем, что отчет был создан
    assert output_report_path.exists()

    # Проверяем содержимое отчета
    content = output_report_path.read_text()
    assert "/url1" in content
    assert "/url2" in content
    assert "12.34" in content
    assert "7.89" in content
