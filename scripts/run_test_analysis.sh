#!/bin/bash
# Script to run test analysis on the codebase

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🔍 Running Test Analysis on Codebase"
echo "===================================="
echo ""

# Check if API key is configured
if [ -f .env ] && grep -q "ANTHROPIC_API_KEY" .env && ! grep -q "ANTHROPIC_API_KEY=$" .env; then
    echo "✅ API key configured"
    USE_API=true
else
    echo "⚠️  API key not configured - will run parser tests only"
    USE_API=false
fi

echo ""
echo "📋 Step 1: Running Unit Tests"
echo "-----------------------------"
python3 -m pytest tests/ -v --tb=short || {
    echo "⚠️  Some tests failed, but continuing..."
}

echo ""
echo "📋 Step 2: Testing Code Parser"
echo "-----------------------------"
python3 -c "
from src.core.parser import CodeParser
import os

parser = CodeParser()
print('✅ CodeParser initialized')

# Test file detection
files = parser.get_files_to_analyze('src', max_files=10)
print(f'✅ Found {len(files)} Python files in src/')

# Test file parsing
if files:
    test_file = files[0]
    result = parser.analyze_file(test_file)
    if result:
        print(f'✅ Successfully parsed: {test_file}')
        print(f'   Language: {result.get(\"language\", \"unknown\")}')
        print(f'   Lines: {len(result.get(\"content\", \"\").splitlines())} chars')
    else:
        print(f'⚠️  Could not parse: {test_file}')
"

echo ""
if [ "$USE_API" = true ]; then
    echo "📋 Step 3: Running AI Analysis (Sample)"
    echo "----------------------------------------"
    echo "Analyzing a sample file with Claude API..."
    echo ""
    
    # Find a small Python file to test
    TEST_FILE=$(find src -name "*.py" -type f | head -1)
    
    if [ -n "$TEST_FILE" ]; then
        python3 -m src.cli.main analyze "$TEST_FILE" \
            --format json \
            --output test-analysis-result.json \
            --severity high 2>&1 | head -30 || {
            echo "⚠️  Analysis completed with warnings"
        }
        
        if [ -f test-analysis-result.json ]; then
            echo ""
            echo "✅ Analysis complete! Results saved to: test-analysis-result.json"
            echo ""
            echo "📊 Summary:"
            python3 -c "
import json
try:
    with open('test-analysis-result.json', 'r') as f:
        data = json.load(f)
    print(f'  Files analyzed: {data.get(\"files_analyzed\", 0)}')
    print(f'  Total findings: {len(data.get(\"findings\", []))}')
    if data.get('findings'):
        by_severity = {}
        for f in data['findings']:
            sev = f.get('severity', 'unknown')
            by_severity[sev] = by_severity.get(sev, 0) + 1
        print('  Findings by severity:')
        for sev, count in by_severity.items():
            print(f'    {sev}: {count}')
except Exception as e:
    print(f'  Could not parse results: {e}')
" 2>/dev/null || echo "  Check test-analysis-result.json for details"
        fi
    fi
else
    echo "📋 Step 3: Skipped (API key not configured)"
    echo "----------------------------------------"
    echo "To run full AI analysis:"
    echo "  1. Create .env file"
    echo "  2. Add: ANTHROPIC_API_KEY=sk-ant-..."
    echo "  3. Run this script again"
fi

echo ""
echo "📋 Step 4: Code Coverage Report"
echo "-------------------------------"
python3 -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -q 2>&1 | tail -15 || echo "⚠️  Coverage report generation had issues"

if [ -d htmlcov ]; then
    echo ""
    echo "✅ Coverage report generated: htmlcov/index.html"
fi

echo ""
echo "✅ Test Analysis Complete!"
echo ""
echo "📁 Output files:"
[ -f test-analysis-result.json ] && echo "  - test-analysis-result.json"
[ -d htmlcov ] && echo "  - htmlcov/index.html (coverage report)"
[ -f .coverage ] && echo "  - .coverage (coverage data)"


