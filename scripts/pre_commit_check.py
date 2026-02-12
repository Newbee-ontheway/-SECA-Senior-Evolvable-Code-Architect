#!/usr/bin/env python3
"""
Pre-commit Hook — unified entry point for commit-time checks.

Usage: python pre_commit_check.py [--project-root DIR]
Default project root: two levels up from this script.

Checks:
  1. validate_sessions.py — rule numbering consistency
  2. check_file_size.py — 400-line threshold
  3. last_session.md timestamp — warn if stale (>24h)

Exit code: 0 = pass, 1 = blocked (validation/size errors)
Note: stale timestamp is WARNING only, does not block commit.

Design principles:
  - Read-only: never modifies any files
  - Bypassable: git commit --no-verify
  - Fast: <3s target, no AI API calls
"""

import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def get_project_root() -> Path:
    """Resolve project root: --project-root flag or two levels up."""
    if "--project-root" in sys.argv:
        idx = sys.argv.index("--project-root")
        if idx + 1 < len(sys.argv):
            return Path(sys.argv[idx + 1])
    # Default: ../../ from _ai_evolution/scripts/
    return Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).parent


def run_check(script: Path, args: list[str]) -> tuple[int, str]:
    """Run a Python check script, capture output and return code."""
    cmd = [sys.executable, str(script)] + args
    # Force UTF-8 encoding for subprocesses to avoid GBK crash on Windows
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=10, env=env, encoding="utf-8"
    )
    output = result.stdout + result.stderr
    return result.returncode, output.strip()


def check_timestamp_staleness(project_root: Path) -> tuple[bool, str]:
    """
    Check if last_session.md timestamp is older than 24 hours.
    Returns (is_stale, message).
    """
    last_session = project_root / "_ai_evolution" / "last_session.md"
    if not last_session.exists():
        return False, "last_session.md not found — skipping timestamp check"

    with open(last_session, "r", encoding="utf-8") as f:
        for line in f:
            # Match: **Date**: 2026-02-13 凌晨 02:30
            match = re.search(r"\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})", line)
            if match:
                date_str = match.group(1)
                try:
                    last_date = datetime.strptime(date_str, "%Y-%m-%d")
                    age = datetime.now() - last_date
                    if age > timedelta(hours=24):
                        days = age.days
                        return True, (
                            f"last_session.md last updated {date_str} "
                            f"({days} day(s) ago) — consider updating before commit"
                        )
                    else:
                        return False, f"last_session.md timestamp OK ({date_str})"
                except ValueError:
                    return False, f"Could not parse date: {date_str}"

    return False, "No **Date** field found in last_session.md"


def main():
    project_root = get_project_root()
    scripts_dir = project_root / "_ai_evolution" / "scripts"
    blocked = False

    print("=" * 50)
    print("  SECA Pre-commit Checks")
    print("=" * 50)

    # --- Check 1: validate_sessions.py ---
    print("\n[1/3] Session validation...")
    validate_script = scripts_dir / "validate_sessions.py"
    if validate_script.exists():
        ret, output = run_check(validate_script, [])
        if ret != 0:
            print(f"  BLOCKED — validation errors found:")
            for line in output.splitlines():
                print(f"    {line}")
            blocked = True
        else:
            # Only show the summary line, not all the detail
            for line in output.splitlines():
                if "校验通过" in line or "错误" in line:
                    print(f"  {line}")
                    break
            else:
                print("  OK")
    else:
        print(f"  SKIP — {validate_script} not found")

    # --- Check 2: check_file_size.py ---
    print("\n[2/3] File size check (400-line threshold)...")
    size_script = scripts_dir / "check_file_size.py"
    if size_script.exists():
        ret, output = run_check(size_script, [str(project_root)])
        if ret != 0:
            print(f"  BLOCKED — oversized files found:")
            for line in output.splitlines():
                print(f"    {line}")
            blocked = True
        else:
            print(f"  {output.splitlines()[-1] if output else 'OK'}")
    else:
        print(f"  SKIP — {size_script} not found")

    # --- Check 3: last_session.md timestamp ---
    print("\n[3/3] Session timestamp freshness...")
    is_stale, msg = check_timestamp_staleness(project_root)
    if is_stale:
        print(f"  WARNING — {msg}")
        # Warning only, does NOT block commit
    else:
        print(f"  {msg}")

    # --- Result ---
    print("\n" + "=" * 50)
    if blocked:
        print("COMMIT BLOCKED — fix errors above, or use: git commit --no-verify")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
