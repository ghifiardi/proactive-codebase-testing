"""Tests for reporter modules."""

import pytest
import json
from src.core.findings import AnalysisResult, Finding, FindingType, Severity, Location
from src.reporters.json_reporter import JSONReporter
from src.reporters.html_reporter import HTMLReporter
from src.reporters.sarif_reporter import SARIFReporter


@pytest.fixture
def sample_result():
    """Create sample analysis result."""
    # NOTE: The code_snippet below contains an intentional SQL injection pattern
    # for testing purposes. This is example vulnerable code that the analyzer
    # should detect, not actual production code with a vulnerability.
    finding = Finding(
        type=FindingType.SECURITY,
        severity=Severity.CRITICAL,
        message="SQL injection vulnerability",
        location=Location(file_path="test.py", line=10),
        remediation="Use parameterized queries",
        confidence=0.95,
        code_snippet="query = f'SELECT * FROM users WHERE id = {user_input}'",  # Test example: SQL injection pattern
    )

    return AnalysisResult(
        findings=[finding],
        files_analyzed=1,
        total_lines=50,
    )


def test_json_reporter(sample_result, tmp_path):
    """Test JSON reporter."""
    reporter = JSONReporter()
    json_str = reporter.generate(sample_result)

    # Verify it's valid JSON
    data = json.loads(json_str)
    assert "findings" in data
    assert len(data["findings"]) == 1

    # Test saving
    output_file = tmp_path / "report.json"
    reporter.save(sample_result, str(output_file))
    assert output_file.exists()


def test_html_reporter(sample_result, tmp_path):
    """Test HTML reporter."""
    reporter = HTMLReporter()
    html_str = reporter.generate(sample_result)

    # Verify it's HTML
    assert "<!DOCTYPE html>" in html_str
    assert "SQL injection" in html_str

    # Test saving
    output_file = tmp_path / "report.html"
    reporter.save(sample_result, str(output_file))
    assert output_file.exists()


def test_sarif_reporter(sample_result, tmp_path):
    """Test SARIF reporter."""
    reporter = SARIFReporter()
    sarif_str = reporter.generate(sample_result)

    # Verify it's valid SARIF JSON
    data = json.loads(sarif_str)
    assert "version" in data
    assert "runs" in data
    assert len(data["runs"][0]["results"]) == 1

    # Test saving
    output_file = tmp_path / "report.sarif"
    reporter.save(sample_result, str(output_file))
    assert output_file.exists()


def test_reporter_severity_filter(sample_result):
    """Test reporter severity filtering."""
    # Add a low severity finding
    low_finding = Finding(
        type=FindingType.QUALITY,
        severity=Severity.LOW,
        message="Code style issue",
        location=Location(file_path="test.py", line=20),
    )
    sample_result.findings.append(low_finding)

    # Filter to only high severity
    reporter = JSONReporter(min_severity=Severity.HIGH)
    json_str = reporter.generate(sample_result)
    data = json.loads(json_str)

    # Should only have the critical finding
    assert len(data["findings"]) == 1
    assert data["findings"][0]["severity"] == "critical"

