# API Reference

Complete API documentation for Proactive Codebase Testing Platform.

## Base URL

```
http://localhost:8000/api
```

## Authentication

Currently, the API uses the `ANTHROPIC_API_KEY` environment variable. Future versions will support API key authentication via headers.

## Endpoints

### POST /api/analyze

Analyze code for security vulnerabilities, bugs, and quality issues.

**Request Body:**
```json
{
  "code": "string (required)",
  "language": "string (required)",
  "analysis_type": "string (optional, default: 'comprehensive')",
  "file_name": "string (optional, default: 'unknown')"
}
```

**Parameters:**
- `code` (string, required): Source code to analyze
- `language` (string, required): Programming language (python, javascript, go, etc.)
- `analysis_type` (string, optional): Type of analysis
  - `security`: Security vulnerabilities only
  - `bugs`: Bug detection only
  - `quality`: Code quality issues only
  - `comprehensive`: All analysis types (default)
- `file_name` (string, optional): Name of the file being analyzed

**Response:**
```json
{
  "findings": [
    {
      "type": "SECURITY",
      "severity": "critical",
      "message": "SQL injection vulnerability",
      "location": {
        "file_path": "app.py",
        "line": 42
      },
      "remediation": "Use parameterized queries",
      "confidence": 0.95,
      "code_snippet": "query = f'SELECT * FROM users WHERE id = {user_input}'"
    }
  ],
  "files_analyzed": 1,
  "total_lines": 50,
  "findings_by_severity": {
    "critical": 1,
    "high": 0,
    "medium": 0,
    "low": 0,
    "info": 0
  },
  "success": true
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: Invalid request (missing required fields)
- `500 Internal Server Error`: Analysis failed

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SELECT * FROM users WHERE id = " + user_input,
    "language": "python",
    "analysis_type": "security"
  }'
```

---

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

**Example:**
```bash
curl http://localhost:8000/api/health
```

---

### GET /api/languages

Get list of supported programming languages.

**Response:**
```json
{
  "languages": [
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
    "sql"
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/languages
```

---

### GET /api/stats

Get analysis statistics (placeholder for future implementation).

**Response:**
```json
{
  "total_analyses": 0,
  "total_findings": 0,
  "findings_by_severity": {}
}
```

---

### GET /api/docs

Interactive API documentation (Swagger UI).

Visit in browser: `http://localhost:8000/api/docs`

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

**Common Error Codes:**
- `400`: Bad Request - Invalid input
- `422`: Unprocessable Entity - Validation error
- `500`: Internal Server Error - Server error
- `503`: Service Unavailable - API unavailable

---

## Rate Limiting

Currently no rate limiting is implemented. Future versions will include:
- Per-IP rate limiting
- Per-API-key rate limiting
- Request throttling

---

## SDK Examples

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/api/analyze",
    json={
        "code": "def vulnerable_function(user_input):\n    query = f'SELECT * FROM users WHERE id = {user_input}'",
        "language": "python",
        "analysis_type": "security"
    }
)

result = response.json()
for finding in result["findings"]:
    print(f"{finding['severity']}: {finding['message']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const response = await axios.post('http://localhost:8000/api/analyze', {
  code: 'SELECT * FROM users WHERE id = ' + userInput,
  language: 'python',
  analysis_type: 'security'
});

response.data.findings.forEach(finding => {
  console.log(`${finding.severity}: ${finding.message}`);
});
```

### cURL

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d @- << EOF
{
  "code": "def test(): pass",
  "language": "python"
}
EOF
```

---

## WebSocket Support (Future)

Future versions may include WebSocket support for real-time analysis streaming.

---

## Versioning

API versioning will be implemented in future releases. Current version: `v0.1.0`

