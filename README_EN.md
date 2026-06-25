# 🚀 AdSuper

<p align="center">
  <a href="https://github.com/Chaniug/FilterFusion">
    <img src="https://img.shields.io/badge/Main%20Project-FilterFusion-blue?logo=github&style=for-the-badge" />
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
  <b>📦 Community-driven ad rule collection platform</b><br>
  <sub>Submit · Review · Auto-publish · Share worldwide</sub>
</p>

<p align="center">
  <a href="https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml">
    <img src="https://img.shields.io/badge/📝_Submit_Rule-Issue-success?style=for-the-badge" />
  </a>
  <a href="https://raw.githubusercontent.com/Chaniug/AdSuper/main/adnew.txt">
    <img src="https://img.shields.io/badge/📥_Subscribe-adnew.txt-blue?style=for-the-badge" />
  </a>
  <a href="https://github.com/Chaniug/AdSuper/releases">
    <img src="https://img.shields.io/badge/📦_Releases-View-orange?style=for-the-badge" />
  </a>
</p>

---

**[中文](./README.md)** | **English**

---

## 📖 Table of Contents

- [🎯 About AdSuper](#-about-adsuper)
- [✨ Key Features](#-key-features)
- [🔄 Workflow](#-workflow)
- [🚀 Quick Start](#-quick-start)
- [📝 Submission Guide](#-submission-guide)
- [🧩 Rule Format Guide](#-rule-format-guide)
- [❓ FAQ](#-faq)
- [📊 Project Statistics](#-project-statistics)
- [🔗 Relationship with FilterFusion](#-relationship-with-filterfusion)
- [🤝 Contributing Guidelines](#-contributing-guidelines)

---

## 🎯 About AdSuper

> **AdSuper** is a community-driven **ad filter rule collection and management platform** dedicated to aggregating high-quality ad-filtering rules from around the web.

<table>
<tr>
<td width="50%" valign="top">

### 🎯 Project Goals

- 🏗️ Establish a community-driven rule review system
- 🤗 Enable anyone to easily submit rules
- ⚙️ Automate syncing, review, and packaging
- 🔄 Provide continuous updates to FilterFusion

</td>
<td width="50%" valign="top">

### 📌 Who Should Use This

- 🎯 Ad-filtering rule enthusiasts
- 🤝 Volunteers wanting to help
- 😤 Users with missed/false blocks
- 💻 Developers maintaining rule libraries

</td>
</tr>
</table>

---

## ✨ Key Features

<table>
<tr>
<td width="50%" valign="top">

### 🛡️ Automated Review
Collect, review, and package rules automatically via GitHub Issues

### 🤝 Community Collaboration
Anyone can submit rules - truly crowdsourced

### ⚡ Efficient Sync
Rules automatically sync to FilterFusion with real-time updates

</td>
<td width="50%" valign="top">

### 📊 Quality Assurance
Strict review process ensures rule quality

### 🔄 Regular Releases
Automatic rule package release every Monday

### 📈 Statistics Display
Contributor stats, activity metrics, complete history

</td>
</tr>
</table>

---

## 🔄 Workflow

```
┌─────────────────┐
│  User Submits   │
│     Issue       │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Rule Review    │
└────────┬────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
 ❌ Reject  ✅ Approve
 (Close)      ↓
       ┌─────────────────────┐
       │ Added to adnew.txt  │
       │ (synced every 3d)   │
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ Weekly Release (Mon)│
       └──────────┬──────────┘
                  ↓
       ┌─────────────────────┐
       │ Sync to FilterFusion│
       └─────────────────────┘
```

---

## 🚀 Quick Start

### 📥 Method 1: Subscribe to Rules (Just Use)

> Just want to use the rules? Add the URL below to your ad blocker

Add the following URL to your ad blocker (uBlock Origin / AdGuard / AdBlock etc.):

```
https://raw.githubusercontent.com/Chaniug/AdSuper/main/adnew.txt
```

<details>
<summary>📋 How to add subscription URL?</summary>

| Blocker | Steps |
|---------|-------|
| **uBlock Origin** | Settings → Filter lists → Custom → Import → Paste URL |
| **AdGuard** | Settings → Filters → Add subscription → Paste URL |
| **AdBlock Plus** | Settings → Advanced → Add filter subscription → Paste URL |
| **Brave Browser** | Settings → Shields → Filter lists → Custom → Paste URL |

</details>

### 📝 Method 2: Submit Rules (Contribute)

1. **Click to Submit** → [Submit New Rule Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml)

2. **Fill in Details**:
   - Rule type (domain, element hiding, etc.)
   - Specific rule content
   - Explanation of why this rule is needed

3. **Wait for Review**:
   - ✅ Maintainers will review within 24-48 hours
   - Approved → marked `good`
   - Rejected → marked `not planned`

4. **Auto-Inclusion**:
   - Approved rules synced to `adnew.txt` every 3 days
   - Released in weekly rule package (every Monday)

### 💬 Method 3: Participate in Discussion

- Visit [Discussions](https://github.com/Chaniug/AdSuper/discussions) to share ideas
- Report issues on [Issues](https://github.com/Chaniug/AdSuper/issues)

---

## 📝 Submission Guide

### ✅ Pre-Submission Checklist

Before submitting a rule, ensure:

- [ ] Rule syntax is correct (see Format Guide below)
- [ ] Rule doesn't already exist in the library
- [ ] Rule actually blocks the intended ads
- [ ] Won't cause false positives
- [ ] Wrap rules in code blocks (```) for easier extraction

### 📋 Correct Submission Examples

<table>
<tr>
<td width="50%" valign="top">

#### ✅ Good Example

Rules wrapped in code block:

```
Issue Title: Block xxxxx ad domain
Issue Content:
```
||ads.example.com^
```
Explanation: This domain serves lots of pop-up ads
```

</td>
<td width="50%" valign="top">

#### ❌ Bad Example

Rules mixed with text:
```
Issue Title: New rules
Issue Content: I found these rules
||ads1.com^ and ||ads2.com^ to block
```

Recognizable but harder to review.

</td>
</tr>
</table>

### 📌 Rule Source Information

When submitting, it's helpful to mention the rule source:

| Source | Description |
|--------|-------------|
| 🔍 Self-discovered | Ads you discovered yourself |
| 📚 Migrated | Rules migrated from other lists |
| 👥 User-reported | Common ads reported by users |
| 🔗 Other | Other sources (please specify) |

---

## 🧩 Rule Format Guide

<details>
<summary><b>1️⃣ Domain Matching Rules (Most Common)</b></summary>

```
||example.com^
```

**Explanation**:
- `||` marks domain start
- `example.com` is the domain to match
- `^` is a separator (marks domain end)
- Effect: Blocks all requests from `example.com` and `*.example.com`

**Examples**:
```
||ads.google.com^           # Block Google ad services
||doubleclick.net^          # Block DoubleClick ad network
||analytics.google.com^     # Block Google Analytics (optional)
```

</details>

<details>
<summary><b>2️⃣ Rules with Parameters</b></summary>

```
||ads.example.com^$script,image
```

**Parameter Explanation**:
- `$script` - Only block script files
- `$image` - Only block images
- `$stylesheet` - Only block stylesheets
- `$xmlhttprequest` - Only block AJAX requests
- `$third-party` - Only block third-party requests

**Examples**:
```
||ads.example.com^$script          # Only block scripts
||tracker.com^$xmlhttprequest      # Only block tracking requests
||ads.cdn.com^$image,script        # Block images and scripts
```

</details>

<details>
<summary><b>3️⃣ Paths and Wildcards</b></summary>

```
||example.com/ads/*^
example.com/banner*
```

**Explanation**:
- `*` represents any character
- `/ads/*` matches anything after `/ads/`

**Examples**:
```
||ads.example.com/tracker*         # Block /tracker and following
example.com/banner-*-ad            # Block banner-XXX-ad pattern resources
```

</details>

<details>
<summary><b>4️⃣ Element Hiding Rules</b></summary>

```
example.com##.ad-banner
```

**Explanation**:
- `##` marks element hiding
- `.ad-banner` is a CSS selector
- Effect: Hides elements with class `ad-banner` on `example.com`

**Examples**:
```
example.com##.advertisement        # Hide ad class elements
example.com##div[id*="ad"]        # Hide divs with "ad" in id
example.com##a[href*="ads"]       # Hide links to ads
```

</details>

<details>
<summary><b>5️⃣ Whitelist Rules</b></summary>

```
@@||example.com^$document
```

**Explanation**:
- `@@` marks whitelist (exception)
- Don't block requests from this domain
- Usually prevents false positives

**Examples**:
```
@@||analytics.example.com^         # Whitelist specific domain
@@||trusted-cdn.com^$script        # Whitelist trusted scripts
```

</details>

<details>
<summary><b>6️⃣ Regular Expression Rules (Advanced)</b></summary>

```
/banner.*\.jpg$/
```

**Explanation**:
- `/` surrounds regex pattern
- Used for complex matching logic

**Examples**:
```
/^https?:\/\/ads\d+\.example\.com/  # Match ads1.example.com, ads2.example.com, etc.
/(ads|banner|promo)\.(jpg|png|gif)$/  # Match multiple filenames and extensions
```

</details>

<details>
<summary><b>7️⃣ Comments</b></summary>

```
! This is a comment
# This is also a comment
```

</details>

---

## ❓ FAQ

<details>
<summary><b>Q1: How do I know if my rule is effective?</b></summary>

When submitting, please explain:
- Which website has this ad
- How to reproduce the ad
- Whether you've tested the rule

Maintainers will only approve rules they've verified.

</details>

<details>
<summary><b>Q2: Why was my rule rejected?</b></summary>

Common reasons:
1. **Incorrect syntax** - Check rule syntax
2. **Too broad** - Might block legitimate content
3. **Duplicate** - Similar rule already exists
4. **Unverifiable** - Can't confirm effectiveness
5. **Unrelated** - Targets individual site preference

**Solutions**:
- Revise and resubmit
- Explain in comments
- Ask maintainers for guidance

</details>

<details>
<summary><b>Q3: How long until a rule takes effect?</b></summary>

1. Rule approved - immediately marked ✅ `good`
2. Auto-sync - rules synced to `adnew.txt` every 3 days
3. Regular packaging - release published every Monday
4. FilterFusion sync - main project pulls updates
5. User update - automatic when users refresh rules

**Estimated time**: 3-9 days from submission to user effect (median ~5 days)

</details>

<details>
<summary><b>Q4: Can I submit multiple rules in one Issue?</b></summary>

**Yes**. AdSuper's rule extractor supports multiple formats:

- ✅ Code blocks (recommended, separate multiple rules with newlines)
- ✅ List items (`- ||xxx^` or `1. ||xxx^`)
- ✅ Inline backticks (`` `||xxx^` ``)
- ✅ Rules directly in title or body

**Recommendation**: Same-type rules can be in one Issue (use code blocks for easier review). Different-type rules (e.g., domain rules vs. element hiding) should be submitted separately for better tracking.

</details>

<details>
<summary><b>Q5: How do I modify or delete an approved rule?</b></summary>

- **Modify**: Create new Issue with corrected rule
- **Delete**: Comment on completed Issue explaining reason, maintainer will handle

</details>

<details>
<summary><b>Q6: What rule formats are supported?</b></summary>

AdSuper supports **Adblock Plus (ABP) standard format**:

| Format | Support |
|--------|---------|
| Domain matching rules | ✅ Full |
| Element hiding rules | ✅ Full |
| Paths and wildcards | ✅ Full |
| Regular expressions | ✅ Full |
| Whitelist rules | ✅ Full |
| uBlock Origin-specific | ⚠️ Partial |
| DNS-level rules | ❌ Not supported |

</details>

<details>
<summary><b>Q7: Where will my submitted rule be used?</b></summary>

Your rule will be used in:
1. **AdSuper itself** - `adnew.txt` rule file
2. **FilterFusion** - Aggregated in main project rules
3. **Worldwide users** - Anyone subscribing to these rules

</details>

<details>
<summary><b>Q8: I have questions about a rule, how do I discuss?</b></summary>

You can:
1. Comment on the related Issue
2. Ask in [Discussions](https://github.com/Chaniug/AdSuper/discussions)
3. Submit new Issue explaining the problem

</details>

<details>
<summary><b>Q9: How do I become a contributor?</b></summary>

- Submit approved rules automatically makes you a contributor
- Active rule submissions earn special badges
- Code and discussion contributions also count

View [Contributors](https://github.com/Chaniug/AdSuper/graphs/contributors)

</details>

<details>
<summary><b>Q10: Can I use this commercially?</b></summary>

**Yes**. AdSuper rules and code follow:

| Content | License |
|---------|---------|
| Rule content | Community rules, free to use |
| Project code | MIT License (commercial use allowed) |
| Only requirement | Keep original license and copyright notice |

</details>

---

## 📊 Project Statistics

### 👥 Contributors

<p align="center">
  <img src="https://contrib.rocks/image?repo=Chaniug/AdSuper" alt="Contributors" />
</p>

### 📈 Activity

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Chaniug&repo=AdSuper&theme=github-compact" alt="Activity Graph" />
</p>

### 📋 Rule Statistics

| Metric | Description |
|--------|-------------|
| 📝 Total Rules | Growing continuously |
| 🔄 Auto-Updates | Synced every 3 days + released every Monday |
| 👥 Contributors | See above stats |
| ⭐ Project Stars | Thank you for support! |

---

## 🔗 Relationship with FilterFusion

<table>
<tr>
<td width="50%" align="center">

### 🎯 FilterFusion

**Main Project**

Aggregates multiple rule sources, generates final ad-filtering list

</td>
<td width="50%" align="center">

### 🤝 AdSuper

**Sub-Project**

Community rule collection platform, provides rule source for main project

</td>
</tr>
</table>

### Architecture

```
Community users submit rules to AdSuper
         ↓
     Review and include
         ↓
FilterFusion automatically pulls rules
         ↓
Merge with other rule sources and deduplicate
         ↓
Generate final rule file
         ↓
Users subscribe and use
```

**Summary**:
- 🌟 AdSuper is the **rule input source** for FilterFusion
- 🔄 FilterFusion is the **final aggregation** of AdSuper rules
- 📚 For more resources and details, visit [FilterFusion](https://github.com/Chaniug/FilterFusion)

---

## 🤝 Contributing Guidelines

### Ways to Contribute

<table>
<tr>
<td width="50%" valign="top">

#### 1️⃣ Submit Rules (Most Direct)

[📝 Submit Rule Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad&template=rule_report.yml)

- Fill in rule content and explanation
- Wait for review

</td>
<td width="50%" valign="top">

#### 2️⃣ Participate in Discussion

[💬 Join Discussions](https://github.com/Chaniug/AdSuper/discussions)

- Help other users
- Suggest improvements

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 3️⃣ Report Issues

[🐛 Submit Issue](https://github.com/Chaniug/AdSuper/issues)

- Found a bug? Report it
- Suggest improvements
- Report new ad sources

</td>
<td width="50%" valign="top">

#### 4️⃣ Code Contribution

- Fork the project
- Improve scripts and automation
- Submit Pull Request

</td>
</tr>
</table>

### Contribution Requirements

| Type | Requirements |
|------|--------------|
| ✅ **Must** | Correct rule syntax · Wrap rules in code blocks · Clear explanation |
| ⚠️ **Recommended** | Test rule effectiveness · Check for false positives · Follow existing rule style |

---

## 📬 Contact & Support

### 🔗 Quick Links

| Link | Description |
|------|-------------|
| [FilterFusion](https://github.com/Chaniug/FilterFusion) | 🎯 Main project |
| [Submit Rule](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad) | 📝 Submit new rule |
| [Discussions](https://github.com/Chaniug/AdSuper/discussions) | 💬 Join discussion |
| [Issues](https://github.com/Chaniug/AdSuper/issues) | 🐛 Report issue |
| [Releases](https://github.com/Chaniug/AdSuper/releases) | 📦 View releases |

### 📱 Social Media

| Platform | Link |
|----------|------|
| 🌐 Website | [my.valk.ccwu.cc](https://my.valk.ccwu.cc/) |
| 🐦 X (Twitter) | [@valkjin](https://x.com/valkjin) |
| ✈️ Telegram | [@valkjin](https://t.me/valkjin) |
| 📧 Email | [cheniug99@gmail.com](mailto:cheniug99@gmail.com) |

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Chaniug&repo=AdSuper&label=Views&color=0e75b6&style=flat" alt="Views" />
  <img src="https://img.shields.io/github/last-commit/Chaniug/AdSuper?style=flat&color=blue" alt="Last Commit" />
  <img src="https://img.shields.io/github/license/Chaniug/AdSuper?style=flat&color=green" alt="License" />
</p>

<p align="center">
  <b>🙏 Thank you to every contributor and user for your support!</b><br>
  <sub>💡 Got ideas? 💪 Want to participate? 👋 Welcome to join us!</sub>
</p>

<p align="center">
  <sub>Made with ❤️ by the AdSuper community</sub>
</p>
