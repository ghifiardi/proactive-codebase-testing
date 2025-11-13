"""Tests for analyzer module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.analyzer import CodeAnalyzer
from src.core.findings import FindingType, Severity


@pytest.fixture
def mock_api_key():
    """Mock API key for testing."""
    return "sk-test-key"


@pytest.fixture
def analyzer(mock_api_key):
    """Create analyzer instance for testing."""
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": mock_api_key}):
        return CodeAnalyzer(api_key=mock_api_key)


def test_analyzer_initialization(analyzer):
    """Test analyzer initialization."""
    assert analyzer.api_key == "sk-test-key"
    assert analyzer.model == "claude-3-5-sonnet-20241022"


def test_analyzer_missing_api_key():
    """Test analyzer fails without API key."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not provided"):
            CodeAnalyzer()


@patch("src.core.analyzer.Anthropic")
def test_analyze_code_success(mock_anthropic, analyzer):
    """Test successful code analysis."""
    # Mock API response
    mock_response = MagicMock()
    mock_response.content = [
        MagicMock(
            text='{"findings": [{"type": "SECURITY", "severity": "critical", "line": 10, "message": "SQL injection", "remediation": "Use parameterized queries", "confidence": 0.95}]}'
        )
    ]

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_response
    mock_anthropic.return_value = mock_client
    analyzer.client = mock_client

    # NOTE: The code below contains an intentional SQL injection pattern for testing.
    # This is example vulnerable code that the analyzer should detect, not actual
    # production code. In production, use parameterized queries:
    # cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
    findings = analyzer.analyze_code(
        code="SELECT * FROM users WHERE id = {user_input}",  # Test example: SQL injection pattern
        language="python",
        file_name="test.py",
    )

    assert len(findings) == 1
    assert findings[0].type == FindingType.SECURITY
    assert findings[0].severity == Severity.CRITICAL
    assert findings[0].message == "SQL injection"


def test_analyze_code_empty(analyzer):
    """Test analysis with empty code."""
    findings = analyzer.analyze_code(code="", language="python")
    assert len(findings) == 0


def test_parse_finding(analyzer):
    """Test finding parsing."""
    finding_data = {
        "type": "SECURITY",
        "severity": "critical",
        "line": 42,
        "message": "Test finding",
        "remediation": "Fix it",
        "confidence": 0.9,
    }

    finding = analyzer._parse_finding(finding_data, "test.py")
    assert finding.type == FindingType.SECURITY
    assert finding.severity == Severity.CRITICAL
    assert finding.location.line == 42


def test_parse_api_response(analyzer):
    """Test API response parsing."""
    response = '{"findings": [{"type": "BUG", "severity": "high", "line": 5, "message": "Null pointer"}]}'
    findings = analyzer._parse_api_response(response, "test.py")

    assert len(findings) == 1
    assert findings[0].type == FindingType.BUG
    assert findings[0].severity == Severity.HIGH

