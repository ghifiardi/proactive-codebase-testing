#!/bin/bash
# Interactive script to push workflows to GitHub

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "🚀 GitHub Push Helper"
echo "===================="
echo ""

# Check if remote exists
if git remote | grep -q origin; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ Remote 'origin' found: $REMOTE_URL"
    echo ""
    read -p "Do you want to push to this remote? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "📤 Pushing to GitHub..."
        git push -u origin main && {
            echo ""
            echo "✅ Successfully pushed to GitHub!"
            echo ""
            echo "Next steps:"
            echo "1. Go to: https://github.com/$(echo $REMOTE_URL | sed 's/.*github.com[:/]\([^.]*\).*/\1/')"
            echo "2. Click 'Actions' tab to see workflows"
            echo "3. Workflows will run automatically"
        } || {
            echo ""
            echo "❌ Push failed. Common issues:"
            echo "   - Authentication required (use Personal Access Token)"
            echo "   - Repository doesn't exist (create it on GitHub first)"
            echo "   - No write permissions"
        }
        exit 0
    fi
fi

# No remote or user wants to change it
echo ""
echo "📋 Current status:"
echo "  - Branch: $(git branch --show-current)"
echo "  - Commits ready: $(git log --oneline | wc -l | xargs)"
echo "  - Remote: $(git remote -v 2>/dev/null | head -1 || echo 'None configured')"
echo ""

echo "To push to GitHub, you need to:"
echo ""
echo "1. Create a repository on GitHub (if you don't have one):"
echo "   → Go to: https://github.com/new"
echo "   → Repository name: proactive-codebase-testing"
echo "   → Don't initialize with README"
echo "   → Click 'Create repository'"
echo ""

read -p "Do you have a GitHub repository URL? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter GitHub repository URL (https://github.com/USER/REPO.git): " REPO_URL
    
    if [[ -z "$REPO_URL" ]]; then
        echo "❌ No URL provided"
        exit 1
    fi
    
    # Add or update remote
    if git remote | grep -q origin; then
        git remote set-url origin "$REPO_URL"
        echo "✅ Updated remote to: $REPO_URL"
    else
        git remote add origin "$REPO_URL"
        echo "✅ Added remote: $REPO_URL"
    fi
    
    echo ""
    echo "📤 Pushing to GitHub..."
    git push -u origin main && {
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        REPO_NAME=$(echo $REPO_URL | sed 's/.*github.com[:/]\([^.]*\).*/\1/')
        echo "View your repository:"
        echo "  https://github.com/$REPO_NAME"
        echo ""
        echo "View workflows:"
        echo "  https://github.com/$REPO_NAME/actions"
        echo ""
        echo "✅ Workflows are now active and will run automatically!"
    } || {
        echo ""
        echo "❌ Push failed. Please check:"
        echo "   1. Repository exists on GitHub"
        echo "   2. You have write access"
        echo "   3. Authentication is set up (Personal Access Token or SSH)"
        echo ""
        echo "For HTTPS, you'll need a Personal Access Token:"
        echo "  https://github.com/settings/tokens"
        echo ""
        echo "For SSH, set up SSH keys:"
        echo "  https://docs.github.com/en/authentication/connecting-to-github-with-ssh"
    }
else
    echo ""
    echo "📝 Manual steps:"
    echo ""
    echo "1. Create repository on GitHub:"
    echo "   https://github.com/new"
    echo ""
    echo "2. Add remote and push:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "   git push -u origin main"
    echo ""
    echo "3. Or use SSH:"
    echo "   git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git"
    echo "   git push -u origin main"
fi

