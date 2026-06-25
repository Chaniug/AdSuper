"""
规则验证器单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.rule_validator import (
    Rule,
    RuleType,
    ValidationErrorType,
    RuleValidator,
)


class TestValidateRule:
    """测试 validate_rule 方法"""

    def setup_method(self):
        self.validator = RuleValidator()

    def test_domain_rule(self):
        result = self.validator.validate_rule("||example.com^")
        assert result.is_valid is True
        assert result.rule_type == RuleType.DOMAIN

    def test_domain_with_options(self):
        result = self.validator.validate_rule("||example.com^$important")
        assert result.is_valid is True
        assert result.rule_type == RuleType.DOMAIN

    def test_exception_rule(self):
        result = self.validator.validate_rule("@@||example.com^$document")
        assert result.is_valid is True
        assert result.rule_type == RuleType.EXCEPTION

    def test_element_rule(self):
        result = self.validator.validate_rule("example.com##.ad-banner")
        assert result.is_valid is True
        assert result.rule_type == RuleType.ELEMENT

    def test_multi_domain_element_rule(self):
        result = self.validator.validate_rule("domain1.com,domain2.com##.ad")
        assert result.is_valid is True
        assert result.rule_type == RuleType.ELEMENT

    def test_script_rule(self):
        result = self.validator.validate_rule("||ads.com^$script")
        assert result.is_valid is True
        assert result.rule_type == RuleType.SCRIPT

    def test_image_rule(self):
        result = self.validator.validate_rule("||ads.com^$image")
        assert result.is_valid is True
        assert result.rule_type == RuleType.IMAGE

    def test_third_party_rule(self):
        result = self.validator.validate_rule("||tracker.com^$third-party")
        assert result.is_valid is True
        assert result.rule_type == RuleType.THIRD_PARTY

    def test_app_rule(self):
        result = self.validator.validate_rule("||example.com^$app=com.test.app")
        assert result.is_valid is True
        assert result.rule_type == RuleType.APP

    def test_network_rule_pipe_http(self):
        result = self.validator.validate_rule("|https://ads.example.com/collect|")
        assert result.is_valid is True
        assert result.rule_type == RuleType.NETWORK

    def test_network_rule_http_url(self):
        result = self.validator.validate_rule("http://ads.example.com/")
        assert result.is_valid is True
        assert result.rule_type == RuleType.NETWORK

    def test_comment_rule(self):
        result = self.validator.validate_rule("! 这是注释")
        assert result.is_valid is True
        assert result.rule_type == RuleType.COMMENT

    def test_pure_domain(self):
        result = self.validator.validate_rule("example.com")
        assert result.is_valid is True
        assert result.rule_type == RuleType.DOMAIN

    def test_pure_domain_new_tld(self):
        """支持新 TLD（如 .photo, .online）"""
        result = self.validator.validate_rule("example.photo")
        assert result.is_valid is True

    def test_regex_rule(self):
        result = self.validator.validate_rule("/banner.*\\.jpg$/")
        assert result.is_valid is True
        assert result.rule_type == RuleType.OTHER

    def test_extra_spaces_error(self):
        result = self.validator.validate_rule("||example.com^  $script")
        assert result.is_valid is False
        assert result.error.error_type == ValidationErrorType.EXTRA_SPACES
        assert result.error.is_format_error is True

    def test_invalid_comment_error(self):
        result = self.validator.validate_rule("# 无效注释")
        assert result.is_valid is False
        assert result.error.error_type == ValidationErrorType.INVALID_COMMENT
        assert result.error.is_format_error is True

    def test_invalid_format_error(self):
        result = self.validator.validate_rule("这只是普通文本")
        assert result.is_valid is False
        assert result.error.error_type == ValidationErrorType.INVALID_FORMAT
        assert result.error.is_format_error is False

    def test_empty_rule(self):
        result = self.validator.validate_rule("")
        assert result.is_valid is True
        assert result.content == ""


class TestValidateRules:
    """测试 validate_rules 批量验证"""

    def setup_method(self):
        self.validator = RuleValidator()

    def test_mixed_rules(self):
        rules = ["||example.com^", "普通文本", "@@||ads.com^"]
        valid, errors = self.validator.validate_rules(rules)
        assert len(valid) == 2
        assert len(errors) == 1
        assert errors[0].error_type == ValidationErrorType.INVALID_FORMAT

    def test_all_valid(self):
        rules = ["||a.com^", "||b.com^"]
        valid, errors = self.validator.validate_rules(rules)
        assert len(valid) == 2
        assert errors == []

    def test_all_invalid(self):
        rules = ["文本1", "文本2"]
        valid, errors = self.validator.validate_rules(rules)
        assert valid == []
        assert len(errors) == 2


class TestSortRules:
    """测试 sort_rules 方法"""

    def setup_method(self):
        self.validator = RuleValidator()

    def test_sort_by_priority(self):
        # 注释应在域名之前
        rules = [
            Rule(content="||a.com^", type=RuleType.DOMAIN, line_number=1),
            Rule(content="! comment", type=RuleType.COMMENT, line_number=2),
        ]
        sorted_rules = self.validator.sort_rules(rules)
        assert sorted_rules[0].type == RuleType.COMMENT
        assert sorted_rules[1].type == RuleType.DOMAIN


class TestCheckConflicts:
    """测试 check_conflicts 方法"""

    def setup_method(self):
        self.validator = RuleValidator()

    def test_conflict_detected(self):
        rules = [
            Rule(content="@@||example.com^", type=RuleType.EXCEPTION, line_number=1),
            Rule(content="||example.com^", type=RuleType.DOMAIN, line_number=2),
        ]
        conflicts = self.validator.check_conflicts(rules)
        assert len(conflicts) == 1

    def test_no_conflict(self):
        rules = [
            Rule(content="||a.com^", type=RuleType.DOMAIN, line_number=1),
            Rule(content="||b.com^", type=RuleType.DOMAIN, line_number=2),
        ]
        conflicts = self.validator.check_conflicts(rules)
        assert conflicts == []
