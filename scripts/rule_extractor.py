"""
规则提取模块
提供从文本中提取 adblock 规则的功能
"""

import re
from typing import List, Tuple


def is_likely_rule(line: str) -> bool:
    """
    检查一行文本是否可能是 adblock 规则。
    使用宽松的判断，让 RuleValidator 来做精确验证。
    
    Args:
        line: 要检查的文本行
        
    Returns:
        是否是可能的规则
    """
    if not line:
        return False
    
    line = line.strip()
    
    # 跳过空行
    if not line:
        return False
    
    # 跳过 Markdown 标题（以 # 开头且不是 ## 规则）
    if line.startswith('#') and not line.startswith('!') and '##' not in line[1:]:
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
    支持 ``` 和 ~~~ 分隔符。
    
    Args:
        text: 要提取代码块的文本
        
    Returns:
        代码块列表
    """
    blocks = []
    
    # 匹配 ``` 代码块
    pattern_backticks = r'```[\w]*\n([\s\S]*?)\n```'
    for match in re.finditer(pattern_backticks, text):
        blocks.append(match.group(1))
    
    # 如果没有找到 ``` 代码块，尝试 ~~~ 代码块
    if not blocks:
        pattern_tildes = r'~~~\n([\s\S]*?)\n~~~'
        for match in re.finditer(pattern_tildes, text):
            blocks.append(match.group(1))
    
    return blocks


def extract_rules_from_text(text: str, source: str = 'body') -> List[Tuple[str, str]]:
    """
    从文本中提取规则。
    
    Args:
        text: 要提取规则的文本
        source: 规则来源（用于标识）
        
    Returns:
        [(规则文本, 来源)] 列表
    """
    rules = []
    seen = set()
    
    for line in text.split('\n'):
        line = line.strip()
        if is_likely_rule(line):
            if line and line not in seen:
                seen.add(line)
                rules.append((line, source))
    
    return rules


def extract_rules_from_issue(title: str, body: str = None) -> List[Tuple[str, str]]:
    """
    从 issue 的标题和正文中提取所有广告规则。
    
    Args:
        title: issue 标题
        body: issue 正文（可选）
        
    Returns:
        [(规则文本, 来源)] 列表，来源为 'title' 或 'body'
    """
    rules = []
    seen = set()
    
    # 处理标题
    title = title.strip()
    if is_likely_rule(title):
        if title not in seen:
            seen.add(title)
            rules.append((title, 'title'))
    
    # 处理正文
    if body:
        # 首先尝试从 Markdown 代码块中提取
        code_blocks = extract_code_blocks(body)
        
        if code_blocks:
            # 从代码块中提取
            for block in code_blocks:
                block_rules = extract_rules_from_text(block, 'body')
                for rule, src in block_rules:
                    if rule not in seen:
                        seen.add(rule)
                        rules.append((rule, src))
        else:
            # 从整个正文中提取
            body_rules = extract_rules_from_text(body, 'body')
            for rule, src in body_rules:
                if rule not in seen:
                    seen.add(rule)
                    rules.append((rule, src))
    
    return rules
