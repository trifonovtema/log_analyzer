from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class LatestLog:
    filename: str
    date: datetime
    path: Path


@dataclass
class UrlStats:
    count: int = 0
    time_sum: float = 0
    time_max: float = 0
    times: list[float] = field(default_factory=list)
    time_avg:float=0
    time_med:float=0
