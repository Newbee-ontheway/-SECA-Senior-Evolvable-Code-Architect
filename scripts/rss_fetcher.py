#!/usr/bin/env python3
"""
RSS Feed Fetcher — data pipeline component for the RSS Briefing skill.
Reads feed sources from a YAML config file, fetches and parses RSS/Atom feeds,
outputs structured data (JSON or human-readable markdown).

Usage:
    python rss_fetcher.py                                   # default config, 7 days
    python rss_fetcher.py --days 1 --json                   # JSON output for AI consumption
    python rss_fetcher.py --config path/to/feeds.yaml       # custom feed source
    python rss_fetcher.py --blog "antirez" --brief          # filter by blog
    python rss_fetcher.py --keyword "AI" --days 3 --brief   # keyword filter
    python rss_fetcher.py --list                            # list configured feeds
    python rss_fetcher.py --tag ai --days 7 --brief         # filter by tag

Config: _ai_evolution/configs/feed_sources.yaml (editable)

Prerequisites:
    pip install feedparser pyyaml
"""

import sys
import os
import json
import argparse
import html
import re
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("ERROR: feedparser not installed. Fix: pip install feedparser", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Fix: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


# ── Default config path (relative to this script) ────────────────────
DEFAULT_CONFIG = Path(__file__).parent.parent / "configs" / "feed_sources.yaml"


def load_feeds(config_path: str | Path) -> tuple[list[dict], str]:
    """Load feed list from YAML config. Returns (feeds, collection_name)."""
    config_path = Path(config_path)
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    collection_name = config.get("name", "Unnamed")
    feeds = config.get("feeds", [])

    if not feeds:
        print(f"ERROR: No feeds found in {config_path}", file=sys.stderr)
        sys.exit(1)

    return feeds, collection_name


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_date(entry) -> datetime | None:
    """Extract published date from a feed entry, return timezone-aware UTC datetime."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                from calendar import timegm
                return datetime.fromtimestamp(timegm(t), tz=timezone.utc)
            except (ValueError, OverflowError):
                continue
    return None


def fetch_feed(feed_info: dict, timeout: int = 15) -> list[dict]:
    """Fetch and parse a single RSS/Atom feed. Returns list of article dicts."""
    name = feed_info["name"]
    url = feed_info["url"]
    tags = feed_info.get("tags", [])

    try:
        parsed = feedparser.parse(url, request_headers={"User-Agent": "RSS-Fetcher/2.0"})
    except Exception as e:
        return [{"_error": True, "blog": name, "message": str(e)}]

    if parsed.bozo and not parsed.entries:
        err = getattr(parsed, "bozo_exception", "Unknown parse error")
        return [{"_error": True, "blog": name, "message": str(err)}]

    articles = []
    for entry in parsed.entries:
        title = entry.get("title", "(no title)")
        link = entry.get("link", "")
        summary_raw = entry.get("summary", "") or entry.get("description", "")
        summary = strip_html(summary_raw)[:300]
        pub_date = parse_date(entry)

        articles.append({
            "_error": False,
            "blog": name,
            "title": title,
            "link": link,
            "summary": summary,
            "tags": tags,
            "date": pub_date,
            "date_str": pub_date.strftime("%Y-%m-%d %H:%M") if pub_date else None,
        })

    return articles


def fetch_all(feeds: list[dict], max_workers: int = 8) -> tuple[list[dict], list[dict]]:
    """Fetch all feeds concurrently. Returns (articles, errors)."""
    articles = []
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(fetch_feed, f): f for f in feeds}
        for future in as_completed(futures):
            feed_info = futures[future]
            try:
                results = future.result()
            except Exception as e:
                errors.append({"blog": feed_info["name"], "message": str(e)})
                continue

            for item in results:
                if item.get("_error"):
                    errors.append(item)
                else:
                    articles.append(item)

    articles.sort(key=lambda a: a["date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return articles, errors


def filter_articles(
    articles: list[dict],
    days: int | None = None,
    keywords: list[str] | None = None,
    blogs: list[str] | None = None,
    tags: list[str] | None = None,
) -> list[dict]:
    """Filter articles by date, keywords, blog name, or tags."""
    result = articles

    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        result = [a for a in result if a["date"] and a["date"] >= cutoff]

    if blogs:
        blogs_lower = [b.lower() for b in blogs]
        result = [a for a in result if a["blog"].lower() in blogs_lower]

    if tags:
        tags_lower = [t.lower() for t in tags]
        result = [a for a in result if any(t.lower() in tags_lower for t in a.get("tags", []))]

    if keywords:
        keywords_lower = [k.lower() for k in keywords]
        def matches(article):
            text = f"{article['title']} {article['summary']}".lower()
            return any(kw in text for kw in keywords_lower)
        result = [a for a in result if matches(a)]

    return result


# ── Output Formatters ─────────────────────────────────────────────────

def format_json(articles: list[dict], errors: list[dict], collection_name: str) -> str:
    """JSON output for AI consumption."""
    # Strip non-serializable datetime objects
    serializable = []
    for a in articles:
        item = {k: v for k, v in a.items() if k != "date" and k != "_error"}
        serializable.append(item)

    output = {
        "collection": collection_name,
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "article_count": len(serializable),
        "articles": serializable,
        "errors": [{"blog": e.get("blog", "?"), "message": e.get("message", "")} for e in errors],
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


def format_brief(articles: list[dict]) -> str:
    """Compact output — one line per article."""
    lines = [f"# RSS Feed — {len(articles)} articles", ""]
    for a in articles:
        date_str = a["date"].strftime("%m-%d") if a["date"] else "??"
        tag_str = f" [{', '.join(a.get('tags', [])[:2])}]" if a.get("tags") else ""
        lines.append(f"- [{date_str}] **{a['blog']}**: {a['title']}{tag_str}")
        lines.append(f"  {a['link']}")
    return "\n".join(lines)


def format_full(articles: list[dict]) -> str:
    """Full output with summaries, grouped by date."""
    lines = [f"# RSS Feed — {len(articles)} articles",
             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]

    current_date = None
    for a in articles:
        date_str = a["date"].strftime("%Y-%m-%d") if a["date"] else "Unknown date"
        day_str = a["date"].strftime("%Y-%m-%d") if a["date"] else None

        if day_str != current_date:
            current_date = day_str
            lines.append(f"## {date_str}")
            lines.append("")

        tag_str = f" `{'` `'.join(a.get('tags', []))}`" if a.get("tags") else ""
        lines.append(f"### {a['title']}")
        lines.append(f"**{a['blog']}** — {date_str}{tag_str}")
        if a["summary"]:
            lines.append(f"> {a['summary'][:200]}")
        lines.append(f"Link: {a['link']}")
        lines.append("")

    return "\n".join(lines)


def format_list(feeds: list[dict], collection_name: str) -> str:
    """List all configured feeds."""
    lines = [f"# {collection_name}", ""]
    lines.append("| # | Blog | Tags | RSS URL |")
    lines.append("|---|------|------|---------|")
    for i, f in enumerate(feeds, 1):
        tags = ", ".join(f.get("tags", []))
        lines.append(f"| {i} | {f['name']} | {tags} | {f['url']} |")
    lines.append(f"\nTotal: {len(feeds)} feeds")
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch RSS feeds and output structured data for AI or human consumption"
    )
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG),
                        help=f"Path to feed sources YAML (default: {DEFAULT_CONFIG})")
    parser.add_argument("--days", type=int, default=None,
                        help="Only show articles from the last N days")
    parser.add_argument("--blog", action="append", default=None,
                        help="Filter by blog name (repeatable, case-insensitive)")
    parser.add_argument("--tag", action="append", default=None,
                        help="Filter by tag (repeatable)")
    parser.add_argument("--keyword", action="append", default=None,
                        help="Filter by keyword in title/summary (repeatable)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON (for AI pipeline consumption)")
    parser.add_argument("--brief", action="store_true",
                        help="Compact markdown output (one line per article)")
    parser.add_argument("--save", type=str, default=None,
                        help="Save output to file")
    parser.add_argument("--list", action="store_true",
                        help="List configured feeds and exit")
    parser.add_argument("--workers", type=int, default=8,
                        help="Concurrent fetch threads (default: 8)")

    args = parser.parse_args()

    # Load config
    feeds, collection_name = load_feeds(args.config)

    # --list mode
    if args.list:
        print(format_list(feeds, collection_name))
        return

    # Pre-filter feeds by blog name (optimization: don't fetch unneeded feeds)
    feeds_to_fetch = feeds
    if args.blog:
        blogs_lower = [b.lower() for b in args.blog]
        feeds_to_fetch = [f for f in feeds if f["name"].lower() in blogs_lower]
        if not feeds_to_fetch:
            print(f"ERROR: No matching blogs for: {args.blog}", file=sys.stderr)
            print("Use --list to see available blogs.", file=sys.stderr)
            sys.exit(1)

    if args.tag:
        tags_lower = [t.lower() for t in args.tag]
        feeds_to_fetch = [f for f in feeds_to_fetch
                          if any(t.lower() in tags_lower for t in f.get("tags", []))]
        if not feeds_to_fetch:
            print(f"ERROR: No feeds match tags: {args.tag}", file=sys.stderr)
            sys.exit(1)

    # Fetch
    print(f"Fetching {len(feeds_to_fetch)} feeds...", file=sys.stderr)
    articles, errors = fetch_all(feeds_to_fetch, max_workers=args.workers)

    # Report errors
    if errors:
        print(f"\n⚠ {len(errors)} feed(s) had issues:", file=sys.stderr)
        for e in errors:
            print(f"  - {e.get('blog', '?')}: {e.get('message', 'unknown')}", file=sys.stderr)
        print(file=sys.stderr)

    # Filter
    articles = filter_articles(articles, days=args.days, keywords=args.keyword, tags=None)

    if not articles:
        if args.json:
            print(format_json([], errors, collection_name))
        else:
            print("No articles found matching your filters.")
        return

    # Format
    if args.json:
        output = format_json(articles, errors, collection_name)
    elif args.brief:
        output = format_brief(articles)
    else:
        output = format_full(articles)

    print(output)

    # Save
    if args.save:
        with open(args.save, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n✅ Saved to {args.save}", file=sys.stderr)

    # Stats (non-JSON mode)
    if not args.json:
        blogs_seen = set(a["blog"] for a in articles)
        print(f"\n📊 {len(articles)} articles from {len(blogs_seen)} blogs", file=sys.stderr)


if __name__ == "__main__":
    main()
