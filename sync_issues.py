import os
import sys
import traceback
from github import Github
from scripts.rule_validator import RuleValidator
from scripts.rule_manager import RuleManager
from scripts.utils import log
from scripts.rule_extractor import extract_rules_from_issue

REPO_OWNER = "Chaniug"
REPO_NAME = "AdSuper"
REQUIRED_LABELS = {"ad-rule", "completed"}  # 需要同时有这两个标签
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


def get_github_repo():
    g = Github(GITHUB_TOKEN)
    repo_name = f"{REPO_OWNER}/{REPO_NAME}"
    try:
        repo = g.get_repo(repo_name)
        return repo, repo_name, g
    except Exception as e:
        log(f'无法访问仓库 {repo_name}，请检查仓库名和 GITHUB_TOKEN 权限！')
        log(str(e))
        sys.exit(1)

def get_filtered_issues(repo, g, required_labels):
    """
    使用 GitHub 搜索 API 获取带有指定标签的已关闭 issues
    这比获取所有 issues 后在本地过滤更高效
    """
    # 构建搜索查询
    # 注意：GitHub API 的 label 查询是 AND 关系
    labels_query = ' '.join([f'label:{label}' for label in required_labels])
    query = f"repo:{REPO_OWNER}/{REPO_NAME} is:issue is:closed {labels_query}"
    
    try:
        issues = g.search_issues(query)
        log(f"搜索查询: {query}")
        log(f"找到 {issues.totalCount} 个匹配的 issues")
        return issues
    except Exception as e:
        log(f"搜索 issues 失败: {e}")
        # 降级方案：获取所有已关闭的 issues 并在本地过滤
        log("降级方案：获取所有已关闭的 issues 并在本地过滤...")
        return repo.get_issues(state="closed")

def issue_has_required_labels(issue, required_labels):
    issue_labels = {label.name for label in issue.labels}
    return required_labels.issubset(issue_labels)

def main():
    log(f"当前工作目录：{os.getcwd()}")
    log("开始同步带 ad-rule 和 completed 标签且已关闭（closed）的 issues...")
    try:
        repo, repo_name, g = get_github_repo()
        validator = RuleValidator()
        manager = RuleManager()
        # 使用优化的 API 调用获取 issues
        issues = get_filtered_issues(repo, g, REQUIRED_LABELS)
        all_new_rules = []
        for issue in issues:
            # 注意：搜索 API 返回的结果可能已经过滤了标签，但为了安全起见，再次检查
            if not issue_has_required_labels(issue, REQUIRED_LABELS):
                continue
            # 使用共享模块提取规则
            rule_tuples = extract_rules_from_issue(issue.title, issue.body)
            rules = [r for r, src in rule_tuples]
            if rules:
                valid_rules, errors = validator.validate_rules(rules, f"issue #{issue.number}")
                if errors:
                    log(f"\n在 issue #{issue.number} 中发现以下问题：")
                    format_errors = []
                    content_errors = []
                    for error in errors:
                        if "多余空格" in error or "无效注释" in error:
                            format_errors.append(error)
                        else:
                            content_errors.append(error)
                    if format_errors:
                        log("⚠️ 格式问题(已自动修复)：")
                        for error in format_errors:
                            log(f"- {error}")
                    if content_errors:
                        log("❌ 内容错误(将被跳过)：")
                        for error in content_errors:
                            log(f"- {error}")
                all_new_rules.extend(valid_rules)
        if not all_new_rules:
            log("没有找到新的规则")
            # 保证 adnew.txt 存在
            if not os.path.exists('adnew.txt'):
                with open('adnew.txt', 'w', encoding='utf-8') as f:
                    f.write("! 自动生成的空 adnew.txt\n")
            return
        log(f"\n找到 {len(all_new_rules)} 条有效规则，开始合并...")
        new_filename = manager.merge_rules(all_new_rules)
        log(f"规则已合并到 {new_filename}")
        log("规则合并完成！")
    except Exception as e:
        log(f"主流程异常: {e}")
        log(traceback.format_exc())
        if not os.path.exists('adnew.txt'):
            with open('adnew.txt', 'w', encoding='utf-8') as f:
                f.write("! 自动生成的空 adnew.txt\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
