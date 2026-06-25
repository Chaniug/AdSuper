# AdSuper 规则格式说明

本文档说明 AdSuper 项目支持的所有广告过滤规则格式。

## 规则类型

### 1. 注释规则
以 `!` 开头的行，用于添加注释。

**示例**：
```
! 这是一个注释
! AdSuper 规则文件
```

---

### 2. 例外规则
以 `@@` 开头的规则，用于排除特定规则。

**示例**：
```
@@||example.com^
@@||ads.example.com^$important,document
@@||exception.com^$domain=example.com
```

---

### 3. 域名规则
以 `||` 开头的规则，用于屏蔽特定域名或 URL。

**格式**：
- `||domain^` - 屏蔽域名及其所有子路径
- `||domain^$option` - 带选项的域名规则
- `||domain$option` - 不带 `^` 的选项规则
- `||domain/path` - 屏蔽特定路径

**支持的选项**：
- `$important` - 重要规则（不会被后续规则禁用）
- `$document` - 应用于整个文档
- `$script` - 仅匹配脚本请求
- `$image` - 仅匹配图片请求
- `$third-party` - 仅匹配第三方请求
- `$app=com.example` - 应用于特定应用

**示例**：
```
||ads.example.com^
||tracker.example.com^$important
||cdn.example.com/ads/*.jpg$image
```

---

### 4. 元素隐藏规则
包含 `##` 的规则，用于隐藏页面元素。

**格式**：
- `domain##selector` - 单域名规则
- `domain1,domain2##selector` - 多域名规则
- `~third-party,domain##selector` - 带例外条件的规则

**支持的选择器**：
- 简单选择器：`.ad-banner`, `#ad-container`
- 属性选择器：`[class*="ad"]`, `[id^="ads-"]`
- 伪类：`:has()`, `:contains()`, `:matches-css()`
- 复杂选择器：`div.ad:not([id])`, `a:nth-child(3) > img`

**示例**：
```
example.com##.ad-banner
example.com###ad-container
aa3zz.com##*:matches-css(position:fixed):not(body):not(html)
apkmirror.com##div.ains:has(div.gooWidget)
godamh.com##.adshow:style(display: none !important;)
```

---

### 5. 元素隐藏例外规则
包含 `#@#` 的规则，用于排除特定元素隐藏规则。

**示例**：
```
example.com#@#.allowed-ad
```

---

### 6. 内联脚本规则
包含 `#$#` 的规则，用于注入内联脚本。

**示例**：
```
example.com#$#window.adsEnabled = false;
```

---

### 7. 网络请求规则
以 `|` 开头的规则，用于匹配完整的网络请求 URL。

**示例**：
```
|http://ads.example.com/|
|https://tracker.example.com/collect|
```

---

### 8. 高级规则选项

#### 移除 URL 参数
```
||example.com^$removeparam=utm_source
```

#### 设置 Content-Security-Policy
```
||example.com^$csp=script-src 'self'
```

#### 重定向请求
```
||ads.example.com^$redirect=noop.js
```

#### 禁用其他规则
```
||example.com^$badfilter
```

---

## 规则提取逻辑

### 从 GitHub Issues 提取规则

AdSuper 从带有 `ad` 和 `good` 标签的已关闭 issues 中提取规则。

**提取逻辑**：
1. **优先从 Markdown 代码块提取**：规则应该放在 ` ```adblock ` 或 ` ~~~ ` 代码块中。
2. ** fallback：从整个正文提取**：如果没有代码块，则从整个 issue 正文中提取。
3. **宽松判断**：使用启发式方法判断一行是否可能是规则，然后由 `RuleValidator` 进行精确验证。

**示例 Issue 格式**：

````markdown
标题：||ads.example.com^$important

正文：

以下是需要屏蔽的广告规则：

```adblock
||ads.example.com^$important
||tracker.example.com^
@@||exception.example.com^
example.com##.ad-banner
```
````

### 支持的规则格式

规则提取功能支持以下格式：
- ✅ 注释：`!` 开头的行
- ✅ 例外规则：`@@` 开头的行
- ✅ 域名规则：`||` 开头
- ✅ 元素隐藏规则：包含 `##`
- ✅ 元素隐藏例外：包含 `#@#`
- ✅ 内联脚本规则：包含 `#$#`
- ✅ 高级 CSS 选择器：`:has()`, `:contains()`, `:matches-css()` 等伪类
- ✅ 属性选择器：`[class*="ad"]`, `[id^="ads-"]`
- ✅ 多域名规则：`domain1,domain2##selector`
- ✅ 带例外条件的规则：`~third-party,domain##selector`

---

## 规则验证

提取的规则会经过 `RuleValidator` 的验证：
1. **格式检查**：检查规则格式是否正确
2. **冲突检测**：检测例外规则和普通规则的冲突
3. **去重**：移除重复的规则
4. **排序**：按规则类型排序

---

## 示例规则文件

查看项目中的 `adnew.txt` 和 `AdSuper.txt` 文件，了解实际的规则示例。

---

## 故障排除

### 规则未被提取
- 确保规则放在 ` ```adblock ` 代码块中
- 确保规则格式正确
- 运行 `python sync_issues.py` 测试规则提取和同步功能

### 规则验证失败
- 检查规则是否包含多个连续空格
- 检查注释格式是否正确（应使用 `!` 或 `##`）
- 查看运行日志中的错误信息

---

## 更多信息

- AdBlock Plus 规则编写指南：https://adblockplus.org/filter-cheatsheet
- uBlock Origin 维基：https://github.com/gorhill/uBlock/wiki/Filter-syntax
- AdSuper 项目文档：`PROJECT_DOCUMENTATION.md`
