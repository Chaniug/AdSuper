"""
AdSuper 核心脚本包

模块说明:
- config: 配置中心（仓库、标签、文件路径）
- sync_issues: 主入口，从 GitHub Issues 同步规则
- rule_extractor: 从 Issue 文本中提取广告规则
- rule_validator: 规则格式验证、冲突检测、排序
- rule_manager: 规则加载、合并、保存（原子写入）
- utils: 日志、重试、GitHub API 限速处理
"""

__version__ = "2.0.0"
