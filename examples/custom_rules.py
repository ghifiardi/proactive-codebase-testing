"""
Example: Custom Analysis Rules

This example shows how to create custom analysis rules and prompts
for company-specific security standards and coding conventions.
"""

# Custom prompt for company-specific security standards
COMPANY_SECURITY_PROMPT = """
Analyze the following {language} code for company-specific security violations.

Company Security Standards:
1. All API endpoints must use authentication
2. No hardcoded credentials (use environment variables)
3. All user input must be sanitized
4. Database queries must use ORM (no raw SQL)
5. All external API calls must have timeout and retry logic
6. Secrets must be stored in company secret manager
7. All logging must exclude sensitive data

Code:
```{language}
{code}
```

For each violation found, provide:
- Type: COMPANY_SECURITY_VIOLATION
- Severity: critical, high, medium, or low
- Line: Line number
- Message: Description of violation
- Remediation: How to fix according to company standards
- Confidence: 0.0 to 1.0

Format as JSON:
{{
  "findings": [
    {{
      "type": "COMPANY_SECURITY_VIOLATION",
      "severity": "high",
      "line": 42,
      "message": "Hardcoded API key found - violates company security standard #2",
      "remediation": "Move API key to environment variable or company secret manager",
      "confidence": 0.95
    }}
  ]
}}
"""

# Custom prompt for framework-specific rules
FRAMEWORK_PROMPT = """
Analyze the following {language} code for framework best practices.

Framework: Django
Standards:
1. Use Django ORM instead of raw SQL
2. Use Django's built-in authentication
3. Use Django's CSRF protection
4. Use Django's form validation
5. Follow Django's project structure

Code:
```{language}
{code}
```

Identify violations and provide findings in JSON format.
"""

# Example: Using custom prompts
def analyze_with_custom_rules(code, language, custom_prompt):
    """Analyze code with custom rules."""
    from src.core.analyzer import CodeAnalyzer
    from anthropic import Anthropic
    import os
    
    analyzer = CodeAnalyzer()
    
    # Format custom prompt
    formatted_prompt = custom_prompt.format(
        language=language,
        code=code
    )
    
    # Call Claude API with custom prompt
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": formatted_prompt
        }]
    )
    
    # Parse response (similar to analyzer._parse_api_response)
    # ... parsing logic ...
    
    return findings


# Example: Custom rule for specific patterns
CUSTOM_PATTERN_RULES = {
    "hardcoded_secrets": {
        "pattern": r"(api[_-]?key|password|secret|token)\s*=\s*['\"][^'\"]+['\"]",
        "severity": "critical",
        "message": "Hardcoded secret detected",
        "remediation": "Use environment variables or secret manager"
    },
    "sql_injection_risk": {
        "pattern": r"f?['\"].*SELECT.*\{.*\}.*['\"]",
        "severity": "critical",
        "message": "Potential SQL injection - string formatting in SQL",
        "remediation": "Use parameterized queries or ORM"
    },
    "missing_error_handling": {
        "pattern": r"def\s+\w+\([^)]*\):\s*\n\s*(?!.*try:).*",
        "severity": "medium",
        "message": "Function missing error handling",
        "remediation": "Add try-except blocks for error handling"
    }
}


def check_custom_patterns(code, file_path):
    """Check code against custom pattern rules."""
    import re
    from src.core.findings import Finding, FindingType, Severity, Location
    
    findings = []
    
    for rule_name, rule in CUSTOM_PATTERN_RULES.items():
        matches = re.finditer(rule["pattern"], code, re.MULTILINE)
        
        for match in matches:
            line_number = code[:match.start()].count('\n') + 1
            
            finding = Finding(
                type=FindingType.SECURITY,
                severity=Severity[rule["severity"].upper()],
                message=rule["message"],
                location=Location(file_path=file_path, line=line_number),
                remediation=rule["remediation"],
                confidence=0.8,
                code_snippet=match.group(0),
                rule_id=rule_name
            )
            
            findings.append(finding)
    
    return findings


# Example: Combine custom rules with standard analysis
def comprehensive_analysis_with_custom_rules(directory):
    """Run comprehensive analysis including custom rules."""
    from src.core.analyzer import CodeAnalyzer
    from src.core.parser import CodeParser
    
    analyzer = CodeAnalyzer()
    parser = CodeParser()
    
    # Standard analysis
    result = analyzer.analyze_directory(directory, parser=parser)
    
    # Add custom pattern checks
    files = parser.get_files_to_analyze(directory)
    for file_path in files:
        file_data = parser.analyze_file(file_path)
        if file_data:
            custom_findings = check_custom_patterns(
                file_data["content"],
                file_data["path"]
            )
            result.findings.extend(custom_findings)
    
    return result


if __name__ == "__main__":
    # Example usage
    result = comprehensive_analysis_with_custom_rules(".")
    print(f"Found {len(result.findings)} total findings")
    
    for finding in result.findings:
        print(f"{finding.severity.value}: {finding.message}")

