# 🚀 AdSuper

<p align="center">
  <a href="https://github.com/Chaniug/FilterFusion">
    <img src="https://img.shields.io/badge/主项目-FilterFusion-blue?logo=github&style=for-the-badge" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/Chaniug/AdSuper?style=for-the-badge&color=orange" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/commits/main">
    <img src="https://img.shields.io/github/commit-activity/m/Chaniug/AdSuper?style=for-the-badge&color=success" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/issues">
    <img src="https://img.shields.io/github/issues/Chaniug/AdSuper?style=for-the-badge&color=yellow" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/stargazers">
    <img src="https://img.shields.io/github/stars/Chaniug/AdSuper?style=for-the-badge&color=blue" />
  </a>
</p>

<p align="center">
  <b>📦 社区驱动的广告规则收集平台</b><br>
  <sub>提交规则 · 审核收录 · 自动发布 · 全网共享</sub>
</p>

<p align="center">
  <a href="https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml">
    <img src="https://img.shields.io/badge/📝_提交规则-Issue-success?style=for-the-badge" />
  </a>
  <a href="https://raw.githubusercontent.com/Chaniug/AdSuper/main/adnew.txt">
    <img src="https://img.shields.io/badge/📥_订阅规则-adnew.txt-blue?style=for-the-badge" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/releases">
    <img src="https://img.shields.io/badge/📦_查看发布-Releases-orange?style=for-the-badge" />
  </a>
</p>

---

**中文** | **[English](./README_EN.md)** 

---

## 📖 目录

- [🎯 关于 AdSuper](#-关于-adsuper)
- [✨ 核心特性](#-核心特性)
- [🔄 工作流程](#-工作流程)
- [🚀 快速开始](#-快速开始)
- [📝 规则提交指南](#-规则提交指南)
- [🧩 规则格式详解](#-规则格式详解)
- [❓ 常见问题 FAQ](#-常见问题-faq)
- [📊 项目统计](#-项目统计)
- [🔗 与 FilterFusion 的关系](#-与-filterfusion-的关系)
- [🤝 贡献指南](#-贡献指南)

---

## 🎯 关于 AdSuper

> **AdSuper** 是一个面向社区的**广告规则收集与管理平台**，致力于汇聚全网最优质的广告过滤规则。

<table>
<tr>
<td width="50%" valign="top">

### 🎯 项目目标

- 🏗️ 建立社区驱动的规则审核系统
- 🤗 让任何人都能轻松提交规则
- ⚙️ 自动化同步、审核、打包规则
- 🔄 为 FilterFusion 提供持续规则更新

</td>
<td width="50%" valign="top">

### 📌 适用人群

- 🎯 广告过滤规则爱好者
- 🤝 希望帮助社区的志愿者
- 😤 遇到漏拦截/误拦截的用户
- 💻 维护自己规则库的开发者

</td>
</tr>
</table>

---

## ✨ 核心特性

<table>
<tr>
<td width="50%" valign="top">

### 🛡️ 自动化审核
通过 GitHub Issues 自动收集、审核和打包规则，全程零人工干预

### 🤝 社区协作
任何人都可以提交规则，人人可贡献，规则质量由社区共同维护

### ⚡ 高效同步
规则自动同步至 FilterFusion，实时更新到用户手中

</td>
<td width="50%" valign="top">

### 📊 质量保证
严格的审核流程，确保每条规则都经过测试验证

### 🔄 定期发布
每周一自动发布规则包，永远保持最新

### 📈 统计展示
贡献者统计、活跃度展示、完整历史记录一目了然

</td>
</tr>
</table>

---

## 🔄 工作流程

```
┌─────────────────┐
│  用户提交 Issue  │
└────────┬────────┘
         ↓
┌─────────────────┐
│  规则审核        │
└────────┬────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
 ❌ 不合适    ✅ 合适
 (关闭)       ↓
       ┌─────────────────────┐
       │ 自动收录到 adnew.txt │
       │  (每 3 天同步一次)   │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ 每周一打包发布 Release│
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ 同步到 FilterFusion  │
       └─────────────────────┘
```

---

## 🚀 快速开始

### 📥 方式一：直接订阅规则（仅使用）

> 只想用规则？把下面链接添加到广告拦截器即可

将以下链接添加到你的广告拦截器（uBlock Origin / AdGuard / AdBlock 等）：

```
https://raw.githubusercontent.com/Chaniug/AdSuper/main/adnew.txt
```

<details>
<summary>📋 如何添加订阅链接？</summary>

| 拦截器 | 操作 |
|--------|------|
| **uBlock Origin** | 设置 → 规则列表 → 自定义 → 导入 → 粘贴链接 |
| **AdGuard** | 设置 → 过滤器 → 添加订阅 → 粘贴链接 |
| **AdBlock Plus** | 设置 → 高级 → 添加过滤规则订阅 → 粘贴链接 |
| **Brave 浏览器** | 设置 → Shields → 过滤列表 → 自定义 → 粘贴链接 |

</details>

### 📝 方式二：提交规则（参与贡献）

1. **点击提交** → [提交新规则 Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml)

2. **填写内容**：
   - 规则类型（域名、元素隐藏等）
   - 具体的规则内容
   - 说明为什么需要这条规则

3. **等待审核**：
   - ✅ 维护者会在 24-48 小时内审核
   - 通过 → 标记 `good`
   - 拒绝 → 标记 `not planned`

4. **自动收录**：
   - 通过的规则每 3 天自动同步到 `adnew.txt`
   - 每周一发布 Release 规则包

### 💬 方式三：参与讨论

- 在 [Discussions](https://github.com/Chaniug/AdSuper/discussions) 分享想法
- 在 [Issues](https://github.com/Chaniug/AdSuper/issues) 反馈问题

---

## 📝 规则提交指南

### ✅ 提交前检查清单

在提交规则前，请确保：

- [ ] 规则语法正确（见下方格式详解）
- [ ] 规则尚未存在于库中
- [ ] 规则有实际的拦截效果
- [ ] 不会误拦截正常网站
- [ ] 用代码块（```）包裹规则内容，方便提取

### 📋 提交规则的正确做法

<table>
<tr>
<td width="50%" valign="top">

#### ✅ 好的例子

用代码块包裹规则：

```
Issue 标题: 拦截 xxxxx 广告域名
Issue 内容:
```
||ads.example.com^
```
说明: 这个域名投放大量弹窗广告
```

</td>
<td width="50%" valign="top">

#### ❌ 不好的例子

规则夹在文字中：
```
Issue 标题: 新规则
Issue 内容: 我发现这些规则 
||ads1.com^ 和 ||ads2.com^ 都要拦截
```

虽然也能识别，但不便于审核。

</td>
</tr>
</table>

### 📌 规则来源说明

提交规则时，最好说明规则来源：

| 来源 | 说明 |
|------|------|
| 🔍 自己发现 | 自己浏览时发现的垃圾广告域名 |
| 📚 规则库转移 | 从其他规则库迁移过来的 |
| 👥 用户反馈 | 用户反馈的常见广告 |
| 🔗 其他 | 其他来源（请注明） |

---

## 🧩 规则格式详解

<details>
<summary><b>1️⃣ 域名匹配规则（最常用）</b></summary>

```
||example.com^
```

**说明**：
- `||` 表示域名的开始
- `example.com` 是要匹配的域名
- `^` 表示分隔符（域名结束）
- 效果：拦截来自 `example.com` 和 `*.example.com` 的所有请求

**示例**：
```
||ads.google.com^           # 拦截 Google 广告服务
||doubleclick.net^          # 拦截 DoubleClick 广告网络
||analytics.google.com^     # 拦截 Google Analytics（可选）
```

</details>

<details>
<summary><b>2️⃣ 带参数的规则</b></summary>

```
||ads.example.com^$script,image
```

**参数说明**：
- `$script` - 仅拦截脚本文件
- `$image` - 仅拦截图片
- `$stylesheet` - 仅拦截样式表
- `$xmlhttprequest` - 仅拦截 AJAX 请求
- `$third-party` - 仅拦截第三方请求

**示例**：
```
||ads.example.com^$script          # 只拦截脚本
||tracker.com^$xmlhttprequest      # 只拦截追踪请求
||ads.cdn.com^$image,script        # 拦截图片和脚本
```

</details>

<details>
<summary><b>3️⃣ 路径和通配符</b></summary>

```
||example.com/ads/*^
example.com/banner*
```

**说明**：
- `*` 代表任意字符
- `/ads/*` 匹配 `/ads/` 后的所有内容

**示例**：
```
||ads.example.com/tracker*         # 拦截 /tracker 开头的所有请求
example.com/banner-*-ad            # 拦截 banner-XXX-ad 形式的资源
```

</details>

<details>
<summary><b>4️⃣ 元素隐藏规则</b></summary>

```
example.com##.ad-banner
```

**说明**：
- `##` 表示元素隐藏
- `.ad-banner` 是 CSS 选择器
- 效果：隐藏 `example.com` 上 class 为 `ad-banner` 的元素

**示例**：
```
example.com##.advertisement        # 隐藏广告类元素
example.com##div[id*="ad"]        # 隐藏 id 包含 "ad" 的 div
example.com##a[href*="ads"]       # 隐藏链接到广告的 a 标签
```

</details>

<details>
<summary><b>5️⃣ 白名单规则</b></summary>

```
@@||example.com^$document
```

**说明**：
- `@@` 表示白名单（例外）
- 不拦截该域名上的请求
- 通常用于避免误拦截

**示例**：
```
@@||analytics.example.com^         # 白名单某个域名
@@||trusted-cdn.com^$script        # 白名单可信脚本
```

</details>

<details>
<summary><b>6️⃣ 正则表达式规则（高级）</b></summary>

```
/banner.*\.jpg$/
```

**说明**：
- `/` 包围正则表达式
- 用于复杂的匹配逻辑

**示例**：
```
/^https?:\/\/ads\d+\.example\.com/  # 匹配 ads1.example.com、ads2.example.com 等
/(ads|banner|promo)\.(jpg|png|gif)$/  # 匹配多个文件名和扩展名
```

</details>

<details>
<summary><b>7️⃣ 注释</b></summary>

```
! 这是注释
# 这也是注释
```

</details>

---

## ❓ 常见问题 FAQ

<details>
<summary><b>Q1: 如何知道规则是否有效？</b></summary>

提交规则时请说明：
- 你在哪个网站看到这个广告
- 如何复现这个广告
- 提交的规则是否已测试

维护者会在测试后才会批准规则。

</details>

<details>
<summary><b>Q2: 我提交的规则被拒绝了，为什么？</b></summary>

常见原因：
1. **规则格式错误** - 检查语法是否正确
2. **规则过于宽泛** - 可能误拦截正常网站
3. **规则重复** - 已存在类似规则
4. **无法验证** - 难以确认效果
5. **与隐私无关** - 仅针对某个网站的个人需求

**解决方法**：
- 重新修改规则
- 在 Comment 中解释问题
- 咨询维护者或社区

</details>

<details>
<summary><b>Q3: 规则多久会生效？</b></summary>

1. 规则通过审核 - 立即标记为 ✅ `good`
2. 自动同步 - 每 3 天运行一次，将规则收录到 `adnew.txt`
3. 定期打包 - 每周一发布 Release 规则包
4. FilterFusion 同步 - 主项目定期拉取新规则
5. 用户更新规则 - 用户订阅规则后自动获取

**预计时间**：从提交到用户生效 **3-9 天**（中位数约 5 天）

</details>

<details>
<summary><b>Q4: 可以提交多条规则在一个 Issue 里吗？</b></summary>

**可以**。AdSuper 的规则提取器支持多种格式：

- ✅ 代码块包裹（推荐，多条规则用换行分隔）
- ✅ 列表项格式（`- ||xxx^` 或 `1. ||xxx^`）
- ✅ 内联反引号（`` `||xxx^` ``）
- ✅ 规则直接写在标题或正文

**建议**：同类型的规则可以放一个 Issue，用代码块包裹便于审核。不同类型的规则（如域名规则和元素隐藏规则）建议分开提交，方便追踪讨论。

</details>

<details>
<summary><b>Q5: 如何修改或删除已通过的规则？</b></summary>

- **修改**：新建 Issue 说明问题，重新提交修改后的规则
- **删除**：在对应的已完成 Issue 中评论说明原因，维护者会处理

</details>

<details>
<summary><b>Q6: 规则会支持哪些格式？</b></summary>

AdSuper 支持 **Adblock Plus (ABP) 通用格式**：

| 格式 | 支持情况 |
|------|---------|
| 域名匹配规则 | ✅ 完全支持 |
| 元素隐藏规则 | ✅ 完全支持 |
| 路径和通配符 | ✅ 完全支持 |
| 正则表达式 | ✅ 完全支持 |
| 白名单规则 | ✅ 完全支持 |
| uBlock Origin 专有语法 | ⚠️ 部分支持 |
| DNS 级别规则 | ❌ 不支持 |

</details>

<details>
<summary><b>Q7: 提交的规则会被用在哪里？</b></summary>

你的规则会被用在：
1. **AdSuper 自身** - `adnew.txt` 规则文件
2. **FilterFusion** - 主项目的规则聚合中
3. **全网用户** - 任何订阅这些规则的用户

</details>

<details>
<summary><b>Q8: 我对某个规则有疑问，怎么讨论？</b></summary>

你可以：
1. 在对应 Issue 的 Comment 中讨论
2. 在 [Discussions](https://github.com/Chaniug/AdSuper/discussions) 区提问
3. 提交新 Issue 说明问题

</details>

<details>
<summary><b>Q9: 如何成为项目贡献者？</b></summary>

- 提交被采纳的规则自动成为贡献者
- 活跃提交规则的用户会获得特殊徽章
- 参与讨论和代码贡献也算贡献

查看 [贡献者名单](https://github.com/Chaniug/AdSuper/graphs/contributors)

</details>

<details>
<summary><b>Q10: 可以用于商业项目吗？</b></summary>

**可以**。AdSuper 的规则和代码遵循：

| 内容 | 许可 |
|------|------|
| 规则内容 | 开源社区规则，自由使用 |
| 项目代码 | MIT License（允许商业使用） |
| 唯一要求 | 保留原始许可证和版权声明 |

</details>

---

## 📊 项目统计

### 👥 贡献者

<p align="center">
  <img src="https://contrib.rocks/image?repo=Chaniug/AdSuper" alt="Contributors" />
</p>

### 📈 活跃度

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Chaniug&repo=AdSuper&theme=github-compact" alt="Activity Graph" />
</p>

### 📋 规则统计

| 指标 | 说明 |
|------|------|
| 📝 总规则数 | 持续增长 |
| 🔄 自动更新 | 每 3 天同步 + 每周一发布 |
| 👥 贡献者数 | 见上方统计 |
| ⭐ 项目 Star | 感谢支持 |

---

## 🔗 与 FilterFusion 的关系

<table>
<tr>
<td width="50%" align="center">

### 🎯 FilterFusion

**主项目**

聚合多源规则，生成最终的广告过滤列表

</td>
<td width="50%" align="center">

### 🤝 AdSuper

**子项目**

社区规则收集平台，为主项目提供规则源

</td>
</tr>
</table>

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

**总结**：
- 🌟 AdSuper 是 FilterFusion 的**规则输入来源**
- 🔄 FilterFusion 是 AdSuper 规则的**最终汇总地**
- 📚 更多规则资源和详情，请访问 [FilterFusion](https://github.com/Chaniug/FilterFusion)

---

## 🤝 贡献指南

### 贡献方式

<table>
<tr>
<td width="50%" valign="top">

#### 1️⃣ 提交规则（最直接）

[📝 点此提交规则 Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml)

- 填写规则内容和说明
- 等待审核

</td>
<td width="50%" valign="top">

#### 2️⃣ 参与讨论

[💬 Join Discussions](https://github.com/Chaniug/AdSuper/discussions)

- 帮助其他用户
- 提出改进建议

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 3️⃣ 报告问题

[🐛 提交 Issue](https://github.com/Chaniug/AdSuper/issues)

- 发现 BUG？反馈给我们
- 提出改进建议
- 反馈新的广告来源

</td>
<td width="50%" valign="top">

#### 4️⃣ 代码贡献

- Fork 项目
- 改进脚本和自动化流程
- 提交 Pull Request

</td>
</tr>
</table>

### 贡献要求

| 类型 | 要求 |
|------|------|
| ✅ **必须** | 规则语法正确 · 用代码块包裹规则内容 · 提供清晰的说明 |
| ⚠️ **建议** | 测试规则是否有效 · 检查是否会误拦截 · 参考现有规则风格 |

---

## 📬 联系与支持

### 🔗 快速链接

| 链接 | 说明 |
|------|------|
| [FilterFusion](https://github.com/Chaniug/FilterFusion) | 🎯 主项目 |
| [提交规则](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad) | 📝 提交新规则 |
| [Discussions](https://github.com/Chaniug/AdSuper/discussions) | 💬 参与讨论 |
| [Issues](https://github.com/Chaniug/AdSuper/issues) | 🐛 报告问题 |
| [Releases](https://github.com/Chaniug/AdSuper/releases) | 📦 查看发布 |

### 📱 社交媒体

| 平台 | 链接 |
|------|------|
| 🌐 个人主页 | [my.valk.ccwu.cc](https://my.valk.ccwu.cc/) |
| 🐦 X (Twitter) | [@valkjin](https://x.com/valkjin) |
| ✈️ Telegram | [@valkjin](https://t.me/valkjin) |
| 📧 邮箱 | [cheniug99@gmail.com](mailto:cheniug99@gmail.com) |

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Chaniug&repo=AdSuper&label=Views&color=0e75b6&style=flat" alt="Views" />
  <img src="https://img.shields.io/github/last-commit/Chaniug/AdSuper?style=flat&color=blue" alt="Last Commit" />
  <img src="https://img.shields.io/github/license/Chaniug/AdSuper?style=flat&color=green" alt="License" />
</p>

<p align="center">
  <b>🙏 感谢每一位贡献者和用户的支持！</b><br>
  <sub>💡 有想法？💪 想参与？👋 欢迎加入我们！</sub>
</p>

<p align="center">
  <sub>Made with ❤️ by the AdSuper community</sub>
</p>
