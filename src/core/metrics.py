"""Metrics collection for observability."""

import time
from typing import Dict, List
from collections import defaultdict


class MetricsCollector:
    """Collects and exposes application metrics."""

    def __init__(self) -> None:
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.request_latencies: Dict[str, List[float]] = defaultdict(list)

    def record_request(self, path: str, duration: float) -> None:
        """Record a request's path and duration in seconds."""
        self.request_counts[path] += 1
        self.request_latencies[path].append(duration)

    def get_metrics(self) -> Dict:
        """Return a summary of all metrics."""
        summary = {}
        for path, count in self.request_counts.items():
            latencies = self.request_latencies[path]
            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
            summary[path] = {
                "count": count,
                "avg_latency_ms": round(avg_latency * 1000, 2)
            }
        return summary