"""Pydantic models for API requests and responses."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from ..core.findings import FindingType, Severity


class AnalyzeRequest(BaseModel):
    """Request model for code analysis."""

    code: str = Field(..., description="Source code to analyze")
    language: str = Field(..., description="Programming language")
    analysis_type: str = Field(
        default="comprehensive",
        description="Type of analysis: security, bugs, quality, comprehensive",
    )
    file_name: Optional[str] = Field(
        default="unknown", description="Name of the file being analyzed"
    )

    class Config:
        json_schema_extra = {
            "example": {
                # NOTE: This example shows vulnerable code that the analyzer should detect.
                # In production, use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
                "code": "SELECT * FROM users WHERE id = {user_input}",  # Example: SQL injection pattern
                "language": "python",
                "analysis_type": "security",
                "file_name": "app.py",
            }
        }


class FindingResponse(BaseModel):
    """Response model for a single finding."""

    type: str
    severity: str
    message: str
    location: Dict[str, Any]
    remediation: Optional[str] = None
    confidence: float
    code_snippet: Optional[str] = None
    rule_id: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """Response model for analysis results."""

    findings: List[FindingResponse]
    files_analyzed: int
    total_lines: int
    findings_by_severity: Dict[str, int]
    success: bool = True
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str = "ok"
    version: str = "0.1.0"


class LanguagesResponse(BaseModel):
    """Response model for supported languages."""

    languages: List[str]


class StatsResponse(BaseModel):
    """Response model for statistics."""

    total_analyses: int = 0
    total_findings: int = 0
    findings_by_severity: Dict[str, int] = {}

