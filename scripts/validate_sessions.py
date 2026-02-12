#!/usr/bin/env python3
"""
Session Note Validator — 确定性校验脚本

用法: python validate_sessions.py [project_dir]
默认: session_notes/projects/001-textbook/

校验内容:
1. 从所有 pm 文件提取 "## 规则 N" 编号
2. 从 summary 文件提取表格中的规则编号
3. 对比是否一致（漏了？多了？编号不连续？）
4. 从 SESSION_INDEX 提取规则范围，验证是否匹配
"""

import os
import re
import sys
from pathlib import Path


def extract_rules_from_pm(filepath: Path) -> list[int]:
    """从 pm 文件中提取所有 '## 规则 N' 的编号"""
    rules = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^##\s+规则\s+(\d+)", line)
            if match:
                rules.append(int(match.group(1)))
    return sorted(rules)


def extract_rules_from_summary(filepath: Path) -> list[int]:
    """从 summary 表格中提取 '| N |' 开头的规则编号"""
    rules = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = re.match(r"^\|\s*(\d+)\s*\|", line)
            if match:
                rules.append(int(match.group(1)))
    return sorted(rules)


def extract_range_from_index(filepath: Path) -> dict[str, tuple[int, int]]:
    """从 SESSION_INDEX 提取每个日期的规则范围"""
    ranges = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            match = re.search(
                r"\[(\d{4}-\d{2}-\d{2})\].*规则\s+(\d+)-(\d+)", line
            )
            if match:
                date = match.group(1)
                ranges[date] = (int(match.group(2)), int(match.group(3)))
    return ranges


def validate(project_dir: str):
    project_path = Path(project_dir)
    errors = []
    warnings = []

    # 1. 收集所有 pm 文件中的规则
    pm_files = sorted(project_path.glob("*-pm*.md"))
    pm_files += sorted(project_path.glob("*-late*.md"))
    pm_files = [f for f in pm_files if "summary" not in f.name]

    all_pm_rules = {}  # date -> [rule_numbers]
    all_rules = []

    for f in pm_files:
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        if not date_match:
            continue
        date = date_match.group(1)
        rules = extract_rules_from_pm(f)
        if rules:
            if date not in all_pm_rules:
                all_pm_rules[date] = []
            all_pm_rules[date].extend(rules)
            all_rules.extend(rules)
            print(f"  📄 {f.name}: 规则 {rules}")

    all_rules = sorted(set(all_rules))
    print(f"\n📊 PM 文件中共发现 {len(all_rules)} 条规则: {all_rules}")

    # 2. 检查编号连续性
    if all_rules:
        expected = list(range(all_rules[0], all_rules[-1] + 1))
        missing = set(expected) - set(all_rules)
        if missing:
            errors.append(f"❌ 规则编号不连续! 缺少: {sorted(missing)}")

    # 3. 对比 summary 文件
    summary_files = sorted(project_path.glob("*-summary.md"))
    for sf in summary_files:
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", sf.name)
        if not date_match:
            continue
        date = date_match.group(1)
        summary_rules = extract_rules_from_summary(sf)
        pm_rules = sorted(set(all_pm_rules.get(date, [])))

        print(f"\n📋 {sf.name}:")
        print(f"   Summary 中: {summary_rules}")
        print(f"   PM 文件中:  {pm_rules}")

        missing_in_summary = set(pm_rules) - set(summary_rules)
        extra_in_summary = set(summary_rules) - set(pm_rules)

        if missing_in_summary:
            errors.append(
                f"❌ {sf.name}: Summary 漏了规则 {sorted(missing_in_summary)}"
            )
        if extra_in_summary:
            errors.append(
                f"❌ {sf.name}: Summary 多了规则 {sorted(extra_in_summary)}"
            )
        if not missing_in_summary and not extra_in_summary:
            print("   ✅ 一致")

    # 4. 对比 SESSION_INDEX
    index_file = project_path / "SESSION_INDEX.md"
    if index_file.exists():
        index_ranges = extract_range_from_index(index_file)
        print(f"\n📚 SESSION_INDEX.md 规则范围:")
        for date, (start, end) in index_ranges.items():
            pm_rules = sorted(set(all_pm_rules.get(date, [])))
            if pm_rules:
                actual_start, actual_end = pm_rules[0], pm_rules[-1]
                status = "✅" if (start == actual_start and end == actual_end) else "❌"
                print(f"   {date}: INDEX 说 {start}-{end}, 实际 {actual_start}-{actual_end} {status}")
                if status == "❌":
                    errors.append(
                        f"❌ SESSION_INDEX {date}: 范围 {start}-{end} 与实际 {actual_start}-{actual_end} 不符"
                    )

    # 5. 输出结果
    print("\n" + "=" * 50)
    if errors:
        print(f"🚨 发现 {len(errors)} 个错误:")
        for e in errors:
            print(f"   {e}")
    else:
        print("✅ 所有校验通过!")

    if warnings:
        print(f"\n⚠️ {len(warnings)} 个警告:")
        for w in warnings:
            print(f"   {w}")

    return len(errors)


if __name__ == "__main__":
    default_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "session_notes", "projects", "001-textbook"
    )
    project_dir = sys.argv[1] if len(sys.argv) > 1 else default_dir
    print(f"🔍 校验目录: {project_dir}\n")
    exit_code = validate(project_dir)
    sys.exit(exit_code)
