import os
import sys
import traceback
from github import Github
from scripts.rule_validator import RuleValidator, Rule
from scripts.rule_manager import RuleManager
from scripts.utils import log

def get_github_repo() -> tuple:
    g = Github(os.getenv('GITHUB_TOKEN'))
    repo_name = os.getenv('GITHUB_REPOSITORY')
    if not repo_name:
        repo_name = 'chani/AdSuper'
    try:
        repo = g.get_repo(repo_name)
        return repo, repo_name
    except Exception as e:
        log(f'无法访问仓库 {repo_name}，请检查仓库名和 GITHUB_TOKEN 权限！')
        log(str(e))
        sys.exit(1)

def extract_rules_from_issue(issue) -> list:
    rules = []
    if '||' in issue.title or '##' in issue.title:
        rules.append(issue.title.strip())
        log(f"从 issue #{issue.number} 的标题中提取规则: {issue.title}")
    if issue.body:
        lines = issue.body.split('\n')
        for line in lines:
            line = line.strip()
            if line and ('||' in line or '##' in line):
                rules.append(line)
                log(f"从 issue #{issue.number} 的内容中提取规则: {line}")
    return rules

def main():
    log(f"当前工作目录：{os.getcwd()}")
    log("开始从 GitHub Issues 获取新规则...")
    try:
        repo, repo_name = get_github_repo()
        validator = RuleValidator()
        manager = RuleManager()  # 默认写根目录
        issues = repo.get_issues(state='all')
        all_new_rules = []
        for issue in issues:
            label_names = [label.name for label in issue.labels]
            if 'ad-rule' not in label_names:
                continue
            rules = extract_rules_from_issue(issue)
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
            return
        log(f"\n找到 {len(all_new_rules)} 条有效规则，开始合并...")
        new_filename = manager.merge_rules(all_new_rules)
        log(f"merge_rules 返回文件名: {new_filename}")
        log("当前目录所有文件:")
        log(str(os.listdir('.')))
        adnew_path = os.path.join('.', new_filename)
        if not os.path.exists(adnew_path):
            log(f"错误：文件 {adnew_path} 未生成")
            sys.exit(1)
        log(f"规则已合并到 {adnew_path}")
        log("规则合并完成！")
    except Exception as e:
        log(f"主流程异常: {e}")
        log(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()