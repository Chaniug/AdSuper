import os
import sys
import traceback
from github import Github
from scripts.rule_validator import RuleValidator
from scripts.rule_manager import RuleManager
from scripts.utils import log
import re

# 配置项
REPO_OWNER = "Chaniug"
REPO_NAME = "AdSuper"
REQUIRED_LABELS = {"ad-rule", "completed"}  # 同时需要有这两个标签才同步
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def extract_rules_from_issue(issue):
    """
    从 issue 的标题和正文中提取所有广告规则。
    返回 [(规则文本, 来源)] 列表，来源为 'title' 或 'body'。
    """
    rules = []
    rule_patterns = [
        r'\|\|[^\s\^$，。！？；：、…]+?\^[^\s，。！？；：、…]*',       # ||domain^$option
        r'@@\|\|[^\s\^$，。！？；：、…]+?\^[^\s，。！？；：、…]*',    # @@||domain^$option
        r'(^|[^\S\r\n])\$.+',                                     # $script,$image等修饰符一整行
        r'[^#\s][^\s]*#@?#.+',                                   # example.com#@#something
        r'[^#\s][^\s]*##.+',                                     # example.com##something
        r'[^#\s][^\s]*#\$#.+',                                   # example.com#$#something
        r'[^#\s][^\s]*##\^.+',                                   # example.com##^something
        r'##[^\s，。！？；：、…]+',                                 # ##.ad-banner
        r'@@[^\s]+',                                             # @@规则(非||也可)
        r'^!.*$',                                                # 注释
    ]
    pattern = re.compile('|'.join(rule_patterns), re.MULTILINE)

    seen = set()
    lines = [issue.title.strip()]
    if issue.body:
        lines += issue.body.split('\n')

    for idx, line in enumerate(lines):
        source = 'title' if idx == 0 else 'body'
        for match in pattern.finditer(line):
            rule = match.group().strip()
            if rule and rule not in seen:
                seen.add(rule)
                rules.append((rule, source))
    return rules

def get_github_repo():
    g = Github(GITHUB_TOKEN)
    repo_name = f"{REPO_OWNER}/{REPO_NAME}"
    try:
        repo = g.get_repo(repo_name)
        return repo, repo_name
    except Exception as e:
        log(f'无法访问仓库 {repo_name}，请检查仓库名和 GITHUB_TOKEN 权限！')
        log(str(e))
        sys.exit(1)

def issue_has_required_labels(issue, required_labels):
    issue_labels = {label.name for label in issue.labels}
    return required_labels.issubset(issue_labels)

def main():
    log(f"当前工作目录：{os.getcwd()}")
    log("开始同步带 ad-rule 和 completed 标签的 issues...")
    try:
        repo, repo_name = get_github_repo()
        validator = RuleValidator()
        manager = RuleManager()
        # 获取所有 open 状态的 issue
        issues = repo.get_issues(state="open")
        all_new_rules = []
        for issue in issues:
            if not issue_has_required_labels(issue, REQUIRED_LABELS):
                continue
            rule_tuples = extract_rules_from_issue(issue)
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
        log(f"merge_rules 返回文件名: {new_filename}")
        log(f"os.getcwd(): {os.getcwd()}")
        log(f"os.listdir('.'): {os.listdir('.')}")
        log(f"adnew.txt exists: {os.path.exists('adnew.txt')}")
        adnew_path = os.path.join('.', new_filename)
        if not os.path.exists(adnew_path):
            log(f"错误：文件 {adnew_path} 未生成")
            sys.exit(1)
        log(f"规则已合并到 {adnew_path}")
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
