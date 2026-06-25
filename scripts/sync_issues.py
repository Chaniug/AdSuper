"""
AdSuper 规则同步主模块
从 GitHub Issues 中提取广告规则，验证后合并到 adnew.txt。

运行方式:
    python -m scripts.sync_issues
"""

import os
import sys
import traceback
from typing import List

from github import Github

from . import config
from .rule_validator import RuleValidator, Rule
from .rule_manager import RuleManager
from .rule_extractor import extract_rules_from_issue
from .utils import (
    log,
    setup_logging,
    retry_on_exception,
    is_github_api_error_retryable,
    handle_github_rate_limit,
)


@retry_on_exception(
    max_retries=3,
    exceptions=(Exception,),
    should_retry=is_github_api_error_retryable,
)
def get_github_repo():
    """连接 GitHub API 并返回仓库对象。

    Returns:
        (repo, repo_full_name, github_client) 元组
    Raises:
        RuntimeError: 无法访问仓库时抛出（由调用方决定如何退出）
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        log("⚠️  未设置 GITHUB_TOKEN 环境变量，API 调用可能受速率限制", "WARNING")

    g = Github(token)
    repo_full_name = f"{config.REPO_OWNER}/{config.REPO_NAME}"
    try:
        repo = g.get_repo(repo_full_name)
        log(f"✓ 成功连接仓库: {repo_full_name}", "INFO")
        return repo, repo_full_name, g
    except Exception as e:
        msg = f"无法访问仓库 {repo_full_name}，请检查仓库名和 GITHUB_TOKEN 权限"
        log(f"❌ {msg}: {e}", "ERROR")
        raise RuntimeError(msg) from e


@retry_on_exception(
    max_retries=3,
    exceptions=(Exception,),
    should_retry=is_github_api_error_retryable,
)
def get_filtered_issues(repo, g, required_labels):
    """使用 GitHub 搜索 API 获取候选 Issues。

    注意：不使用 -label:processed 预过滤，因为 GitHub 搜索 API 对
    "曾经有过 processed 标签、后被删除"的 Issue 索引更新不及时，会导致
    误排除。改为只搜必需标签，由 issue_has_required_labels() 在本地
    二次校验 processed 标记。
    失败时降级为获取所有已关闭 Issue 并本地过滤。
    """
    labels_query = " ".join([f"label:{label}" for label in required_labels])
    query = (
        f"repo:{config.REPO_OWNER}/{config.REPO_NAME} is:issue is:closed "
        f"{labels_query}"
    )

    try:
        issues = g.search_issues(query)
        log(f"搜索查询: {query}", "DEBUG")
        log(f"找到 {issues.totalCount} 个候选 issues（含已处理，将在本地过滤）", "INFO")
        return issues
    except Exception as e:
        log(f"搜索 issues 失败: {e}", "WARNING")
        log("降级方案：获取所有已关闭的 issues 并在本地过滤...", "WARNING")
        return repo.get_issues(state="closed")


def issue_has_required_labels(issue, required_labels):
    """检查 issue 是否有所需标签。

    注意：不再检查 processed 标签（已废弃增量机制）。
    现在每次运行都会重新处理所有带必需标签的已关闭 Issue。
    """
    issue_labels = {label.name for label in issue.labels}
    return required_labels.issubset(issue_labels)


def ensure_adnew_exists():
    """确保 adnew.txt 文件存在（首次运行时创建空文件）。"""
    if not os.path.exists(config.OUTPUT_FILE):
        with open(config.OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("! 自动生成的空 adnew.txt\n")
        log(f"✓ 已创建空的 {config.OUTPUT_FILE}", "INFO")


def main():
    """主流程：从 GitHub Issues 同步规则到 adnew.txt。"""
    # 初始化日志系统（幂等，多次调用安全）
    setup_logging(level="INFO")

    log(f"当前工作目录: {os.getcwd()}", "INFO")
    log(
        f"开始同步带 {config.REQUIRED_LABELS} 标签且已关闭（closed）的 issues...",
        "INFO",
    )

    try:
        repo, repo_full_name, g = get_github_repo()

        # 在批量 API 调用前检查速率限制
        handle_github_rate_limit(g)

        validator = RuleValidator()
        manager = RuleManager()

        issues = get_filtered_issues(repo, g, config.REQUIRED_LABELS)

        all_new_rules: List[Rule] = []
        processed_count = 0

        for issue in issues:
            # 二次验证标签（搜索 API 结果可能不精确）
            if not issue_has_required_labels(issue, config.REQUIRED_LABELS):
                continue

            processed_count += 1
            log(f"处理 Issue #{issue.number}...", "DEBUG")

            # 提取规则
            rule_tuples = extract_rules_from_issue(issue.title, issue.body)
            rule_strings = [r for r, _ in rule_tuples]

            if rule_strings:
                valid_rules, errors = validator.validate_rules(
                    rule_strings, f"issue #{issue.number}"
                )

                if errors:
                    log(f"\n在 issue #{issue.number} 中发现以下问题：", "WARNING")
                    for err in errors:
                        level = "WARNING" if err.is_format_error else "ERROR"
                        log(f"- {err.message}", level)

                all_new_rules.extend(valid_rules)

            # 注意：已废弃 processed 增量标记机制。
            # 现在每次运行都会重新处理所有带必需标签的已关闭 Issue，
            # 这样修改规则后可以立即生效，无需手动移除标签。

        log(f"处理了 {processed_count} 个 Issues", "INFO")

        if not all_new_rules:
            log("没有新的待处理 Issue，adnew.txt 无需更新", "INFO")
            ensure_adnew_exists()
            return

        log(f"\n找到 {len(all_new_rules)} 条有效规则，开始合并...", "INFO")
        new_filename = manager.merge_rules(all_new_rules)
        log(f"规则已合并到 {new_filename}", "INFO")
        log("规则合并完成！", "INFO")

    except RuntimeError as e:
        # get_github_repo 抛出的预期错误
        log(f"❌ {e}", "ERROR")
        ensure_adnew_exists()
        sys.exit(1)
    except Exception as e:
        log(f"主流程异常: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        ensure_adnew_exists()
        sys.exit(1)


if __name__ == "__main__":
    main()
