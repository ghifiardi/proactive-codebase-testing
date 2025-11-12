# Proactive Codebase Testing Platform - Complete Documentation

**Version:** 0.1.0  
**Date:** November 12, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Overview](#overview)
3. [Architecture](#architecture)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Deployment Guide](#deployment-guide)
8. [Integration Guide](#integration-guide)
9. [Implementation Details](#implementation-details)
10. [Testing & Quality Assurance](#testing--quality-assurance)
11. [Production Hardening](#production-hardening)
12. [Troubleshooting](#troubleshooting)
13. [Roadmap](#roadmap)
14. [Contributing](#contributing)

---

## Executive Summary

The **Proactive Codebase Testing Platform** is an AI-powered code analysis system that uses Claude API to detect security vulnerabilities, bugs, and code quality issues before deployment. Built using a spec-first development workflow, the platform provides CLI, REST API, and CI/CD integration capabilities.

### Key Features

- ✅ **AI-Powered Analysis** - Uses Claude 3.5 Sonnet for intelligent code analysis
- ✅ **Multi-Language Support** - Analyzes 20+ programming languages
- ✅ **Multiple Interfaces** - CLI tool, REST API, and GitHub Actions integration
- ✅ **Flexible Output** - JSON, HTML, and SARIF report formats
- ✅ **Production Ready** - Rate limiting, monitoring, logging, and security headers
- ✅ **Comprehensive Testing** - >80% test coverage with automated CI/CD
- ✅ **Docker Support** - Containerized deployment with multi-stage builds

### Business Value

- **Security**: Detect vulnerabilities before they reach production
- **Quality**: Improve code quality and reduce technical debt
- **Efficiency**: Automate code review processes
- **Compliance**: Meet security and quality standards
- **Cost Savings**: Reduce bug fixes and security incidents

---

## Overview

### What It Does

The platform analyzes source code using AI to identify:

1. **Security Vulnerabilities**
   - SQL injection
   - Cross-site scripting (XSS)
   - Authentication issues
   - Hardcoded secrets
   - Insecure deserialization
   - And more...

2. **Bugs**
   - Null pointer exceptions
   - Resource leaks
   - Race conditions
   - Logic errors
   - Off-by-one errors

3. **Code Quality Issues**
   - Code smells
   - Anti-patterns
   - Best practice violations
   - Duplicate code
   - Missing error handling

### How It Works

```
Source Code → Parser → Analyzer (Claude API) → Findings → Reporter → Output
```

1. **Parser** extracts code and detects language
2. **Analyzer** sends code to Claude API with analysis prompts
3. **Findings** are parsed and structured
4. **Reporter** formats output (JSON, HTML, SARIF)
5. **Output** is delivered via CLI, API, or CI/CD

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                      │
├──────────────┬──────────────┬──────────────────────────┤
│   CLI Tool   │   REST API   │   GitHub Actions         │
└──────┬───────┴──────┬───────┴──────────┬──────────────┘
       │              │                  │
       └──────────────┼──────────────────┘
                      │
       ┌──────────────▼──────────────┐
       │      Core Engine            │
       ├─────────────────────────────┤
       │  • Parser                   │
       │  • Analyzer (Claude API)    │
       │  • Findings Processor       │
       │  • Reporters                │
       └──────────────┬──────────────┘
                      │
       ┌──────────────▼──────────────┐
       │   Production Features       │
       ├─────────────────────────────┤
       │  • Rate Limiting            │
       │  • Monitoring               │
       │  • Logging                  │
       │  • Security Headers         │
       └─────────────────────────────┘
```

### Component Overview

#### Core Components

1. **Parser** (`src/core/parser.py`)
   - Language detection (20+ languages)
   - File extraction with encoding detection
   - Directory traversal with ignore patterns
   - File size limits

2. **Analyzer** (`src/core/analyzer.py`)
   - Claude API integration
   - Retry logic and error handling
   - Response parsing
   - Confidence scoring

3. **Findings** (`src/core/findings.py`)
   - Data structures (Finding, Location, AnalysisResult)
   - Severity levels (Critical, High, Medium, Low, Info)
   - Finding types (Security, Bug, Quality)

4. **Prompts** (`src/core/prompts.py`)
   - Security analysis prompts
   - Bug detection prompts
   - Code quality prompts
   - Comprehensive prompts

#### Interface Components

1. **CLI** (`src/cli/main.py`)
   - Typer-based command-line interface
   - Commands: analyze, health, version
   - Output format selection
   - Severity filtering

2. **REST API** (`src/api/`)
   - FastAPI-based HTTP API
   - 5 endpoints (analyze, health, languages, stats, docs)
   - Request/response validation
   - Auto-generated documentation

3. **Reporters** (`src/reporters/`)
   - JSON Reporter
   - HTML Reporter (visual dashboard)
   - SARIF Reporter (GitHub compatible)

#### Production Components

1. **Middleware** (`src/api/middleware.py`)
   - Rate limiting
   - Monitoring
   - Security headers
   - Error handling

2. **Monitoring** (`src/core/monitoring.py`)
   - Metrics collection
   - Performance tracking
   - Analysis statistics

3. **Logging** (`src/core/logging_config.py`)
   - Rotating file handlers
   - Structured logging
   - Configurable levels

---

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com))
- Git (optional, for version control)

### Quick Installation

```bash
# 1. Clone or download the repository
cd proactive-codebase-testing

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=sk-ant-...

# 5. Verify installation
python -m src.cli.main health
```

### Docker Installation

```bash
# Build image
docker build -t pct:latest --target api .

# Run container
docker run -d \
  --name pct-api \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  pct:latest
```

### Docker Compose

```bash
# Development
docker-compose up

# Production
docker-compose -f docker-compose.prod.yml up -d
```

---

## Usage Guide

### Command Line Interface

#### Basic Analysis

```bash
# Analyze current directory
python -m src.cli.main analyze .

# Analyze specific directory
python -m src.cli.main analyze /path/to/code

# Analyze single file
python -m src.cli.main analyze app.py
```

#### Output Formats

```bash
# JSON output
python -m src.cli.main analyze . --format json --output report.json

# HTML report
python -m src.cli.main analyze . --format html --output report.html

# SARIF format (for GitHub)
python -m src.cli.main analyze . --format sarif --output report.sarif

# Console output (default)
python -m src.cli.main analyze .
```

#### Options

```bash
# Filter by severity
python -m src.cli.main analyze . --severity high

# Analysis type
python -m src.cli.main analyze . --type security

# Fail on critical findings (for CI/CD)
python -m src.cli.main analyze . --fail-on-critical

# Combine options
python -m src.cli.main analyze . \
  --format html \
  --output report.html \
  --severity high \
  --fail-on-critical
```

### REST API

#### Start Server

```bash
# Development (with auto-reload)
uvicorn src.api.server:app --reload

# Production
uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

#### API Endpoints

**1. Analyze Code**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SELECT * FROM users WHERE id = " + user_input,
    "language": "python",
    "analysis_type": "security"
  }'
```

**2. Health Check**
```bash
curl http://localhost:8000/api/health
```

**3. Supported Languages**
```bash
curl http://localhost:8000/api/languages
```

**4. Statistics**
```bash
curl http://localhost:8000/api/stats
```

**5. Interactive Documentation**
Visit: `http://localhost:8000/api/docs`

### GitHub Actions

The platform includes GitHub Actions workflows for:

- **Security Scanning** - Automatic scans on push/PR
- **Scheduled Scans** - Weekly security scans
- **Security Gates** - Block PRs with critical findings
- **Testing** - Automated test suite
- **Build & Deploy** - Docker image building

See `.github/workflows/` for configuration.

---

## API Reference

### POST /api/analyze

Analyze code for security vulnerabilities, bugs, and quality issues.

**Request:**
```json
{
  "code": "string (required)",
  "language": "string (required)",
  "analysis_type": "string (optional)",
  "file_name": "string (optional)"
}
```

**Response:**
```json
{
  "findings": [...],
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

### GET /api/health

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

### GET /api/languages

Get list of supported programming languages.

**Response:**
```json
{
  "languages": ["python", "javascript", ...]
}
```

### GET /api/stats

Get analysis statistics.

**Response:**
```json
{
  "total_analyses": 100,
  "total_findings": 250,
  "findings_by_severity": {...}
}
```

See `docs/API.md` for complete API documentation.

---

## Deployment Guide

### Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.server:app --reload
```

### Docker Deployment

```bash
docker build -t pct:latest --target api .
docker run -d -p 8000:8000 -e ANTHROPIC_API_KEY=sk-... pct:latest
```

### Cloud Deployment

#### Heroku

```bash
heroku create your-app
heroku config:set ANTHROPIC_API_KEY=sk-...
git push heroku main
```

#### AWS Elastic Beanstalk

```bash
eb init
eb create production
eb setenv ANTHROPIC_API_KEY=sk-...
eb deploy
```

#### Google Cloud Run

```bash
gcloud run deploy pct \
  --image gcr.io/PROJECT_ID/pct \
  --set-env-vars ANTHROPIC_API_KEY=sk-...
```

#### Kubernetes

See `docs/DEPLOYMENT.md` for Kubernetes deployment manifests.

### Environment Variables

**Required:**
- `ANTHROPIC_API_KEY` - Anthropic API key

**Optional:**
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `API_HOST` - API server host (default: 0.0.0.0)
- `API_PORT` - API server port (default: 8000)
- `RATE_LIMIT_PER_MINUTE` - Rate limit (default: 60)
- `MAX_FILE_SIZE_KB` - Max file size (default: 100)
- `ANALYSIS_TIMEOUT_SECONDS` - Timeout (default: 30)

See `docs/DEPLOYMENT.md` for complete deployment guide.

---

## Integration Guide

### GitHub Integration

**Pre-commit Hook:**
```bash
pip install pre-commit
# Add to .pre-commit-config.yaml
pre-commit install
```

**GitHub Actions:**
Already configured in `.github/workflows/`

### Slack Integration

```python
from examples.slack_integration import send_to_slack

result = analyzer.analyze_directory(".")
send_to_slack(result.findings, "https://hooks.slack.com/...")
```

### Email Integration

```python
from examples.email_integration import send_email_report

send_email_report(result, "team@example.com", ...)
```

### Jira Integration

```python
from examples.jira_integration import create_jira_issues

create_jira_issues(result.findings, ...)
```

See `docs/INTEGRATION.md` for complete integration examples.

---

## Implementation Details

### Development Workflow

The platform was built using a **spec-first development workflow**:

1. **Research Phase** - Complete investigation and architecture design
2. **Plan Phase** - 12-step detailed implementation plan
3. **Implement Phase** - Step-by-step implementation (Langkah 1-12)

### Implementation Steps (Langkah)

**Langkah 1-3: Core Foundation**
- Project setup and data structures
- Code parser with language detection
- Analyzer with Claude API integration

**Langkah 4: Reporters**
- JSON, HTML, and SARIF reporters
- Severity filtering
- Output formatting

**Langkah 5: CLI Interface**
- Typer-based command-line tool
- Multiple output formats
- Exit code handling

**Langkah 6: REST API**
- FastAPI-based HTTP API
- Request/response validation
- Auto-generated documentation

**Langkah 7: GitHub Integration**
- GitHub Actions workflows
- SARIF upload
- PR comments

**Langkah 8: Testing**
- Comprehensive test suite
- >80% code coverage
- Mocked API tests

**Langkah 9: Docker Optimization**
- Multi-stage Docker builds
- Docker Compose setup
- Production configuration

**Langkah 10: Advanced CI/CD**
- Multi-platform testing
- Scheduled scans
- Security gates
- Performance testing

**Langkah 11: Extended Documentation**
- API reference
- Deployment playbooks
- Integration guides
- Examples

**Langkah 12: Production Hardening**
- Rate limiting
- Monitoring and metrics
- Security headers
- Production logging

### File Structure

```
proactive-codebase-testing/
├── src/
│   ├── core/              # Core analysis engine
│   ├── cli/               # Command-line interface
│   ├── api/               # REST API
│   └── reporters/         # Output formatters
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example code
├── .github/workflows/      # CI/CD workflows
├── Dockerfile             # Container image
├── docker-compose.yml     # Development setup
└── requirements.txt       # Dependencies
```

### Technology Stack

- **Language**: Python 3.10+
- **AI API**: Anthropic Claude 3.5 Sonnet
- **Web Framework**: FastAPI
- **CLI Framework**: Typer
- **Testing**: pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

---

## Testing & Quality Assurance

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/ --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v
```

### Test Coverage

- **Current Coverage**: >80%
- **Test Files**: 3 comprehensive test modules
- **Test Count**: 40+ unit tests

### Quality Metrics

- ✅ Type hints on all functions
- ✅ Docstrings on all public APIs
- ✅ Error handling throughout
- ✅ PEP 8 compliant code
- ✅ Pinned dependency versions
- ✅ No secrets in code

### CI/CD Testing

Automated testing runs on:
- Push to main/develop branches
- Pull requests
- Scheduled (daily at 2 AM UTC)
- Multiple Python versions (3.10, 3.11, 3.12)
- Multiple platforms (Ubuntu, macOS)

---

## Production Hardening

### Security Features

1. **Rate Limiting**
   - Per-IP rate limiting
   - Configurable requests per minute
   - 429 response with Retry-After header

2. **Security Headers**
   - X-Content-Type-Options
   - X-Frame-Options
   - X-XSS-Protection
   - Strict-Transport-Security
   - Content-Security-Policy

3. **Error Handling**
   - Global error handling middleware
   - Error ID generation
   - Proper error logging

4. **API Key Security**
   - Environment variable storage
   - Never exposed in responses
   - Rotation support

### Monitoring

1. **Metrics Collection**
   - Request/response timing
   - Analysis statistics
   - Finding counts by severity
   - Performance metrics (min, max, avg, p95)

2. **Logging**
   - Rotating file handlers (10MB, 5 backups)
   - Structured logging format
   - Configurable log levels
   - Console and file output

3. **Health Checks**
   - `/api/health` endpoint
   - Docker health checks
   - Kubernetes liveness/readiness probes

### Performance

- **Response Times**: <2s for typical analysis
- **Throughput**: 60 requests/minute (configurable)
- **Resource Limits**: CPU and memory limits in Docker
- **Caching**: Future enhancement

---

## Troubleshooting

### Common Issues

**1. "ANTHROPIC_API_KEY not provided"**
```bash
# Check environment variable
echo $ANTHROPIC_API_KEY

# Or check .env file
cat .env | grep ANTHROPIC_API_KEY
```

**2. "Rate limit exceeded"**
- Reduce request frequency
- Increase `RATE_LIMIT_PER_MINUTE` in environment
- Implement request queuing

**3. "File encoding issues"**
- Files are automatically detected with fallback to UTF-8
- Check file encoding manually if issues persist

**4. "API timeout"**
- Increase `ANALYSIS_TIMEOUT_SECONDS`
- Analyze smaller files
- Check network connectivity

**5. "Docker build fails"**
- Check Docker version (requires 20.10+)
- Ensure sufficient disk space
- Check Dockerfile syntax

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python -m src.cli.main analyze . --format json | jq
```

### Getting Help

- Check `docs/` directory for detailed guides
- Review `examples/` for usage patterns
- Check GitHub Issues
- Review logs: `tail -f logs/api.log`

---

## Roadmap

### Completed (v0.1.0)

- ✅ Core analysis engine
- ✅ CLI interface
- ✅ REST API
- ✅ Multiple output formats
- ✅ Docker support
- ✅ CI/CD integration
- ✅ Production hardening
- ✅ Comprehensive documentation

### Planned (v0.2.0)

- [ ] Database persistence
- [ ] User authentication
- [ ] Web dashboard
- [ ] Caching layer
- [ ] Custom rule engine
- [ ] WebSocket support
- [ ] Real-time streaming

### Future (v0.3.0+)

- [ ] Multi-user support
- [ ] Team collaboration
- [ ] Historical analysis
- [ ] Trend reporting
- [ ] Compliance scanning
- [ ] Custom model support

---

## Contributing

### Development Setup

```bash
# Clone repository
git clone <repo-url>
cd proactive-codebase-testing

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Write tests for new features

### Pull Request Process

1. Create feature branch
2. Make changes
3. Add tests
4. Run tests and linting
5. Update documentation
6. Create pull request

---

## Support & Resources

### Documentation

- **README.md** - Quick start guide
- **docs/API.md** - Complete API reference
- **docs/DEPLOYMENT.md** - Deployment guide
- **docs/INTEGRATION.md** - Integration examples
- **LANGKAH_9_12_SUMMARY.md** - Implementation summary

### Examples

- **examples/custom_rules.py** - Custom analysis rules
- **examples/vulnerable_code.py** - Test code
- **examples/slack_integration.py** - Slack integration
- **examples/email_integration.py** - Email integration

### Contact

- GitHub Issues: [Report issues](https://github.com/yourname/proactive-codebase-testing/issues)
- Documentation: See `docs/` directory
- Examples: See `examples/` directory

---

## License

MIT License - see LICENSE file for details

---

## Acknowledgments

- Built with [Claude API](https://claude.ai) by Anthropic
- CLI by [Typer](https://typer.tiangolo.com/)
- Web framework [FastAPI](https://fastapi.tiangolo.com/)
- Prompts inspired by OWASP, CWE, and security best practices

---

**Made with ❤️ for secure, clean code**

*Last Updated: November 12, 2025*

