from github import Github
import os
from datetime import datetime, timedelta

# 初始化GitHub客户端
g = Github(os.getenv('GITHUB_TOKEN'))
repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

def is_useful_issue(issue):
    """判断issue是否有用"""
    # 可根据需要修改筛选条件
    return not issue.pull_request and 'ad-rule' in [label.name.lower() for label in issue.labels]

def format_issue_content(issue):
    """格式化issue内容"""
    return f"""
# Issue {issue.number}: {issue.title}
# Created at: {issue.created_at}
{issue.body}
"""

def main():
    print("Starting issue sync process...")
    
    try:
        # 获取过去24小时内的issues
        since = datetime.now() - timedelta(days=1)
        issues = repo.get_issues(state='closed', since=since, sort='updated', direction='desc')
        
        useful_issues = [issue for issue in issues if is_useful_issue(issue)]
        print(f"Found {len(useful_issues)} useful issues")
        
        if useful_issues:
            with open('AdSuper.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n\n# Updated at: {datetime.now()}\n")
                for issue in useful_issues:
                    content = format_issue_content(issue)
                    f.write(content)
                    print(f"Added content from issue #{issue.number}")
                    
        print("Sync completed successfully")
    except Exception as e:
        print(f"Error during sync: {str(e)}")
        raise

if __name__ == '__main__':
    main()