# 如何添加 GitHub Actions 工作流

## 📝 步骤 1：创建工作流文件

在你的仓库中创建文件：`.github/workflows/validate-rules.yml`

## 📋 步骤 2：复制以下内容

```yaml
name: Validate Ad Rules

on:
  pull_request:
    paths:
      - 'adnew.txt'
  issues:
    types: [closed]
  schedule:
    # 每周一检查一次
    - cron: '0 0 * * 1'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install requests
      
      - name: Run rule validation
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python scripts/validate_rules.py
      
      - name: Comment on PR if validation fails
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ 规则验证失败！\n\n请检查以下几点：\n1. 确保所有 Issue 中的规则都已添加到 adnew.txt\n2. 运行 `python scripts/validate_rules.py` 查看详细信息\n3. 查看 Actions 日志了解具体错误'
            })
      
      - name: Upload validation report
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: VALIDATION_REPORT.md
```

## 🚀 步骤 3：通过 Web UI 创建（推荐）

### 方法 A：GitHub Web 界面（最简单）

1. 打开你的仓库: https://github.com/Chaniug/AdSuper
2. 点击 "Add file" → "Create new file"
3. 输入路径: `.github/workflows/validate-rules.yml`
4. 粘贴上面的 YAML 内容
5. 点击 "Commit changes"
6. 选择 "Create a new branch for this commit and start a pull request"

### 方法 B：使用 Git 命令行

```bash
# 克隆仓库
git clone https://github.com/Chaniug/AdSuper.git
cd AdSuper

# 切换到特性分支
git checkout -b feature/add-ci-workflow

# 创建目录
mkdir -p .github/workflows

# 创建文件并粘贴内容
cat > .github/workflows/validate-rules.yml << 'EOF'
[粘贴上面的 YAML 内容]
EOF

# 提交
git add .github/workflows/validate-rules.yml
git commit -m "ci: 添加规则验证工作流"

# 推送
git push origin feature/add-ci-workflow
```

## ✅ 步骤 4：创建 Pull Request

1. 仓库会提示创建 PR
2. 标题: "feat: 添加规则验证工作流"
3. 描述: 参考下面的模板

### PR 描述模板

```markdown
## 🎯 目标
添加自动化工作流来验证规则完整性

## 🔧 改动内容
- 添加 GitHub Actions 工作流: `.github/workflows/validate-rules.yml`
- 工作流触发条件:
  - PR 修改 adnew.txt 时
  - Issue 被关闭时
  - 每周一自动运行

## 📊 工作流功能
- ✅ 自动验证规则完整性
- ✅ 检测遗漏的规则
- ✅ 生成验证报告
- ✅ PR 验证失败时自动评论

## 🧪 测试方式
1. 修改 adnew.txt 并创建 PR
2. 观察 Actions 选项卡中的工作流运行
3. 验证通过/失败

## 📝 相关 Issue
- 解决规则遗漏问题
```

## 🎯 工作流触发条件

| 事件 | 触发时机 |
|------|---------|
| `pull_request` | 当 PR 修改 `adnew.txt` 时运行 |
| `issues` | 当 Issue 被标记为完成时运行 |
| `schedule` | 每周一 00:00 UTC 自动运行 |

## 📋 工作流步骤

1. **检出代码** - 获取最新的仓库代码
2. **配置 Python** - 设置 Python 3.11 环境
3. **安装依赖** - 安装 requests 库
4. **运行验证** - 执行 `validate_rules.py` 脚本
5. **失败通知** - 如果验证失败，在 PR 上评论提醒
6. **上传报告** - 生成验证报告供下载

## 🔐 权限需求

工作流使用 `GITHUB_TOKEN`，这是 GitHub 自动提供的，无需特殊配置。

## 🐛 常见问题

**Q: 如何查看工作流运行日志？**
A: 进入仓库 → Actions 标签 → 点击相应的工作流运行

**Q: 如何修改触发条件？**
A: 编辑 `.github/workflows/validate-rules.yml` 中的 `on:` 部分

**Q: 工作流失败怎么办？**
A: 查看 Actions 日志，通常原因是规则格式错误或遗漏

