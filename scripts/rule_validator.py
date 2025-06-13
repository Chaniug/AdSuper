import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import datetime

class RuleType(Enum):
    """规则类型枚举"""
    DOMAIN = "domain"      # 域名规则
    ELEMENT = "element"    # 元素规则
    SCRIPT = "script"      # 脚本规则
    IMAGE = "image"        # 图片规则
    EXCEPTION = "exception" # 例外规则
    NETWORK = "network"    # 网络规则
    THIRD_PARTY = "third-party" # 第三方规则
    APP = "app"           # 应用规则
    COMMENT = "comment"    # 注释
    OTHER = "other"       # 其他规则

@dataclass
class Rule:
    """规则数据类"""
    content: str
    type: RuleType
    line_number: int
    description: str = ""
    source: str = ""  # 规则来源（issue编号等）
    created_at: datetime = None

class RuleValidator:
    """规则验证器"""
    
    def __init__(self):
        # 编译正则表达式以提高性能
        self.patterns = {
            RuleType.DOMAIN: re.compile(r'^\|\|[\w.-]+(\^|\$).*$'),
            RuleType.ELEMENT: re.compile(r'^[\w.-]+##.+$'),
            RuleType.SCRIPT: re.compile(r'^\|\|[\w.-]+\$script.*$'),
            RuleType.IMAGE: re.compile(r'^\|\|[\w.-]+\$image.*$'),
            RuleType.EXCEPTION: re.compile(r'^@@.+$'),
            RuleType.NETWORK: re.compile(r'^[\d.]+(\^|\$).*$'),
            RuleType.THIRD_PARTY: re.compile(r'^\|\|[\w.-]+\$third-party.*$'),
            RuleType.APP: re.compile(r'^\|\|[\w.-]+\$app=.*$'),
            RuleType.COMMENT: re.compile(r'^!.*$'),
        }
        
        # 规则优先级顺序
        self.priority_order = [
            RuleType.COMMENT,
            RuleType.EXCEPTION,
            RuleType.DOMAIN,
            RuleType.ELEMENT,
            RuleType.SCRIPT,
            RuleType.IMAGE,
            RuleType.NETWORK,
            RuleType.THIRD_PARTY,
            RuleType.APP,
            RuleType.OTHER
        ]

    def validate_rule(self, rule: str, line_number: int, source: str = "") -> Tuple[bool, str, RuleType]:
        """
        验证单条规则，返回(是否有效, 规则内容, 规则类型)
        """
        rule = rule.strip()
        if not rule:
            return True, "", RuleType.OTHER
            
        # 检查常见格式错误
        if '  ' in rule:  # 多个空格
            return False, f"规则 '{rule}' 包含多个连续空格", RuleType.OTHER
        if rule.startswith('#') and not rule.startswith('##'):  # 无效注释
            return False, f"规则 '{rule}' 使用无效注释格式(应使用##或!)", RuleType.OTHER
            
        # 检查规则类型
        for rule_type, pattern in self.patterns.items():
            if pattern.match(rule):
                return True, rule, rule_type
                
        # 检查其他可能的规则格式
        if rule.startswith('http'):
            return True, rule, RuleType.OTHER
        if ':' in rule and not rule.startswith('||'):
            return True, rule, RuleType.OTHER
        if '/' in rule and not rule.startswith('||'):
            return True, rule, RuleType.OTHER
            
        return False, f"无效的规则格式: {rule}", RuleType.OTHER

    def validate_rules(self, rules: List[str], source: str = "") -> Tuple[List[Rule], List[str]]:
        """
        批量验证规则，返回(有效规则列表, 错误信息列表)
        """
        valid_rules: List[Rule] = []
        errors: List[str] = []
        
        for i, rule in enumerate(rules, 1):
            is_valid, content, rule_type = self.validate_rule(rule, i, source)
            if is_valid and content:
                valid_rules.append(Rule(
                    content=content,
                    type=rule_type,
                    line_number=i,
                    source=source,
                    created_at=datetime.now()
                ))
            elif not is_valid:
                errors.append(f"规则 '{rule}' 格式无效: {content}")
                
        return valid_rules, errors

    def sort_rules(self, rules: List[Rule]) -> List[Rule]:
        """
        按优先级排序规则
        """
        def get_priority(rule: Rule) -> int:
            try:
                return self.priority_order.index(rule.type)
            except ValueError:
                return len(self.priority_order)
                
        return sorted(rules, key=lambda x: (get_priority(x), x.content))

    def check_conflicts(self, rules: List[Rule]) -> List[Tuple[Rule, Rule, str]]:
        """
        检查规则冲突，返回冲突规则对列表
        """
        conflicts = []
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i+1:]:
                if self._is_conflicting(rule1, rule2):
                    conflicts.append((
                        rule1,
                        rule2,
                        f"规则冲突: {rule1.content} 和 {rule2.content}"
                    ))
        return conflicts

    def _is_conflicting(self, rule1: Rule, rule2: Rule) -> bool:
        """
        检查两条规则是否冲突
        """
        # 如果一个是例外规则，一个是普通规则，且匹配相同目标
        if (rule1.type == RuleType.EXCEPTION and rule2.type != RuleType.EXCEPTION) or \
           (rule2.type == RuleType.EXCEPTION and rule1.type != RuleType.EXCEPTION):
            r1 = rule1.content[2:] if rule1.type == RuleType.EXCEPTION else rule1.content
            r2 = rule2.content[2:] if rule2.type == RuleType.EXCEPTION else rule2.content
            return r1 == r2
            
        return False