# 🚀 AdSuper规则收集与管理工具

[![主项目 @Chaniug/FilterFusion](https://img.shields.io/badge/Main%20Project-FilterFusion-blue?logo=github)](https://github.com/Chaniug/FilterFusion)
[![贡献者](https://img.shields.io/github/contributors/Chaniug/AdSuper)](https://github.com/Chaniug/AdSuper/graphs/contributors)
[![活跃度](https://img.shields.io/github/commit-activity/m/Chaniug/AdSuper)](https://github.com/Chaniug/AdSuper/commits/master)
[![Issues](https://img.shields.io/github/issues/Chaniug/AdSuper)](https://github.com/Chaniug/AdSuper/issues)
[![Stars](https://img.shields.io/github/stars/Chaniug/AdSuper?style=social)](https://github.com/Chaniug/AdSuper/stargazers)

---

## 😎 项目简介

🎯 **AdSuper** 是一个专为广告过滤规则收集与管理设计的项目。它通过 GitHub Issues 让大家轻松提交和反馈广告过滤规则，自动化同步并打包规则文件，助力主项目 [FilterFusion](https://github.com/Chaniug/FilterFusion) 的持续完善！

- 🛡️ 自动化收集与审核规则
- 🤝 社区协作，人人可贡献
- ⚡ 高效同步与打包，规则更新及时

---

## 📝 如何参与和提交规则？

1. **点击右上角的 `New Issue` 按钮**，或[点这里提交](https://github.com/Chaniug/AdSuper/issues/new?labels=ad-rule)。
2. 在 Issue 标题或正文中填写你要反馈的广告过滤规则（支持 Adblock/ABP 语法）。
3. **务必添加 `ad-rule` 标签**（新建 Issue 默认已选中）。
4. 等待维护者审核，标记为 `completed` 后，规则将会自动收录！
5. 如规则不合适将被标记为 `not planned` 或关闭/删除。

---

## 🧩 规则反馈示例

```txt
||example-ad.com^
||ads.anotherdomain.com^$script,image
@@||gooddomain.com^$document
example.org##.ad-banner
```

> ❤️ **每条规则建议单独开 issue，方便追踪和讨论。**

---

## 📦 文件说明

| 文件名              | 说明                       |
|---------------------|----------------------------|
| `AdSuper.txt`       | 主规则文件（需人工维护）   |
| `adnew.txt`         | 自动收集合并的新规则文件   |
| `sync_issues.py`    | 同步脚本                   |
| `.github/workflows/`| 自动化脚本 & 打包配置      |

---

## 🔗 主项目 FilterFusion

本项目为 [@Chaniug/FilterFusion](https://github.com/Chaniug/FilterFusion) 的规则收集与维护仓库。  
**最新、最完整的规则整合与下载请前往主项目！**

---

## 🤗 贡献指南

- 欢迎任何人提交广告规则！只需点击 [New Issue](https://github.com/Chaniug/AdSuper/issues/new?labels=ad-rule) 填写内容即可。
- 规则被采纳后会自动收录进 adnew.txt 并定期打包发布。
- 定期活跃与贡献还可获得贡献者徽章！

---

## 💡 特色与优势

- 🌍 全社区协作、支持多种规则格式
- 🧑‍💻 完全自动化同步和打包
- 🕒 每5天自动发布新规则包（[Release](https://github.com/Chaniug/AdSuper/releases)）
- 🏆 贡献值与活跃度实时展示

---

> 📢 **有建议或问题？欢迎随时[提Issue](https://github.com/Chaniug/AdSuper/issues)或参与讨论！**

---
