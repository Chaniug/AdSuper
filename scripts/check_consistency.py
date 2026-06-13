#!/usr/bin/env python3
"""
AdSuper 数据一致性检查工具
检查 adnew.txt 和 AdSuper.txt 的数据一致性
"""

import sys
from pathlib import Path
from typing import Set, Dict, List

def load_rules_from_file(filename: str) -> Set[str]:
    """从文件中加载规则（跳过注释和空行）"""
    rules = set()
    comments = []
    
    if not Path(filename).exists():
        print(f"❌ 找不到文件: {filename}")
        return rules
    
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('!'):
                if line.startswith('!'):
                    comments.append(line)
                continue
            rules.add(line)
    
    return rules

def check_consistency():
    """检查 adnew.txt 和 AdSuper.txt 的一致性"""
    print("🔍 开始检查数据一致性...\n")
    
    # 加载两个文件中的规则
    adnew_rules = load_rules_from_file("adnew.txt")
    adsuper_rules = load_rules_from_file("AdSuper.txt")
    
    print(f"📄 adnew.txt 中找到 {len(adnew_rules)} 条规则")
    print(f"📄 AdSuper.txt 中找到 {len(adsuper_rules)} 条规则\n")
    
    # 检查 adnew.txt 是否包含 AdSuper.txt 的所有规则
    missing_in_adnew = adsuper_rules - adnew_rules
    extra_in_adnew = adnew_rules - adsuper_rules
    
    if missing_in_adnew:
        print(f"⚠️  发现 {len(missing_in_adnew)} 条规则在 adnew.txt 中缺失：")
        for rule in sorted(missing_in_adnew):
            print(f"  - {rule}")
        print()
    else:
        print("✅ adnew.txt 包含所有 AdSuper.txt 中的规则\n")
    
    if extra_in_adnew:
        print(f"ℹ️  发现 {len(extra_in_adnew)} 条规则在 adnew.txt 中额外存在：")
        for rule in sorted(extra_in_adnew):
            print(f"  - {rule}")
        print()
    else:
        print("✅ adnew.txt 中没有额外规则\n")
    
    # 总结
    if missing_in_adnew:
        print("❌ 数据不一致：adnew.txt 缺少规则")
        print("建议：运行 sync_issues.py 重新生成 adnew.txt")
        return False
    else:
        print("✅ 数据一致性检查通过！")
        return True

def main():
    success = check_consistency()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
