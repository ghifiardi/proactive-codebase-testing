"""Code parser for language detection and file extraction."""

import os
import chardet
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Language detection mapping
LANGUAGE_EXTENSIONS = {
    # Python
    ".py": "python",
    # JavaScript/TypeScript
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    # Go
    ".go": "go",
    # Java
    ".java": "java",
    # C/C++
    ".c": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".h": "c",
    ".hpp": "cpp",
    # C#
    ".cs": "csharp",
    # Ruby
    ".rb": "ruby",
    # PHP
    ".php": "php",
    # Swift
    ".swift": "swift",
    # Kotlin
    ".kt": "kotlin",
    # Rust
    ".rs": "rust",
    # Shell
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    # HTML/CSS
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    # JSON/YAML
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    # SQL
    ".sql": "sql",
}

# Files/directories to ignore
IGNORE_PATTERNS = {
    ".git",
    ".svn",
    ".hg",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    ".env",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "*.pyc",
    "*.pyo",
    "*.min.js",
    "*.min.css",
}


class CodeParser:
    """Parser for extracting code from files and detecting languages."""

    def __init__(self, max_file_size_kb: int = 100):
        """Initialize parser.

        Args:
            max_file_size_kb: Maximum file size in KB to analyze
        """
        self.max_file_size_kb = max_file_size_kb

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension.

        Args:
            file_path: Path to the file

        Returns:
            Language name or None if not supported
        """
        ext = Path(file_path).suffix.lower()
        return LANGUAGE_EXTENSIONS.get(ext)

    def should_analyze_file(self, file_path: str) -> bool:
        """Check if file should be analyzed.

        Args:
            file_path: Path to the file

        Returns:
            True if file should be analyzed
        """
        path = Path(file_path)

        # Check if file exists
        if not path.exists() or not path.is_file():
            return False

        # Check file size
        size_kb = path.stat().st_size / 1024
        if size_kb > self.max_file_size_kb:
            logger.warning(f"File {file_path} too large ({size_kb:.1f}KB), skipping")
            return False

        # Check ignore patterns
        for pattern in IGNORE_PATTERNS:
            if pattern in path.parts or path.name.endswith(pattern.replace("*", "")):
                return False

        # Check if language is supported
        if not self.detect_language(str(file_path)):
            return False

        return True

    def read_file(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Read file content with encoding detection.

        Args:
            file_path: Path to the file

        Returns:
            Tuple of (content, encoding) or (None, None) on error
        """
        try:
            path = Path(file_path)

            # Try to detect encoding
            with open(path, "rb") as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result.get("encoding", "utf-8")

            # Read with detected encoding, fallback to utf-8
            try:
                with open(path, "r", encoding=encoding, errors="replace") as f:
                    content = f.read()
                return content, encoding
            except (UnicodeDecodeError, LookupError):
                # Fallback to utf-8
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                return content, "utf-8"

        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None, None

    def analyze_file(self, file_path: str) -> Optional[Dict[str, any]]:
        """Analyze a single file and extract code.

        Args:
            file_path: Path to the file

        Returns:
            Dictionary with file info or None on error
        """
        if not self.should_analyze_file(file_path):
            return None

        language = self.detect_language(file_path)
        if not language:
            return None

        content, encoding = self.read_file(file_path)
        if content is None:
            return None

        return {
            "path": str(Path(file_path).absolute()),
            "language": language,
            "content": content,
            "encoding": encoding,
            "size_bytes": len(content.encode(encoding or "utf-8")),
            "line_count": len(content.splitlines()),
        }

    def get_files_to_analyze(self, directory: str) -> List[str]:
        """Get list of files to analyze from directory.

        Args:
            directory: Root directory to scan

        Returns:
            List of file paths
        """
        files = []
        path = Path(directory)

        if not path.exists():
            logger.error(f"Directory does not exist: {directory}")
            return files

        if path.is_file():
            # Single file
            if self.should_analyze_file(str(path)):
                files.append(str(path))
            return files

        # Walk directory
        for root, dirs, filenames in os.walk(path):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORE_PATTERNS]

            for filename in filenames:
                file_path = os.path.join(root, filename)
                if self.should_analyze_file(file_path):
                    files.append(file_path)

        return files

