#!/usr/bin/env python3
"""
V3.5 结构验证脚本
用于检测文档中的路径引用是否与实际文件系统一致

使用方法:
    python verify_structure.py [目录路径]
    
默认扫描当前目录

## Prerequisites (环境要求)
- **Python Version**: 3.6+ (使用 pathlib, typing, f-strings)
- **Dependencies**: 无外部依赖，仅使用标准库
- **Working Directory**: 应从项目根目录运行，或传入根目录路径
- **OS Compatibility**: Windows/Linux/macOS (自动处理路径分隔符)

## Known Limitations (已知限制)
- 只检查 markdown 链接格式 [text](path)，不检查代码块内路径
- 不验证外部 URL (http/https)
- 不检查锚点链接是否有效 (#section)
- 隐藏目录 (以.开头) 会被跳过

## Outputs (输出)
- Exit code 0: 所有路径有效
- Exit code 1: 发现空引用

## Migration Notes (迁移注意)
当将此脚本迁移到其他项目时：
1. 确认 Python 版本 >= 3.6
2. 路径模式可能需要根据项目约定调整
3. 忽略规则可能需要扩展
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Set

class StructureVerifier:
    def __init__(self, root_dir: str):
        """Initialize verifier with root directory and configure patterns.

        Args:
            root_dir: Path to the project root directory to scan.
        """
        self.root_dir = Path(root_dir).resolve()
        self.issues: List[dict] = []
        self.checked_paths: Set[str] = set()
        
        # 匹配各种路径引用格式 - 只检查实际的 markdown 链接
        self.path_patterns = [
            # Markdown 链接到本地文件: [text](./path) 或 [text](../path)
            r'\[([^\]]*)\]\((\.[./\\][^)]+)\)',
        ]
        
        # 忽略的路径模式
        self.ignore_patterns = [
            r'^https?://',          # URLs
            r'^#',                  # Anchor links
            r'^\[.*\]$',            # Placeholder patterns like [topic]
            r'your_project',        # Example paths
            r'<.*>',                # Template placeholders
        ]
    
    def should_ignore(self, path: str) -> bool:
        """检查路径是否应该被忽略"""
        for pattern in self.ignore_patterns:
            if re.search(pattern, path, re.IGNORECASE):
                return True
        return False
    
    def normalize_path(self, path: str, source_file: Path) -> Path:
        """标准化路径为绝对路径"""
        # 移除 markdown 锚点
        path = path.split('#')[0]
        
        # 处理 file:// URLs
        if path.startswith('file:///'):
            path = path[8:]
            if os.name == 'nt' and path.startswith('/'):
                path = path[1:]  # Windows: /c:/... -> c:/...
        
        path_obj = Path(path)
        
        # 如果是相对路径，相对于源文件解析
        if not path_obj.is_absolute():
            path_obj = (source_file.parent / path_obj).resolve()
        
        return path_obj
    
    def extract_paths_from_file(self, file_path: Path) -> List[Tuple[str, int]]:
        """从文件中提取所有路径引用"""
        paths = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    for pattern in self.path_patterns:
                        matches = re.findall(pattern, line)
                        for match in matches:
                            # 处理元组（链接格式）
                            if isinstance(match, tuple):
                                path = match[1] if len(match) > 1 else match[0]
                            else:
                                path = match
                            
                            path = path.strip()
                            if path and not self.should_ignore(path):
                                paths.append((path, line_num))
        except Exception as e:
            self.issues.append({
                'type': 'error',
                'file': str(file_path),
                'message': f'无法读取文件: {e}'
            })
        
        return paths
    
    def verify_path(self, path: str, line_num: int, source_file: Path) -> bool:
        """验证路径是否存在"""
        try:
            abs_path = self.normalize_path(path, source_file)
            
            # 跳过已检查的路径
            path_key = str(abs_path)
            if path_key in self.checked_paths:
                return True
            self.checked_paths.add(path_key)
            
            # 检查是否在项目目录内
            try:
                abs_path.relative_to(self.root_dir)
            except ValueError:
                # 路径在项目外，跳过
                return True
            
            if not abs_path.exists():
                self.issues.append({
                    'type': 'broken_link',
                    'file': str(source_file.relative_to(self.root_dir)),
                    'line': line_num,
                    'path': path,
                    'expected': str(abs_path)
                })
                return False
            
            return True
        except Exception as e:
            return True  # 解析失败时不报错
    
    def scan_directory(self):
        """扫描目录中的所有 Markdown 文件"""
        md_files = list(self.root_dir.rglob('*.md'))
        
        print(f"扫描目录: {self.root_dir}")
        print(f"找到 {len(md_files)} 个 Markdown 文件\n")
        
        for md_file in md_files:
            # 跳过隐藏目录
            if any(part.startswith('.') for part in md_file.parts):
                continue
            
            paths = self.extract_paths_from_file(md_file)
            for path, line_num in paths:
                self.verify_path(path, line_num, md_file)
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("=" * 60)
        report.append("V3.5 结构验证报告")
        report.append("=" * 60)
        report.append("")
        
        if not self.issues:
            report.append("✅ 未发现问题！所有路径引用均有效。")
        else:
            broken_links = [i for i in self.issues if i['type'] == 'broken_link']
            errors = [i for i in self.issues if i['type'] == 'error']
            
            if broken_links:
                report.append(f"❌ 发现 {len(broken_links)} 个空引用:")
                report.append("")
                for issue in broken_links:
                    report.append(f"  文件: {issue['file']}:{issue['line']}")
                    report.append(f"  引用: {issue['path']}")
                    report.append(f"  预期: {issue['expected']}")
                    report.append("")
            
            if errors:
                report.append(f"⚠️ 发现 {len(errors)} 个错误:")
                report.append("")
                for issue in errors:
                    report.append(f"  文件: {issue['file']}")
                    report.append(f"  消息: {issue['message']}")
                    report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)


def main():
    """CLI entry point. Accepts optional directory path argument."""
    # 确定扫描目录
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        # 默认扫描脚本所在目录的父目录
        root_dir = Path(__file__).parent.parent
    
    verifier = StructureVerifier(root_dir)
    verifier.scan_directory()
    
    report = verifier.generate_report()
    print(report)
    
    # 返回状态码
    sys.exit(1 if verifier.issues else 0)


if __name__ == '__main__':
    main()
