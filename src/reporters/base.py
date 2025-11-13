"""Base reporter class."""

from abc import ABC, abstractmethod
from typing import Optional
from ..core.findings import AnalysisResult, Severity


class BaseReporter(ABC):
    """Base class for all reporters."""

    def __init__(self, min_severity: Optional[Severity] = None):
        """Initialize reporter.

        Args:
            min_severity: Minimum severity to include (None = all)
        """
        self.min_severity = min_severity

    def filter_findings(self, result: AnalysisResult) -> AnalysisResult:
        """Filter findings by minimum severity.

        Args:
            result: Analysis result

        Returns:
            Filtered analysis result
        """
        if self.min_severity is None:
            return result

        # Severity order for comparison
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }

        min_level = severity_order.get(self.min_severity, 4)
        filtered = [
            f
            for f in result.findings
            if severity_order.get(f.severity, 4) <= min_level
        ]

        return AnalysisResult(
            findings=filtered,
            files_analyzed=result.files_analyzed,
            total_lines=result.total_lines,
            analysis_time_seconds=result.analysis_time_seconds,
            timestamp=result.timestamp,
            metadata=result.metadata,
        )

    @abstractmethod
    def generate(self, result: AnalysisResult) -> str:
        """Generate report.

        Args:
            result: Analysis result

        Returns:
            Report as string
        """
        pass

    @abstractmethod
    def save(self, result: AnalysisResult, output_path: str) -> None:
        """Save report to file.

        Args:
            result: Analysis result
            output_path: Path to save report
        """
        pass

