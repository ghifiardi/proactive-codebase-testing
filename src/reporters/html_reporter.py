"""HTML reporter for visual dashboard."""

from typing import Optional
from jinja2 import Template
from ..core.findings import AnalysisResult, Severity
from .base import BaseReporter

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Analysis Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-card h3 { color: #666; font-size: 0.9em; margin-bottom: 10px; }
        .stat-card .value { font-size: 2em; font-weight: bold; }
        .critical { color: #dc3545; }
        .high { color: #fd7e14; }
        .medium { color: #ffc107; }
        .low { color: #17a2b8; }
        .info { color: #6c757d; }
        .findings {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .finding {
            border-left: 4px solid;
            padding: 15px;
            margin-bottom: 15px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .finding.critical { border-color: #dc3545; }
        .finding.high { border-color: #fd7e14; }
        .finding.medium { border-color: #ffc107; }
        .finding.low { border-color: #17a2b8; }
        .finding.info { border-color: #6c757d; }
        .finding-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .finding-title { font-weight: bold; font-size: 1.1em; }
        .finding-severity {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .finding-location { color: #666; font-size: 0.9em; margin: 5px 0; }
        .finding-message { margin: 10px 0; }
        .finding-remediation {
            background: #e7f3ff;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            border-left: 3px solid #2196F3;
        }
        .finding-remediation strong { color: #1976D2; }
        .code-snippet {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            margin: 10px 0;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        .no-findings {
            text-align: center;
            padding: 40px;
            color: #28a745;
            font-size: 1.2em;
        }
        .timestamp { color: rgba(255,255,255,0.8); font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Code Analysis Report</h1>
            <div class="timestamp">Generated: {{ timestamp }}</div>
        </header>

        <div class="summary">
            <div class="stat-card">
                <h3>Total Findings</h3>
                <div class="value">{{ total_findings }}</div>
            </div>
            <div class="stat-card">
                <h3>Critical</h3>
                <div class="value critical">{{ critical_count }}</div>
            </div>
            <div class="stat-card">
                <h3>High</h3>
                <div class="value high">{{ high_count }}</div>
            </div>
            <div class="stat-card">
                <h3>Medium</h3>
                <div class="value medium">{{ medium_count }}</div>
            </div>
            <div class="stat-card">
                <h3>Files Analyzed</h3>
                <div class="value">{{ files_analyzed }}</div>
            </div>
            <div class="stat-card">
                <h3>Total Lines</h3>
                <div class="value">{{ total_lines }}</div>
            </div>
        </div>

        <div class="findings">
            <h2>Findings</h2>
            {% if findings %}
                {% for finding in findings %}
                <div class="finding {{ finding.severity }}">
                    <div class="finding-header">
                        <div class="finding-title">{{ finding.type }}: {{ finding.message }}</div>
                        <span class="finding-severity {{ finding.severity }}">{{ finding.severity }}</span>
                    </div>
                    <div class="finding-location">
                        📁 {{ finding.location.file_path }}
                        {% if finding.location.line %}
                            (Line {{ finding.location.line }})
                        {% endif %}
                    </div>
                    {% if finding.code_snippet %}
                    <div class="code-snippet">{{ finding.code_snippet }}</div>
                    {% endif %}
                    {% if finding.remediation %}
                    <div class="finding-remediation">
                        <strong>💡 Remediation:</strong> {{ finding.remediation }}
                    </div>
                    {% endif %}
                </div>
                {% endfor %}
            {% else %}
                <div class="no-findings">
                    ✅ No findings detected! Your code looks good.
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""


class HTMLReporter(BaseReporter):
    """Reporter that outputs HTML format."""

    def generate(self, result: AnalysisResult) -> str:
        """Generate HTML report.

        Args:
            result: Analysis result

        Returns:
            HTML string
        """
        filtered_result = self.filter_findings(result)
        summary = filtered_result.get_summary()

        template = Template(HTML_TEMPLATE)
        return template.render(
            timestamp=filtered_result.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
            total_findings=summary["total_findings"],
            critical_count=summary["findings_by_severity"]["critical"],
            high_count=summary["findings_by_severity"]["high"],
            medium_count=summary["findings_by_severity"]["medium"],
            low_count=summary["findings_by_severity"]["low"],
            info_count=summary["findings_by_severity"]["info"],
            files_analyzed=summary["files_analyzed"],
            total_lines=summary["total_lines"],
            findings=[
                {
                    "type": f.type.value,
                    "severity": f.severity.value,
                    "message": f.message,
                    "location": f.location,
                    "code_snippet": f.code_snippet,
                    "remediation": f.remediation,
                }
                for f in filtered_result.findings
            ],
        )

    def save(self, result: AnalysisResult, output_path: str) -> None:
        """Save HTML report to file.

        Args:
            result: Analysis result
            output_path: Path to save report
        """
        html_str = self.generate(result)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_str)

