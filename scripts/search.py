#!/usr/bin/env python3
"""
Batch web search tool — cognitive layering helper.
Searches multiple queries via DuckDuckGo, returns compact results.
Designed to minimize token consumption when AI reads the output.

Usage:
    python search.py "query1" "query2" "query3"
    python search.py --max 3 "single query"          # top 3 results
    python search.py --site github.com "AI memory"    # site-scoped

Prerequisites:
    pip install duckduckgo-search

Output format: structured text, one block per query, ~50-80 tokens per result.
"""

import sys
import argparse
from datetime import datetime

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("ERROR: ddgs not installed.")
        print("Fix:   pip install ddgs")
        sys.exit(1)


def search_one(query: str, max_results: int = 5, site: str = None) -> list[dict]:
    """Search one query, return list of {title, url, snippet}."""
    if site:
        query = f"site:{site} {query}"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")[:200],  # truncate long snippets
            }
            for r in results
        ]
    except Exception as e:
        return [{"title": "SEARCH ERROR", "url": "", "snippet": str(e)}]


def format_results(query: str, results: list[dict]) -> str:
    """Format results as compact text for AI consumption."""
    lines = [f"## Q: {query}", f"   ({len(results)} results, {datetime.now().strftime('%Y-%m-%d %H:%M')})"]
    for i, r in enumerate(results, 1):
        lines.append(f"  {i}. [{r['title']}]")
        lines.append(f"     {r['url']}")
        if r["snippet"]:
            lines.append(f"     > {r['snippet']}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Batch web search — compact output for AI context"
    )
    parser.add_argument("queries", nargs="+", help="Search queries (one per argument)")
    parser.add_argument("--max", type=int, default=5, help="Max results per query (default: 5)")
    parser.add_argument("--site", type=str, default=None, help="Restrict to site (e.g. github.com)")
    args = parser.parse_args()

    print(f"# Search Results — {len(args.queries)} queries")
    print(f"# Site filter: {args.site or 'none'}")
    print()

    for query in args.queries:
        results = search_one(query, max_results=args.max, site=args.site)
        print(format_results(query, results))


if __name__ == "__main__":
    main()
