# Documentation Publishing Workflows

This directory contains GitHub Actions workflows for automatically generating and publishing documentation.

## Available Workflows

### 1. `publish-docs.yml`
**Purpose:** Auto-commit generated documentation to repository

**Triggers:**
- Push to main/develop (when docs change)
- Manual trigger (workflow_dispatch)
- Weekly schedule (Monday 9 AM UTC)

**Actions:**
- Generates all documentation formats
- Commits and pushes to current branch
- Creates release on tag push

**Use when:** You want documentation in the repository

---

### 2. `upload-docs-artifacts.yml`
**Purpose:** Upload documentation as GitHub Actions artifacts

**Triggers:**
- Push to main branch
- Manual trigger
- Release published

**Actions:**
- Generates all documentation
- Uploads as downloadable artifacts
- Available for 90 days

**Use when:** You want downloadable documentation without committing to repo

**Download:** Actions → Latest workflow run → Artifacts

---

### 3. `push-docs-branch.yml`
**Purpose:** Push documentation to dedicated `docs` branch

**Triggers:**
- Push to main (when docs/scripts change)
- Manual trigger

**Actions:**
- Generates documentation
- Creates/updates `docs` branch
- Keeps main branch clean

**Use when:** You want documentation in separate branch

---

### 4. `create-docs-release.yml`
**Purpose:** Create GitHub release with documentation

**Triggers:**
- Tag push (v* or docs-v*)
- Manual trigger with version input

**Actions:**
- Generates all documentation
- Creates zip archive
- Creates GitHub release with assets

**Use when:** You want versioned documentation releases

---

## Quick Start

### Option 1: Auto-commit to Repository

```bash
# Push to trigger workflow
git push origin main

# Documentation will be auto-committed
```

### Option 2: Manual Trigger

1. Go to GitHub → Actions
2. Select workflow
3. Click "Run workflow"
4. Documentation will be generated and published

### Option 3: Create Release

```bash
# Create tag
git tag docs-v1.0.0
git push origin docs-v1.0.0

# Release will be created with documentation
```

---

## Configuration

### Required Secrets

No secrets required for basic operation. Uses `GITHUB_TOKEN` automatically.

### Optional: Custom Token

If you need more permissions, add secret:
- `GITHUB_TOKEN` (custom token with repo permissions)

---

## Output Locations

### In Repository
- `documentation_output/` - Main platform docs
- `competitive advantage/documentation_output/` - Competitive analysis

### As Artifacts
- Download from: Actions → Artifacts
- Available for 90 days

### In Releases
- Attached to GitHub releases
- Downloadable as zip or individual files

---

## File Formats Generated

- **Markdown** (.md) - Source documentation
- **DOCX** (.docx) - Microsoft Word
- **PPTX** (.pptx) - PowerPoint presentation
- **HTML** (.html) - Web version

---

## Troubleshooting

### "pandoc not found"
- Workflow installs pandoc automatically
- If issues persist, check workflow logs

### "python-pptx not installed"
- Workflow installs it automatically
- Check requirements.txt includes it

### "Permission denied"
- Ensure workflow has `contents: write` permission
- Check repository settings → Actions → General → Workflow permissions

### "No changes to commit"
- Normal if documentation hasn't changed
- Check if source files were modified

---

## Customization

### Change Output Location
Edit workflow files and change:
```yaml
path: documentation_output/*
```

### Change Branch
Edit `push-docs-branch.yml`:
```yaml
git checkout -b your-branch-name
```

### Change Schedule
Edit `publish-docs.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
```

---

## Best Practices

1. **Use artifacts** for temporary documentation
2. **Use releases** for versioned documentation
3. **Use docs branch** to keep main clean
4. **Auto-commit** for always up-to-date docs

---

## Support

For issues:
- Check workflow logs in Actions tab
- Review error messages
- Ensure dependencies are installed
- Verify file paths are correct

