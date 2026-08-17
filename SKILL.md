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
2. **一、学术论文进展** (10 items: 6 high-IF journal papers + 4 arXiv papers)
3. **二、厂商动态** (10 items)
4. **三、开源项目与数据集** (10 items)
5. **四、专利技术** (10 items)
6. **五、行业标准** (10 items)

Total: 53-55 entries, each with a valid source link dated within the past 7 days.

## Source Rating System (Admiralty / NATO AJP-2.1)

Each entry carries a **dual-character rating** (e.g., `B2`): first char = **Source Reliability (A–F)**, second char = **Information Credibility (1–6)**. The two dimensions are rated independently — a highly reliable source may still publish unconfirmed information.

### Dimension 1 — Source Reliability (A–F)

| Grade | Badge Color | Scope |
|-------|-------|-------|
| A | `#6abf69` (green) | Government agency announcements & official platform published texts (CNCA/认监委, 全国标准信息公共服务平台 std.samr.gov.cn, NEA/MIIT) · Top-tier journals/conferences (Nature/Science series, IF>30) |
| B | `#4a90d9` (blue) | SCI journals (IF 5-30), IEEE/JPS/EST · Authoritative media (新浪财经 finance.sina.com.cn, 东方财富, 财联社) · Consultation notices from government-commissioned standards bodies (中电联 GB/DL 征求意见函) · Exchange filings/prospectuses · Broker research on authoritative platforms |
| C | `#e67e22` (orange) | arXiv preprints · Enterprise official releases · Professional open-source (GitHub) · Industry news platforms (北极星, 国际能源网, MarkLines) · Corporate patents (Google Patents first-hand texts) · Group standards (T/CEC 团体标准) · Industry data platforms (企查查/爱企查) |
| D/E | `#9b59b6` (purple) | Industry blogs, self-media aggregators (reference only, add disclaimer) |
| F | `#95a5a6` (gray) | Cannot be judged (fallback, rarely used) |

### Dimension 2 — Information Credibility (1–6)

| Score | Meaning |
|-------|---------|
| 1 | Confirmed by independent sources |
| 2 | Probably true — reliable single-source first-hand text (official announcement, DOI paper text, patent text, exchange filing) |
| 3 | Possibly true — single-source relay/reprint, unverified (arXiv claims, industry-platform reprints, aggregator stats) |
| 4 | Doubtful · 5 = Improbable · 6 = Cannot be judged |

### Section-to-Rating Mapping (defaults, adjust per entry as evidence dictates)

| Section | Typical ratings |
|---------|-----------------|
| Papers | Nature/Science-tier = **A2**; other high-IF SCI = **B2**; arXiv preprints = **C3** (not peer-reviewed → credibility 3) |
| Vendor | Authoritative media reporting official events = **B2**; enterprise official site = **C2**; industry news relaying official announcements = **C2** (dual-source) or **C3** (single relay); aggregator stats (企查查) = **C3**; self-media = **D3** |
| Open Source | GitHub repo first-hand = **C2** |
| Patents | Google Patents first-hand text = **C2**; 企查查/爱企查 relay of patent grant = **C3** |
| Standards | Official platform published text (CNCA, std.samr.gov.cn) = **A2**; GB/DL consultation notices via 中电联 = **B2** (commissioned industry association, not government itself); 中电联 T/CEC group standards = **C2** |

**Critical rules**:
1. Rate the **direct publisher** of the linked text, not the ultimate authority behind the story. A DL-standard consultation notice is published by 中电联 (industry association commissioned by government) → B, not A. It becomes A only after NEA/国标委 officially publishes the final text on a government platform.
2. Do not let source reliability leak into credibility: high-grade source + unconfirmed claim still gets credibility 3.
3. Apply ratings consistently within each source type.

### Grading Legend Block (insert between trends and Section 一)

```html
<section style="margin:24px 0 12px 0;padding:14px 16px;background:#f5f9ff;border-left:3px solid #4a90d9;border-radius:4px;"><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:4px;">📌 信源分级说明 · Admiralty / NATO AJP-2.1</div><div style="font-size:12px;color:#555;line-height:1.7;margin-bottom:10px;">本报告采用 OSINT 开源情报领域公认的 Admiralty 评级标准（北约 AJP-2.1）：每条内容以双字符评级标注，首字符评<strong>信源可靠性</strong>，次字符评<strong>信息可信度</strong>，如 B2 = 通常可靠信源 × 很可能属实。两维独立评估，互不绑定。</div><div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin-bottom:4px;">信源可靠性 Source Reliability（A–F）</div><div style="font-size:13px;color:#333;line-height:2.1;"><span style="background:#6abf69;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">A</span> 完全可靠 · 政府机构公告与官方平台正式发布文本 · SCI 顶刊顶会<br/><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B</span> 通常可靠 · SCI 期刊 · 权威学术出版 · 权威媒体 · 受政府委托标准组织的征求意见公告<br/><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C</span> 相当可靠 · arXiv 预印本 · 专业开源社区 · 企业官方发布 · 行业资讯 · 团体标准<br/><span style="background:#9b59b6;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">D/E</span> 通常不可靠 / 不可靠 · 行业博客 / 自媒体<br/><span style="background:#95a5a6;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">F</span> 无法判断</div><div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin:8px 0 4px;">信息可信度 Information Credibility（1–6）</div><div style="font-size:13px;color:#333;line-height:2.1;"><b>1</b> 完全可信，已被独立信源证实&nbsp;&nbsp;<b>2</b> 很可能属实，可靠单源一手文本&nbsp;&nbsp;<b>3</b> 可能属实，单源转述待核&nbsp;&nbsp;<b>4</b> 存疑&nbsp;&nbsp;<b>5</b> 不可能&nbsp;&nbsp;<b>6</b> 真实性无法判断</div><div style="font-size:12px;color:#888;line-height:1.7;margin-top:8px;">注：信源可靠性仅刻画信源先验，不等价于信息已被证实；D/E 及 4/5 档条目仅供参考，不构成投资建议。</div></section>
```

## Content Source Requirements

- **Papers (CRITICAL - 6+4 composition rule)**: The 10 papers MUST consist of exactly **6 high-impact-factor journal papers** + **4 arXiv preprints**.
  - **6 journal papers**: Selected from high-IF SCI journals (see "Recommended High-IF Journals" table below). A2 for Nature/Science-tier (IF>30), B2 for other SCI journals (IF 5-30). Each must include journal name in tag row and a valid DOI link (`https://doi.org/...`). Verify DOI via Crossref API before use.
  - **4 arXiv papers**: Selected from arXiv preprints within the past 7 days. All rated **C3** (preprint = C-grade source, not peer-reviewed = credibility 3). Each must include "arXiv" in tag row and a valid arXiv link (`https://arxiv.org/abs/XXXX.XXXXX`).
  - Each paper's tag row must include the journal source name (e.g., "Applied Energy", "arXiv").
- **Vendor news**: Use reliable sources only (新浪财经 finance.sina.com.cn, 东方财富, 财联社, 人民网, OFweek desktop URLs). **NEVER use toutiao.com links**. **NEVER use cj.sina.com.cn / 新浪看点 self-media articles** — they are user-generated content (user-ID URLs), not editorial; replace with a finance.sina.com.cn official report or downgrade to D3.
- **Open source**: GitHub Releases from the past 7 days.
- **Patents**: Google Patents, prefer CN patents, published within 7 days.
- **Standards**: National standards system, MIIT, NEA official sites.

## Recommended High-IF Journals for Papers

When selecting the 6 journal papers, prioritize journals from this list (2024 JCR Impact Factor data):

### Top-tier journals (IF > 30) → A2 badge (`background:#6abf69`)

| Journal | IF (2024) | Publisher | BMS Relevance |
|---------|-----------|-----------|---------------|
| Nature Energy | 60.1 | Springer Nature | Medium |
| Electrochemical Energy Reviews | 36.3 | Springer | Medium-High |
| Joule | 35.4 | Cell Press / Elsevier | Medium |
| Energy & Environmental Science | 30.8 | Royal Society of Chemistry | Medium-High |

### B2-tier journals (IF 5-30, SCI)

| Journal | IF (2024) | Publisher | BMS Relevance |
|---------|-----------|-----------|---------------|
| Energy Storage Materials | ~18.9 | Elsevier | Medium-High |
| ACS Energy Letters | ~19.3 | ACS | Medium |
| Applied Energy | ~11.0 | Elsevier | **High** |
| Energy Conversion and Management | ~9.9 | Elsevier | Medium-High |
| Battery Energy | ~9.0 | Wiley | **High** |
| Journal of Energy Storage | ~8.9 | Elsevier | **High** |
| Journal of Power Sources | ~8.0 | Elsevier | **High** |
| IEEE Trans. on Industrial Electronics | ~7.5 | IEEE | **High** |
| IEEE Trans. on Power Electronics | ~6.5 | IEEE | **High** |
| Electrochimica Acta | ~5.5 | Elsevier | Medium |

**Selection priority**: Prefer journals marked "High" BMS relevance when available. If no suitable High-relevance paper is found in a given week, expand to Medium-High or Medium relevance journals.

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

### Paper Entry Template (arXiv / C3)
```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C3</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">arXiv</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">TopicTag</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">N · Paper Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50-100 char abstract</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">💡 <b>创新:</b>50-100 char innovation</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://arxiv.org/abs/XXXX.XXXXX</span></div></section>
```

### Paper Entry Template (SCI Journal / A2 or B2)
Same structure but:
- A2 badge: `background:#6abf69` (Nature/Science-tier); B2 badge: `background:#4a90d9` (other SCI)
- C3 badge: `background:#e67e22` (arXiv)
- Journal name badge: e.g., "Applied Energy", "J. Power Sources"
- Source URL: `https://doi.org/...`

### Vendor News Entry Template
```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag1</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag2</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">N · Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50-100 char abstract</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">URL</span></div></section>
```

### Patent Entry Template (border-left: #e67e22)
Includes: 申请人, 摘要, 创新 (each 50-100 chars)

### Standard Entry Template (border-left: #e67e22)
Includes: 目的, 核心内容, 实施 (each 50-100 chars)

### Footer Template
```html
<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;"><div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">事实核查声明：本期内容来源已按 Admiralty / NATO AJP-2.1 标准双维评级标注，D/E 级信源条目仅供参考，不构成投资建议。</div><div style="font-size:14px;color:#4a90d9;font-weight:bold;">🔋 BMS 算法追踪</div><div style="font-size:11px;color:#aaa;margin-top:4px;">关注电池管理系统前沿 | 每周更新</div></section>
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
2. Verify: title contains date, Chinese chars > 5000, H2 count = 6, URL count > 50, journal badge count = 10, DOI count >= 6, arXiv count = 4, legend mentions "AJP-2.1" and appears before Section 一, dual-char rating badges (A2/B2/C2/C3/D3) counts match the generated report, and zero legacy `T[1-4]` badges remain (`re.findall(r">T[1-4]<", c)` must be empty)

## Common Pitfalls and Solutions

1. **Chinese garbling**: Use `ensure_ascii=False` + `encode('utf-8')` + `Content-Type: application/json; charset=utf-8` + `r.content.decode('utf-8')`
2. **`<a>` tags stripped by WeChat**: Use `<span style="color:#4a90d9;">URL</span>` instead
3. **Format inconsistency within sections**: Use Python template functions to generate all entries uniformly
4. **Rating misclassification (Admiralty)**: Rate the direct publisher, not the ultimate authority — 中电联 GB/DL consultation notices = B2 (not A2); government platform published texts = A2; arXiv = C3 (never B2 — preprints are not peer-reviewed); enterprise official = C2; self-media = D3. Credibility stays independent of source grade.
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
16. **Paper composition rule (CRITICAL)**: The 10 papers MUST be exactly 6 high-IF journal papers + 4 arXiv papers. Do NOT use 10 arXiv papers or 10 journal papers. Journal papers must have DOI links verified via Crossref; arXiv papers must have valid arXiv IDs. If fewer than 6 suitable journal papers are found in a given week, expand the search to adjacent fields (battery materials, electrochemistry, power electronics) rather than filling with more arXiv papers.
17. **OFweek mobile URLs return 403**: `mp.m.ofweek.com` URLs return HTTP 403 for HEAD/GET requests from scripts. Always use desktop OFweek URLs instead: `libattery.ofweek.com/YYYY-MM/ART-XXXXX-XXXXX-XXXXXXXXX.html` or `chuneng.ofweek.com/news/YYYY-MM/ART-XXXXX-XXXXX-XXXXXXXXX.html`. Verify the desktop URL exists before using.
18. **IEEE DOI format**: IEEE Xplore document numbers (arnumber) are NOT the DOI suffix. For example, arnumber 11301847 does NOT mean DOI `10.1109/TIE.2025.11301847`. Always verify IEEE DOIs via Crossref API (`api.crossref.org/works?query=...&filter=container-title:IEEE+Transactions+on+Industrial+Electronics`). The correct DOI suffix is typically a shorter number like `3634458`.
19. **Elsevier DOI year mismatch**: Elsevier DOIs use the DOI registration/creation year, which may differ from the publication year. For example, a paper published in 2025 may have DOI `10.1016/j.est.2024.115200` (created in 2024). Always verify via Crossref rather than guessing the year.
20. **Google Patents always timeout**: `patents.google.com` consistently times out for HEAD/GET requests from scripts (10+ seconds). Skip Google Patents URLs in link verification — the URL format `patents.google.com/patent/{PUBLICATION_NUMBER}` is reliable when the patent number is correct. Verify patent numbers via financial media or CNIPA instead.
21. **MIIT.gov.cn returns 403**: `miit.gov.cn` returns HTTP 403 for script requests. These URLs are valid in browsers but cannot be verified via `requests.head()`. Treat 403 from miit.gov.cn as "valid but not script-verifiable" rather than a broken link.
22. **Cover image text layout**: When generating cover images via AI, specify that text should be "centered and gathered, occupying roughly 60% of image width and 50% of image height" — NOT stretched edge to edge. AI image generators tend to stretch text to fill the full width, which looks unprofessional. Use visual engine to evaluate the generated cover before pushing.
23. **Unicode corruption scan refinement**: Common Chinese characters like 锂(U+9502), 机(U+673A), 蓄(U+84C4), 斩(U+65A9), 钧(U+94A7) are LEGITIMATE in battery-related text and should NOT be flagged as corrupted. Only truly rare characters like 霂(U+9702) indicate corruption. The scan function should only check for characters that would never appear legitimately in battery/BMS content.
24. **中电联 standard.cec.org.cn rating trap**: The site is operated by CEC (中国电力企业联合会), an industry ASSOCIATION commissioned by government — not a government agency. Two file types live there: DL power-industry standards & GB consultation notices = **B2** (commissioned body publishing, first-hand text); T/CEC group standards = **C2**. Only after NEA/国标委 publishes the final text on a government platform does the item qualify for A2.
25. **cj.sina.com.cn is self-media**: Sina 看点 articles under user-ID URLs (e.g. `cj.sina.com.cn/articles/view/2868676035/...`) are user-generated content, NOT 新浪财经 editorial. Do not rate them B. Either replace with a finance.sina.com.cn official report (search for the same event) or downgrade to D3.
26. **Aggregator links are not source links**: Never use 企查查/爱企查 **search-page URLs** (`aiqicha.baidu.com/s?q=...`) or `qcc.com` search links as entry sources — they are unstable and unverifiable. For patents, always use `patents.google.com/patent/{PUBLICATION_NUMBER}/zh` (C2, first-hand text); 企查查 detail-page relays of patent grants rate **C3** (relay, not first-hand).

## Complete Color Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Green | `#6abf69` | A badge background (reliability A) |
| Blue | `#4a90d9` | B badge, paper/open-source left border, link text, H2 underline |
| Orange | `#e67e22` | C badge, patent/standard left border |
| Purple | `#9b59b6` | D/E badge |
| Gray | `#95a5a6` | F badge (cannot be judged) |
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
- [ ] Papers: 10 items (6 high-IF journal + 4 arXiv), all have journal name in tag row, ratings consistent (A2 top-tier IF>30, B2 SCI IF 5-30, C3 arXiv)
- [ ] Papers: exactly 6 journal papers with DOI links + 4 arXiv papers with arXiv links
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