"""API routes for code analysis."""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, status

from ..core.analyzer import CodeAnalyzer
from ..core.findings import Finding
from .models import (
    AnalyzeRequest,
    AnalyzeResponse,
    HealthResponse,
    LanguagesResponse,
    FindingResponse,
    StatsResponse,
)
from .. import __version__

logger = logging.getLogger(__name__)

router = APIRouter()

# Supported languages
SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "typescript",
    "go",
    "java",
    "c",
    "cpp",
    "csharp",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "rust",
    "bash",
    "html",
    "css",
    "json",
    "yaml",
    "sql",
]


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest):
    """Analyze code for security vulnerabilities, bugs, and quality issues."""
    from ..core.monitoring import PerformanceMonitor, log_analysis_metrics
        
    try:
        with PerformanceMonitor("api_analyze", tags={"language": request.language, "type": request.analysis_type}):
            analyzer = CodeAnalyzer()

            findings = analyzer.analyze_code(
                code=request.code,
                language=request.language,
                file_name=request.file_name or "unknown",
                analysis_type=request.analysis_type,
            )

            # Convert findings to response format
            finding_responses = [
                FindingResponse(
                    type=f.type.value,
                    severity=f.severity.value,
                    message=f.message,
                    location=f.location.to_dict(),
                    remediation=f.remediation,
                    confidence=f.confidence,
                    code_snippet=f.code_snippet,
                    rule_id=f.rule_id,
                )
                for f in findings
            ]

            # Calculate statistics
            findings_by_severity = {
                "critical": len([f for f in findings if f.severity.value == "critical"]),
                "high": len([f for f in findings if f.severity.value == "high"]),
                "medium": len([f for f in findings if f.severity.value == "medium"]),
                "low": len([f for f in findings if f.severity.value == "low"]),
                "info": len([f for f in findings if f.severity.value == "info"]),
            }

            result = AnalyzeResponse(
                findings=finding_responses,
                files_analyzed=1,
                total_lines=len(request.code.splitlines()),
                findings_by_severity=findings_by_severity,
                success=True,
            )
            
            # Log metrics
            from ..core.findings import AnalysisResult
            analysis_result = AnalysisResult(
                findings=findings,  # Use actual findings
                files_analyzed=1,
                total_lines=len(request.code.splitlines()),
            )
            
            log_analysis_metrics(analysis_result, request.analysis_type, request.language)
            
            return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("Error analyzing code")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}",
        )


@router.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", version=__version__)


@router.get("/api/languages", response_model=LanguagesResponse)
async def get_languages():
    """Get list of supported programming languages."""
    return LanguagesResponse(languages=SUPPORTED_LANGUAGES)


@router.get("/api/stats", response_model=StatsResponse)
async def get_stats():
    """Get analysis statistics (placeholder for future implementation)."""
    return StatsResponse(
        total_analyses=0,
        total_findings=0,
        findings_by_severity={},
    )

