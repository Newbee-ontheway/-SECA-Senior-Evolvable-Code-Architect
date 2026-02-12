#!/usr/bin/env python3
"""
File Size Checker — deterministic check for the 400-line rule

Usage: python check_file_size.py [directory] [--threshold N]
Default: project root, threshold 400

Scans .md, .py, .typ files and warns about any exceeding the threshold.
"""

import os
import sys
from pathlib import Path

DEFAULT_THRESHOLD = 400
EXTENSIONS = {".md", ".py", ".typ", ".js", ".ts"}
EXCLUDE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".agent"}


def check_file_sizes(root_dir: str, threshold: int = DEFAULT_THRESHOLD):
    root = Path(root_dir)
    warnings = []
    checked = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            filepath = Path(dirpath) / filename
            if filepath.suffix not in EXTENSIONS:
                continue

            checked += 1
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    line_count = sum(1 for _ in f)

                if line_count > threshold:
                    rel_path = filepath.relative_to(root)
                    warnings.append((str(rel_path), line_count))
            except (OSError, UnicodeDecodeError):
                continue

    return checked, warnings


if __name__ == "__main__":
    root_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    threshold = DEFAULT_THRESHOLD
    if "--threshold" in sys.argv:
        idx = sys.argv.index("--threshold")
        if idx + 1 < len(sys.argv):
            threshold = int(sys.argv[idx + 1])

    checked, warnings = check_file_sizes(root_dir, threshold)

    if warnings:
        warnings.sort(key=lambda x: x[1], reverse=True)
        print(f"⚠️  {len(warnings)} files exceed {threshold} lines:")
        for path, lines in warnings:
            print(f"   {path}: {lines} lines")
        sys.exit(1)
    else:
        print(f"✅ All {checked} files within {threshold} line threshold.")

