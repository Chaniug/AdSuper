import os
import sys
import traceback
import requests
from github import Github
from scripts.rule_validator import RuleValidator, Rule
from scripts.rule_manager import RuleManager
from scripts.utils import log
import re

# ============= 需根据你的项目实际修改的配置 ===============
REPO_OWNER = "Chaniug"
REPO_NAME = "AdSuper"
PROJECT_NUMBER = 4             # 项目编号（数字，不是id）
DONE_STATUS = "Done"           # "完成"状态的字段值
NOT_PLANNED_STATUS = "Not Planned"  # "不计划实现"状态的字段值
STATUS_FIELD = "Status"        # 状态字段名
# ========================================================

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def run_graphql(query, variables=None):
    headers = {
        "Authorization": f"bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    json_data = {"query": query}
    if variables:
        json_data["variables"] = variables
    r = requests.post("https://api.github.com/graphql", json=json_data, headers=headers)
    r.raise_for_status()
    return r.json()

def get_project_v2_items():
    # 查询 project v2 的所有卡片及其字段（包含状态、关联 issue）
    query = """
    query($owner: String!, $name: String!, $number: Int!, $after: String) {
      repository(owner: $owner, name: $name) {
        projectV2(number: $number) {
          id
          title
          items(first: 100, after: $after) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              id
              content {
                ... on Issue {
                  id
                  number
                  title
                  url
                }
              }
              fieldValues(first: 30) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "owner": REPO_OWNER,
        "name": REPO_NAME,
        "number": PROJECT_NUMBER,
        "after": None
    }
    issues = []
    while True:
        data = run_graphql(query, variables)
        project = data["data"]["repository"]["projectV2"]
        if not project:
            log("未找到指定的项目板，请确认项目板编号和仓库名无误。")
            sys.exit(1)
        items = project["items"]["nodes"]
        issues.extend(items)
        page_info = project["items"]["pageInfo"]
        if page_info["hasNextPage"]:
            variables["after"] = page_info["endCursor"]
        else:
            break
    return issues

def filter_issues_by_status(items, done_status=DONE_STATUS, not_plan_status=NOT_PLANNED_STATUS, status_field=STATUS_FIELD):
    issues_done = []
    issues_not_plan = set()
    for item in items:
        issue = item.get('content')
        if not issue or 'number' not in issue:
            continue
        status = None
        for v in item.get('fieldValues', {}).get('nodes', []):
            if v.get("field", {}).get("name") == status_field:
                status = v.get("name")
        if status == done_status:
            issues_done.append(issue['number'])
        elif status == not_plan_status:
            issues_not_plan.add(issue['number'])
    # 最终有效 issue
    return [n for n in issues_done if n not in issues_not_plan]

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

def get_github_repo() -> tuple:
    g = Github(GITHUB_TOKEN)
    repo_name = f"{REPO_OWNER}/{REPO_NAME}"
    try:
        repo = g.get_repo(repo_name)
        return repo, repo_name
    except Exception as e:
        log(f'无法访问仓库 {repo_name}，请检查仓库名和 GITHUB_TOKEN 权限！')
        log(str(e))
        sys.exit(1)

def main():
    log(f"当前工作目录：{os.getcwd()}")
    log("开始从 GitHub Projects v2 获取新规则...")
    try:
        repo, repo_name = get_github_repo()
        validator = RuleValidator()
        manager = RuleManager()
        # 获取项目板 items
        items = get_project_v2_items()
        valid_issue_numbers = filter_issues_by_status(items)
        if not valid_issue_numbers:
            log("没有符合条件的项目板 issue")
            # 保证 adnew.txt 存在
            if not os.path.exists('adnew.txt'):
                with open('adnew.txt', 'w', encoding='utf-8') as f:
                    f.write("! 自动生成的空 adnew.txt\n")
            return

        all_new_rules = []
        for issue_number in valid_issue_numbers:
            try:
                issue = repo.get_issue(number=issue_number)
            except Exception as e:
                log(f"无法获取 issue #{issue_number}: {e}")
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
        # 保证 adnew.txt 存在
        if not os.path.exists('adnew.txt'):
            with open('adnew.txt', 'w', encoding='utf-8') as f:
                f.write("! 自动生成的空 adnew.txt\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
