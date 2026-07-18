---
name: "bms-weekly-report"
description: "Generates a weekly BMS (Battery Management System) tracking report with 6 sections (trends, papers, vendor news, open source, patents, standards) and pushes it to WeChat Official Account draft box. Invoke when user asks to create/publish/update the BMS weekly report or says 'BMS 算法追踪'."
---

# BMS Weekly Report Generator

This skill generates a comprehensive weekly BMS (Battery Management System) technology tracking report and pushes it to a WeChat Official Account draft box.

## When to Invoke

- User asks to generate/create/publish the BMS weekly report
- User says "BMS 算法追踪" or "周报" or "weekly report"
- User asks to update or fix the BMS report content
- User asks to push content to WeChat draft box

## Report Structure

The report contains 6 sections in this exact order:

1. **本周趋势展望** (3-5 items, at the top, no source links, each 1-2 sentences)
2. **一、学术论文进展** (10 items)
3. **二、厂商动态** (10 items)
4. **三、开源项目与数据集** (10 items)
5. **四、专利技术** (10 items)
6. **五、行业标准** (10 items)

Total: 53-55 entries, each with a valid source link dated within the past 7 days.

## Source Grading System

| Tier | Color | Scope |
|------|-------|-------|
| T1 | `#6abf69` (green) | Top-tier journals/conferences, government data, academicians/top labs |
| T2 | `#4a90d9` (blue) | SCI journals, IEEE/JPS/EST, authoritative media, arXiv top-level |
| T3 | `#e67e22` (orange) | Enterprise official releases, domestic core journals, industry news |
| T4 | `#9b59b6` (purple) | Industry blogs, self-media (avoid if possible) |

### Section-to-Tier Mapping

| Section | T1 | T2 | T3 | T4 |
|---------|----|----|----|----|
| Papers | Nature/Science | SCI journals, arXiv top-level | Domestic core journals | — |
| Vendor | Government policy | Authoritative media | Enterprise official | Industry news/self-media |
| Open Source | — | — | GitHub projects | — |
| Patents | — | — | Enterprise patents | — |
| Standards | Mandatory national | Recommended national | Group standards | — |

**Critical rule**: Apply tiers consistently within each source type.

## Content Source Requirements

- **Papers**: Prioritize SCI journals (Applied Energy, J. Power Sources, Nature Energy). Use arXiv as fallback. Each paper's tag row must include the journal source name (e.g., "arXiv", "Applied Energy").
- **Vendor news**: Use reliable sources only (新浪财经, 东方财富, 搜狐, 人民网, OFweek). **NEVER use toutiao.com links**.
- **Open source**: GitHub Releases from the past 7 days.
- **Patents**: Google Patents, prefer CN patents, published within 7 days.
- **Standards**: National standards system, MIIT, NEA official sites.

## HTML Format Specification

### All styles must be inline (WeChat strips `<style>` and `<a>` tags)

### H2 Title Style
```html
<h2 style="font-size:19px;color:#111;margin:24px 0 12px 0;padding-bottom:8px;border-bottom:2px solid #4a90d9;font-weight:bold;text-align:left;">Section Title</h2>
```

### Left Border Colors by Section

| Section | Border Color |
|---------|-------------|
| Trends | `#4a90d9` (blue) |
| Papers | `#4a90d9` (blue) |
| Vendor News | `#27ae60` (green) |
| Open Source | `#4a90d9` (blue) |
| Patents | `#e67e22` (orange) |
| Standards | `#e67e22` (orange) |

### Paper Entry Template (arXiv / T2)
```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">T2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">arXiv</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">TopicTag</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">N · Paper Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50-100 char abstract</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">💡 <b>创新:</b>50-100 char innovation</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://arxiv.org/abs/XXXX.XXXXX</span></div></section>
```

### Paper Entry Template (SCI Journal / T1)
Same structure but:
- T1 badge: `background:#6abf69` instead of `#4a90d9`
- Journal name badge: e.g., "Applied Energy", "J. Power Sources"
- Source URL: `https://doi.org/...`

### Vendor News Entry Template
```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#6abf69;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">T1</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag1</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag2</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">N · Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50-100 char abstract</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">URL</span></div></section>
```

### Patent Entry Template (border-left: #e67e22)
Includes: 申请人, 摘要, 创新 (each 50-100 chars)

### Standard Entry Template (border-left: #e67e22)
Includes: 目的, 核心内容, 实施 (each 50-100 chars)

### Footer Template
```html
<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;"><div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">事实核查声明：本期内容来源已标注，T4级信源仅供参考，不构成投资建议。</div><div style="font-size:14px;color:#4a90d9;font-weight:bold;">🔋 BMS 算法追踪</div><div style="font-size:11px;color:#aaa;margin-top:4px;">关注电池管理系统前沿 | 每周更新</div></section>
```

## Content Length Requirements

| Field | Length (Chinese chars) |
|-------|----------------------|
| Trend items | 30-60 chars (1-2 sentences) |
| Paper abstract/innovation | 50-100 chars each |
| Vendor abstract | 50-100 chars |
| Open source abstract | 50-100 chars |
| Patent abstract/innovation | 50-100 chars each |
| Standard purpose/core content | 50-100 chars each |

## WeChat Push Specification

### Parameters
- **AppID**: `wx6faba10fc6b42653`
- **AppSecret**: `edf800d13ce266ad5c8d7e15a75ea6eb`
- **Title format**: `BMS 算法追踪 YYYY-MM-DD`
- **Author**: `算法`
- **Cover image**: Deep blue tech background, two lines of text: "BMS 算法追踪" and date "YYYY-MM-DD"

### API Flow
1. Get access_token: `GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}`
2. Upload cover image: `POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image`
3. Push draft: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}`

### CRITICAL: Encoding Requirements

**Wrong approaches that cause Chinese garbling:**
```python
# WRONG: json= parameter
r = requests.post(url, json=draft_data)
# WRONG: r.json() for response
result = r.json()
# WRONG: missing charset in Content-Type
headers = {'Content-Type': 'application/json'}
```

**Correct approach:**
```python
import json, requests

payload = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')
headers = {'Content-Type': 'application/json; charset=utf-8'}
r = requests.post(url, data=payload, headers=headers)
result = json.loads(r.content.decode('utf-8'))
```

### Post-Push Verification
1. Read back draft via `POST /cgi-bin/draft/get`
2. Verify: title contains date, Chinese chars > 5000, H2 count = 6, URL count > 50, journal badge count = 10

## Common Pitfalls and Solutions

1. **Chinese garbling**: Use `ensure_ascii=False` + `encode('utf-8')` + `Content-Type: application/json; charset=utf-8` + `r.content.decode('utf-8')`
2. **`<a>` tags stripped by WeChat**: Use `<span style="color:#4a90d9;">URL</span>` instead
3. **Format inconsistency within sections**: Use Python template functions to generate all entries uniformly
4. **Tier misclassification**: Top-tier=T1, SCI/arXiv=T2, enterprise/core=T3, self-media=T4
5. **Missing journal name in paper tag row**: First tag position must be journal source name
6. **toutiao.com links**: Never use; replace with 新浪财经/东方财富/搜狐/人民网/OFweek
7. **Date out of range**: All entries must be within 7 days of publish date
8. **Python string quote conflicts**: Chinese quotes `""` inside Python strings cause SyntaxError; use `\u201c` `\u201d` Unicode escapes
9. **Trends section placement**: Must be at the very top, before all other sections, with no introductory paragraph
10. **Cover image format**: Deep blue background with two lines of text, generated via AI image generation
11. **Unicode escape sequence corruption (CRITICAL)**: When writing Chinese chars as `\uXXXX` in Python strings, if the next character is a hex digit (0-9, a-f, A-F), Python may incorrectly absorb it into the escape sequence. `\u` takes EXACTLY 4 hex digits. Example: `\u9700` (需) followed by `20636` is correct, but `\u9702` (霂) is wrong. **Known corruption pairs**: 锐(U+9510)→锂(U+9502), 锔(U+9514)→锂(U+9502), 斛(U+659B)→斩(U+65A9), 铢(U+94E2)→钧(U+94A7), 轶(U+8F76)→机(U+673A), 蓓(U+84D3)→蓄(U+84C4), 霂(U+9702)→需(U+9700). **Always render strings and scan for rare CJK chars after generation**. Prefer writing actual UTF-8 Chinese characters directly in Python source instead of `\uXXXX` escapes when possible.
12. **DOI verification**: Always verify DOI URLs via `requests.head()` before including. Applied Energy DOIs follow format `10.1016/j.apenergy.YYYY.NNNNNN` — verify the article number via Crossref API (`api.crossref.org`) before use.
13. **GitHub releases links**: Some repos have no tagged releases. Use the repo main URL (`github.com/user/repo`) instead of `/releases` when no releases exist. Verify via GitHub API: `api.github.com/repos/{owner}/{repo}`.
14. **Google Patents timeouts**: `patents.google.com` may timeout in HEAD requests. Verify patent numbers via CNIPA (`epub.cnipa.gov.cn`) or financial media sources instead. The Google Patents URL format `patents.google.com/patent/{PUBLICATION_NUMBER}` is reliable when the patent number is correct.
15. **CIAPS standard URLs**: `ciaps.org.cn/news/standard` does not exist. Use `escn.com.cn` or CIAPS announcement pages with specific item IDs (e.g., `ciaps.org.cn/news/show-htm-itemid-XXXXX.html`).

## Complete Color Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Green | `#6abf69` | T1 badge background |
| Blue | `#4a90d9` | T2 badge, paper/open-source left border, link text, H2 underline |
| Orange | `#e67e22` | T3 badge, patent/standard left border |
| Purple | `#9b59b6` | T4 badge |
| Dark Green | `#27ae60` | Vendor news left border |
| Light Green | `#d4edda` | Topic tag badge background |
| Dark Green Text | `#155724` | Topic tag badge text |
| Light Green BG | `#e8f5e9` | Date badge background |
| Dark Green Date | `#2e7d32` | Date badge text |
| Near Black | `#111` | Title text |
| Dark Gray | `#333` | Body text |
| Gray | `#888` | Source label text |
| Light Gray BG | `#f5f5f5` | Footer background |
| Light Gray | `#aaa` | Footer subtitle |

## Execution Checklist

After generating content, verify:

- [ ] 6 H2 sections in correct order (trends first, standards last)
- [ ] Trends: 3-5 items, no links, no intro paragraph, each 1-2 sentences
- [ ] Papers: 10 items, all have journal name in tag row, tiers consistent (T1 top-tier, T2 SCI/arXiv, T3 domestic core)
- [ ] Vendor news: 10 items, no toutiao.com links, border `#27ae60`
- [ ] Open source: 10 items, all GitHub links, border `#4a90d9`
- [ ] Patents: 10 items, each has 申请人/摘要/创新 (50-100 chars), border `#e67e22`
- [ ] Standards: 10 items, each has 目的/核心内容/实施 (50-100 chars), border `#e67e22`
- [ ] All dates within 7 days, format `📅YYYY-MM-DD`
- [ ] All links use `<span>` not `<a>`
- [ ] All styles are inline
- [ ] Footer section present
- [ ] Title format: `BMS 算法追踪 YYYY-MM-DD`
- [ ] Cover image: deep blue, two lines of text
- [ ] Push encoding: `ensure_ascii=False` + `charset=utf-8`
- [ ] Post-push verification passed
- [ ] **Unicode corruption scan**: Render all strings, check for rare CJK chars (frequency=1), verify no `\uXXXX` followed by hex digit in source
- [ ] **Link validation**: Run `requests.head()` on all URLs; fix any 404/timeout; verify DOIs via Crossref; verify GitHub repos exist; verify patent numbers via CNIPA
