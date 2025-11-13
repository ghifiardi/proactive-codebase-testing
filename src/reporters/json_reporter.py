"""JSON reporter for structured output."""

import json
from typing import Optional
from ..core.findings import AnalysisResult, Severity
from .base import BaseReporter


class JSONReporter(BaseReporter):
    """Reporter that outputs JSON format."""

    def generate(self, result: AnalysisResult) -> str:
        """Generate JSON report.

        Args:
            result: Analysis result

        Returns:
            JSON string
        """
        filtered_result = self.filter_findings(result)
        return filtered_result.to_json()

    def save(self, result: AnalysisResult, output_path: str) -> None:
        """Save JSON report to file.

        Args:
            result: Analysis result
            output_path: Path to save report
        """
        json_str = self.generate(result)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)

