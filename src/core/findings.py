"""Data structures for analysis findings."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime


class FindingType(str, Enum):
    """Types of findings that can be detected."""

    SECURITY = "security"
    BUG = "bug"
    QUALITY = "quality"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"


class Severity(str, Enum):
    """Severity levels for findings."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class Location:
    """Location of a finding in source code."""

    file_path: str
    line: Optional[int] = None
    column: Optional[int] = None
    end_line: Optional[int] = None
    end_column: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "file_path": self.file_path,
            "line": self.line,
            "column": self.column,
            "end_line": self.end_line,
            "end_column": self.end_column,
        }


@dataclass
class Finding:
    """A single finding from code analysis."""

    type: FindingType
    severity: Severity
    message: str
    location: Location
    remediation: Optional[str] = None
    confidence: float = 1.0
    code_snippet: Optional[str] = None
    rule_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "message": self.message,
            "location": self.location.to_dict(),
            "remediation": self.remediation,
            "confidence": self.confidence,
            "code_snippet": self.code_snippet,
            "rule_id": self.rule_id,
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        import json

        return json.dumps(self.to_dict(), indent=2)


@dataclass
class AnalysisResult:
    """Result of analyzing code."""

    findings: List[Finding] = field(default_factory=list)
    files_analyzed: int = 0
    total_lines: int = 0
    analysis_time_seconds: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_findings_by_severity(self, severity: Severity) -> List[Finding]:
        """Get findings filtered by severity."""
        return [f for f in self.findings if f.severity == severity]

    def get_findings_by_type(self, finding_type: FindingType) -> List[Finding]:
        """Get findings filtered by type."""
        return [f for f in self.findings if f.type == finding_type]

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        findings_by_severity = {}
        for severity in Severity:
            findings_by_severity[severity.value] = len(
                self.get_findings_by_severity(severity)
            )

        findings_by_type = {}
        for finding_type in FindingType:
            findings_by_type[finding_type.value] = len(
                self.get_findings_by_type(finding_type)
            )

        return {
            "total_findings": len(self.findings),
            "findings_by_severity": findings_by_severity,
            "findings_by_type": findings_by_type,
            "files_analyzed": self.files_analyzed,
            "total_lines": self.total_lines,
            "analysis_time_seconds": self.analysis_time_seconds,
            "timestamp": self.timestamp.isoformat(),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.get_summary(),
            "metadata": self.metadata,
        }

    def to_json(self) -> str:
        """Convert to JSON string."""
        import json

        return json.dumps(self.to_dict(), indent=2)

