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
    <img src="https://img.shields.io/github/stars/Chaniug/AdSuper?style=social" />
  </a>
</p>

**[中文](./README.md)** | **English**

---

## 📖 Table of Contents

- [About AdSuper](#-about-adsuper)
- [Key Features](#-key-features)
- [Workflow](#-workflow)
- [Quick Start](#-quick-start)
- [Submission Guide](#-submission-guide)
- [Rule Format Guide](#-rule-format-guide)
- [FAQ](#-faq)
- [Project Statistics](#-project-statistics)
- [Relationship with FilterFusion](#-relationship-with-filterfusion)
- [Contributing Guidelines](#-contributing-guidelines)

---

## 😎 About AdSuper

**AdSuper** is a community-driven **ad filter rule collection and management platform** dedicated to aggregating high-quality ad-filtering rules from around the web.

🎯 **Project Goals**:
- Establish a community-driven rule review system
- Enable anyone to easily submit and maintain ad-filtering rules
- Automate rule syncing, review, and packaging to ensure quality and timeliness
- Provide continuous rule updates to the FilterFusion main project

📌 **Who Should Use This**:
- Ad-filtering rule enthusiasts
- Volunteers who want to help improve rules
- Users encountering missed or false-positive blocks
- Developers who want to maintain their own rule libraries

---

## ⚡ Key Features

| Feature | Description |
|---------|-------------|
| 🛡️ **Automated Review** | Automatically collect, review, and package rules via GitHub Issues |
| 🤝 **Community Collaboration** | Anyone can submit rules - truly crowdsourced |
| ⚡ **Efficient Sync** | Rules automatically sync to FilterFusion with real-time updates |
| 📊 **Quality Assurance** | Strict review process ensures rule quality |
| 🔄 **Regular Releases** | Automatic rule package releases every 5 days |
| 📈 **Statistics Display** | Contributor stats, activity metrics, complete history |

---

## 🔄 Workflow

```
User Submits Issue
     ↓
[Issue Template] Rule Review
     ↓
❌ Not Suitable → Mark "not planned" (Close)
     ↓ ✅ Suitable
Automatically Added to adnew.txt
     ↓
Regular Packaging (Every 5 Days)
     ↓
Release Published
     ↓
Sync to FilterFusion Main Project
```

---

## 🚀 Quick Start

### Method 1: Submit an Issue (Recommended)

1. **Click to Submit**: [Submit New Rule Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule&template=rule_report.yml)

2. **Fill in Details**:
   - Rule type (domain, element hiding, etc.)
   - Specific rule content
   - Explanation of why this rule is needed

3. **Wait for Review**:
   - Maintainers will review within 24-48 hours
   - Approved rules marked ✅ `completed`
   - Rejected rules marked ❌ `not planned`

4. **Auto-Inclusion**:
   - Approved rules automatically added to the rule library
   - Included in next release package

### Method 2: Participate in Discussion

- Visit [Discussions](https://github.com/Chaniug/AdSuper/discussions) to share ideas
- Report issues on [Issues](https://github.com/Chaniug/AdSuper/issues)
- Join the community

---

## 📝 Submission Guide

### Pre-Submission Checklist

Before submitting a rule, ensure:

- [ ] Rule syntax is correct (see Format Guide below)
- [ ] Rule doesn't already exist in the library
- [ ] Rule actually blocks the intended ads
- [ ] Won't cause false positives
- [ ] One Issue contains only one rule

### Correct Submission Examples

✅ **Good Example**:
```
Issue Title: Block xxxxx ad domain
Issue Content: ||ads.example.com^
Explanation: This domain serves lots of pop-up ads
```

❌ **Bad Example**:
```
Issue Title: New rules
Issue Content: Multiple rules mixed together
||ads1.com^
||ads2.com^
```

### Rule Source Information

When submitting, it's helpful to mention the rule source:
- Ads you discovered yourself
- Rules migrated from other lists
- Common ads reported by users
- Other sources (please specify)

---

## 🧩 Rule Format Guide

### 1. Domain Matching Rules (Most Common)

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

### 2. Rules with Parameters

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

### 3. Paths and Wildcards

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

### 4. Element Hiding Rules

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

### 5. Whitelist Rules

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

### 6. Regular Expression Rules (Advanced)

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

### 7. Comments

```
! This is a comment
# This is also a comment
```

---

## ❓ FAQ

### Q1: How do I know if my rule is effective?

**A**: When submitting, please explain:
- Which website has this ad
- How to reproduce the ad
- Whether you've tested the rule

Maintainers will only approve rules they've verified.

### Q2: Why was my rule rejected?

**A**: Common reasons:
1. **Incorrect syntax** - Check rule syntax
2. **Too broad** - Might block legitimate content
3. **Duplicate** - Similar rule already exists
4. **Unverifiable** - Can't confirm effectiveness
5. **Unrelated** - Targets individual site preference

**Solutions**:
- Revise and resubmit
- Explain in comments
- Ask maintainers for guidance

### Q3: How long until a rule takes effect?

**A**: Timeline:
1. Rule approved - immediately marked ✅ `completed`
2. Regular packaging - released every 5 days
3. FilterFusion sync - main project pulls updates
4. User update - automatic when users refresh rules

**Estimated time**: 5-7 days from submission to user effect

### Q4: Can I submit multiple rules in one Issue?

**A**: **Not recommended**. Reasons:
- Hard to track individual rules
- Lower review efficiency
- If one rule has issues, entire Issue affected

**Recommendation**: One rule per Issue.

### Q5: How do I modify or delete an approved rule?

**A**: 
- **Modify**: Create new Issue with corrected rule
- **Delete**: Comment on completed Issue explaining reason, maintainer will handle

### Q6: What rule formats are supported?

**A**: AdSuper supports **Adblock Plus (ABP) standard format**:
- ✅ Domain matching rules
- ✅ Element hiding rules
- ✅ Paths and wildcards
- ✅ Regular expressions
- ✅ Whitelist rules
- ⚠️ uBlock Origin-specific syntax (partial support)
- ❌ DNS-level rules (not supported)

### Q7: Where will my submitted rule be used?

**A**: Your rule will be used in:
1. **AdSuper itself** - `adnew.txt` rule file
2. **FilterFusion** - Aggregated in main project rules
3. **Worldwide users** - Anyone subscribing to these rules

### Q8: I have questions about a rule, how do I discuss?

**A**: You can:
1. Comment on the related Issue
2. Ask in [Discussions](https://github.com/Chaniug/AdSuper/discussions)
3. Submit new Issue explaining the problem

### Q9: How do I become a contributor?

**A**: 
- Submit approved rules automatically makes you a contributor
- Active rule submissions earn special badges
- Code and discussion contributions also count

View [Contributors](https://github.com/Chaniug/AdSuper/graphs/contributors)

### Q10: Can I use this commercially?

**A**: **Yes**. AdSuper rules and code follow:
- **Rule content** - Community rules, free to use
- **Project code** - MIT License (commercial use allowed)
- **Only requirement** - Keep original license and copyright notice

---

## 📊 Project Statistics

### Contributors

<p align="center">
  <img src="https://contrib.rocks/image?repo=Chaniug/AdSuper" alt="Contributors" />
</p>

### Activity

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=Chaniug&repo=AdSuper&theme=github-compact" alt="Activity Graph" />
</p>

### Rule Statistics

- 📝 **Total Rules** - Growing continuously
- 🔄 **Auto-Updates** - Released every 5 days
- 👥 **Contributors** - See above stats
- ⭐ **Project Stars** - Thank you for support!

---

## 🔗 Relationship with FilterFusion

| Project | Description |
|---------|------------|
| **FilterFusion** | 🎯 Main project - Aggregates multiple rule sources, generates final ad-filtering list |
| **AdSuper** | 🤝 Sub-project - Community rule collection platform, provides rule source for main project |

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

#### 1. Submit Rules (Most Direct)
- [Submit Rule Issue](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule&template=rule_report.yml)
- Fill in rule content and explanation
- Wait for review

#### 2. Participate in Discussion
- Visit [Discussions](https://github.com/Chaniug/AdSuper/discussions)
- Help other users
- Suggest improvements

#### 3. Report Issues
- Found a bug? [Submit Issue](https://github.com/Chaniug/AdSuper/issues)
- Suggest improvements
- Report new ad sources

#### 4. Code Contribution
- Fork the project
- Improve scripts and automation
- Submit Pull Request

### Contribution Requirements

✅ **Must**:
- Correct rule syntax
- One rule per Issue
- Clear explanation

⚠️ **Recommended**:
- Test rule effectiveness
- Check for false positives
- Follow existing rule style

---

## 📬 Contact & Support

### Quick Links

- 🔗 [Main Project FilterFusion](https://github.com/Chaniug/FilterFusion)
- 📝 [Submit Rule](https://github.com/Chaniug/AdSuper/issues/new?assignees=&labels=ad-rule)
- 💬 [Discussions](https://github.com/Chaniug/AdSuper/discussions)
- 🐛 [Report Issue](https://github.com/Chaniug/AdSuper/issues)
- 📦 [View Releases](https://github.com/Chaniug/AdSuper/releases)

### Social Media

- 🌐 [Personal Website](https://valk.ccwu.cc/)
- 🐦 [X (Twitter)](https://x.com/chenboss14)
- ✈️ [Telegram](https://t.me/chaniug)
- 📧 [Email](mailto:cheniug99@gmail.com)

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=Chaniug&repo=AdSuper&label=Views&color=0e75b6&style=flat" alt="Views" />
  <img src="https://img.shields.io/github/last-commit/Chaniug/AdSuper?style=flat&color=blue" alt="Last Commit" />
</p>

<p align="center">
  <b>🙏 Thank you to every contributor and user for your support!</b><br>
  💡 Got ideas? 💪 Want to participate? 👋 Welcome to join us!
</p>
