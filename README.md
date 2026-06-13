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
    <img src="https://img.shields.io/github/stars/Chaniug/AdSuper?style=social" />
  </a>
</p>

**中文** | **[English](./README_EN.md)** 

---

## 📖 目录

- [关于 AdSuper](#-关于-adsuper)
- [核心特性](#-核心特性)
- [工作流程](#-工作流程)
- [快速开始](#-快速开始)
- [规则提交指南](#-规则提交指南)
- [规则格式详解](#-规则格式详解)
- [常见问题 FAQ](#-常见问题-faq)
- [项目统计](#-项目统计)
- [与 FilterFusion 的关系](#-与-filterfusion-的关系)
- [贡献指南](#-贡献指南)

---

## 😎 关于 AdSuper

**AdSuper** 是一个面向社区的**广告规则收集与管理平台**，致力于汇聚全网最优质的广告过滤规则。

🎯 **项目目标**：
- 建立一个由社区驱动的规则审核系统
- 让任何人都能轻松提交和维护广告过滤规则
- 自动化同步、审核、打包规则，保证规则的质量和时效性
- 为 FilterFusion 主项目提供持续的规则更新

📌 **适用人群**：
- 广告过滤规则爱好者
- 希望帮助社区改进规则的志愿者
- 遇到漏拦截或误拦截的用户
- 希望维护自己规则库的开发者

---

## ⚡ 核心特性

| 特性 | 说明 |
|------|------|
| 🛡️ **自动化审核** | 通过 GitHub Issues 自动收集、审核和打包规则 |
| 🤝 **社区协作** | 任何人都可以提交规则，人人可贡献 |
| ⚡ **高效同步** | 规则自动同步至 FilterFusion，实时更新 |
| 📊 **质量保证** | 严格的审核流程，确保规则质量 |
| 🔄 **定期发布** | 每 5 天自动发布一次规则包 |
| 📈 **统计展示** | 贡献者统计、活跃度展示、完整历史记录 |

---

## 🔄 工作流程

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

## 🚀 快速开始

### 方式一：直接提交 Issue（推荐）

1. **点击提交**：[提交新规则 Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule&template=rule_report.yml)

2. **填写内容**：
   - 规则类型（域名、元素隐藏等）
   - 具体的规则内容
   - 说明为什么需要这条规则

3. **等待审核**：
   - 维护者会在 24-48 小时内审核
   - 通过标记 ✅ `completed`
   - 拒绝标记 ❌ `not planned`

4. **自动收录**：
   - 通过的规则自动添加到规则库
   - 下次发布时包含在规则包中

### 方式二：参与讨论

- 在 [Discussions](https://github.com/Chaniug/AdSuper/discussions) 分享想法
- 在 [Issues](https://github.com/Chaniug/AdSuper/issues) 反馈问题

---

## 📝 规则提交指南

### 提交前检查清单

在提交规则前，请确保：

- [ ] 规则语法正确（见下方格式详解）
- [ ] 规则尚未存在于库中
- [ ] 规则有实际的拦截效果
- [ ] 不会误拦截正常网站
- [ ] 一条 Issue 只包含一条规则

### 提交规则的正确做法

✅ **好的例子**：
```
Issue 标题: 拦截 xxxxx 广告域名
Issue 内容: ||ads.example.com^
说明: 这个域名投放大量弹窗广告
```

❌ **不好的例子**：
```
Issue 标题: 新规则
Issue 内容: 多条规则混在一起
||ads1.com^
||ads2.com^
```

### 规则来源说明

提交规则时，最好说明规则来源：
- 自己发现的垃圾广告域名
- 从其他规则库转移的
- 用户反馈的常见广告
- 其他来源（请注明）

---

## 🧩 规则格式详解

### 1. 域名匹配规则（最常用）

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

### 2. 带参数的规则

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

### 3. 路径和通配符

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

### 4. 元素隐藏规则

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

### 5. 白名单规则

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

### 6. 正则表达式规则（高级）

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

### 7. 注释

```
! 这是注释
# 这也是注释
```

---

## ❓ 常见问题 FAQ

### Q1: 如何知道规则是否有效？

**A**: 提交规则时请说明：
- 你在哪个网站看到这个广告
- 如何复现这个广告
- 提交的规则是否已测试

维护者会在测试后才会批准规则。

### Q2: 我提交的规则被拒绝了，为什么？

**A**: 常见原因：
1. **规则格式错误** - 检查语法是否正确
2. **规则过于宽泛** - 可能误拦截正常网站
3. **规则重复** - 已存在类似规则
4. **无法验证** - 难以确认效果
5. **与隐私无关** - 仅针对某个网站的个人需求

**解决方法**：
- 重新修改规则
- 在 Comment 中解释问题
- 咨询维护者或社区

### Q3: 规则多久会生效？

**A**: 
1. 规则通过审核 - 立即标记为 ✅ `completed`
2. 定期打包发布 - 每 5 天发布一次 Release
3. FilterFusion 同步 - 主项目定期拉取新规则
4. 用户更新规则 - 用户订阅规则后自动获取

**预计时间**：从提交到用户生效 **5-7 天**（中位数）

### Q4: 可以提交多条规则在一个 Issue 里吗？

**A**: **不推荐**。原因：
- 难以追踪和讨论每条规则
- 审核效率低
- 如果一条规则有问题，整个 Issue 受影响

**建议**：一条 Issue 对应一条规则。

### Q5: 如何修改或删除已通过的规则？

**A**: 
- **修改**：新建 Issue 说明问题，重新提交修改后的规则
- **删除**：在对应的已完成 Issue 中评论说明原因，维护者会处理

### Q6: 规则会支持哪些格式？

**A**: AdSuper 支持 **Adblock Plus (ABP) 通用格式**：
- ✅ 域名匹配规则
- ✅ 元素隐藏规则
- ✅ 路径和通配符
- ✅ 正则表达式
- ✅ 白名单规则
- ⚠️ uBlock Origin 专有语法（部分支持）
- ❌ DNS 级别规则（不支持）

### Q7: 提交的规则会被用在哪里？

**A**: 你的规则会被用在：
1. **AdSuper 自身** - `adnew.txt` 规则文件
2. **FilterFusion** - 主项目的规则聚合中
3. **全网用��** - 任何订阅这些规则的用户

### Q8: 我对某个规则有疑问，怎么讨论？

**A**: 你可以：
1. 在对应 Issue 的 Comment 中讨论
2. 在 [Discussions](https://github.com/Chaniug/AdSuper/discussions) 区提问
3. 提交新 Issue 说明问题

### Q9: 如何成为项目贡献者？

**A**: 
- 提交被采纳的规则自动成为贡献者
- 活跃提交规则的用户会获得特殊徽章
- 参与讨论和代码贡献也算贡献

查看 [贡献者名单](https://github.com/Chaniug/AdSuper/graphs/contributors)

### Q10: 可以用于商业项目吗？

**A**: **可以**。AdSuper 的规则和代码遵循：
- **规则内容** - 开源社区规则，自由使用
- **项目代码** - MIT License（允许商业使用）
- **唯一要求** - 保留原始许可证和版权声明

---

## 📊 项目统计

### 贡献者

<p align="center">
  <img src="https://contrib.rocks/image?repo=Chaniug/AdSuper" alt="Contributors" />
</p>

### 活跃度

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Chaniug&repo=AdSuper&theme=github-compact" alt="Activity Graph" />
</p>

### 规则统计

- 📝 **总规则数** - 持续增长
- 🔄 **自动更新** - 每 5 天发布一次
- 👥 **贡献者数** - 见上方统计
- ⭐ **项目 Star** - 感谢支持

---

## 🔗 与 FilterFusion 的关系

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

**总结**：
- 🌟 AdSuper 是 FilterFusion 的**规则输入来源**
- 🔄 FilterFusion 是 AdSuper 规则的**最终汇总地**
- 📚 更多规则资源和详情，请访问 [FilterFusion](https://github.com/Chaniug/FilterFusion)

---

## 🤝 贡献指南

### 贡献方式

#### 1. 提交规则（最直接）
- [点此提交规则 Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule&template=rule_report.yml)
- 填写规则内容和说明
- 等待审核

#### 2. 参与讨论
- [Join Discussions](https://github.com/Chaniug/AdSuper/discussions) 区讨论
- 帮助其他用户
- 提出改进建议

#### 3. 报告问题
- 发现 BUG？[提交 Issue](https://github.com/Chaniug/AdSuper/issues)
- 提出改进建议
- 反馈新的广告来源

#### 4. 代码贡献
- Fork 项目
- 改进脚本和自动化流程
- 提交 Pull Request

### 贡献要求

✅ **必须**：
- 规则语法正确
- 一个 Issue 一条规则
- 提供清晰的说明

⚠️ **建议**：
- 测试规则是否有效
- 检查是否会误拦截
- 参考现有规则风格

---

## 📬 联系与支持

### 快速链接

- 🔗 [主项目 FilterFusion](https://github.com/Chaniug/FilterFusion)
- 📝 [提交规则](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule)
- 💬 [参与讨论](https://github.com/Chaniug/AdSuper/discussions)
- 🐛 [报告问题](https://github.com/Chaniug/AdSuper/issues)
- 📦 [查看发布](https://github.com/Chaniug/AdSuper/releases)

### 社交媒体

- 🌐 [个人主页](https://my.valk.ccwu.cc/)
- 🐦 [X (Twitter)](https://x.com/valkjin)
- ✈️ [Telegram](https://t.me/valkjin)
- 📧 [邮箱](mailto:cheniug99@gmail.com)

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Chaniug&repo=AdSuper&label=Views&color=0e75b6&style=flat" alt="Views" />
  <img src="https://img.shields.io/github/last-commit/Chaniug/AdSuper?style=flat&color=blue" alt="Last Commit" />
</p>

<p align="center">
  <b>🙏 感谢每一位贡献者和用户的支持！</b><br>
  💡 有想法？💪 想参与？👋 欢迎加入我们！
</p>
