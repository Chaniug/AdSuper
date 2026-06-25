"""
规则验证器
提供 adblock 规则的格式验证、类型分类、冲突检测和排序功能。
"""

import re
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from datetime import datetime


class RuleType(Enum):
    """规则类型枚举"""
    DOMAIN = "domain"          # 域名规则
    ELEMENT = "element"        # 元素规则
    SCRIPT = "script"          # 脚本规则
    IMAGE = "image"            # 图片规则
    EXCEPTION = "exception"    # 例外规则
    NETWORK = "network"        # 网络规则
    THIRD_PARTY = "third-party"  # 第三方规则
    APP = "app"                # 应用规则
    COMMENT = "comment"        # 注释
    OTHER = "other"            # 其他规则


class ValidationErrorType(Enum):
    """验证错误类型（结构化分类，供调用方精确处理）"""
    EXTRA_SPACES = "extra_spaces"        # 格式错误: 多余空格（可自动修复）
    INVALID_COMMENT = "invalid_comment"  # 格式错误: 无效注释（可自动修复）
    INVALID_FORMAT = "invalid_format"    # 内容错误: 无效规则格式（跳过）


@dataclass
class Rule:
    """规则数据类"""
    content: str
    type: RuleType
    line_number: int
    description: str = ""
    source: str = ""
    created_at: Optional[datetime] = None


@dataclass
class ValidationError:
    """验证错误（结构化，替代字符串匹配）"""
    rule: str
    error_type: ValidationErrorType
    message: str

    @property
    def is_format_error(self) -> bool:
        """是否为可修复的格式错误（vs 内容错误）"""
        return self.error_type in (
            ValidationErrorType.EXTRA_SPACES,
            ValidationErrorType.INVALID_COMMENT,
        )


@dataclass
class ValidationResult:
    """单条规则验证结果"""
    is_valid: bool
    content: str
    rule_type: RuleType
    error: Optional[ValidationError] = None


class RuleValidator:
    """规则验证器"""

    def __init__(self):
        # AdBlock 规则格式说明：
        # - ||domain^ : 域名规则，^ 表示域名结束
        # - ||domain$filter : 带选项的域名规则，$ 是选项分隔符
        # - domain##selector : 元素隐藏规则
        # - domain1,domain2##selector : 多域名元素规则
        self.patterns = {
            # 注意: 顺序很重要！更具体的类型必须在前，否则会被通用模式抢先匹配
            # SCRIPT: ||domain$script (必须先于 DOMAIN)
            RuleType.SCRIPT: re.compile(r'^\|\|[^\s]+\$script'),
            # IMAGE: ||domain$image (必须先于 DOMAIN)
            RuleType.IMAGE: re.compile(r'^\|\|[^\s]+\$image'),
            # THIRD_PARTY: ||domain$third-party (必须先于 DOMAIN)
            RuleType.THIRD_PARTY: re.compile(r'^\|\|[^\s]+\$third-party'),
            # APP: ||domain$app=com.example (必须先于 DOMAIN)
            RuleType.APP: re.compile(r'^\|\|[^\s]+\$app=.+'),
            # EXCEPTION: @@开头的例外规则
            RuleType.EXCEPTION: re.compile(r'^@@.+'),
            # DOMAIN: ||domain^ 或 ||domain^$option 或 ||domain$option
            # 注意: 放在具体类型之后，作为带 $ 选项规则的兜底
            RuleType.DOMAIN: re.compile(r'^\|\|[^\s^]+(\^(\$.+)?|\$.+)?$'),
            # ELEMENT: 支持单域名和多域名格式 (domain1,domain2##selector)
            RuleType.ELEMENT: re.compile(r'^([\w.-]+,)*[\w.-]+##.+'),
            # NETWORK: 网络规则 (如 ||domain/path 或 |http://...)
            RuleType.NETWORK: re.compile(r'^(\|\|[^\s]+\/|[|]https?://).*'),
            # COMMENT: 以 ! 开头的注释行
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
            RuleType.OTHER,
        ]

    def validate_rule(self, rule: str, line_number: int = 0, source: str = "") -> ValidationResult:
        """
        验证单条规则，返回结构化结果。

        Args:
            rule: 规则文本
            line_number: 行号
            source: 来源标识

        Returns:
            ValidationResult: 包含 is_valid/content/rule_type/error
        """
        rule = rule.strip()
        if not rule:
            return ValidationResult(True, "", RuleType.OTHER)

        # 检查格式错误（可修复类）
        if '  ' in rule:  # 多个连续空格
            err = ValidationError(
                rule=rule,
                error_type=ValidationErrorType.EXTRA_SPACES,
                message=f"规则 '{rule}' 包含多个连续空格",
            )
            return ValidationResult(False, err.message, RuleType.OTHER, err)

        if rule.startswith('#') and not rule.startswith('##'):  # 无效注释
            err = ValidationError(
                rule=rule,
                error_type=ValidationErrorType.INVALID_COMMENT,
                message=f"规则 '{rule}' 使用无效注释格式(应使用##或!)",
            )
            return ValidationResult(False, err.message, RuleType.OTHER, err)

        # 检查规则类型
        for rule_type, pattern in self.patterns.items():
            if pattern.match(rule):
                return ValidationResult(True, rule, rule_type)

        # 兜底匹配
        # 仅接受以 http(s):// 开头的完整 URL 规则
        if rule.startswith(('http://', 'https://')):
            return ValidationResult(True, rule, RuleType.NETWORK)
        # 接受正则表达式规则（以 / 开头和结尾）
        if rule.startswith('/') and rule.endswith('/'):
            return ValidationResult(True, rule, RuleType.OTHER)
        # 接受纯域名规则（放宽 TLD 限制，支持新 TLD 如 .photo/.online）
        if re.match(r'^[\w.-]+\.[a-zA-Z]{2,}$', rule):
            return ValidationResult(True, rule, RuleType.DOMAIN)

        # 无效规则格式
        err = ValidationError(
            rule=rule,
            error_type=ValidationErrorType.INVALID_FORMAT,
            message=f"无效的规则格式: {rule}",
        )
        return ValidationResult(False, err.message, RuleType.OTHER, err)

    def validate_rules(self, rules: List[str], source: str = "") -> Tuple[List[Rule], List[ValidationError]]:
        """
        批量验证规则。

        Args:
            rules: 规则字符串列表
            source: 来源标识

        Returns:
            (valid_rules, errors): 有效 Rule 对象列表 + 错误列表
        """
        valid_rules: List[Rule] = []
        errors: List[ValidationError] = []

        for i, rule in enumerate(rules, 1):
            result = self.validate_rule(rule, i, source)
            if result.is_valid and result.content:
                valid_rules.append(Rule(
                    content=result.content,
                    type=result.rule_type,
                    line_number=i,
                    source=source,
                    created_at=datetime.now(),
                ))
            elif not result.is_valid and result.error:
                errors.append(result.error)

        return valid_rules, errors

    def sort_rules(self, rules: List[Rule]) -> List[Rule]:
        """按优先级排序规则。"""
        def get_priority(rule: Rule) -> int:
            try:
                return self.priority_order.index(rule.type)
            except ValueError:
                return len(self.priority_order)

        return sorted(rules, key=lambda x: (get_priority(x), x.content))

    def check_conflicts(self, rules: List[Rule]) -> List[Tuple[Rule, Rule, str]]:
        """
        检查规则冲突（例外规则 vs 普通规则）。
        时间复杂度: O(n)
        """
        conflicts = []
        exception_rules = {}  # key: 去掉@@前缀的内容
        normal_rules = {}

        for rule in rules:
            if rule.type == RuleType.EXCEPTION:
                key = rule.content[2:] if rule.content.startswith('@@') else rule.content
                exception_rules[key] = rule
            else:
                normal_rules[rule.content] = rule

        for exc_content, exception_rule in exception_rules.items():
            if exc_content in normal_rules:
                normal_rule = normal_rules[exc_content]
                conflicts.append((
                    exception_rule,
                    normal_rule,
                    f"规则冲突: {exception_rule.content} 和 {normal_rule.content} "
                    f"(例外规则会禁用普通规则)"
                ))

        return conflicts
