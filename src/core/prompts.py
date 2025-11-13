"""Prompts for Claude API analysis."""

from typing import Dict, Optional


def get_security_prompt(file_name: str, code: str, language: str) -> str:
    """Get security vulnerability analysis prompt.

    Args:
        file_name: Name of the file being analyzed
        code: Source code content
        language: Programming language

    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following {language} code for security vulnerabilities.

File: {file_name}

Code:
```{language}
{code}
```

Please identify:
1. SQL injection vulnerabilities
2. Cross-site scripting (XSS) vulnerabilities
3. Authentication and authorization issues
4. Insecure data storage or transmission
5. Hardcoded secrets, API keys, or credentials
6. Insecure deserialization
7. Server-side request forgery (SSRF)
8. Path traversal vulnerabilities
9. Command injection
10. Insecure random number generation

For each vulnerability found, provide:
- Type: The vulnerability type (e.g., SQL_INJECTION, XSS)
- Severity: critical, high, medium, or low
- Location: Line number(s) where the issue occurs
- Message: Clear description of the vulnerability
- Remediation: How to fix the issue
- Confidence: Your confidence level (0.0 to 1.0)

Format your response as JSON with this structure:
{{
  "findings": [
    {{
      "type": "SECURITY",
      "severity": "critical",
      "line": 42,
      "message": "SQL injection vulnerability: user input directly concatenated into SQL query",
      "remediation": "Use parameterized queries or prepared statements",
      "confidence": 0.95,
      "code_snippet": "query = f'SELECT * FROM users WHERE id = {{user_input}}'"  # Example: SQL injection pattern (for demonstration)
    }}
  ]
}}

If no vulnerabilities are found, return: {{"findings": []}}
"""


def get_bug_detection_prompt(file_name: str, code: str, language: str) -> str:
    """Get bug detection prompt.

    Args:
        file_name: Name of the file being analyzed
        code: Source code content
        language: Programming language

    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following {language} code for bugs and logic errors.

File: {file_name}

Code:
```{language}
{code}
```

Please identify:
1. Null pointer/null reference exceptions
2. Array/string index out of bounds
3. Division by zero
4. Infinite loops or recursion
5. Resource leaks (unclosed files, connections)
6. Race conditions
7. Off-by-one errors
8. Type mismatches
9. Uninitialized variables
10. Logic errors

For each bug found, provide:
- Type: The bug type (e.g., NULL_POINTER, RESOURCE_LEAK)
- Severity: critical, high, medium, or low
- Location: Line number(s) where the bug occurs
- Message: Clear description of the bug
- Remediation: How to fix the bug
- Confidence: Your confidence level (0.0 to 1.0)

Format your response as JSON with this structure:
{{
  "findings": [
    {{
      "type": "BUG",
      "severity": "high",
      "line": 15,
      "message": "Potential null pointer: variable 'user' may be None before access",
      "remediation": "Add null check before accessing user properties",
      "confidence": 0.85,
      "code_snippet": "name = user.name"
    }}
  ]
}}

If no bugs are found, return: {{"findings": []}}
"""


def get_quality_prompt(file_name: str, code: str, language: str) -> str:
    """Get code quality analysis prompt.

    Args:
        file_name: Name of the file being analyzed
        code: Source code content
        language: Programming language

    Returns:
        Formatted prompt string
    """
    return f"""Analyze the following {language} code for code quality issues.

File: {file_name}

Code:
```{language}
{code}
```

Please identify:
1. Code smells (long methods, large classes)
2. Anti-patterns
3. Best practice violations
4. Duplicate code
5. Poor naming conventions
6. Missing error handling
7. Inefficient algorithms
8. Missing documentation
9. Complex conditional logic
10. Tight coupling

For each issue found, provide:
- Type: The issue type (e.g., CODE_SMELL, ANTI_PATTERN)
- Severity: critical, high, medium, low, or info
- Location: Line number(s) where the issue occurs
- Message: Clear description of the issue
- Remediation: How to improve the code
- Confidence: Your confidence level (0.0 to 1.0)

Format your response as JSON with this structure:
{{
  "findings": [
    {{
      "type": "QUALITY",
      "severity": "medium",
      "line": 50,
      "message": "Method is too long (150 lines), consider breaking into smaller functions",
      "remediation": "Extract logical sections into separate methods",
      "confidence": 0.90,
      "code_snippet": "def process_data(): ..."
    }}
  ]
}}

If no issues are found, return: {{"findings": []}}
"""


def get_comprehensive_prompt(file_name: str, code: str, language: str) -> str:
    """Get comprehensive analysis prompt (security + bugs + quality).

    Args:
        file_name: Name of the file being analyzed
        code: Source code content
        language: Programming language

    Returns:
        Formatted prompt string
    """
    return f"""Perform a comprehensive analysis of the following {language} code.

File: {file_name}

Code:
```{language}
{code}
```

Analyze for:
1. Security vulnerabilities (SQL injection, XSS, authentication issues, etc.)
2. Bugs and logic errors (null pointers, resource leaks, race conditions, etc.)
3. Code quality issues (code smells, anti-patterns, best practices, etc.)

For each finding, provide:
- Type: SECURITY, BUG, or QUALITY
- Severity: critical, high, medium, low, or info
- Location: Line number(s) where the issue occurs
- Message: Clear description of the issue
- Remediation: How to fix or improve
- Confidence: Your confidence level (0.0 to 1.0)

Format your response as JSON with this structure:
{{
  "findings": [
    {{
      "type": "SECURITY",
      "severity": "critical",
      "line": 42,
      "message": "SQL injection vulnerability",
      "remediation": "Use parameterized queries",
      "confidence": 0.95,
      "code_snippet": "query = f'SELECT * FROM users WHERE id = {{user_input}}'"  # Example: SQL injection pattern (for demonstration)
    }},
    {{
      "type": "BUG",
      "severity": "high",
      "line": 15,
      "message": "Potential null pointer",
      "remediation": "Add null check",
      "confidence": 0.85,
      "code_snippet": "name = user.name"
    }}
  ]
}}

If no findings are found, return: {{"findings": []}}
"""


def get_prompt(analysis_type: str, file_name: str, code: str, language: str) -> str:
    """Get analysis prompt by type.

    Args:
        analysis_type: Type of analysis (security, bugs, quality, comprehensive)
        file_name: Name of the file being analyzed
        code: Source code content
        language: Programming language

    Returns:
        Formatted prompt string
    """
    prompts = {
        "security": get_security_prompt,
        "bugs": get_bug_detection_prompt,
        "quality": get_quality_prompt,
        "comprehensive": get_comprehensive_prompt,
    }

    prompt_func = prompts.get(analysis_type.lower(), get_comprehensive_prompt)
    return prompt_func(file_name, code, language)

