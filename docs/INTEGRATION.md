# Integration Guides

How to integrate Proactive Codebase Testing Platform with popular tools and services.

## Table of Contents

1. [GitHub Integration](#github-integration)
2. [GitLab Integration](#gitlab-integration)
3. [Slack Integration](#slack-integration)
4. [Email Integration](#email-integration)
5. [Jira Integration](#jira-integration)
6. [Custom Integrations](#custom-integrations)

---

## GitHub Integration

### GitHub Actions

Already configured! See `.github/workflows/security-scan.yml`

### Pre-commit Hook

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: local
    hooks:
      - id: pct-analyze
        name: Proactive Codebase Testing
        entry: python -m src.cli.main analyze
        language: system
        pass_filenames: false
        always_run: true
        args: ['--fail-on-critical']
EOF

# Install hook
pre-commit install
```

### GitHub App (Future)

Future versions will support GitHub App integration for:
- Automatic PR comments
- Branch protection rules
- Security alerts

---

## GitLab Integration

### GitLab CI/CD

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security

security-scan:
  stage: security
  image: python:3.11
  before_script:
    - pip install -r requirements.txt
  script:
    - python -m src.cli.main analyze . --format sarif --output gl-sast-report.sarif
  artifacts:
    reports:
      sast: gl-sast-report.sarif
  only:
    - merge_requests
    - main
```

---

## Slack Integration

### Send Findings to Slack

```python
# examples/slack_integration.py
import requests
import json
from src.core.analyzer import CodeAnalyzer
from src.core.parser import CodeParser

def send_to_slack(findings, webhook_url):
    """Send analysis findings to Slack."""
    for finding in findings:
        color = {
            "critical": "#dc3545",
            "high": "#fd7e14",
            "medium": "#ffc107",
            "low": "#17a2b8",
            "info": "#6c757d"
        }.get(finding.severity.value, "#6c757d")
        
        payload = {
            "attachments": [{
                "color": color,
                "title": f"{finding.severity.value.upper()}: {finding.type.value}",
                "text": finding.message,
                "fields": [
                    {"title": "File", "value": finding.location.file_path, "short": True},
                    {"title": "Line", "value": str(finding.location.line or "N/A"), "short": True},
                    {"title": "Remediation", "value": finding.remediation or "N/A", "short": False}
                ]
            }]
        }
        
        requests.post(webhook_url, json=payload)

# Usage
analyzer = CodeAnalyzer()
parser = CodeParser()
result = analyzer.analyze_directory(".", parser=parser)

send_to_slack(
    result.findings,
    "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
)
```

### Daily Digest

```python
# examples/slack_daily_digest.py
from datetime import datetime
import requests

def send_daily_digest(result, webhook_url):
    """Send daily summary to Slack."""
    summary = result.get_summary()
    
    message = f"""
🔍 *Daily Security Scan - {datetime.now().strftime('%Y-%m-%d')}*

*Summary:*
• Total Findings: {summary['total_findings']}
• Critical: {summary['findings_by_severity']['critical']}
• High: {summary['findings_by_severity']['high']}
• Files Analyzed: {summary['files_analyzed']}

View full report: <link-to-report>
"""
    
    requests.post(webhook_url, json={"text": message})
```

---

## Email Integration

### Send Report via Email

```python
# examples/email_integration.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from src.reporters.html_reporter import HTMLReporter

def send_email_report(result, to_email, smtp_server, smtp_port, username, password):
    """Send HTML report via email."""
    # Generate HTML report
    reporter = HTMLReporter()
    html_content = reporter.generate(result)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = "Code Security Analysis Report"
    
    # Attach HTML
    msg.attach(MIMEText(html_content, 'html'))
    
    # Send
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.quit()

# Usage
from src.core.analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()
result = analyzer.analyze_directory(".")

send_email_report(
    result,
    "team@example.com",
    "smtp.gmail.com",
    587,
    "your-email@gmail.com",
    "your-password"
)
```

---

## Jira Integration

### Create Jira Issues from Findings

```python
# examples/jira_integration.py
from jira import JIRA

def create_jira_issues(findings, jira_url, username, api_token, project_key):
    """Create Jira issues for critical/high findings."""
    jira = JIRA(jira_url, basic_auth=(username, api_token))
    
    for finding in findings:
        if finding.severity.value in ['critical', 'high']:
            issue_dict = {
                'project': {'key': project_key},
                'summary': f"{finding.severity.value.upper()}: {finding.message[:100]}",
                'description': f"""
File: {finding.location.file_path}
Line: {finding.location.line}
Type: {finding.type.value}
Severity: {finding.severity.value}

Message:
{finding.message}

Remediation:
{finding.remediation or 'N/A'}
""",
                'issuetype': {'name': 'Bug'},
                'priority': {'name': 'High' if finding.severity.value == 'critical' else 'Medium'}
            }
            
            issue = jira.create_issue(fields=issue_dict)
            print(f"Created issue: {issue.key}")

# Usage
from src.core.analyzer import CodeAnalyzer
analyzer = CodeAnalyzer()
result = analyzer.analyze_directory(".")

create_jira_issues(
    result.findings,
    "https://your-company.atlassian.net",
    "your-email@example.com",
    "your-api-token",
    "PROJ"
)
```

---

## Custom Integrations

### Webhook Integration

```python
# examples/webhook_integration.py
import requests
import json

def send_webhook(result, webhook_url):
    """Send analysis results to custom webhook."""
    payload = {
        "timestamp": result.timestamp.isoformat(),
        "summary": result.get_summary(),
        "findings": [f.to_dict() for f in result.findings]
    }
    
    response = requests.post(
        webhook_url,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    return response.status_code == 200
```

### Database Integration

```python
# examples/database_integration.py
import sqlite3
from datetime import datetime

def save_to_database(result, db_path):
    """Save findings to SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            type TEXT,
            severity TEXT,
            file_path TEXT,
            line INTEGER,
            message TEXT,
            remediation TEXT,
            confidence REAL
        )
    """)
    
    # Insert findings
    for finding in result.findings:
        cursor.execute("""
            INSERT INTO findings 
            (timestamp, type, severity, file_path, line, message, remediation, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result.timestamp.isoformat(),
            finding.type.value,
            finding.severity.value,
            finding.location.file_path,
            finding.location.line,
            finding.message,
            finding.remediation,
            finding.confidence
        ))
    
    conn.commit()
    conn.close()
```

---

## Integration Best Practices

1. **Rate Limiting**: Respect API rate limits
2. **Error Handling**: Always handle errors gracefully
3. **Retries**: Implement retry logic for network calls
4. **Logging**: Log all integration activities
5. **Security**: Never expose API keys or secrets
6. **Testing**: Test integrations in development first

---

## Support

For integration questions:
- Check examples in `examples/` directory
- Review API documentation in `docs/API.md`
- Open GitHub issue for help

