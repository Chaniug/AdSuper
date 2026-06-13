#!/usr/bin/env python3
"""
规则提取功能测试脚本
用于验证修复后的规则提取功能
"""

from scripts.rule_extractor import is_likely_rule, extract_code_blocks, extract_rules_from_issue

# 测试数据：模拟 issue 内容
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

def test_is_likely_rule():
    """测试 is_likely_rule 函数"""
    print("=" * 60)
    print("测试 is_likely_rule 函数")
    print("=" * 60)
    
    test_cases = [
        # (规则文本, 期望结果)
        ("! 这是一个注释", True),
        ("||ads.example.com^$important", True),
        ("@@||exception.example.com^", True),
        ("example.com##.ad-banner", True),
        ("example.com##div:has(> div.popup)", True),
        ("||tracker.example.com/path$image", True),
        ("普通文本，不是规则", False),
        ("# 这是一个 Markdown 标题", False),
        ("", False),
    ]
    
    passed = 0
    failed = 0
    
    for rule_text, expected in test_cases:
        result = is_likely_rule(rule_text)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} '{rule_text}' -> {result} (期望: {expected})")
    
    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_extract_code_blocks():
    """测试 extract_code_blocks 函数"""
    print("\n" + "=" * 60)
    print("测试 extract_code_blocks 函数")
    print("=" * 60)
    
    test_text = """
    这是一些文本。
    
    ```adblock
    ||rule1.com^
    ||rule2.com^
    ```
    
    更多文本。
    
    ~~~
    ||rule3.com^
    ~~~
    """
    
    blocks = extract_code_blocks(test_text)
    
    print(f"找到 {len(blocks)} 个代码块:")
    for i, block in enumerate(blocks, 1):
        print(f"\n代码块 {i}:")
        print(block)
    
    return len(blocks) > 0


def test_extract_rules_from_issue():
    """测试 extract_rules_from_issue 函数"""
    print("\n" + "=" * 60)
    print("测试 extract_rules_from_issue 函数")
    print("=" * 60)
    
    rules = extract_rules_from_issue(SAMPLE_ISSUE_TITLE, SAMPLE_ISSUE_BODY)
    
    print(f"提取到 {len(rules)} 条规则:")
    for i, (rule, source) in enumerate(rules, 1):
        print(f"{i}. [{source}] {rule}")
    
    # 验证是否提取了所有预期的规则
    expected_rules = [
        "||ads.example.com^$important",
        "||ads.example.com^$important",
        "||tracker.example.com^",
        "@@||exception.example.com^",
        "example.com##.ad-banner",
        "example.com##div.ad:has(> div.popup)",
        "example.com##a:nth-child(3) > img, a:nth-child(4) > img",
        "example.com##div:matches-css(position:fixed)",
        "~third-party,example.com##.ad-banner",
    ]
    
    print(f"\n预期规则数: {len(expected_rules)}")
    print(f"实际提取规则数: {len(rules)}")
    
    # 检查是否所有预期规则都被提取
    extracted_rule_texts = [rule for rule, src in rules]
    missing = [rule for rule in expected_rules if rule not in extracted_rule_texts]
    
    if missing:
        print(f"\n⚠️  遗漏的规则:")
        for rule in missing:
            print(f"  - {rule}")
        return False
    else:
        print(f"\n✅ 所有预期规则都被正确提取!")
        return True


def main():
    """主测试函数"""
    print("=" * 60)
    print("规则提取功能测试")
    print("=" * 60)
    
    results = []
    
    # 测试 is_likely_rule
    results.append(test_is_likely_rule())
    
    # 测试 extract_code_blocks
    results.append(test_extract_code_blocks())
    
    # 测试 extract_rules_from_issue
    results.append(test_extract_rules_from_issue())
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"通过: {passed}/{total} 个测试")
    
    if all(results):
        print("\n✅ 所有测试通过!")
        return 0
    else:
        print("\n❌ 部分测试失败!")
        return 1


if __name__ == "__main__":
    exit(main())
