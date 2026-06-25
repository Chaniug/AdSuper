"""
规则提取模块
提供从文本中提取 adblock 规则的功能。
"""

import re
from typing import List, Optional, Tuple


# Markdown 列表项前缀正则：- / * / + / 1. / 2) 等
_LIST_PREFIX_RE = re.compile(r'^\s*([-*+]|\d+[.)])\s+')

# Markdown 图片语法 ![alt](url)
_MARKDOWN_IMAGE_RE = re.compile(r'^!\[.*?\]\(.*?\)')

# Markdown 链接语法 [text](url) —— 整行都是链接的情况
_MARKDOWN_LINK_RE = re.compile(r'^\[.*?\]\(.*?\)$')


def _strip_markdown_decoration(line: str) -> str:
    """
    剥离行首/行尾的 Markdown 装饰，露出可能的真实规则。

    处理:
    - 列表项前缀: "- ||xxx^" -> "||xxx^", "1. ||xxx^" -> "||xxx^"
    - 行首/行尾单反引号: "`||xxx^`" -> "||xxx^"
    - 行首/行尾双反引号: "``||xxx^``" -> "||xxx^"
    - 行首 > 引用: "> ||xxx^" -> "||xxx^"

    注意: 只剥一层装饰，避免过度处理。
    """
    line = line.strip()

    # 剥列表项前缀
    line = _LIST_PREFIX_RE.sub('', line, count=1)
    line = line.strip()

    # 剥引用前缀
    if line.startswith('>'):
        line = line.lstrip('>').strip()

    # 剥首尾反引号（1 或 2 个）
    line = re.sub(r'^`{1,2}(.*?)`{1,2}$', r'\1', line)

    return line


def is_likely_rule(line: str) -> bool:
    """
    检查一行文本是否可能是 adblock 规则。
    使用宽松的判断，让 RuleValidator 来做精确验证。

    Args:
        line: 要检查的文本行（调用方应先 strip）

    Returns:
        是否是可能的规则
    """
    line = line.strip()

    # 跳过空行
    if not line:
        return False

    # 跳过 Markdown 标题（以 # 开头但不是 ## 元素隐藏规则）
    if line.startswith('#') and '##' not in line[1:]:
        return False

    # 跳过 Markdown 图片语法 ![alt](url)
    if _MARKDOWN_IMAGE_RE.match(line):
        return False

    # 跳过整行都是 Markdown 链接 [text](url)
    if _MARKDOWN_LINK_RE.match(line):
        return False

    # 注释（以 ! 开头）
    if line.startswith('!'):
        return True

    # 元素隐藏规则（domain##selector / domain#@#selector / domain#$#selector）
    # 注意: ## 前面必须是域名，避免 ### xxx 这种 Markdown 标题被误判
    if re.search(r'^[\w.-]+(##|#@#|#\$#).+', line):
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


def extract_inline_backticks(text: str) -> List[str]:
    """
    提取内联反引号包裹的内容（如 `||example.com^`）。

    用于识别用户在段落中用单反引号包裹的规则。
    不会匹配多行代码块（那是 extract_code_blocks 的职责）。

    Args:
        text: 要提取的文本

    Returns:
        反引号内联内容列表
    """
    # 匹配单反引号内联代码（不跨行），排除已经被三反引号代码块匹配的部分
    # 简单实现: 找所有 `xxx` 模式，xxx 不含反引号和换行
    return re.findall(r'`([^`\n]+)`', text)


def extract_rules_from_text(
    text: str, source: str = 'body'
) -> List[Tuple[str, str]]:
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

    for raw_line in text.split('\n'):
        # 预处理: 剥离 Markdown 装饰（列表前缀、反引号、引用前缀）
        line = _strip_markdown_decoration(raw_line)
        if is_likely_rule(line) and line not in seen:
            seen.add(line)
            rules.append((line, source))

    return rules


def extract_rules_from_issue(
    title: str, body: Optional[str] = None
) -> List[Tuple[str, str]]:
    """
    从 issue 的标题和正文中提取所有广告规则。

    提取优先级: 标题 > 代码块 > 内联反引号 > 正文全文
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

    # 处理标题（标题里的列表前缀/反引号少见，但仍然预处理）
    title = _strip_markdown_decoration(title)
    if is_likely_rule(title):
        _add_if_new(title, 'title')

    # 处理正文
    if body:
        # 先尝试代码块（优先级最高）
        code_blocks = extract_code_blocks(body)

        if code_blocks:
            # 从代码块提取
            for block in code_blocks:
                for rule, src in extract_rules_from_text(block, 'body'):
                    _add_if_new(rule, src)

        # 扫描内联反引号（中等优先级，无论是否有代码块都扫描）
        for inline_content in extract_inline_backticks(body):
            cleaned = _strip_markdown_decoration(inline_content)
            if is_likely_rule(cleaned):
                _add_if_new(cleaned, 'body')

        # 兜底: 从整个正文按行提取
        # 即使有代码块也走全文扫描，因为代码块外可能还有规则
        # （如代码块里 3 条，代码块外又用列表项加了 2 条）
        # 去重由 _add_if_new 保证不会重复
        for rule, src in extract_rules_from_text(body, 'body'):
            _add_if_new(rule, src)

    return rules
