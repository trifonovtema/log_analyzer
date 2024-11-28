from statistics import median
from typing import Iterable

from .models import UrlStats


def calculate_report_data(
    url_stats: dict[str, UrlStats],
    total_requests: int,
    total_request_time: float,
) -> list[dict]:
    report_data = []
    for url, stats in url_stats.items():
        stats.time_avg = stats.time_sum / stats.count
        stats.time_med = median(stats.times)
        report_data.append(
            {
                "url": url,
                "count": round(stats.count, 3),
                "count_perc": round(stats.count / total_requests * 100, 3),
                "time_sum": round(stats.time_sum, 3),
                "time_perc": round(stats.time_sum / total_request_time * 100, 3),
                "time_avg": round(stats.time_avg, 3),
                "time_max": round(stats.time_max, 3),
                "time_med": round(stats.time_med, 3),
            }
        )
    return report_data


def process_log_data(
    log_entries: Iterable[dict[str, str]],
    report_size: int,
):
    url_stats: dict[str, UrlStats] = {}
    total_requests = 0
    total_request_time = 0.0

    for entry in log_entries:
        if entry is None:
            continue

        request = entry.get("request", "")
        request_parts = request.split(" ")

        url = request_parts[1]
        request_time = float(entry["request_time"])

        if url not in url_stats:
            url_stats[url] = UrlStats()

        stats = url_stats[url]
        stats.count += 1
        stats.time_sum += request_time
        stats.time_max = max(stats.time_max, request_time)
        stats.times.append(request_time)

        total_requests += 1
        total_request_time += request_time

    report_data = calculate_report_data(url_stats, total_requests, total_request_time)

    return sorted(report_data, key=lambda x: x["time_sum"], reverse=True)[:report_size]
