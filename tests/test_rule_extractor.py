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
    extract_inline_backticks,
    _strip_markdown_decoration,
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

    def test_markdown_image_skipped(self):
        # Markdown 图片语法不应被误识别为规则
        assert is_likely_rule("![screenshot](https://example.com/img.png)") is False

    def test_markdown_link_skipped(self):
        # 整行是 Markdown 链接时不应被误识别
        assert is_likely_rule("[click here](https://example.com)") is False


class TestStripMarkdownDecoration:
    """测试 _strip_markdown_decoration 函数"""

    def test_list_dash_prefix(self):
        assert _strip_markdown_decoration("- ||example.com^") == "||example.com^"

    def test_list_asterisk_prefix(self):
        assert _strip_markdown_decoration("* ||example.com^") == "||example.com^"

    def test_list_plus_prefix(self):
        assert _strip_markdown_decoration("+ ||example.com^") == "||example.com^"

    def test_list_numbered_dot_prefix(self):
        assert _strip_markdown_decoration("1. ||example.com^") == "||example.com^"

    def test_list_numbered_paren_prefix(self):
        assert _strip_markdown_decoration("2) ||example.com^") == "||example.com^"

    def test_blockquote_prefix(self):
        assert _strip_markdown_decoration("> ||example.com^") == "||example.com^"

    def test_inline_backticks_single(self):
        assert _strip_markdown_decoration("`||example.com^`") == "||example.com^"

    def test_inline_backticks_double(self):
        assert _strip_markdown_decoration("``||example.com^``") == "||example.com^"

    def test_no_decoration(self):
        assert _strip_markdown_decoration("||example.com^") == "||example.com^"


class TestExtractInlineBackticks:
    """测试 extract_inline_backticks 函数"""

    def test_single_inline(self):
        result = extract_inline_backticks("规则是 `||example.com^` 请加上")
        assert result == ["||example.com^"]

    def test_multiple_inline(self):
        text = "规则：`||a.com^` 和 `||b.com^`"
        result = extract_inline_backticks(text)
        assert result == ["||a.com^", "||b.com^"]

    def test_no_inline(self):
        assert extract_inline_backticks("普通文本无反引号") == []

    def test_multiline_text(self):
        text = "第一行\n`||a.com^`\n第三行"
        result = extract_inline_backticks(text)
        assert result == ["||a.com^"]


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


class TestNonCompliantSubmissions:
    """测试非规范提交场景（用户不按表单要求）"""

    def test_rules_with_list_dash_prefix(self):
        """用户用 - 列表项包裹规则"""
        body = "- ||example.com^\n- ||ads.com^$third-party\n- example.com##.ad"
        rules = extract_rules_from_issue("规则", body=body)
        assert len(rules) == 3
        assert rules[0] == ("||example.com^", "body")
        assert rules[1] == ("||ads.com^$third-party", "body")
        assert rules[2] == ("example.com##.ad", "body")

    def test_rules_with_numbered_list(self):
        """用户用 1. 2. 3. 编号"""
        body = "1. ||example.com^\n2. ||ads.com^$third-party\n3. example.com##.ad"
        rules = extract_rules_from_issue("规则", body=body)
        assert len(rules) == 3

    def test_rules_with_inline_backticks(self):
        """用户用内联反引号包裹规则"""
        body = "我的规则是 `||example.com^` 请加上"
        rules = extract_rules_from_issue("规则", body=body)
        assert len(rules) == 1
        assert rules[0] == ("||example.com^", "body")

    def test_rules_with_multiple_inline_backticks(self):
        """用户用多个内联反引号"""
        body = "规则：`||a.com^` 和 `||b.com^`"
        rules = extract_rules_from_issue("规则", body=body)
        assert len(rules) == 2

    def test_rules_with_blockquote_prefix(self):
        """用户用 > 引用前缀"""
        body = "> ||example.com^\n> ||ads.com^"
        rules = extract_rules_from_issue("规则", body=body)
        assert len(rules) == 2

    def test_rules_mixed_with_text_no_codeblock(self):
        """规则和说明文字混在一起，无代码块"""
        body = "你好，我想拦截以下域名：\n||example.com^\n还有这个：\n||ads.com^\n谢谢！"
        rules = extract_rules_from_issue("广告规则", body=body)
        assert len(rules) == 2

    def test_markdown_image_not_extracted(self):
        """Markdown 图片语法不应被误识别为规则"""
        body = "请看截图\n![screenshot](https://example.com/img.png)"
        rules = extract_rules_from_issue("广告规则", body=body)
        assert len(rules) == 0

    def test_markdown_link_not_extracted(self):
        """整行 Markdown 链接不应被误识别为规则"""
        body = "[click here](https://example.com)"
        rules = extract_rules_from_issue("广告规则", body=body)
        assert len(rules) == 0

    def test_rules_with_mixed_formats(self):
        """混合格式：代码块 + 内联反引号 + 列表项"""
        body = """代码块：
```
||block.com^
```

内联：`||inline.com^`

列表：
- ||list.com^"""
        rules = extract_rules_from_issue("规则", body=body)
        rule_strings = [r for r, _ in rules]
        assert "||block.com^" in rule_strings
        assert "||inline.com^" in rule_strings
        assert "||list.com^" in rule_strings
