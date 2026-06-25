"""
规则提取器单元测试
"""

import sys
from pathlib import Path

# 将项目根目录加入 sys.path，便于导入 scripts 包
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.rule_extractor import (
    is_likely_rule,
    extract_code_blocks,
    extract_rules_from_text,
    extract_rules_from_issue,
)


class TestIsLikelyRule:
    """测试 is_likely_rule 函数"""

    def test_empty_line(self):
        assert is_likely_rule("") is False
        assert is_likely_rule("   ") is False

    def test_comment(self):
        assert is_likely_rule("! 这是注释") is True

    def test_domain_rule(self):
        assert is_likely_rule("||example.com^") is True

    def test_exception_rule(self):
        assert is_likely_rule("@@||example.com^") is True

    def test_element_hiding(self):
        assert is_likely_rule("example.com##.ad-banner") is True

    def test_element_hiding_exception(self):
        assert is_likely_rule("example.com#@#.ad") is True

    def test_inline_script(self):
        assert is_likely_rule("example.com#$#window.adsEnabled = false;") is True

    def test_network_rule_http(self):
        assert is_likely_rule("|http://ads.example.com/") is True
        assert is_likely_rule("|https://tracker.example.com/collect") is True

    def test_rule_with_options(self):
        assert is_likely_rule("||ads.example.com^$script,image") is True

    def test_markdown_heading_skipped(self):
        # 纯 Markdown 标题（非 ## 规则）应被跳过
        assert is_likely_rule("# 标题") is False
        assert is_likely_rule("## 标题") is False  # ## 后面没有选择器

    def test_markdown_heading_with_element_rule(self):
        # ## 出现在后面的应被识别为规则（如 example.com##selector）
        assert is_likely_rule("example.com##.ad") is True

    def test_plain_text_skipped(self):
        assert is_likely_rule("这是一段普通文本") is False
        assert is_likely_rule("hello world") is False


class TestExtractCodeBlocks:
    """测试 extract_code_blocks 函数"""

    def test_backtick_block(self):
        text = "```adblock\n||example.com^\n||ads.com^\n```"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 1
        assert "||example.com^" in blocks[0]
        assert "||ads.com^" in blocks[0]

    def test_tilde_block(self):
        text = "~~~\n||example.com^\n~~~"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 1
        assert "||example.com^" in blocks[0]

    def test_mixed_blocks(self):
        """支持 ``` 和 ~~~ 混合使用"""
        text = "```adblock\n||a.com^\n```\n~~~\n||b.com^\n~~~"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 2

    def test_multiple_backtick_blocks(self):
        text = "```adblock\n||a.com^\n```\n文本\n```\n||b.com^\n```"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 2

    def test_no_code_block(self):
        text = "这是普通文本，没有代码块"
        blocks = extract_code_blocks(text)
        assert blocks == []


class TestExtractRulesFromText:
    """测试 extract_rules_from_text 函数"""

    def test_basic_extraction(self):
        text = "||example.com^\n普通文本\n@@||ads.com^"
        rules = extract_rules_from_text(text)
        assert len(rules) == 2
        assert rules[0] == ("||example.com^", "body")
        assert rules[1] == ("@@||ads.com^", "body")

    def test_deduplication(self):
        text = "||example.com^\n||example.com^\n||example.com^"
        rules = extract_rules_from_text(text)
        assert len(rules) == 1

    def test_custom_source(self):
        text = "||example.com^"
        rules = extract_rules_from_text(text, source="custom")
        assert rules[0] == ("||example.com^", "custom")

    def test_empty_text(self):
        assert extract_rules_from_text("") == []


class TestExtractRulesFromIssue:
    """测试 extract_rules_from_issue 函数"""

    def test_title_only(self):
        rules = extract_rules_from_issue("||example.com^", body=None)
        assert len(rules) == 1
        assert rules[0] == ("||example.com^", "title")

    def test_title_not_rule(self):
        rules = extract_rules_from_issue("拦截广告", body=None)
        assert len(rules) == 0

    def test_body_with_code_block(self):
        body = "说明:\n```adblock\n||example.com^\n||ads.com^\n```"
        rules = extract_rules_from_issue("标题", body=body)
        assert len(rules) == 2
        assert all(src == "body" for _, src in rules)

    def test_body_without_code_block(self):
        body = "||example.com^\n普通说明\n@@||ads.com^"
        rules = extract_rules_from_issue("标题", body=body)
        assert len(rules) == 2

    def test_title_and_body_deduplication(self):
        """标题和正文中的重复规则应去重"""
        rules = extract_rules_from_issue("||example.com^", body="||example.com^\n||other.com^")
        assert len(rules) == 2  # title + other.com
        assert rules[0] == ("||example.com^", "title")

    def test_empty_body(self):
        rules = extract_rules_from_issue("||example.com^", body="")
        assert len(rules) == 1
