---
name: optimize-scripts-and-workflows
overview: 优化项目中的脚本和 workflows，删除重复功能，重构代码结构，优化 workflow 配置，但不改变文件位置
todos:
  - id: delete-duplicate-workflow
    content: 删除重复的 workflow 文件 `.github/workflows/sync_issues.yml`
    status: pending
  - id: update-auto-release
    content: 更新 `auto_release.yml` 的 actions 版本到 v6 并添加 pip 缓存
    status: pending
    dependencies:
      - delete-duplicate-workflow
  - id: update-validate-rules
    content: 更新 `validate-rules.yml` 的 actions 版本到 v6
    status: pending
    dependencies:
      - delete-duplicate-workflow
  - id: optimize-sync-rules
    content: 为 `sync-rules.yml` 添加 pip 缓存支持
    status: pending
    dependencies:
      - delete-duplicate-workflow
  - id: verify-workflows
    content: 验证所有 workflows 的 YAML 语法和配置正确性
    status: pending
    dependencies:
      - update-auto-release
      - update-validate-rules
      - optimize-sync-rules
---

## 项目脚本和 Workflows 优化需求

### 问题分析

1. **重复的 Workflow 文件**

- `.github/workflows/sync-rules.yml` 和 `.github/workflows/sync_issues.yml` 功能完全重复
- 两者都调用 `python sync_issues.py` 同步 GitHub Issues 到规则文件
- 会导致重复运行和资源浪费

2. **需要更新的 Actions 版本**（Node.js 24 支持）

- `auto_release.yml`: 使用 `actions/checkout@v4`（不支持 Node.js 24）
- `validate-rules.yml`: 使用 `actions/checkout@v4` 和 `actions/setup-python@v5`（不支持 Node.js 24）
- 从 2026年6月16日起，GitHub Actions 将强制使用 Node.js 24

3. **Workflow 配置优化点**

- Python 版本不统一（3.10 和 3.11）
- 部分 workflow 缺少 pip 缓存支持
- 错误处理可以改进

### 优化目标

- 删除功能重复的 workflow 文件
- 更新所有 workflows 到支持 Node.js 24 的 actions 版本
- 统一 Python 版本为 3.11
- 为所有 workflows 添加 pip 缓存支持
- 保持所有文件位置不变

## 技术方案

### 1. 删除重复的 Workflow

- **文件**: `.github/workflows/sync_issues.yml`
- **原因**: 功能与 `sync-rules.yml` 完全重复，都是同步 issues 到规则文件
- **影响**: 无，`sync-rules.yml` 已经包含所有必要功能

### 2. 更新 `auto_release.yml`

- 更新 `actions/checkout@v4` → `actions/checkout@v6`
- 添加 pip 缓存支持
- 统一 Python 版本为 3.11
- 保持现有发布功能不变

### 3. 更新 `validate-rules.yml`

- 更新 `actions/checkout@v4` → `actions/checkout@v6`
- 更新 `actions/setup-python@v5` → `actions/setup-python@v6`
- 保持现有验证功能不变

### 4. 优化 `sync-rules.yml`

- 添加 pip 缓存支持（目前缺少）
- 改进错误处理和日志输出
- 保持现有同步功能不变

### 5. 脚本文件分析

- `scripts/__init__.py`: 必需，不能删除
- `scripts/check_consistency.py`: 保留，作为手动检查工具
- `scripts/rule_extractor.py`: 核心模块，不能删除
- `scripts/rule_manager.py`: 核心模块，不能删除
- `scripts/rule_validator.py`: 核心模块，不能删除
- `scripts/utils.py`: 核心模块，不能删除
- `scripts/validate_rules.py`: 保留，对应 `validate-rules.yml` workflow
- `sync_issues.py`: 核心脚本，不能删除

### 实施步骤

1. 删除 `.github/workflows/sync_issues.yml`
2. 更新 `.github/workflows/auto_release.yml`
3. 更新 `.github/workflows/validate-rules.yml`
4. 优化 `.github/workflows/sync-rules.yml`