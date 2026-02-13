#!/usr/bin/env python3
"""
Session bootstrap — compact context loader for AI startup.
Reads last_session.md, project_context.md, agent_profile.md
and outputs a compressed summary (~800 tokens vs ~3000 raw).

Usage:
    python _ai_evolution/scripts/session_bootstrap.py

Prerequisites:
    Python 3.8+, no external dependencies.
    Working directory: project root.
"""

import os
import re
import sys
from datetime import datetime


def find_ai_evolution():
    """Find _ai_evolution/ relative to script or cwd."""
    # Try relative to script location first
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ai_dir = os.path.dirname(script_dir)  # scripts/ -> _ai_evolution/
    if os.path.isfile(os.path.join(ai_dir, "last_session.md")):
        return ai_dir
    # Try cwd
    cwd_ai = os.path.join(os.getcwd(), "_ai_evolution")
    if os.path.isfile(os.path.join(cwd_ai, "last_session.md")):
        return cwd_ai
    print("ERROR: Cannot find _ai_evolution/ directory")
    sys.exit(1)


def read_file(path):
    """Read file, return content or empty string."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def extract_section(content, header, max_lines=15):
    """Extract a markdown section by header, limited to max_lines."""
    pattern = rf"^##\s+{re.escape(header)}\s*$"
    lines = content.split("\n")
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line.strip(), re.IGNORECASE):
            start = i + 1
            continue
        if start is not None and line.strip().startswith("## "):
            end = i
            section = lines[start:end]
            break
    else:
        if start is not None:
            section = lines[start:]
        else:
            return ""
    # Strip empty lines at boundaries
    section = [l for l in section if l.strip()]
    if len(section) > max_lines:
        section = section[:max_lines] + [f"  ... ({len(section) - max_lines} more lines)"]
    return "\n".join(section)


def extract_metadata(content):
    """Extract **Key**: Value pairs from top of file."""
    pairs = {}
    for line in content.split("\n")[:10]:
        m = re.match(r"\*\*(.+?)\*\*:\s*(.+)", line.strip())
        if m:
            pairs[m.group(1)] = m.group(2)
    return pairs


def summarize_last_session(content):
    """Compress last_session.md to key facts."""
    meta = extract_metadata(content)
    output = ["## Last Session"]
    if "Date" in meta:
        output.append(f"- Date: {meta['Date']}")
    if "Session Note" in meta:
        output.append(f"- Note: {meta['Session Note']}")

    # Count completed items (### headings under Completed)
    completed_section = extract_section(content, "Completed This Session", max_lines=50)
    completed_count = len(re.findall(r"^###\s", completed_section, re.MULTILINE))
    output.append(f"- Completed: {completed_count} items")

    # Pending items
    pending = extract_section(content, "Pending", max_lines=10)
    if pending:
        output.append("- Pending:")
        for line in pending.split("\n"):
            if line.strip().startswith("- ["):
                output.append(f"  {line.strip()}")

    # Key decisions (compact)
    decisions = extract_section(content, "Key Decisions Made", max_lines=8)
    if decisions:
        output.append("- Key decisions:")
        for line in decisions.split("\n"):
            if line.strip().startswith("- "):
                output.append(f"  {line.strip()}")

    # INDEX stats
    stats = extract_section(content, "Current INDEX Stats", max_lines=8)
    if stats:
        for line in stats.split("\n"):
            if "Total" in line or "total" in line:
                output.append(f"- {line.strip()}")

    return "\n".join(output)


def summarize_project_context(content):
    """Compress project_context.md to essentials."""
    meta = extract_metadata(content)
    output = ["## Project"]

    # Overview
    overview = extract_section(content, "1. Project Overview", max_lines=5)
    for line in overview.split("\n"):
        if "Name" in line or "Goal" in line:
            output.append(f"  {line.strip()}")

    # Tools table
    tools = extract_section(content, "3. My Tools", max_lines=12)
    if tools:
        output.append("- Tools:")
        for line in tools.split("\n"):
            if "|" in line and "---" not in line and "Tool" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    output.append(f"  - {parts[0]}: {parts[1]}")

    return "\n".join(output)


def summarize_agent_profile(content):
    """Compress agent_profile.md to actionable preferences."""
    output = ["## User Prefs"]

    # Environment
    env = extract_section(content, "Environment", max_lines=6)
    if env:
        for line in env.split("\n"):
            if line.strip().startswith("- **"):
                output.append(f"  {line.strip()}")

    # Key behavioral notes
    output.append("- Communication: Chinese explanations, English code")
    output.append("- Style: Direct, no emojis, no baby-talk")
    output.append("- Decision: Anti-blackbox, portability first")
    output.append("- Learning: 分析/为什么→learning mode; 改/更新/跑→exec mode")

    return "\n".join(output)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ai_dir = find_ai_evolution()

    last_session = read_file(os.path.join(ai_dir, "last_session.md"))
    project_ctx = read_file(os.path.join(ai_dir, "project_context.md"))
    agent_prof = read_file(os.path.join(ai_dir, "agent_profile.md"))

    print(f"# Session Bootstrap — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    if last_session:
        print(summarize_last_session(last_session))
    else:
        print("## Last Session\n- No previous session found")
    print()

    if project_ctx:
        print(summarize_project_context(project_ctx))
    else:
        print("## Project\n- No project context found")
    print()

    if agent_prof:
        print(summarize_agent_profile(agent_prof))
    else:
        print("## User Prefs\n- No agent profile found")
    print()


if __name__ == "__main__":
    main()
