"""
规则提取模块
提供从文本中提取 adblock 规则的功能。
"""

import re
from typing import List, Optional, Tuple


def is_likely_rule(line: str) -> bool:
    """
    检查一行文本是否可能是 adblock 规则。
    使用宽松的判断，让 RuleValidator 来做精确验证。

    Args:
        line: 要检查的文本行

    Returns:
        是否是可能的规则
    """
    line = line.strip()

    # 跳过空行
    if not line:
        return False

    # 跳过 Markdown 标题（以 # 开头但不是 ## 元素隐藏规则）
    # 注意: 以 # 开头的行不可能以 ! 开头，原逻辑中的
    # `not line.startswith('!')` 是冗余条件，已移除
    if line.startswith('#') and '##' not in line[1:]:
        return False

    # 注释（以 ! 开头）
    if line.startswith('!'):
        return True

    # 元素隐藏规则（包含 ##, #@#, 或 #$#）
    if '##' in line or '#@#' in line or '#$#' in line:
        return True

    # 网络请求规则和例外规则（以 || 或 @@ 开头）
    if line.startswith('||') or line.startswith('@@'):
        return True

    # 其他网络请求规则（以 |http 或 |https 开头）
    if line.startswith('|http') or line.startswith('|https'):
        return True

    # 带选项的规则（包含 $）
    if '$' in line:
        # 检查 $ 前面是否有模式
        dollar_idx = line.find('$')
        if dollar_idx > 0 and not line[:dollar_idx].isspace():
            return True

    return False


def extract_code_blocks(text: str) -> List[str]:
    """
    从文本中提取 Markdown 代码块。
    支持 ``` 和 ~~~ 分隔符，可混合使用。

    Args:
        text: 要提取代码块的文本

    Returns:
        代码块列表（按出现顺序）
    """
    blocks = []

    # 匹配 ``` 代码块
    # 修复: 可选换行，支持不以换行开头/结尾的代码块
    pattern_backticks = r'```[\w]*\n?([\s\S]*?)\n?```'
    for match in re.finditer(pattern_backticks, text):
        blocks.append(match.group(1))

    # 同时匹配 ~~~ 代码块（不再要求 ``` 优先，支持混合使用）
    pattern_tildes = r'~~~[\w]*\n?([\s\S]*?)\n?~~~'
    for match in re.finditer(pattern_tildes, text):
        blocks.append(match.group(1))

    return blocks


def extract_rules_from_text(text: str, source: str = 'body') -> List[Tuple[str, str]]:
    """
    从文本中提取规则（带去重）。

    Args:
        text: 要提取规则的文本
        source: 规则来源（用于标识）

    Returns:
        [(规则文本, 来源)] 列表
    """
    rules: List[Tuple[str, str]] = []
    seen = set()

    for line in text.split('\n'):
        line = line.strip()
        if is_likely_rule(line) and line not in seen:
            seen.add(line)
            rules.append((line, source))

    return rules


def extract_rules_from_issue(title: str, body: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    从 issue 的标题和正文中提取所有广告规则。

    提取优先级: 标题 > 代码块 > 正文全文
    去重逻辑: 后出现的重复规则会被跳过

    Args:
        title: issue 标题
        body: issue 正文（可选）

    Returns:
        [(规则文本, 来源)] 列表，来源为 'title' 或 'body'
    """
    rules: List[Tuple[str, str]] = []
    seen = set()

    def _add_if_new(rule: str, src: str):
        """辅助函数: 去重添加规则"""
        if rule and rule not in seen:
            seen.add(rule)
            rules.append((rule, src))

    # 处理标题
    title = title.strip()
    if is_likely_rule(title):
        _add_if_new(title, 'title')

    # 处理正文
    if body:
        code_blocks = extract_code_blocks(body)

        if code_blocks:
            # 优先从代码块提取
            for block in code_blocks:
                for rule, src in extract_rules_from_text(block, 'body'):
                    _add_if_new(rule, src)
        else:
            # 无代码块时从整个正文提取
            for rule, src in extract_rules_from_text(body, 'body'):
                _add_if_new(rule, src)

    return rules
