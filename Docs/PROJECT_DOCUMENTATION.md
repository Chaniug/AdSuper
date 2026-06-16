# AdSuper 项目文档

## 项目概述

**AdSuper** 是一个面向社区的**广告规则收集与管理平台**，致力于汇聚全网最优质的广告过滤规则。该项目是 [FilterFusion](https://github.com/Chaniug/FilterFusion) 的子项目，作为社区规则收集平台为主项目提供规则源。

### 项目目标

- 建立一个由社区驱动的规则审核系统
- 让任何人都能轻松提交和维护广告过滤规则
- 自动化同步、审核、打包规则，保证规则的质量和时效性
- 为 FilterFusion 主项目提供持续的规则更新

### 适用人群

- 广告过滤规则爱好者
- 希望帮助社区改进规则的志愿者
- 遇到漏拦截或误拦截的用户
- 希望维护自己规则库的开发者

---

## 项目架构

### 目录结构

```
AdSuper/
├── adnew.txt                 # 自动生成的规则文件（输出）
├── AdSuper.txt               # 基础规则文件（输入）
├── LICENSE                   # MIT 开源许可证
├── README.md                 # 中文说明文档
├── README_EN.md              # 英文说明文档
├── requirements.txt          # Python 依赖清单
├── sync_issues.py            # 主脚本：同步 GitHub Issues 中的规则
└── scripts/                  # Python 脚本模块
    ├── __init__.py           # 包初始化文件
    ├── rule_extractor.py    # 规则提取模块
    ├── rule_validator.py     # 规则验证器
    ├── rule_manager.py       # 规则管理器
    └── utils.py              # 工具函数
```

### 技术栈

- **编程语言**: Python 3
- **核心依赖**:
  - `PyGithub` - GitHub API 交互
  - `requests` - HTTP 请求
  - `python-dateutil` - 日期时间处理

---

## 核心功能

### 1. 自动化规则审核

通过 GitHub Issues 自动收集、审核和打包规则：

- 用户提交 Issue（使用预设模板）
- 维护者审核（24-48小时内）
- 通过的规则自动标记 `completed`
- 拒绝的规则标记 `not planned` 并关闭

### 2. 规则验证

内置严格的规则验证机制：

- **格式验证**: 检查规则语法是否符合 Adblock Plus (ABP) 标准
- **冲突检测**: 自动检测例外规则与普通规则的冲突
- **去重处理**: 自动去除重复规则
- **排序优化**: 按规则类型和优先级自动排序

### 3. 规则管理

- **合并规则**: 将新规则与现有规则合并
- **备份机制**: 自动备份规则文件（保留最新3个备份）
- **完整性验证**: 检查所有已完成的 Issues 中的规则是否都被正确包含

### 4. 定期发布

- 每 5 天自动发布一次规则包
- 生成 Release 并同步到 FilterFusion 主项目

---

## 工作流程

```
用户提交 Issue
     ↓
[Issue 模板] 规则审核
     ↓
❌ 不合适 → 标记 not planned (关闭)
     ↓ ✅ 合适
自动收录到 adnew.txt
     ↓
定期打包 (每 5 天)
     ↓
发布 Release
     ↓
同步到 FilterFusion 主项目
```

---

## 规则格式详解

AdSuper 支持 **Adblock Plus (ABP) 通用格式**，包括以下规则类型：

### 1. 域名匹配规则（最常用）

```
||example.com^
```

- `||` 表示域名的开始
- `example.com` 是要匹配的域名
- `^` 表示分隔符（域名结束）
- 效果：拦截来自 `example.com` 和 `*.example.com` 的所有请求

### 2. 带参数的规则

```
||ads.example.com^$script,image
```

常用参数：
- `$script` - 仅拦截脚本文件
- `$image` - 仅拦截图片
- `$stylesheet` - 仅拦截样式表
- `$xmlhttprequest` - 仅拦截 AJAX 请求
- `$third-party` - 仅拦截第三方请求

### 3. 元素隐藏规则

```
example.com##.ad-banner
```

- `##` 表示元素隐藏
- `.ad-banner` 是 CSS 选择器
- 效果：隐藏 `example.com` 上 class 为 `ad-banner` 的元素

### 4. 白名单规则

```
@@||example.com^$document
```

- `@@` 表示白名单（例外）
- 不拦截该域名上的请求
- 通常用于避免误拦截

### 5. 正则表达式规则（高级）

```
/banner.*\.jpg$/
```

- `/` 包围正则表达式
- 用于复杂的匹配逻辑

### 6. 注释

```
! 这是注释
# 这也是注释
```

---

## 脚本模块说明

### sync_issues.py

**功能**: 主脚本，从 GitHub Issues 中同步已审核通过的规则

**工作流程**:
1. 连接 GitHub API
2. 获取所有已关闭且带有 `ad-rule` 和 `completed` 标签的 Issues
3. 从 Issue 标题和正文中提取规则
4. 验证规则格式
5. 合并到 `adnew.txt`

**环境变量**:
- `GITHUB_TOKEN` - GitHub 访问令牌（必需）

### scripts/rule_validator.py

**功能**: 规则验证器，提供规则验证、冲突检测、排序等功能

**核心类**:
- `RuleType` - 规则类型枚举
- `Rule` - 规则数据类
- `RuleValidator` - 规则验证器类

**主要方法**:
- `validate_rule()` - 验证单条规则
- `validate_rules()` - 批量验证规则
- `check_conflicts()` - 检查规则冲突
- `sort_rules()` - 按优先级排序规则

### scripts/rule_manager.py

**功能**: 规则管理器，负责规则的加载、合并、保存

**核心类**:
- `RuleManager` - 规则管理器类

**主要方法**:
- `load_existing_rules()` - 加载现有规则
- `merge_rules()` - 合并规则并优化
- `_save_rules()` - 保存规则到文件

### scripts/utils.py

**功能**: 工具函数，提供日志输出、重试机制、GitHub API 辅助等功能

**主要函数**:
- `log()` - 输出带时间戳的日志信息
- `setup_logging()` - 配置日志系统（支持分级日志和文件输出）
- `set_log_level()` - 动态设置日志级别
- `retry_on_exception()` - 重试装饰器（支持指数退避）
- `exponential_backoff()` - 计算指数退避延迟时间
- `is_github_api_error_retryable()` - 判断 GitHub API 错误是否可重试
- `handle_github_rate_limit()` - 处理 GitHub API 速率限制
- `load_rules_from_file()` - 从文件加载规则

---

## 使用方法

### 环境准备

1. 克隆项目仓库：
```bash
git clone https://github.com/Chaniug/AdSuper.git
cd AdSuper
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置 GitHub Token：
```bash
# Linux/macOS
export GITHUB_TOKEN="your_github_token"

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token"
```

### 运行主脚本

同步 GitHub Issues 中的规则：

```bash
python sync_issues.py
```

---

## 贡献指南

### 提交规则（最直接）

1. **点击提交**: [提交新规则 Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule&template=rule_report.yml)

2. **填写内容**:
   - 规则类型（域名、元素隐藏等）
   - 具体的规则内容
   - 说明为什么需要这条规则

3. **等待审核**:
   - 维护者会在 24-48 小时内审核
   - 通过标记 ✅ `completed`
   - 拒绝标记 ❌ `not planned`

### 提交前检查清单

- [ ] 规则语法正确
- [ ] 规则尚未存在于库中
- [ ] 规则有实际的拦截效果
- [ ] 不会误拦截正常网站
- [ ] 一条 Issue 只包含一条规则

### 其他贡献方式

- **参与讨论**: 在 [Discussions](https://github.com/Chaniug/AdSuper/discussions) 分享想法
- **报告问题**: 在 [Issues](https://github.com/Chaniug/AdSuper/issues) 反馈问题
- **代码贡献**: Fork 项目，改进脚本和自动化流程，提交 Pull Request

---

## 与 FilterFusion 的关系

| 项目 | 说明 |
|------|------|
| **FilterFusion** | 🎯 主项目 - 聚合多源规则，生成最终的广告过滤列表 |
| **AdSuper** | 🤝 子项目 - 社区规则收集平台，为主项目提供规则源 |

### 架构示意

```
社区用户提交规则到 AdSuper
         ↓
     审核并收录
         ↓
FilterFusion 自动拉取规则
         ↓
与其他规则源合并去重
         ↓
生成最终规则文件
         ↓
用户订阅使用
```

**总结**:
- 🌟 AdSuper 是 FilterFusion 的**规则输入来源**
- 🔄 FilterFusion 是 AdSuper 规则的**最终汇总地**

---

## 项目统计

- 📝 **总规则数** - 持续增长中（当前 61 条）
- 🔄 **自动更新** - 每 5 天发布一次
- 👥 **贡献者数** - 查看 [贡献者名单](https://github.com/Chaniug/AdSuper/graphs/contributors)
- ⭐ **项目 Star** - 感谢支持

---

## 许可证

本项目遵循 **MIT License**，允许：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用

**唯一要求**: 保留原始许可证和版权声明

---

## 联系与支持

### 快速链接

- 🔗 [主项目 FilterFusion](https://github.com/Chaniug/FilterFusion)
- 📝 [提交规则](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule)
- 💬 [参与讨论](https://github.com/Chaniug/AdSuper/discussions)
- 🐛 [报告问题](https://github.com/Chaniug/AdSuper/issues)
- 📦 [查看发布](https://github.com/Chaniug/AdSuper/releases)

### 社交媒体

- 🌐 [个人主页](https://valk.ccwu.cc/)
- 🐦 [X (Twitter)](https://x.com/chenboss14)
- ✈️ [Telegram](https://t.me/chaniug)
- 📧 [邮箱](mailto:cheniug99@gmail.com)

---

## 常见问题 FAQ

### Q1: 如何知道规则是否有效？

**A**: 提交规则时请说明：
- 你在哪个网站看到这个广告
- 如何复现这个广告
- 提交的规则是否已测试

维护者会在测试后才会批准规则。

### Q2: 规则多久会生效？

**A**: 预计时间：从提交到用户生效 **5-7 天**（中位数）

### Q3: 可以用于商业项目吗？

**A**: **可以**。AdSuper 的规则和代码遵循 MIT License，允许商业使用。

### Q4: 如何成为项目贡献者？

**A**: 提交被采纳的规则自动成为贡献者，查看 [贡献者名单](https://github.com/Chaniug/AdSuper/graphs/contributors)。

---

## 更新日志

### 2026-06-11
- ✅ 更新规则文件（共 61 条规则）
- ✅ 优化规则验证器
- ✅ 改进规则管理器

### 2026-06-08
- ✅ 添加规则完整性验证工具
- ✅ 完善文档

---

**文档版本**: 1.0  
**最后更新**: 2026-06-13  
**作者**: AdSuper 项目团队
