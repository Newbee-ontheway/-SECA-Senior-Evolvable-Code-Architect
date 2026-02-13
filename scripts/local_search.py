#!/usr/bin/env python3
"""local_search.py — BM25 local search for _ai_evolution/ markdown files.

Uses tantivy-py (Rust-based search engine) for fast, persistent full-text search.
Designed to work with AI intent clarification: user gives fuzzy query,
AI translates to keywords, this script finds exact matches.

Usage:
    python local_search.py --build              # Build/rebuild index
    python local_search.py "query keywords"     # Search (auto-builds if no index)
    python local_search.py "session end" -k 10  # Return top 10 results
    python local_search.py --stats              # Show index stats

Build Justification (per /search_before_build):
- Need: BM25 search over local markdown files with persistent index
- Local search: No existing local search script
- External search: rank-bm25 (no persistence), BM25S (extra deps),
  Whoosh (outdated), dotMD (too heavy), tantivy-py (best fit)
- Decision: tantivy-py — precompiled wheel, persistent index,
  incremental updates, query language, zero Python deps
"""

import argparse
import os
import re
import sys
import pathlib
import shutil
from datetime import datetime

try:
    import tantivy
except ImportError:
    print("ERROR: tantivy not installed. Run: pip install tantivy")
    sys.exit(1)


# --- Configuration ---

# Directories to index (relative to ai_evolution root)
INDEX_DIRS = [
    ".",              # Root md files (project_context, skills, etc.)
    "session_notes",  # Session notes and sub-dirs
    "readings",       # Research output
    "workflows",      # Workflow definitions
]

# File extensions to index
INDEX_EXTENSIONS = {".md"}

# Files/dirs to skip
SKIP_PATTERNS = {".git", "__pycache__", ".bm25_index", "node_modules"}

# Index location
INDEX_DIR_NAME = ".search_index"


def find_ai_evolution():
    """Locate _ai_evolution/ directory by walking up from script location."""
    current = pathlib.Path(__file__).resolve().parent
    while current != current.parent:
        if current.name == "_ai_evolution":
            return current
        candidate = current / "_ai_evolution"
        if candidate.is_dir():
            return candidate
        current = current.parent
    # Fallback: script is inside _ai_evolution/scripts/
    script_parent = pathlib.Path(__file__).resolve().parent.parent
    if script_parent.name == "_ai_evolution":
        return script_parent
    print("ERROR: Cannot find _ai_evolution/ directory")
    sys.exit(1)


def strip_markdown(text):
    """Remove markdown formatting for cleaner indexing."""
    # Remove code blocks
    text = re.sub(r'```[\s\S]*?```', ' ', text)
    # Remove inline code
    text = re.sub(r'`[^`]+`', ' ', text)
    # Remove markdown links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove headers markers, bold, italic markers
    text = re.sub(r'[#*_~>|]', ' ', text)
    # Remove table separators
    text = re.sub(r'-{3,}', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_title(content):
    """Extract first heading as document title."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fallback: first non-empty line
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('---'):
            return line[:100]
    return "(no title)"


def collect_files(ai_dir):
    """Collect all markdown files to index."""
    files = []
    for subdir in INDEX_DIRS:
        target = ai_dir / subdir
        if not target.exists():
            continue
        for root, dirs, filenames in os.walk(target):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in SKIP_PATTERNS]
            for fname in filenames:
                fpath = pathlib.Path(root) / fname
                if fpath.suffix.lower() in INDEX_EXTENSIONS:
                    files.append(fpath)
    # Deduplicate (root "." may overlap with subdirs)
    seen = set()
    unique = []
    for f in files:
        resolved = f.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(f)
    return unique


def build_schema():
    """Build the tantivy schema for markdown documents."""
    builder = tantivy.SchemaBuilder()
    builder.add_text_field("title", stored=True, tokenizer_name="en_stem")
    builder.add_text_field("body", stored=True, tokenizer_name="en_stem")
    builder.add_text_field("path", stored=True, tokenizer_name="raw")
    builder.add_integer_field("size", stored=True)
    builder.add_date_field("modified", stored=True)
    return builder.build()


def build_index(ai_dir, force=False):
    """Build or rebuild the search index."""
    sys.stdout.reconfigure(encoding="utf-8")
    index_path = ai_dir / INDEX_DIR_NAME
    if force and index_path.exists():
        shutil.rmtree(index_path)

    index_path.mkdir(exist_ok=True)
    schema = build_schema()
    index = tantivy.Index(schema, path=str(index_path))

    files = collect_files(ai_dir)
    writer = index.writer()

    # Clear existing documents for full rebuild
    # (tantivy doesn't have a simple "delete all", so we rebuild fresh)
    indexed = 0
    errors = 0

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
            title = extract_title(content)
            body = strip_markdown(content)
            rel_path = str(fpath.relative_to(ai_dir))
            stat = fpath.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime)
            # tantivy expects RFC3339 datetime
            mtime_rfc = mtime.strftime("%Y-%m-%dT%H:%M:%S+00:00")

            writer.add_document(tantivy.Document(
                title=[title],
                body=[body],
                path=[rel_path],
                size=stat.st_size,
                modified=mtime_rfc,
            ))
            indexed += 1
        except Exception as e:
            errors += 1
            print(f"  WARN: {fpath.name}: {e}")

    writer.commit()
    writer.wait_merging_threads()

    print(f"Index built: {indexed} files indexed, {errors} errors")
    print(f"Location: {index_path}")
    return index


def search_index(ai_dir, query_str, top_k=5):
    """Search the index and return results."""
    sys.stdout.reconfigure(encoding="utf-8")
    index_path = ai_dir / INDEX_DIR_NAME

    if not index_path.exists():
        print("No index found. Building...")
        build_index(ai_dir)

    schema = build_schema()
    index = tantivy.Index(schema, path=str(index_path))
    index.reload()
    searcher = index.searcher()

    # Search in both title (boosted) and body
    query = index.parse_query(query_str, ["title", "body"])
    search_result = searcher.search(query, top_k)

    if not search_result.hits:
        print(f"No results for: {query_str}")
        return []

    results = []
    for score, doc_address in search_result.hits:
        doc = searcher.doc(doc_address)
        try:
            title = doc["title"][0]
        except (KeyError, IndexError):
            title = "(no title)"
        try:
            path = doc["path"][0]
        except (KeyError, IndexError):
            path = "?"
        try:
            size = doc["size"][0]
        except (KeyError, IndexError):
            size = 0

        results.append({
            "score": score,
            "title": title,
            "path": path,
            "size": size,
        })

    # Print results
    print(f"Results for: {query_str}\n")
    for i, r in enumerate(results):
        print(f"  {i+1}. [{r['score']:.2f}] {r['path']}")
        print(f"     {r['title']}")
    print()

    return results


def show_stats(ai_dir):
    """Show index statistics."""
    sys.stdout.reconfigure(encoding="utf-8")
    index_path = ai_dir / INDEX_DIR_NAME

    if not index_path.exists():
        print("No index found. Run --build first.")
        return

    schema = build_schema()
    index = tantivy.Index(schema, path=str(index_path))
    index.reload()
    searcher = index.searcher()

    # Count documents by searching for everything
    query = index.parse_query("*", ["body"])
    all_results = searcher.search(query, 1000)
    doc_count = len(all_results.hits)

    # Collect files to compare
    files = collect_files(ai_dir)

    # Index directory size
    index_size = sum(
        f.stat().st_size for f in index_path.rglob("*") if f.is_file()
    )

    print(f"Index Stats:")
    print(f"  Documents indexed: {doc_count}")
    print(f"  Files on disk:     {len(files)}")
    print(f"  Index size:        {index_size / 1024:.1f} KB")
    print(f"  Index path:        {index_path}")

    if doc_count != len(files):
        print(f"\n  ⚠️  Mismatch: {len(files) - doc_count} files not indexed. "
              f"Run --build to update.")


def main():
    parser = argparse.ArgumentParser(
        description="BM25 local search for _ai_evolution/ markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python local_search.py "session workflow"     # Search for session workflow
  python local_search.py "BM25 search" -k 10   # Top 10 results
  python local_search.py --build                # Build/rebuild index
  python local_search.py --stats                # Show index stats
"""
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("-k", "--top-k", type=int, default=5,
                        help="Number of results (default: 5)")
    parser.add_argument("--build", action="store_true",
                        help="Build/rebuild search index")
    parser.add_argument("--stats", action="store_true",
                        help="Show index statistics")

    args = parser.parse_args()
    ai_dir = find_ai_evolution()

    if args.build:
        build_index(ai_dir, force=True)
    elif args.stats:
        show_stats(ai_dir)
    elif args.query:
        search_index(ai_dir, args.query, args.top_k)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
