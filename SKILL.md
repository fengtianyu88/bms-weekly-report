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

### Text Alignment (CRITICAL — added 2026-10-22)

Every entry `<section>` and every text `<div>` inside it MUST carry an explicit `text-align:left;`. Do not rely on inheritance.

Reason: WeChat renders divs with **justify** by default. Chinese-only paragraphs hide the problem, but a long English paper title (e.g. `9 · System Identification for Nonlinear Stochastic State-Space Models …`) has its first line stretched to full width, producing a visibly huge gap between `9 ·` and `System`. Users notice this immediately.

Apply to:
- entry `<section>` container
- title div (`N · Title`)
- 摘要 / 创新 / 申请人 / 目的 / 核心内容 / 实施 divs
- source line div (`来源:`)
- trends block

Verification after push: read back the draft and confirm `text-align:left` is still present in the title div (WeChat preserves it), and that no title div has inherited justify.

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
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;text-align:left;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C3</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">arXiv</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">TopicTag</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;text-align:left;">N · Paper Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;text-align:left;">📌 <b>摘要:</b>50-100 char abstract</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;text-align:left;">💡 <b>创新:</b>50-100 char innovation</div><div style="color:#888;font-size:12px;text-align:left;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://arxiv.org/abs/XXXX.XXXXX</span></div></section>
```

### Paper Entry Template (SCI Journal / A2 or B2)
Same structure but:
- A2 badge: `background:#6abf69` (Nature/Science-tier); B2 badge: `background:#4a90d9` (other SCI)
- C3 badge: `background:#e67e22` (arXiv)
- Journal name badge: e.g., "Applied Energy", "J. Power Sources"
- Source URL: `https://doi.org/...`

### Vendor News Entry Template
```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;text-align:left;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅YYYY-MM-DD</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag1</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Tag2</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;text-align:left;">N · Title</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;text-align:left;">📌 <b>摘要:</b>50-100 char abstract</div><div style="color:#888;font-size:12px;text-align:left;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">URL</span></div></section>
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

## Cross-Issue Deduplication (MANDATORY — added 2026-10-22)

A weekly report that repeats last week's items loses credibility. Before pushing, compare the draft against the previous **three** issues (`bms_weekly_*/bms_weekly_YYYY-MM-DD.html`, `bms-weekly-*/…`).

### Identity keys

Extract every entry's identity and match across issues:

| Section | Identity key |
|---------|--------------|
| Papers | DOI (`doi.org/…`) or arXiv ID (`arxiv.org/abs/…`, strip version suffix) |
| Vendors | Article URL |
| Open source | GitHub release tag URL (`.../releases/tag/<tag>`); repo homepage alone is NOT an identity |
| Patents | Patent number (CN…) or source article URL |
| Standards | `hcno` from `openstd.samr.gov.cn/...?hcno=…` or standard number (GB/T 48072-2026) |

`check_duplicates.py` pattern: parse each `<section style="margin-bottom:12px;padding:12px 14px…">`, extract the `N · Title` line and all URLs, then classify:
- **exact duplicate** — shared identity key
- **same project, new version** — same GitHub repo path, different release tag
- **high title similarity** — normalized title `difflib.SequenceMatcher ≥ 0.80`

### Rules

1. **Exact duplicates must be replaced** — 0 tolerated in papers / vendors / open source / patents, and **0 in standards**.
2. **Same-project releases**: at most **1 entry per repo per issue** (2 only if there is a major-version change). A 2026-10-22 draft initially carried 4 Predbat releases in one issue — unacceptable; keep the latest and fill the other slots with projects not covered recently.
3. **Standards rotation**: a standard must not reappear within **4 issues**. Check the standard number against the previous 3 issues before including it.
4. **Standards do not publish weekly**: the national standards platform may have no new battery standard for several weeks. In that case use the most recently published/announced items, keep their **true publication and implementation dates**, and state the actual dates in the `实施` field. Never fabricate a date inside the 7-day window. Papers / vendors / open source / patents must still be within 7 days.
5. After replacement, re-run the duplicate check and re-push; report the counts (exact duplicates / same-project / similar titles) to the user.

## Weekly Data Collection Recipes (verified 2026-10-22)

Use scripts in the week's folder; do not hand-type records from memory.

```text
bms_weekly_MMDD/
  collect_crossref.py     # journal papers
  collect_arxiv.py        # preprints
  collect_sina.py         # vendor news via Sina search API
  collect_github.py       # GitHub releases
  collect_std.py          # national standards list
  build_report.py         # content lists + HTML assembly
  make_cover.py           # PIL cover
  push_wechat.py          # idempotent draft push
  check_duplicates.py     # cross-issue dedup
  verify_links.py         # link/DOI validation
```

### Papers — Crossref

```python
url = (f"https://api.crossref.org/journals/{issn}/works"
       f"?filter=type:journal-article&rows=200"
       f"&select=DOI,title,created,abstract&sort=created&order=desc")
# keep created date in [START, END] and title matches BMS keywords
```

Journals/ISSN: Applied Energy `0306-2619`, J. Power Sources `0378-7753`, J. Energy Storage `2352-152X`, Energy Conversion and Management `0196-8904`, Battery Energy `2768-1688`, Energy Storage Materials `2405-8297`, ACS Energy Letters `2380-8195`, Electrochimica Acta `0013-4686`, IEEE TIE `0278-0046`, IEEE TPEL `0885-8993`, eTransportation `2590-1168`. Elsevier often omits abstracts — write Chinese summaries from the verified title, without inventing numbers.

### Papers — arXiv

```python
params = {"search_query": 'abs:"battery management"', "start": 0, "max_results": 60,
          "sortBy": "submittedDate", "sortOrder": "descending"}
# endpoint: http://export.arxiv.org/api/query
```

Filter `<published>` to the 7-day window; dedupe by arXiv ID.

### Vendor news — Sina search API

```python
u = f"https://search.sina.com.cn/api/news?q={quote(q)}&page=1&size=50"
# fields: dataTime, title, intro, url
```

Query company + battery keywords (宁德时代/比亚迪/亿纬锂能/国轩高科/储能/固态电池/换电…), keep `2026-10-15…10-22`. Candidate URLs come from `finance.sina.com.cn` / `k.sina.com.cn`; **never** `toutiao.com`. Fetch the article text before writing the 50-100 char summary.

### Patent news — Sina AIGC patent channel

Search `site`-style queries such as `10月21日消息 国家知识产权局 电池 专利`, then fetch:
`https://finance.sina.com.cn/stock/aigc/zl/YYYY-MM-DD/doc-xxxx.shtml.md` (the `.md` suffix returns clean markdown).
`patents.google.com` is unreachable from scripts; CNIPA epub returns a JS challenge. Rely on Sina patent reports / 启信宝 detail pages, and cite the actual article.

### Standards — openstd

```python
GET https://openstd.samr.gov.cn/bzgk/std/std_list
    ?p.p1=0&p.p90=circulation_date&p.p91=desc&p.p2=电池
# hcno: re.findall(r"showInfo\('([0-9A-F]{32})'\)", html)
# detail: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=...
```

Also check `ces.org.cn` for T/CES group standards and `std.samr.gov.cn` for TC550 power-storage standards.

### Open source — GitHub

```python
GET https://api.github.com/repos/{owner}/{repo}/releases?per_page=15
GET https://api.github.com/search/repositories?q=topic:battery-management+pushed:>YYYY-MM-DD
```

Use `published_at` for the date. If a repo has no tagged release in the window, do not use it; never point to `/releases` when it does not exist.

## WeChat Push Specification

### Parameters
- **AppID**: `wx6faba10fc6b42653`
- **AppSecret**: `edf800d13ce266ad5c8d7e15a75ea6eb`
- **Title format**: `BMS 算法追踪 YYYY-MM-DD`
- **Author**: `算法`
- **Cover image**: Deep blue tech background, two lines of white bold text "BMS 算法追踪" (large) over date "YYYY-MM-DD" (smaller, hierarchy ~1.8:1), rendered via PIL (see pitfall 22). Size reference (approved by user 2026-08-18): CJK font ~160pt / date ~111pt on a 1800x766 canvas → title glyph ≈ 20% of canvas height / 59% width, date ≈ 11% / 36%, block centered at ~49%

### API Flow
1. Get access_token: `GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}`
2. Upload cover image: `POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image`
3. Push draft: `POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}`

### Idempotent Push (MANDATORY — added 2026-10-22)

Never call `draft/add` on every revision — it leaves duplicate drafts in the account.

```python
DRAFT_FILE = os.path.join(BASE, "draft_id.txt")
# first push:  draft/add  -> save {"media_id": ..., "thumb_media_id": ...}
# later edits: draft/update with the SAME media_id (index 0) -> original draft updated in place
```

`draft/update` payload: `{"media_id": ..., "index": 0, "articles": {...}}`. Keep the uploaded cover's `thumb_media_id` in the same JSON so re-runs do not re-upload the image.

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
2. Verify: title contains date, Chinese chars > 5000, H2 count = 6, entry count = 50, URL count > 50, journal badge count = 10, DOI count >= 6, arXiv count = 4, legend mentions "AJP-2.1" and appears before Section 一, dual-char rating badges (A2/B2/C2/C3/D3) counts match the generated report, and zero legacy `T[1-4]` badges remain (`re.findall(r">T[1-4]<", c)` must be empty)
3. Verify alignment: the title div read back still contains `text-align:left` — if the style was stripped, the English titles will justify-stretch again
4. Verify text integrity: strip tags from both local HTML and readback, then compare character by character (WeChat normalizes some attributes, so MD5 equality is NOT a valid check; visible text equality is)
5. Verify no cross-issue duplicates (see Cross-Issue Deduplication) — exact duplicate count must be 0

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
22. **Cover must be rendered via PIL, not AI generation (CRITICAL)**: AI image generators CANNOT reliably produce two text lines at equal font size (CJK always renders bigger than digits at equal point size, or hierarchy gets re-imposed), and they embed watermarks plus background artifacts that land behind the date text. Render deterministically instead: draw the background programmatically (deep-blue vertical gradient `#08142E`→`#164296`, soft radial glow, thin circuit lines with node dots at bottom), then draw text on a 1800x766 canvas: title line `ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 160)`, date line 111pt — an explicit **hierarchy** (user-confirmed final look), NOT equal glyph heights. Target: title glyph ≈ 20% of canvas height / 59% width, date ≈ 11% / 36%, block centered at ~49%. Avoid extremes: 200pt+equal-height filled ~75% width (oversized), 76pt/96pt equal-height was judged too small, 110pt/139pt equal-height replaced by this hierarchical version. Center each line horizontally. Save as JPEG quality 92.
23. **Unicode corruption scan refinement**: Common Chinese characters like 锂(U+9502), 机(U+673A), 蓄(U+84C4), 斩(U+65A9), 钧(U+94A7) are LEGITIMATE in battery-related text and should NOT be flagged as corrupted. Only truly rare characters like 霂(U+9702) indicate corruption. The scan function should only check for characters that would never appear legitimately in battery/BMS content.
24. **中电联 standard.cec.org.cn rating trap**: The site is operated by CEC (中国电力企业联合会), an industry ASSOCIATION commissioned by government — not a government agency. Two file types live there: DL power-industry standards & GB consultation notices = **B2** (commissioned body publishing, first-hand text); T/CEC group standards = **C2**. Only after NEA/国标委 publishes the final text on a government platform does the item qualify for A2.
25. **cj.sina.com.cn is self-media**: Sina 看点 articles under user-ID URLs (e.g. `cj.sina.com.cn/articles/view/2868676035/...`) are user-generated content, NOT 新浪财经 editorial. Do not rate them B. Either replace with a finance.sina.com.cn official report (search for the same event) or downgrade to D3.
26. **Aggregator links are not source links**: Never use 企查查/爱企查 **search-page URLs** (`aiqicha.baidu.com/s?q=...`) or `qcc.com` search links as entry sources — they are unstable and unverifiable. For patents, always use `patents.google.com/patent/{PUBLICATION_NUMBER}/zh` (C2, first-hand text); 企查查 detail-page relays of patent grants rate **C3** (relay, not first-hand).
27. **Justify alignment makes long English titles look broken (CRITICAL — observed 2026-10-22)**: WeChat divs default to `text-align: justify`. Chinese paragraphs hide it; a long English paper title such as `9 · System Identification for Nonlinear Stochastic State-Space Models …` gets its first line stretched, leaving a huge gap after `9 ·`. Fix: put `text-align:left;` on the entry `<section>` **and** every text div (title / abstract / innovation / applicant / purpose / core / implementation / source / trends). After push, read back and confirm the attribute survived.
28. **Repeating last week's standards**: National standards do not publish weekly, so it is tempting to reuse `GB/T 48072` / `GB/T 47136` / `GB 48146`. A 2026-10-22 draft carried three standards already published in 10-09 and 09-14. Run the cross-issue dedup before pushing and rotate standards — no standard number may repeat within 4 issues.
29. **GitHub link verification may time out transiently**: `github.com` occasionally refuses/times out for 2-3 minutes. Do not mark links broken on the first timeout. Verify existence via `api.github.com/repos/{owner}/{repo}/releases` and retry the HTML check later.
30. **企查查/启信宝 detail pages return 403 to scripts**: `qixin.com` / `qcc.com` block `requests` (403) but open normally in a browser. Treat 403 as "valid but not script-verifiable" (same as miit.gov.cn), not as a broken link.
31. **Too many releases from one repo**: Four Predbat entries in one issue (2026-10-22) crowded out fresh projects. Cap at 1 per repo per issue; use GitHub repository search (`topic:battery-management pushed:>DATE`) to find previously unused projects with releases in the window.

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
- [ ] All dates within 7 days, format `📅YYYY-MM-DD` (standards: use true publication/implementation dates and note the exception)
- [ ] All links use `<span>` not `<a>`
- [ ] All styles are inline
- [ ] **All entry sections and text divs carry `text-align:left`** (verify the title div after readback — no justify-stretch gap in long English titles)
- [ ] Footer section present
- [ ] Title format: `BMS 算法追踪 YYYY-MM-DD`
- [ ] Cover image: deep blue, two lines of text
- [ ] Push encoding: `ensure_ascii=False` + `charset=utf-8`
- [ ] **Idempotent push**: re-runs use `draft/update` with the saved `media_id`; no duplicate drafts
- [ ] **Cross-issue dedup**: 0 exact duplicates vs. the previous 3 issues; ≤1 release per GitHub repo; no standard repeated within 4 issues
- [ ] Post-push verification passed (incl. entry count = 50 and visible-text equality)
- [ ] **Unicode corruption scan**: Render all strings, check for rare CJK chars (frequency=1), verify no `\uXXXX` followed by hex digit in source
- [ ] **Link validation**: Run `requests.head()` on all URLs; fix any 404/timeout; verify DOIs via Crossref; verify GitHub repos exist; verify patent numbers via CNIPA

## Maintenance Log

- **2026-10-22** — Added mandatory `text-align:left` (fixes justify-stretch gap in long English titles); added Cross-Issue Deduplication section + rules (0 exact duplicates, ≤1 release per repo, standards rotation within 4 issues); added Idempotent Push (`draft/update`); added Weekly Data Collection Recipes with verified endpoints; added readback checks for entry count / alignment / visible-text equality; pitfalls 27–31.
