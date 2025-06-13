# AdSuper 广告规则管理工具

## 功能说明

本项目通过GitHub Issues管理广告规则，并自动同步到本地文件：

1. 自动同步带有`ad-rule`标签的issues（包括已关闭的）
2. 合并规则到两个文件：
   - `AdSuper.txt` - 基础规则文件
   - `adnew.txt` - 包含新增规则的合并文件

## 使用说明

1. 创建带有`ad-rule`标签的issue来添加新规则
2. 关闭issue后，规则会自动同步到`adnew.txt`
3. 系统每小时自动运行同步任务

## 文件说明

- `AdSuper.txt`: 基础广告规则文件
- `adnew.txt`: 包含新增规则的合并文件
- `sync_issues.py`: 同步脚本
- `.github/workflows/sync_issues.yml`: GitHub Actions工作流配置

## 开发

```bash
python sync_issues.py
```