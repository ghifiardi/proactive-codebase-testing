# 🔍 Proactive Codebase Testing Platform

**AI-powered code analyzer using Claude API** to find security vulnerabilities, bugs, and code quality issues **before deployment**.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- Python 3.10 or higher
- Anthropic API key (get at [console.anthropic.com](https://console.anthropic.com))

### Installation

```bash
# Clone or download the repository
cd proactive-codebase-testing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### First Analysis

```bash
# Analyze current directory
python -m src.cli.main analyze .

# Analyze specific file
python -m src.cli.main analyze src/

# Generate HTML report
python -m src.cli.main analyze . --format html --output report.html

# Fail on critical findings
python -m src.cli.main analyze . --fail-on-critical
```

---

## 📖 Usage Guide

### Command Line Interface

```bash
# Basic analysis
python -m src.cli.main analyze /path/to/code

# Options
python -m src.cli.main analyze . --format json          # Output format
python -m src.cli.main analyze . --severity high        # Filter by severity
python -m src.cli.main analyze . --fail-on-critical     # Exit 1 if critical found
python -m src.cli.main analyze . --output report.json   # Save to file
```

### REST API

```bash
# Start API server
uvicorn src.api.server:app --reload

# Analyze via API
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "SELECT * FROM users WHERE id = " + user_input,
    "language": "python"
  }'
```

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t proactive-codebase-testing .

# Run CLI
docker run -e ANTHROPIC_API_KEY=sk-... proactive-codebase-testing analyze .

# Run API server
docker run -e ANTHROPIC_API_KEY=sk-... -p 8000:8000 proactive-codebase-testing api
```

---

## 📊 Supported Languages

- Python, JavaScript, TypeScript
- Go, Java, C/C++, C#
- Ruby, PHP, Swift, Kotlin, Rust
- Bash, Shell scripting
- JSON, YAML, HTML, CSS

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/ --cov-report=html
```

---

## 📚 Documentation

- **START_HERE.md** - Quick overview and getting started
- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **README.md** - This file (usage guide)

---

## 📄 License

MIT License - see LICENSE file for details

---

**Made with ❤️ for secure, clean code**
