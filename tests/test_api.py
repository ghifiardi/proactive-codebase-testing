"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.server import app
from unittest.mock import patch, MagicMock
from src.core.findings import Finding, FindingType, Severity, Location

client = TestClient(app)


@patch("src.api.routes.CodeAnalyzer")
def test_analyze_endpoint(mock_analyzer_class):
    """Test /api/analyze endpoint."""
    # Mock analyzer
    mock_analyzer = MagicMock()
    mock_finding = Finding(
        type=FindingType.SECURITY,
        severity=Severity.CRITICAL,
        message="SQL injection",
        location=Location(file_path="test.py", line=10),
        remediation="Use parameterized queries",
    )
    mock_analyzer.analyze_code.return_value = [mock_finding]
    mock_analyzer_class.return_value = mock_analyzer

    # NOTE: The code below contains an intentional SQL injection pattern for testing.
    # This is example vulnerable code that the analyzer should detect, not actual
    # production code. In production, use parameterized queries.
    response = client.post(
        "/api/analyze",
        json={
            "code": "SELECT * FROM users WHERE id = user_input",  # Test example: SQL injection pattern
            "language": "python",
            "analysis_type": "security",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["findings"]) == 1
    assert data["findings"][0]["severity"] == "critical"


def test_health_endpoint():
    """Test /api/health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_languages_endpoint():
    """Test /api/languages endpoint."""
    response = client.get("/api/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert "python" in data["languages"]


def test_stats_endpoint():
    """Test /api/stats endpoint."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_analyses" in data


def test_analyze_endpoint_invalid_request():
    """Test /api/analyze with invalid request."""
    response = client.post(
        "/api/analyze",
        json={
            "code": "",  # Missing required fields
        },
    )
    assert response.status_code == 422  # Validation error

