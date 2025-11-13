"""Command-line interface for code analyzer."""

import sys
import logging
from pathlib import Path
from typing import Optional
import typer

from ..core.analyzer import CodeAnalyzer
from ..core.parser import CodeParser
from ..core.findings import Severity
from ..reporters.json_reporter import JSONReporter
from ..reporters.html_reporter import HTMLReporter
from ..reporters.sarif_reporter import SARIFReporter

app = typer.Typer(help="Proactive Codebase Testing - AI-powered code analyzer")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Path to file or directory to analyze"),
    format: str = typer.Option("console", "--format", "-f", help="Output format: json, html, sarif, console"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    severity: Optional[str] = typer.Option(None, "--severity", "-s", help="Minimum severity: critical, high, medium, low"),
    fail_on_critical: bool = typer.Option(False, "--fail-on-critical", help="Exit with error code if critical findings found"),
    analysis_type: str = typer.Option("comprehensive", "--type", "-t", help="Analysis type: security, bugs, quality, comprehensive"),
):
    """Analyze code for security vulnerabilities, bugs, and quality issues."""
    try:
        typer.echo(f"Analyzing: {path}")

        # Initialize components
        parser = CodeParser()
        analyzer = CodeAnalyzer()

        # Analyze directory or file
        if Path(path).is_file():
            file_data = parser.analyze_file(path)
            if not file_data:
                typer.echo(f"Error: Could not analyze file {path}", err=True)
                sys.exit(1)

            findings = analyzer.analyze_code(
                code=file_data["content"],
                language=file_data["language"],
                file_name=file_data["path"],
                analysis_type=analysis_type,
            )

            from ..core.findings import AnalysisResult
            result = AnalysisResult(
                findings=findings,
                files_analyzed=1,
                total_lines=file_data["line_count"],
            )
        else:
            result = analyzer.analyze_directory(path, analysis_type=analysis_type, parser=parser)

        # Select reporter
        severity_enum = None
        if severity:
            severity_map = {
                "critical": Severity.CRITICAL,
                "high": Severity.HIGH,
                "medium": Severity.MEDIUM,
                "low": Severity.LOW,
            }
            severity_enum = severity_map.get(severity.lower())

        if format == "json":
            reporter = JSONReporter(min_severity=severity_enum)
        elif format == "html":
            reporter = HTMLReporter(min_severity=severity_enum)
        elif format == "sarif":
            reporter = SARIFReporter(min_severity=severity_enum)
        else:  # console
            reporter = None

        # Generate output
        if reporter:
            if output:
                reporter.save(result, output)
                typer.echo(f"Report saved to: {output}")
            else:
                typer.echo(reporter.generate(result))
        else:
            # Console output
            _print_console_report(result, severity_enum)

        # Check for critical findings
        if fail_on_critical:
            critical_count = len(result.get_findings_by_severity(Severity.CRITICAL))
            if critical_count > 0:
                typer.echo(f"Found {critical_count} critical findings!", err=True)
                sys.exit(1)

        typer.echo("✓ Analysis complete!")

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        logger.exception("Analysis failed")
        sys.exit(1)


def _print_console_report(result, min_severity: Optional[Severity] = None):
    """Print analysis results to console."""
    summary = result.get_summary()

    # Summary
    typer.echo("\n=== Analysis Summary ===")
    typer.echo(f"Total Findings: {summary['total_findings']}")
    typer.echo(f"Critical: {summary['findings_by_severity']['critical']}")
    typer.echo(f"High: {summary['findings_by_severity']['high']}")
    typer.echo(f"Medium: {summary['findings_by_severity']['medium']}")
    typer.echo(f"Low: {summary['findings_by_severity']['low']}")
    typer.echo(f"Info: {summary['findings_by_severity']['info']}")
    typer.echo(f"Files Analyzed: {summary['files_analyzed']}")
    typer.echo(f"Total Lines: {summary['total_lines']}")
    typer.echo(f"Analysis Time: {summary['analysis_time_seconds']:.2f}s")

    # Findings
    findings = result.findings
    if min_severity:
        severity_order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }
        min_level = severity_order.get(min_severity, 4)
        findings = [f for f in findings if severity_order.get(f.severity, 4) <= min_level]

    if findings:
        typer.echo("\n=== Findings ===")
        for finding in findings:
            typer.echo(f"\n[{finding.severity.value.upper()}] {finding.type.value.upper()}")
            typer.echo(f"  File: {finding.location.file_path}")
            if finding.location.line:
                typer.echo(f"  Line: {finding.location.line}")
            typer.echo(f"  Message: {finding.message}")
            if finding.remediation:
                typer.echo(f"  Remediation: {finding.remediation}")
    else:
        typer.echo("\n✓ No findings detected!")


@app.command()
def health():
    """Check if analyzer is properly configured."""
    try:
        analyzer = CodeAnalyzer()
        typer.echo("✓ Analyzer is properly configured")
        typer.echo(f"  Model: {analyzer.model}")
    except Exception as e:
        typer.echo(f"✗ Configuration error: {e}", err=True)
        sys.exit(1)


@app.command()
def version():
    """Show version information."""
    from .. import __version__
    typer.echo(f"Proactive Codebase Testing v{__version__}")


if __name__ == "__main__":
    app()

