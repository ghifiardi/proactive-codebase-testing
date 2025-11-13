#!/bin/bash
# Script to generate documentation in multiple formats

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOCS_DIR="$PROJECT_ROOT/docs"
OUTPUT_DIR="$PROJECT_ROOT/documentation_output"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📚 Generating documentation..."

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  pandoc not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install pandoc
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y pandoc
    else
        echo "❌ Please install pandoc manually: https://pandoc.org/installing.html"
        exit 1
    fi
fi

# Generate DOCX from Markdown
echo "📄 Generating DOCX..."
pandoc "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" \
    -o "$OUTPUT_DIR/Proactive_Codebase_Testing_Platform.docx" \
    --reference-doc="$PROJECT_ROOT/templates/reference.docx" 2>/dev/null || \
pandoc "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" \
    -o "$OUTPUT_DIR/Proactive_Codebase_Testing_Platform.docx" \
    --toc \
    --toc-depth=3 \
    -V geometry:margin=1in \
    -V fontsize=11pt

# Generate PDF (requires LaTeX)
if command -v pdflatex &> /dev/null; then
    echo "📕 Generating PDF..."
    pandoc "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" \
        -o "$OUTPUT_DIR/Proactive_Codebase_Testing_Platform.pdf" \
        --toc \
        --toc-depth=3 \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        --pdf-engine=pdflatex
else
    echo "⚠️  pdflatex not found. Skipping PDF generation."
    echo "   Install: brew install basictex (Mac) or sudo apt-get install texlive (Linux)"
fi

# Copy Markdown
echo "📝 Copying Markdown..."
cp "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" "$OUTPUT_DIR/"

# Generate HTML
echo "🌐 Generating HTML..."
pandoc "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" \
    -o "$OUTPUT_DIR/Proactive_Codebase_Testing_Platform.html" \
    --standalone \
    --toc \
    --toc-depth=3 \
    --css="$PROJECT_ROOT/templates/style.css" 2>/dev/null || \
pandoc "$DOCS_DIR/COMPLETE_DOCUMENTATION.md" \
    -o "$OUTPUT_DIR/Proactive_Codebase_Testing_Platform.html" \
    --standalone \
    --toc \
    --toc-depth=3

echo "✅ Documentation generated in: $OUTPUT_DIR"
echo ""
echo "Files created:"
ls -lh "$OUTPUT_DIR"

