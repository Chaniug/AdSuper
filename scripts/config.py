"""
AdSuper 配置中心
集中管理所有可配置常量，支持环境变量覆盖（CI 场景）。
"""

import os
from pathlib import Path

# === 仓库信息（支持环境变量覆盖） ===
REPO_OWNER = os.getenv("REPO_OWNER", "Chaniug")
REPO_NAME = os.getenv("REPO_NAME", "AdSuper")


# === GitHub Issues 标签配置 ===
REQUIRED_LABELS = {"ad", "good"}        # Issue 必须同时拥有这两个标签才会被处理
PROCESSED_LABEL = "processed"           # 处理完成后打上的标记（增量机制）


# === 文件路径（adnew.txt 仍在项目根目录生成） ===
# 项目根目录：config.py 位于 scripts/ 下，向上回溯一层
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE_RULES_FILE = str(PROJECT_ROOT / "AdSuper.txt")   # 基础规则文件（输入）
OUTPUT_FILE = str(PROJECT_ROOT / "adnew.txt")         # 输出规则文件
BACKUP_DIR = str(PROJECT_ROOT / "merged_rules")       # 本地备份目录
