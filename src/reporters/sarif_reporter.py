"""SARIF reporter for GitHub integration."""

import json
from datetime import datetime
from typing import Optional
from ..core.findings import AnalysisResult, Severity, FindingType
from .base import BaseReporter


class SARIFReporter(BaseReporter):
    """Reporter that outputs SARIF format for GitHub."""

    def _severity_to_sarif(self, severity: Severity) -> str:
        """Convert severity to SARIF level.

        Args:
            severity: Finding severity

        Returns:
            SARIF level string
        """
        mapping = {
            Severity.CRITICAL: "error",
            Severity.HIGH: "error",
            Severity.MEDIUM: "warning",
            Severity.LOW: "note",
            Severity.INFO: "note",
        }
        return mapping.get(severity, "warning")

    def _type_to_rule_id(self, finding_type: FindingType) -> str:
        """Convert finding type to rule ID.

        Args:
            finding_type: Finding type

        Returns:
            Rule ID string
        """
        return finding_type.value.upper()

    def generate(self, result: AnalysisResult) -> str:
        """Generate SARIF report.

        Args:
            result: Analysis result

        Returns:
            SARIF JSON string
        """
        filtered_result = self.filter_findings(result)

        # Build SARIF structure
        sarif = {
            "version": "2.1.0",
            "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Proactive Codebase Testing",
                            "version": "0.1.0",
                            "informationUri": "https://github.com/yourname/proactive-codebase-testing",
                            "rules": [],
                        }
                    },
                    "results": [],
                }
            ],
        }

        # Add rules
        rule_ids = set()
        for finding in filtered_result.findings:
            rule_id = self._type_to_rule_id(finding.type)
            if rule_id not in rule_ids:
                sarif["runs"][0]["tool"]["driver"]["rules"].append(
                    {
                        "id": rule_id,
                        "name": finding.type.value.title(),
                        "shortDescription": {"text": finding.type.value.title()},
                    }
                )
                rule_ids.add(rule_id)

        # Add results
        for finding in filtered_result.findings:
            result_item = {
                "ruleId": self._type_to_rule_id(finding.type),
                "level": self._severity_to_sarif(finding.severity),
                "message": {"text": finding.message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": finding.location.file_path.replace("\\", "/")
                            },
                            "region": {},
                        }
                    }
                ],
            }

            # Add line information
            if finding.location.line:
                result_item["locations"][0]["physicalLocation"]["region"][
                    "startLine"
                ] = finding.location.line
                if finding.location.end_line:
                    result_item["locations"][0]["physicalLocation"]["region"][
                        "endLine"
                    ] = finding.location.end_line

            # Add code snippet
            if finding.code_snippet:
                result_item["locations"][0]["physicalLocation"]["region"][
                    "snippet"
                ] = {"text": finding.code_snippet}

            sarif["runs"][0]["results"].append(result_item)

        return json.dumps(sarif, indent=2)

    def save(self, result: AnalysisResult, output_path: str) -> None:
        """Save SARIF report to file.

        Args:
            result: Analysis result
            output_path: Path to save report
        """
        sarif_str = self.generate(result)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(sarif_str)

