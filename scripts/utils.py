import os
from datetime import datetime
from typing import List, Set, Tuple

def load_rules(filename: str) -> Tuple[Set[str], List[str]]:
    """
    加载规则文件，返回规则集合和原始行列表
    """
    if not os.path.exists(filename):
        return set(), []
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    rules = set(line.strip() for line in lines if line.strip() and not line.strip().startswith("!"))
    return rules, lines

def save_rules(filename: str, rules: List[str], header: str = None):
    """
    保存规则到文件，可带header
    """
    with open(filename, "w", encoding="utf-8") as f:
        if header:
            f.write(header + "\n")
        for rule in rules:
            f.write(rule.strip() + "\n")

def deduplicate_rules(rules: List[str]) -> List[str]:
    """
    去重规则，保持顺序
    """
    seen = set()
    result = []
    for rule in rules:
        if rule not in seen:
            seen.add(rule)
            result.append(rule)
    return result

def log(message: str):
    """
    统一日志输出
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def get_today() -> str:
    return datetime.now().strftime("%Y-%m-%d")