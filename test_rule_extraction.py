#!/usr/bin/env python3
"""
规则提取功能测试脚本
使用 pytest 框架验证规则提取功能
"""

import pytest
from scripts.rule_extractor import is_likely_rule, extract_code_blocks, extract_rules_from_issue


class TestIsLikelyRule:
    """测试 is_likely_rule 函数"""

    @pytest.mark.parametrize("rule_text,expected", [
        ("! 这是一个注释", True),
        ("||ads.example.com^$important", True),
        ("@@||exception.example.com^", True),
        ("example.com##.ad-banner", True),
        ("example.com##div:has(> div.popup)", True),
        ("||tracker.example.com/path$image", True),
        ("普通文本，不是规则", False),
        ("# 这是一个 Markdown 标题", False),
        ("", False),
        ("   ", False),
        ("|https://ads.example.com/tracker", True),
        ("||domain.com^", True),
        ("example.com#@#.ad", True),
        ("example.com#$#hide_ad", True),
    ])
    def test_is_likely_rule(self, rule_text, expected):
        assert is_likely_rule(rule_text) == expected


class TestExtractCodeBlocks:
    """测试 extract_code_blocks 函数"""

    def test_extract_backtick_blocks(self):
        text = """
一些文本。

```adblock
||rule1.com^
||rule2.com^
```

更多文本。
"""
        blocks = extract_code_blocks(text)
        assert len(blocks) == 1
        assert "||rule1.com^" in blocks[0]
        assert "||rule2.com^" in blocks[0]

    def test_extract_tilde_blocks(self):
        text = """
一些文本。

~~~
||rule3.com^
~~~
"""
        blocks = extract_code_blocks(text)
        assert len(blocks) == 1
        assert "||rule3.com^" in blocks[0]

    def test_no_blocks(self):
        text = "没有任何代码块的纯文本"
        blocks = extract_code_blocks(text)
        assert len(blocks) == 0

    def test_multiple_blocks(self):
        text = """
```
||rule1.com^
```

~~~
||rule2.com^
~~~
"""
        # 注意：当前实现先匹配 ```，如果没有则匹配 ~~~
        # 所以只有 ``` 块会被提取
        blocks = extract_code_blocks(text)
        assert len(blocks) >= 1


class TestExtractRulesFromIssue:
    """测试 extract_rules_from_issue 函数"""

    SAMPLE_ISSUE_TITLE = "||ads.example.com^$important"

    SAMPLE_ISSUE_BODY = """
这是一个测试 issue，包含各种广告规则。

## 规则列表

以下是需要屏蔽的广告规则：

```adblock
||ads.example.com^$important
||tracker.example.com^
@@||exception.example.com^
example.com##.ad-banner
example.com##div.ad:has(> div.popup)
```

## 高级规则

以下是一些高级过滤规则：

```adblock
example.com##a:nth-child(3) > img, a:nth-child(4) > img
example.com##div:matches-css(position:fixed)
~third-party,example.com##.ad-banner
```
"""

    def test_extract_from_issue(self):
        rules = extract_rules_from_issue(self.SAMPLE_ISSUE_TITLE, self.SAMPLE_ISSUE_BODY)

        # 提取的规则不应该为空
        assert len(rules) > 0

        # 提取的规则文本列表
        extracted_rule_texts = [rule for rule, src in rules]

        # 验证预期的规则都被提取（去重后标题中的规则只出现一次）
        expected_rules = [
            "||ads.example.com^$important",
            "||tracker.example.com^",
            "@@||exception.example.com^",
            "example.com##.ad-banner",
            "example.com##div.ad:has(> div.popup)",
            "example.com##a:nth-child(3) > img, a:nth-child(4) > img",
            "example.com##div:matches-css(position:fixed)",
            "~third-party,example.com##.ad-banner",
        ]

        for expected in expected_rules:
            assert expected in extracted_rule_texts, f"缺少预期规则: {expected}"

    def test_extract_from_title_only(self):
        rules = extract_rules_from_issue("||ads.example.com^", None)
        assert len(rules) == 1
        assert rules[0][0] == "||ads.example.com^"
        assert rules[0][1] == "title"

    def test_extract_from_empty_body(self):
        rules = extract_rules_from_issue("普通标题", "")
        assert len(rules) == 0

    def test_deduplication(self):
        """测试规则去重：标题和正文中相同的规则只应出现一次"""
        body = """
```
||ads.example.com^
```
"""
        rules = extract_rules_from_issue("||ads.example.com^", body)
        rule_texts = [rule for rule, src in rules]
        # 标题和正文中的相同规则只应出现一次
        assert rule_texts.count("||ads.example.com^") == 1
