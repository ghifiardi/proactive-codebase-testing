#!/usr/bin/env python3
"""
Generate all documentation formats: Markdown, DOCX, and PPTX.

Requirements:
- pandoc (for DOCX): brew install pandoc (Mac) or apt-get install pandoc (Linux)
- python-pptx (for PPTX): pip install python-pptx
"""

import sys
import subprocess
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if required dependencies are installed."""
    missing = []
    
    # Check pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        missing.append("pandoc")
    
    # Check python-pptx
    try:
        import pptx
    except ImportError:
        missing.append("python-pptx")
    
    return missing

def generate_docx():
    """Generate DOCX from Markdown using pandoc."""
    docs_dir = project_root / "docs"
    output_dir = project_root / "documentation_output"
    output_dir.mkdir(exist_ok=True)
    
    input_file = docs_dir / "COMPLETE_DOCUMENTATION.md"
    output_file = output_dir / "Proactive_Codebase_Testing_Platform.docx"
    
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return False
    
    try:
        cmd = [
            "pandoc",
            str(input_file),
            "-o", str(output_file),
            "--toc",
            "--toc-depth=3",
            "-V", "geometry:margin=1in",
            "-V", "fontsize=11pt",
            "--reference-doc=/System/Library/Templates/Blank.docx"  # Try system template
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Try without reference doc
            cmd = cmd[:-1]
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ DOCX generated: {output_file}")
            return True
        else:
            print(f"❌ Error generating DOCX: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ pandoc not found. Install: brew install pandoc (Mac) or apt-get install pandoc (Linux)")
        return False

def generate_pptx():
    """Generate PPTX presentation."""
    try:
        from scripts.generate_pptx import create_presentation
        output_path = create_presentation()
        print(f"✅ PPTX generated: {output_path}")
        return True
    except ImportError:
        print("❌ python-pptx not installed. Install: pip install python-pptx")
        return False
    except Exception as e:
        print(f"❌ Error generating PPTX: {e}")
        return False

def copy_markdown():
    """Copy Markdown file to output directory."""
    docs_dir = project_root / "docs"
    output_dir = project_root / "documentation_output"
    output_dir.mkdir(exist_ok=True)
    
    input_file = docs_dir / "COMPLETE_DOCUMENTATION.md"
    output_file = output_dir / "COMPLETE_DOCUMENTATION.md"
    
    if input_file.exists():
        import shutil
        shutil.copy(input_file, output_file)
        print(f"✅ Markdown copied: {output_file}")
        return True
    else:
        print(f"❌ Input file not found: {input_file}")
        return False

def generate_html():
    """Generate HTML from Markdown."""
    docs_dir = project_root / "docs"
    output_dir = project_root / "documentation_output"
    output_dir.mkdir(exist_ok=True)
    
    input_file = docs_dir / "COMPLETE_DOCUMENTATION.md"
    output_file = output_dir / "Proactive_Codebase_Testing_Platform.html"
    
    try:
        cmd = [
            "pandoc",
            str(input_file),
            "-o", str(output_file),
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--css=https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ HTML generated: {output_file}")
            return True
        else:
            print(f"⚠️  HTML generation skipped: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("⚠️  pandoc not found. Skipping HTML generation.")
        return False

def main():
    """Generate all documentation formats."""
    print("📚 Generating Documentation in Multiple Formats\n")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("\nInstall instructions:")
        if "pandoc" in missing:
            print("  • pandoc: brew install pandoc (Mac) or sudo apt-get install pandoc (Linux)")
        if "python-pptx" in missing:
            print("  • python-pptx: pip install python-pptx")
        print()
    
    results = {}
    
    # Generate Markdown (always available)
    print("\n1. Generating Markdown...")
    results['markdown'] = copy_markdown()
    
    # Generate DOCX
    print("\n2. Generating DOCX...")
    results['docx'] = generate_docx()
    
    # Generate PPTX
    print("\n3. Generating PPTX...")
    results['pptx'] = generate_pptx()
    
    # Generate HTML
    print("\n4. Generating HTML...")
    results['html'] = generate_html()
    
    # Summary
    print("\n" + "=" * 60)
    print("\n📊 Generation Summary:")
    print(f"  ✅ Markdown: {'Success' if results.get('markdown') else 'Failed'}")
    print(f"  {'✅' if results.get('docx') else '❌'} DOCX: {'Success' if results.get('docx') else 'Failed'}")
    print(f"  {'✅' if results.get('pptx') else '❌'} PPTX: {'Success' if results.get('pptx') else 'Failed'}")
    print(f"  {'✅' if results.get('html') else '❌'} HTML: {'Success' if results.get('html') else 'Failed'}")
    
    output_dir = project_root / "documentation_output"
    print(f"\n📁 Output directory: {output_dir}")
    print("\nFiles generated:")
    if output_dir.exists():
        for file in sorted(output_dir.glob("*")):
            size = file.stat().st_size / 1024  # KB
            print(f"  • {file.name} ({size:.1f} KB)")
    
    print("\n✅ Documentation generation complete!")

if __name__ == "__main__":
    main()

