"""Monitoring and metrics collection."""

import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class MetricsCollector:
    """Collect and track metrics."""

    def __init__(self):
        self.metrics = defaultdict(list)
        self.counters = defaultdict(int)
        self.start_time = time.time()

    def record_timing(self, metric_name: str, duration: float, tags: Optional[Dict[str, str]] = None):
        """Record timing metric."""
        self.metrics[metric_name].append({
            "value": duration,
            "timestamp": datetime.utcnow().isoformat(),
            "tags": tags or {},
        })

    def increment_counter(self, counter_name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment counter metric."""
        key = f"{counter_name}:{tags or {}}"
        self.counters[key] += value

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        summary = {
            "uptime_seconds": time.time() - self.start_time,
            "counters": dict(self.counters),
            "timings": {},
        }

        # Calculate timing statistics
        for metric_name, values in self.metrics.items():
            if values:
                durations = [v["value"] for v in values]
                summary["timings"][metric_name] = {
                    "count": len(durations),
                    "min": min(durations),
                    "max": max(durations),
                    "avg": sum(durations) / len(durations),
                    "p95": sorted(durations)[int(len(durations) * 0.95)] if durations else 0,
                }

        return summary

    def reset(self):
        """Reset all metrics."""
        self.metrics.clear()
        self.counters.clear()
        self.start_time = time.time()


# Global metrics collector
metrics = MetricsCollector()


class PerformanceMonitor:
    """Context manager for performance monitoring."""

    def __init__(self, metric_name: str, tags: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.tags = tags
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        metrics.record_timing(self.metric_name, duration, self.tags)
        return False


def log_analysis_metrics(result, analysis_type: str, language: str):
    """Log metrics for analysis operation."""
    metrics.increment_counter("analyses_total", tags={"type": analysis_type, "language": language})
    metrics.increment_counter("findings_total", value=len(result.findings))
    metrics.increment_counter("files_analyzed", value=result.files_analyzed)

    # Record timing
    metrics.record_timing(
        "analysis_duration",
        result.analysis_time_seconds,
        tags={"type": analysis_type, "language": language},
    )

    # Record findings by severity
    for severity in ["critical", "high", "medium", "low", "info"]:
        count = len([f for f in result.findings if f.severity.value == severity])
        if count > 0:
            metrics.increment_counter(
                f"findings_{severity}",
                value=count,
                tags={"type": analysis_type},
            )

