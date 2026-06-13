#!/usr/bin/env python3
"""
AdSuper 统一验证工具
合并了原 check_consistency.py 和 validate_rules.py 的功能

功能:
1. 一致性检查: 比较 adnew.txt 和 AdSuper.txt
2. 完整性验证: 检查 GitHub Issues 中的规则是否都在 adnew.txt 中
"""

import re
import sys
import os
import argparse
from pathlib import Path
from typing import Set, Dict, List
from datetime import datetime
from github import Github

# 导入共享的规则提取模块
from .rule_extractor import extract_rules_from_text
# 导入工具函数
from .utils import log, retry_on_exception, is_github_api_error_retryable, load_rules_from_file


class ConsistencyChecker:
    """一致性检查器 - 检查 adnew.txt 和 AdSuper.txt 的一致性"""
    
    def __init__(self, file1: str = "adnew.txt", file2: str = "AdSuper.txt"):
        self.file1 = file1
        self.file2 = file2
    
    def load_rules(self, filename: str) -> Set[str]:
        """从文件中加载规则（跳过注释和空行）- 使用公共函数"""
        return load_rules_from_file(filename, skip_comments=True)
    
    def check(self) -> bool:
        """执行一致性检查"""
        log("🔍 开始一致性检查 (adnew.txt vs AdSuper.txt)...", "INFO")
        
        # 加载两个文件中的规则
        rules1 = self.load_rules(self.file1)
        rules2 = self.load_rules(self.file2)
        
        log(f"📄 {self.file1} 中找到 {len(rules1)} 条规则", "INFO")
        log(f"📄 {self.file2} 中找到 {len(rules2)} 条规则", "INFO")
        
        # 检查差异
        missing_in_file1 = rules2 - rules1
        extra_in_file1 = rules1 - rules2
        
        if missing_in_file1:
            log(f"⚠️  发现 {len(missing_in_file1)} 条规则在 {self.file1} 中缺失：", "WARNING")
            for rule in sorted(missing_in_file1):
                log(f"  - {rule}", "WARNING")
        else:
            log(f"✅ {self.file1} 包含所有 {self.file2} 中的规则", "INFO")
        
        if extra_in_file1:
            log(f"ℹ️  发现 {len(extra_in_file1)} 条规则在 {self.file1} 中额外存在：", "INFO")
            for rule in sorted(extra_in_file1):
                log(f"  - {rule}", "INFO")
        else:
            log(f"✅ {self.file1} 中没有额外规则", "INFO")
        
        # 总结
        if missing_in_file1:
            log("❌ 一致性检查失败：文件不一致", "ERROR")
            log("建议：运行 sync_issues.py 重新生成 adnew.txt", "INFO")
            return False
        else:
            log("✅ 一致性检查通过！", "INFO")
            return True


class CompletenessValidator:
    """完整性验证器 - 检查 GitHub Issues 规则是否都在 adnew.txt 中"""
    
    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.rules_file = "adnew.txt"
        # 使用 PyGithub（统一 API 调用方式）
        self.github_token = os.getenv('GITHUB_TOKEN')
        if self.github_token:
            self.github = Github(self.github_token)
            log(f"✓ 使用 GitHub 认证", "INFO")
        else:
            self.github = Github()
            log(f"⚠️  未设置 GITHUB_TOKEN 环境变量，API 调用可能受速率限制", "WARNING")
        
        # 获取仓库对象
        try:
            self.repo = self.github.get_repo(f"{repo_owner}/{repo_name}")
        except Exception as e:
            log(f"❌ 无法访问仓库 {repo_owner}/{repo_name}: {e}", "ERROR")
            self.repo = None
    
    @retry_on_exception(max_retries=3, exceptions=(Exception,), should_retry=is_github_api_error_retryable)
    def get_completed_issues(self) -> List:
        """获取所有标记为 completed 的 issues（使用 PyGithub）"""
        if not self.repo:
            log("❌ 仓库对象未初始化", "ERROR")
            return []
        
        try:
            # 使用 PyGithub 搜索 API
            query = f"repo:{self.repo_owner}/{self.repo_name} is:issue label:completed"
            issues = self.github.search_issues(query)
            
            # 转换为列表（PyGithub 返回的是 PaginatedList）
            issues_list = list(issues)
            log(f"找到 {len(issues_list)} 个已完成的 Issues", "INFO")
            return issues_list
        except Exception as e:
            log(f"❌ 获取 Issues 失败: {e}", "ERROR")
            return []
    
    def extract_rules_from_issue_body(self, body: str) -> Set[str]:
        """从 Issue 描述中提取规则（使用共享模块）"""
        if not body:
            return set()
        
        # 使用共享模块提取规则
        rules_list = extract_rules_from_text(body, 'body')
        
        # 转换为集合
        rules = set()
        for rule, src in rules_list:
            rules.add(rule)
        
        return rules
    
    def load_rules_from_file(self) -> Set[str]:
        """从 adnew.txt 中加载规则 - 使用公共函数"""
        return load_rules_from_file(self.rules_file, skip_comments=True)
    
    def validate(self) -> bool:
        """执行验证"""
        log("🔍 开始完整性验证 (GitHub Issues vs adnew.txt)...", "INFO")
        
        # 加载文件中的规则
        file_rules = self.load_rules_from_file()
        log(f"📄 {self.rules_file} 中找到 {len(file_rules)} 条规则", "INFO")
        
        # 获取所有已完成的 issues
        issues = self.get_completed_issues()
        log(f"📋 找到 {len(issues)} 个已完成的 Issues", "INFO")
        
        # 收集所有 issue 中的规则
        issue_rules: Dict[int, Set[str]] = {}
        for issue in issues:
            issue_num = issue.number
            body = issue.body or ''
            rules = self.extract_rules_from_issue_body(body)
            if rules:
                issue_rules[issue_num] = rules
        
        # 检查遗漏的规则
        missing_rules: Dict[int, Set[str]] = {}
        for issue_num, rules in issue_rules.items():
            missing = rules - file_rules
            if missing:
                missing_rules[issue_num] = missing
        
        # 输出结果
        if missing_rules:
            log("⚠️  发现遗漏的规则:", "WARNING")
            for issue_num, rules in sorted(missing_rules.items()):
                log(f"Issue #{issue_num}:", "WARNING")
                for rule in sorted(rules):
                    log(f"  - {rule}", "WARNING")
            
            total_missing = sum(len(r) for r in missing_rules.values())
            log(f"❌ 共发现 {total_missing} 条遗漏的规则", "ERROR")
            return False
        else:
            log("✅ 所有规则都已被正确包含！", "INFO")
            return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AdSuper 统一验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行一致性检查
  python scripts/validation.py --mode consistency
  
  # 运行完整性验证
  python scripts/validation.py --mode completeness
  
  # 运行所有检查
  python scripts/validation.py --mode all
        """
    )
    parser.add_argument(
        '--mode',
        choices=['consistency', 'completeness', 'all'],
        default='all',
        help='验证模式: consistency=一致性检查, completeness=完整性验证, all=全部'
    )
    parser.add_argument(
        '--repo-owner',
        default='Chaniug',
        help='GitHub 仓库所有者 (默认: Chaniug)'
    )
    parser.add_argument(
        '--repo-name',
        default='AdSuper',
        help='GitHub 仓库名称 (默认: AdSuper)'
    )
    
    args = parser.parse_args()
    
    # 记录结果
    results = []
    
    # 一致性检查
    if args.mode in ['consistency', 'all']:
        log("=" * 60, "INFO")
        log("执行一致性检查", "INFO")
        log("=" * 60, "INFO")
        
        checker = ConsistencyChecker()
        success = checker.check()
        results.append(('一致性检查', success))
        
        log("", "INFO")
    
    # 完整性验证
    if args.mode in ['completeness', 'all']:
        log("=" * 60, "INFO")
        log("执行完整性验证", "INFO")
        log("=" * 60, "INFO")
        
        validator = CompletenessValidator(args.repo_owner, args.repo_name)
        success = validator.validate()
        results.append(('完整性验证', success))
        
        log("", "INFO")
    
    # 生成报告
    if len(results) > 1:
        log("=" * 60, "INFO")
        log("验证总结", "INFO")
        log("=" * 60, "INFO")
        
        all_passed = True
        for name, success in results:
            status = "✅ 通过" if success else "❌ 失败"
            log(f"{name}: {status}", "INFO")
            if not success:
                all_passed = False
        
        log("", "INFO")
        
        # 生成报告文件
        report_file = "VALIDATION_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"# 验证报告\n\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## 结果\n\n")
            for name, success in results:
                status = "✅ 通过" if success else "❌ 失败"
                f.write(f"- {name}: {status}\n")
            f.write(f"\n## 总结\n\n")
            status_text = "✅ 全部通过" if all_passed else "❌ 存在失败"
            f.write(f"总体结果: {status_text}\n")
        
        # 返回退出码
        sys.exit(0 if all_passed else 1)
    else:
        # 单个检查，直接返回结果
        _, success = results[0]
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
