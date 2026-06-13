#!/usr/bin/env python3
"""
AdSuper 规则验证工具
检查所有已完成的 GitHub Issues 中的规则是否都被包含在 adnew.txt 中
"""

import re
import sys
import os
from pathlib import Path
from typing import Set, Dict, List
import requests
from datetime import datetime

# 导入共享的规则提取模块
from .rule_extractor import extract_rules_from_issue, extract_rules_from_text, extract_code_blocks

class CompletenessValidator:
    def __init__(self, repo_owner: str, repo_name: str):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_base = "https://api.github.com"
        self.rules_file = "adnew.txt"
        # 添加 GitHub API 认证（避免速率限制）
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.headers = {}
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
            print(f"✓ 使用 GitHub 认证")
        else:
            print(f"⚠️  未设置 GITHUB_TOKEN 环境变量，API 调用可能受速率限制")
        
    def get_completed_issues(self) -> List[Dict]:
        """获取所有标记为 completed 的 issues"""
        url = f"{self.api_base}/search/issues"
        params = {
            'q': f'repo:{self.repo_owner}/{self.repo_name} is:issue label:completed',
            'per_page': 100
        }
        
        try:
            # 使用认证 headers（如果可用）
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get('items', [])
        except Exception as e:
            print(f"❌ 获取 Issues 失败: {e}")
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
        """从 adnew.txt 中加载规则"""
        rules = set()
        
        if not Path(self.rules_file).exists():
            print(f"❌ 找不到文件: {self.rules_file}")
            return rules
        
        with open(self.rules_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过注释和空行
                if not line or line.startswith('!'):
                    continue
                rules.add(line)
        
        return rules
    
    def validate(self) -> bool:
        """执行验证"""
        print("🔍 开始验证规则完整性...\n")
        
        # 加载文件中的规则
        file_rules = self.load_rules_from_file()
        print(f"📄 adnew.txt 中找到 {len(file_rules)} 条规则\n")
        
        # 获取所有已完成的 issues
        issues = self.get_completed_issues()
        print(f"📋 找到 {len(issues)} 个已完成的 Issues\n")
        
        # 收集所有 issue 中的规则
        issue_rules: Dict[int, Set[str]] = {}
        for issue in issues:
            issue_num = issue['number']
            body = issue.get('body', '')
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
            print("⚠️  发现遗漏的规则:\n")
            for issue_num, rules in sorted(missing_rules.items()):
                print(f"Issue #{issue_num}:")
                for rule in sorted(rules):
                    print(f"  - {rule}")
                print()
            
            print(f"❌ 共发现 {sum(len(r) for r in missing_rules.values())} 条遗漏的规则")
            return False
        else:
            print("✅ 所有规则都已被正确包含！")
            return True

def main():
    validator = CompletenessValidator("Chaniug", "AdSuper")
    success = validator.validate()
    
    # 生成验证报告
    report_file = "VALIDATION_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# 规则验证报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"验证结果: {'✅ 通过' if success else '❌ 失败'}\n")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
