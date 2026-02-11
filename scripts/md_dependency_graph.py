#!/usr/bin/env python3
"""
Markdown Dependency Graph Generator

Scans all .md files in a project and generates a dependency graph showing
which files reference which other files via markdown links.

Usage:
    python md_dependency_graph.py [directory] [--format mermaid|csv|json]

## Prerequisites
- **Python Version**: 3.6+ (uses pathlib, typing, f-strings)
- **Dependencies**: None (standard library only)
- **Working Directory**: Should be run from project root, or pass root path
- **OS Compatibility**: Windows/Linux/macOS

## Outputs
- Mermaid diagram (default): paste into any Mermaid-compatible viewer
- CSV: for spreadsheet analysis
- JSON: for programmatic consumption

## Known Limitations
- Only detects [text](path) style links, not raw URLs
- Does not follow links to non-.md files (but records them)
- Ignores code blocks and inline code
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple


class MarkdownDependencyGraph:
    """Builds a dependency graph from markdown file cross-references."""

    def __init__(self, root_dir: str):
        """Initialize graph builder with root directory.

        Args:
            root_dir: Path to the project root directory to scan.
        """
        self.root_dir = Path(root_dir).resolve()
        self.edges: List[Tuple[str, str]] = []  # (source, target)
        self.nodes: Set[str] = set()
        self.orphans: Set[str] = set()  # files with no inbound/outbound links
        self.broken: List[Tuple[str, str]] = []  # (source, broken_target)

        # Match markdown links: [text](path)
        self.link_pattern = re.compile(r'\[([^\]]*)\]\((\.[./\\][^)]+)\)')

        # Skip patterns
        self.ignore_patterns = [
            re.compile(r'^https?://'),
            re.compile(r'^#'),
            re.compile(r'^\[.*\]$'),
        ]

    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern.search(path):
                return True
        return False

    def normalize_path(self, path: str, source_file: Path) -> Path:
        """Resolve a relative path to absolute, relative to source file.

        Args:
            path: Raw path string from markdown link.
            source_file: The file containing the link.

        Returns:
            Resolved absolute Path.
        """
        # Remove anchor
        path = path.split('#')[0]

        # Handle file:// URLs
        if path.startswith('file:///'):
            path = path[8:]
            if os.name == 'nt' and path.startswith('/'):
                path = path[1:]

        path_obj = Path(path)
        if not path_obj.is_absolute():
            path_obj = (source_file.parent / path_obj).resolve()

        return path_obj

    def relative_name(self, abs_path: Path) -> str:
        """Get a short relative name for display.

        Args:
            abs_path: Absolute path to convert.

        Returns:
            Relative path string using forward slashes.
        """
        try:
            return str(abs_path.relative_to(self.root_dir)).replace('\\', '/')
        except ValueError:
            return str(abs_path)

    def scan_file(self, filepath: Path):
        """Extract all markdown links from a single file."""
        try:
            content = filepath.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            return

        source = self.relative_name(filepath)
        self.nodes.add(source)

        # Remove code blocks to avoid false matches
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)

        for line_num, line in enumerate(content.split('\n'), 1):
            for match in self.link_pattern.finditer(line):
                raw_path = match.group(2)
                if self.should_ignore(raw_path):
                    continue

                try:
                    abs_target = self.normalize_path(raw_path, filepath)
                    target = self.relative_name(abs_target)

                    if abs_target.exists():
                        self.nodes.add(target)
                        self.edges.append((source, target))
                    else:
                        self.broken.append((source, raw_path))
                except Exception:
                    pass

    def build(self):
        """Scan all markdown files and build the graph."""
        md_files = list(self.root_dir.rglob('*.md'))

        # Skip hidden directories
        md_files = [f for f in md_files if not any(
            part.startswith('.') for part in f.relative_to(self.root_dir).parts
        )]

        for filepath in md_files:
            self.scan_file(filepath)

        # Find orphans (no edges at all)
        linked_nodes = set()
        for src, tgt in self.edges:
            linked_nodes.add(src)
            linked_nodes.add(tgt)
        self.orphans = self.nodes - linked_nodes

    def to_mermaid(self) -> str:
        """Generate Mermaid flowchart diagram."""
        lines = ['graph LR']

        # Create node IDs (sanitize for Mermaid)
        node_ids = {}
        for i, node in enumerate(sorted(self.nodes)):
            node_id = f'N{i}'
            node_ids[node] = node_id
            # Use basename for readability
            basename = Path(node).name
            lines.append(f'    {node_id}["{basename}"]')

        lines.append('')

        # Add edges
        seen_edges = set()
        for src, tgt in self.edges:
            if src in node_ids and tgt in node_ids:
                edge_key = (src, tgt)
                if edge_key not in seen_edges:
                    seen_edges.add(edge_key)
                    lines.append(f'    {node_ids[src]} --> {node_ids[tgt]}')

        return '\n'.join(lines)

    def to_csv(self) -> str:
        """Generate CSV output."""
        lines = ['source,target']
        seen = set()
        for src, tgt in self.edges:
            key = (src, tgt)
            if key not in seen:
                seen.add(key)
                lines.append(f'"{src}","{tgt}"')
        return '\n'.join(lines)

    def to_json(self) -> str:
        """Generate JSON output."""
        # Deduplicate edges
        unique_edges = list(set(self.edges))
        data = {
            'nodes': sorted(list(self.nodes)),
            'edges': [{'source': s, 'target': t} for s, t in unique_edges],
            'orphans': sorted(list(self.orphans)),
            'broken_links': [{'source': s, 'target': t} for s, t in self.broken],
            'stats': {
                'total_files': len(self.nodes),
                'total_links': len(unique_edges),
                'orphan_files': len(self.orphans),
                'broken_links': len(self.broken),
            }
        }
        return json.dumps(data, indent=2, ensure_ascii=False)

    def summary(self) -> str:
        """Generate a text summary of the graph."""
        unique_edges = set(self.edges)

        # Inbound/outbound counts
        inbound: Dict[str, int] = defaultdict(int)
        outbound: Dict[str, int] = defaultdict(int)
        for src, tgt in unique_edges:
            outbound[src] += 1
            inbound[tgt] += 1

        lines = [
            '=' * 60,
            'Markdown Dependency Graph Report',
            '=' * 60,
            f'Total files scanned: {len(self.nodes)}',
            f'Total cross-references: {len(unique_edges)}',
            f'Orphan files (no links): {len(self.orphans)}',
            f'Broken links: {len(self.broken)}',
            '',
        ]

        # Most referenced files (hubs)
        if inbound:
            lines.append('--- Most Referenced Files (Top 10) ---')
            for node, count in sorted(inbound.items(), key=lambda x: -x[1])[:10]:
                lines.append(f'  {count:3d} ← {node}')
            lines.append('')

        # Most linking files
        if outbound:
            lines.append('--- Files With Most Outbound Links (Top 10) ---')
            for node, count in sorted(outbound.items(), key=lambda x: -x[1])[:10]:
                lines.append(f'  {count:3d} → {node}')
            lines.append('')

        # Orphans
        if self.orphans:
            lines.append('--- Orphan Files (No References) ---')
            for orphan in sorted(self.orphans):
                lines.append(f'  • {orphan}')
            lines.append('')

        # Broken links
        if self.broken:
            lines.append('--- Broken Links ---')
            for src, tgt in self.broken:
                lines.append(f'  {src} → {tgt} (NOT FOUND)')
            lines.append('')

        lines.append('=' * 60)
        return '\n'.join(lines)


def main():
    """CLI entry point. Accepts optional directory path and --format flag."""
    # Parse arguments
    fmt = 'summary'
    root_dir = '.'
    args = sys.argv[1:]

    # Extract --format flag
    if '--format' in args:
        idx = args.index('--format')
        if idx + 1 < len(args):
            fmt = args[idx + 1]
        # Remove --format and its value from args
        args = args[:idx] + args[idx + 2:]

    # Remaining first arg is root_dir
    if args:
        root_dir = args[0]

    graph = MarkdownDependencyGraph(root_dir)
    graph.build()

    if fmt == 'mermaid':
        print(graph.to_mermaid())
    elif fmt == 'csv':
        print(graph.to_csv())
    elif fmt == 'json':
        print(graph.to_json())
    else:
        print(graph.summary())
        print()
        print('Tip: Use --format mermaid|csv|json for exportable output')


if __name__ == '__main__':
    main()
