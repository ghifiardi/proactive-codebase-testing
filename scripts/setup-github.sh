#!/bin/bash
# Setup script to prepare and push workflows to GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 Setting up GitHub repository for documentation workflows..."
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already initialized"
fi

# Check for .gitignore
if [ ! -f .gitignore ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Documentation output (optional - remove if you want to commit docs)
documentation_output/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Test
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore exists"
fi

# Check if remote exists
if git remote | grep -q origin; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote 'origin' exists: $REMOTE_URL"
else
    echo "⚠️  No remote 'origin' configured"
    echo ""
    echo "To add a remote, run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo ""
    read -p "Do you want to add a remote now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter GitHub repository URL: " REPO_URL
        git remote add origin "$REPO_URL"
        echo "✅ Remote added: $REPO_URL"
    fi
fi

# Stage workflow files
echo ""
echo "📋 Staging workflow files..."
git add .github/workflows/*.yml .github/workflows/*.md 2>/dev/null || true
git add GITHUB_DOCS_UPLOAD_GUIDE.md 2>/dev/null || true
git add scripts/generate*.py 2>/dev/null || true
git add docs/COMPLETE_DOCUMENTATION.md 2>/dev/null || true

# Check if there are changes
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit (workflows may already be committed)"
else
    echo "✅ Files staged"
    echo ""
    echo "📝 Committing workflows..."
    git commit -m "feat: add GitHub Actions workflows for documentation upload

- Add upload-docs-artifacts.yml (upload as artifacts)
- Add publish-docs.yml (auto-commit to repo)
- Add push-docs-branch.yml (push to docs branch)
- Add create-docs-release.yml (create releases)
- Add documentation generation scripts
- Add comprehensive upload guide" || echo "⚠️  Commit failed or nothing to commit"
    echo "✅ Changes committed"
fi

# Show status
echo ""
echo "📊 Current status:"
git status --short

# Check if we can push
if git remote | grep -q origin; then
    echo ""
    echo "🚀 Ready to push to GitHub!"
    echo ""
    echo "To push, run:"
    echo "  git push -u origin main"
    echo ""
    read -p "Do you want to push now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Pushing to GitHub..."
        git push -u origin main || {
            echo "❌ Push failed. You may need to:"
            echo "   1. Set up authentication (GitHub token or SSH key)"
            echo "   2. Create the repository on GitHub first"
            echo "   3. Check your remote URL"
        }
    fi
else
    echo ""
    echo "⚠️  Cannot push - no remote configured"
    echo "   Add remote: git remote add origin <url>"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push -u origin main"
echo "2. Check Actions: GitHub → Actions → See workflows"
echo "3. Download docs: Actions → Artifacts"

