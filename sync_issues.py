import os
import sys
import traceback
from github import Github
from scripts.rule_validator import RuleValidator
from scripts.rule_manager import RuleManager
from scripts.utils import log, retry_on_exception, is_github_api_error_retryable
from scripts.rule_extractor import extract_rules_from_issue

REPO_OWNER = "Chaniug"
REPO_NAME = "AdSuper"
REQUIRED_LABELS = {"ad", "good"}  # 需要同时有这两个标签
PROCESSED_LABEL = "processed"              # 标记已处理的 Issue（实现增量处理）
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')


@retry_on_exception(max_retries=3, exceptions=(Exception,), should_retry=is_github_api_error_retryable)
def get_github_repo():
    g = Github(GITHUB_TOKEN)
    repo_name = f"{REPO_OWNER}/{REPO_NAME}"
    try:
        repo = g.get_repo(repo_name)
        log(f"✓ 成功连接仓库: {repo_name}", "INFO")
        return repo, repo_name, g
    except Exception as e:
        log(f'❌ 无法访问仓库 {repo_name}，请检查仓库名和 GITHUB_TOKEN 权限！', "ERROR")
        log(str(e), "ERROR")
        sys.exit(1)

@retry_on_exception(max_retries=3, exceptions=(Exception,), should_retry=is_github_api_error_retryable)
def get_filtered_issues(repo, g, required_labels):
    """
    使用 GitHub 搜索 API 获取带有指定标签的已关闭 issues。
    排除已标记 processed 的 issue，实现增量处理。
    """
    labels_query = ' '.join([f'label:{label}' for label in required_labels])
    query = f"repo:{REPO_OWNER}/{REPO_NAME} is:issue is:closed {labels_query} -label:{PROCESSED_LABEL}"

    try:
        issues = g.search_issues(query)
        log(f"搜索查询（排除已处理）: {query}", "DEBUG")
        log(f"找到 {issues.totalCount} 个待处理的 issues", "INFO")
        return issues
    except Exception as e:
        log(f"搜索 issues 失败: {e}", "WARNING")
        # 降级方案：获取所有已关闭的 issues 并在本地过滤
        log("降级方案：获取所有已关闭的 issues 并在本地过滤...", "WARNING")
        return repo.get_issues(state="closed")

def issue_has_required_labels(issue, required_labels):
    """检查 issue 是否有所需标签，且未被标记为已处理"""
    issue_labels = {label.name for label in issue.labels}
    if PROCESSED_LABEL in issue_labels:
        return False
    return required_labels.issubset(issue_labels)

def main():
    log(f"当前工作目录：{os.getcwd()}", "INFO")
    log("开始同步带 ad 和 good 标签且已关闭（closed）的 issues...", "INFO")
    
    g = None  # 初始化 g 变量
    
    try:
        repo, repo_name, g = get_github_repo()

        validator = RuleValidator()
        manager = RuleManager()
        
        # 使用优化的 API 调用获取 issues
        issues = get_filtered_issues(repo, g, REQUIRED_LABELS)
        
        all_new_rules = []
        processed_count = 0
        
        for issue in issues:
            # 注意：搜索 API 返回的结果可能已经过滤了标签，但为了安全起见，再次检查
            if not issue_has_required_labels(issue, REQUIRED_LABELS):
                continue
            
            processed_count += 1
            log(f"处理 Issue #{issue.number}...", "DEBUG")
            
            # 使用共享模块提取规则
            rule_tuples = extract_rules_from_issue(issue.title, issue.body)
            rules = [r for r, src in rule_tuples]
            
            if rules:
                valid_rules, errors = validator.validate_rules(rules, f"issue #{issue.number}")
                
                if errors:
                    log(f"\n在 issue #{issue.number} 中发现以下问题：", "WARNING")
                    format_errors = []
                    content_errors = []
                    for error in errors:
                        if "多余空格" in error or "无效注释" in error:
                            format_errors.append(error)
                        else:
                            content_errors.append(error)
                    if format_errors:
                        log("⚠️ 格式问题(已自动修复)：", "WARNING")
                        for error in format_errors:
                            log(f"- {error}", "WARNING")
                    if content_errors:
                        log("❌ 内容错误(将被跳过)：", "ERROR")
                        for error in content_errors:
                            log(f"- {error}", "ERROR")
                
                all_new_rules.extend(valid_rules)
            
            # 标记 issue 已处理（无论是否有有效规则，避免重复处理）
            try:
                issue.add_to_labels(PROCESSED_LABEL)
                log(f"Issue #{issue.number} 已标记为 {PROCESSED_LABEL}", "DEBUG")
            except Exception as e:
                log(f"标记 Issue #{issue.number} 失败: {e}", "WARNING")
        
        log(f"处理了 {processed_count} 个 Issues", "INFO")
        
        if not all_new_rules:
            log("没有新的待处理 Issue，adnew.txt 无需更新", "INFO")
            # 首次运行时保证 adnew.txt 存在
            if not os.path.exists('adnew.txt'):
                with open('adnew.txt', 'w', encoding='utf-8') as f:
                    f.write("! 自动生成的空 adnew.txt\n")
            return
        
        log(f"\n找到 {len(all_new_rules)} 条有效规则，开始合并...", "INFO")
        new_filename = manager.merge_rules(all_new_rules)
        log(f"规则已合并到 {new_filename}", "INFO")
        log("规则合并完成！", "INFO")
        
    except Exception as e:
        log(f"主流程异常: {e}", "ERROR")
        log(traceback.format_exc(), "ERROR")
        if not os.path.exists('adnew.txt'):
            with open('adnew.txt', 'w', encoding='utf-8') as f:
                f.write("! 自动生成的空 adnew.txt\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
