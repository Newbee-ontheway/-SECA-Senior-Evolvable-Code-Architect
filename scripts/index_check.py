#!/usr/bin/env python3
"""
Index consistency checker — scans _ai_evolution/ index files
and reports which ones need updating.

Checks:
  1. Last Updated date vs today
  2. Scripts in scripts/ not listed in project_context.md tools table
  3. Workflows not listed in project_context.md
  4. Skills count consistency

Usage:
    python _ai_evolution/scripts/index_check.py

Prerequisites:
    Python 3.8+, no external dependencies.
    Working directory: project root.
"""

import os
import re
import sys
from datetime import datetime, timedelta


def find_ai_evolution():
    """Find _ai_evolution/ relative to script or cwd."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ai_dir = os.path.dirname(script_dir)
    if os.path.isfile(os.path.join(ai_dir, "last_session.md")):
        return ai_dir
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


def check_last_updated(content, filename):
    """Check Last Updated date, warn if older than 2 days."""
    m = re.search(r"\*\*Last Updated\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
    if not m:
        return f"⚠️  {filename} — no 'Last Updated' date found"

    try:
        last_date = datetime.strptime(m.group(1), "%Y-%m-%d")
        days_ago = (datetime.now() - last_date).days
        if days_ago <= 1:
            return f"✅ {filename} — updated {m.group(1)} (today/yesterday)"
        elif days_ago <= 3:
            return f"⚠️  {filename} — updated {m.group(1)} ({days_ago} days ago)"
        else:
            return f"❌ {filename} — updated {m.group(1)} ({days_ago} days ago — stale)"
    except ValueError:
        return f"⚠️  {filename} — invalid date format: {m.group(1)}"


def check_scripts_in_context(ai_dir):
    """Check if all scripts are listed in project_context.md."""
    scripts_dir = os.path.join(ai_dir, "scripts")
    if not os.path.isdir(scripts_dir):
        return []

    # Get actual scripts (exclude __pycache__, .pyc)
    actual_scripts = sorted([
        f for f in os.listdir(scripts_dir)
        if f.endswith(".py") and not f.startswith("__")
    ])

    # Read project_context.md and check for mentions
    ctx = read_file(os.path.join(ai_dir, "project_context.md"))
    missing = []
    for script in actual_scripts:
        if script not in ctx:
            missing.append(script)

    return missing


def check_workflows_in_context(ai_dir):
    """Check if all workflows are listed in project_context.md."""
    wf_dir = os.path.join(ai_dir, "workflows")
    if not os.path.isdir(wf_dir):
        return []

    actual_wfs = sorted([
        f for f in os.listdir(wf_dir)
        if f.endswith(".md")
    ])

    ctx = read_file(os.path.join(ai_dir, "project_context.md"))
    missing = []
    for wf in actual_wfs:
        name = wf.replace(".md", "")
        if name not in ctx:
            missing.append(wf)

    return missing


def count_skills(ai_dir):
    """Count skills in skills.md by counting ### headers in Skills section."""
    content = read_file(os.path.join(ai_dir, "skills.md"))
    # Count ### N. headers (skill entries)
    skills = re.findall(r"^### \d+\.", content, re.MULTILINE)
    return len(skills)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ai_dir = find_ai_evolution()
    today = datetime.now().strftime("%Y-%m-%d")

    print(f"# Index Consistency Check — {today}")
    print()

    # 1. Check Last Updated dates
    print("## Date Freshness")
    index_files = [
        ("project_context.md", "project_context.md"),
        ("skills.md", "skills.md"),
        ("lessons_learned.md", "lessons_learned.md"),
        ("agent_profile.md", "agent_profile.md"),
    ]
    for filename, _ in index_files:
        content = read_file(os.path.join(ai_dir, filename))
        if content:
            print(check_last_updated(content, filename))
        else:
            print(f"❌ {filename} — file not found")
    print()

    # 2. Check scripts coverage
    print("## Script Coverage (in project_context.md)")
    missing_scripts = check_scripts_in_context(ai_dir)
    if missing_scripts:
        for s in missing_scripts:
            print(f"⚠️  {s} — not listed in project_context.md")
    else:
        print("✅ All scripts listed")
    print()

    # 3. Check workflows coverage
    print("## Workflow Coverage (in project_context.md)")
    missing_wfs = check_workflows_in_context(ai_dir)
    if missing_wfs:
        for w in missing_wfs:
            print(f"⚠️  {w} — not listed in project_context.md")
    else:
        print("✅ All workflows listed")
    print()

    # 4. Skills count
    print("## Skills Summary")
    skill_count = count_skills(ai_dir)
    print(f"Skills in skills.md: {skill_count}")

    # Count scripts
    scripts_dir = os.path.join(ai_dir, "scripts")
    if os.path.isdir(scripts_dir):
        script_count = len([
            f for f in os.listdir(scripts_dir)
            if f.endswith(".py") and not f.startswith("__")
        ])
        print(f"Scripts in scripts/: {script_count}")

    # Count workflows
    wf_dir = os.path.join(ai_dir, "workflows")
    if os.path.isdir(wf_dir):
        wf_count = len([f for f in os.listdir(wf_dir) if f.endswith(".md")])
        print(f"Workflows in workflows/: {wf_count}")
    print()

    # Summary
    issues = len(missing_scripts) + len(missing_wfs)
    for filename, _ in index_files:
        content = read_file(os.path.join(ai_dir, filename))
        m = re.search(r"\*\*Last Updated\*\*:\s*(\d{4}-\d{2}-\d{2})", content)
        if m:
            try:
                days = (datetime.now() - datetime.strptime(m.group(1), "%Y-%m-%d")).days
                if days > 3:
                    issues += 1
            except ValueError:
                pass

    if issues == 0:
        print("✅ All indices consistent")
    else:
        print(f"⚠️  {issues} issue(s) found — review above")


if __name__ == "__main__":
    main()
