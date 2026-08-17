# BMS 算法追踪周报 — 完整需求规格与实现指南

> **用途**：将本文档传递给 AI 助手，使其能够一次性正确生成 BMS 周报并推送到微信公众号草稿箱。
>
> **适用场景**：每周一次的 BMS（电池管理系统）领域技术追踪报告，涵盖论文、厂商动态、开源项目、专利、标准及趋势展望。
>
> **版本**：v2.0（2026-08-17）。本版由 `bms-weekly-report-skill` 仓库的需求规格迁移合并而来，信源分级体系已由旧版 T1–T4 四级制升级为 **Admiralty / NATO AJP-2.1 双维评级**（信源可靠性 A–F × 信息可信度 1–6），与 SKILL.md 保持一致。

---

## 一、总体概述

生成一份微信公众号周报，主题为「BMS 算法追踪」，包含以下 6 个部分（按顺序）：

1. **本周趋势展望**（3~5 条，位于全文最前面）
2. **一、学术论文进展**（10 条：6 篇高 IF 期刊论文 + 4 篇 arXiv 预印本）
3. **二、厂商动态**（10 条）
4. **三、开源项目与数据集**（10 条）
5. **四、专利技术**（10 条）
6. **五、行业标准**（10 条）

每条内容必须有真实有效的来源链接，且日期在**发布日往前 7 天以内**。

---

## 二、内容来源与信源评级标准（Admiralty / NATO AJP-2.1）

### 评级规则

每条内容以**双字符评级**标注（如 `B2`）：

- **首字符 = 信源可靠性（A–F）**：评的是链接文本的**直接发布方**，不是其背后的最终权威
- **次字符 = 信息可信度（1–6）**：评的是该条信息本身被证实的程度
- **两维独立评估**：高可靠信源也可能发布未经证实的信息，可靠性不得泄漏进可信度

### 信源可靠性（A–F）与徽章颜色

| 等级 | 颜色色值 | 适用范围 |
|------|----------|----------|
| A | `#6abf69`（绿色） | 政府机构公告与官方平台正式发布文本（认监委、全国标准信息公共服务平台、能源局/工信部）· SCI 顶刊顶会（Nature/Science 系列，IF>30） |
| B | `#4a90d9`（蓝色） | SCI 期刊（IF 5-30）· IEEE/JPS/EST · 权威媒体（新浪财经、东方财富、财联社）· 受政府委托标准组织的征求意见公告（中电联 GB/DL 征求意见函）· 交易所披露/招股书 |
| C | `#e67e22`（橙色） | arXiv 预印本 · 专业开源社区 · 企业官方发布 · 行业资讯平台 · 企业专利一手文本 · 团体标准（T/CEC）· 行业数据平台（企查查/爱企查） |
| D/E | `#9b59b6`（紫色） | 行业博客 / 自媒体（仅供参考，须有免责声明） |
| F | `#95a5a6`（灰色） | 无法判断（兜底档，极少使用） |

### 信息可信度（1–6）

| 分值 | 含义 |
|------|------|
| 1 | 完全可信，已被独立信源证实 |
| 2 | 很可能属实，可靠单源一手文本（官方公告、DOI 论文正文、专利文本、交易所披露） |
| 3 | 可能属实，单源转述待核（arXiv 论断、行业平台转述、聚合平台统计） |
| 4 存疑 · 5 不可能 · 6 真实性无法判断 |

### 各部分评级对照（默认值，按证据实况逐条调整）

| 部分 | A | B | C | D/E |
|------|---|---|---|-----|
| 论文 | Nature/Science 级 = **A2** | 其他高 IF SCI = **B2** | arXiv 预印本 = **C3**（未过同行评审 → 可信度 3） | — |
| 厂商动态 | 政府平台正式发布 = **A2** | 权威媒体报道官方事件 = **B2** | 企业官方 = **C2**；行业资讯转述官方公告 = **C2**（双源）或 **C3**（单源转述）；企查查聚合统计 = **C3** | 自媒体 = **D3** |
| 开源项目 | — | — | GitHub 仓库一手 = **C2** | — |
| 专利 | — | — | Google Patents 一手文本 = **C2**；企查查/爱企查转述授权 = **C3** | — |
| 标准 | 官方平台正式发布文本 = **A2** | 中电联 GB/DL 征求意见函 = **B2**（受委托行业协会，非政府本身） | 中电联 T/CEC 团体标准 = **C2** | — |

**关键判定原则**：
1. 评**直接发布方**：DL 标准征求意见函由中电联（受政府委托的行业协会）发布 → B 而非 A；只有能源局/国标委在政府平台正式发布终稿后才算 A
2. arXiv 预印本一律 C3，绝不评 B2（未过同行评审）
3. 可信度独立于信源档位：权威信源 + 未证实内容仍为可信度 3
4. 同一类型来源的评级必须一致

### 各部分来源要求

| 部分 | 来源优先级 | 注意事项 |
|------|-----------|----------|
| 学术论文 | 6 篇高 IF 期刊（优先 Applied Energy、J. Power Sources 等 BMS 高相关）+ 4 篇 arXiv | 顶刊标 A2，其他 SCI 标 B2，arXiv 标 C3；DOI 须经 Crossref 核验 |
| 厂商动态 | 新浪财经、东方财富、财联社、人民网、OFweek 桌面版 | **禁止 toutiao.com**；**禁止 cj.sina.com.cn 新浪看点自媒体文章**（用户 ID URL），须换 finance.sina.com.cn 正式报道或降为 D3 |
| 开源项目 | GitHub Releases 页面 | 需为最近 7 天内的 release |
| 专利 | Google Patents | 优先中国专利（CN 开头），需为最近 7 天内公开；**禁止企查查/爱企查搜索页 URL 作来源** |
| 标准 | 国家标准全文公开系统、认监委、工信部、能源局官网、中电联标准化平台 | 官方平台正式文本 A2，中电联征求意见 B2，团体标准 C2 |

### 信源分级说明模块（插在趋势展望与"一、"之间）

```html
<section style="margin:24px 0 12px 0;padding:14px 16px;background:#f5f9ff;border-left:3px solid #4a90d9;border-radius:4px;"><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:4px;">📌 信源分级说明 · Admiralty / NATO AJP-2.1</div><div style="font-size:12px;color:#555;line-height:1.7;margin-bottom:10px;">本报告采用 OSINT 开源情报领域公认的 Admiralty 评级标准（北约 AJP-2.1）：每条内容以双字符评级标注，首字符评<strong>信源可靠性</strong>，次字符评<strong>信息可信度</strong>，如 B2 = 通常可靠信源 × 很可能属实。两维独立评估，互不绑定。</div><div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin-bottom:4px;">信源可靠性 Source Reliability（A–F）</div><div style="font-size:13px;color:#333;line-height:2.1;"><span style="background:#6abf69;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">A</span> 完全可靠 · 政府机构公告与官方平台正式发布文本 · SCI 顶刊顶会<br/><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B</span> 通常可靠 · SCI 期刊 · 权威学术出版 · 权威媒体 · 受政府委托标准组织的征求意见公告<br/><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C</span> 相当可靠 · arXiv 预印本 · 专业开源社区 · 企业官方发布 · 行业资讯 · 团体标准<br/><span style="background:#9b59b6;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">D/E</span> 通常不可靠 / 不可靠 · 行业博客 / 自媒体<br/><span style="background:#95a5a6;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">F</span> 无法判断</div><div style="font-size:12px;color:#1f5fa8;font-weight:bold;margin:8px 0 4px;">信息可信度 Information Credibility（1–6）</div><div style="font-size:13px;color:#333;line-height:2.1;"><b>1</b> 完全可信，已被独立信源证实&nbsp;&nbsp;<b>2</b> 很可能属实，可靠单源一手文本&nbsp;&nbsp;<b>3</b> 可能属实，单源转述待核&nbsp;&nbsp;<b>4</b> 存疑&nbsp;&nbsp;<b>5</b> 不可能&nbsp;&nbsp;<b>6</b> 真实性无法判断</div><div style="font-size:12px;color:#888;line-height:1.7;margin-top:8px;">注：信源可靠性仅刻画信源先验，不等价于信息已被证实；D/E 及 4/5 档条目仅供参考，不构成投资建议。</div></section>
```

---

## 三、HTML 格式规范

### 3.1 全文结构

```
[本周趋势展望 H2]
  [趋势条目 1~5]
[信源分级说明模块]
[一、学术论文进展 H2]
  [论文条目 1~10]
[二、厂商动态 H2]
  [厂商条目 1~10]
[三、开源项目与数据集 H2]
  [开源条目 1~10]
[四、专利技术 H2]
  [专利条目 1~10]
[五、行业标准 H2]
  [标准条目 1~10]
[页脚声明]
```

### 3.2 H2 标题样式

```html
<h2 style="font-size:19px;color:#111;margin:24px 0 12px 0;padding-bottom:8px;border-bottom:2px solid #4a90d9;font-weight:bold;text-align:left;">标题文本</h2>
```

### 3.3 趋势展望条目模板

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;">
  <div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · 趋势标题</div>
  <div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">一两句话描述，不超过两行。</div>
</section>
```

**要求**：
- 3~5 条，每条一两句话，简洁总结
- 不要加来源链接
- 不要加引导语（如"基于本期内容..."）
- 内容根据全文实际内容提炼

### 3.4 论文条目模板（arXiv / C3）

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C3</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-12</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">arXiv</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">主题标签</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · 论文标题</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50~100字摘要内容</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">💡 <b>创新:</b>50~100字创新点描述</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://arxiv.org/abs/XXXX.XXXXX</span></div></section>
```

### 3.5 论文条目模板（SCI 期刊 / A2 或 B2）

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-17</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">Applied Energy</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">主题标签</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">9 · 论文标题</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50~100字摘要内容</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">💡 <b>创新:</b>50~100字创新点描述</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://doi.org/10.1016/...</span></div></section>
```

顶刊（Nature/Science 系）将评级徽章换为 `A2`（`background:#6abf69`）。

### 3.6 厂商动态条目模板

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#4a90d9;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">B2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-17</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">标签1</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">标签2</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · 标题</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50~100字摘要内容</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://...</span></div></section>
```

**注意**：厂商动态部分左边框颜色为 `#27ae60`（绿色），与论文的 `#4a90d9`（蓝色）区分。评级徽章按来源实况：权威媒体 B2（蓝）、企业官方/行业资讯 C2（橙）、企查查统计 C3（橙）、自媒体 D3（紫）。

### 3.7 开源项目条目模板

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-10</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">标签1</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">标签2</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · 项目名称</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50~100字摘要内容</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://github.com/...</span></div></section>
```

### 3.8 专利条目模板

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#e67e22;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">C2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-16</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">申请人</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">技术标签</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · CN123456789A 专利标题</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>申请人:</b>公司名称</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📌 <b>摘要:</b>50~100字摘要内容</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">💡 <b>创新:</b>50~100字创新点描述</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://patents.google.com/patent/CN123456789A/zh</span></div></section>
```

**注意**：专利部分左边框颜色为 `#e67e22`（橙色），包含申请人、摘要、创新三个字段。评级：Google Patents 一手文本 C2，聚合平台转述 C3。

### 3.9 标准条目模板

```html
<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:#6abf69;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">A2</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">📅2026-08-11</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">强制性国标</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">技术标签</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">1 · GB 38031-2025《标准名称》</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">🎯 <b>目的:</b>50~100字目的描述</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📋 <b>核心内容:</b>50~100字核心内容描述</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">📅 <b>实施:</b>实施日期，发布机构</div><div style="color:#888;font-size:12px;">来源: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://...</span></div></section>
```

**注意**：评级按发布方实况：官方平台正式文本 A2（绿），中电联 GB/DL 征求意见 B2（蓝），T/CEC 团体标准 C2（橙）。

### 3.10 页脚模板

```html
<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;"><div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">事实核查声明：本期内容来源已按 Admiralty / NATO AJP-2.1 标准双维评级标注，D/E 级信源条目仅供参考，不构成投资建议。</div><div style="font-size:14px;color:#4a90d9;font-weight:bold;">🔋 BMS 算法追踪</div><div style="font-size:11px;color:#aaa;margin-top:4px;">关注电池管理系统前沿 | 每周更新</div></section>
```

### 3.11 各部分左边框颜色汇总

| 部分 | 左边框颜色 | 用途 |
|------|-----------|------|
| 趋势展望 | `#4a90d9` | 蓝色 |
| 学术论文 | `#4a90d9` | 蓝色 |
| 厂商动态 | `#27ae60` | 绿色 |
| 开源项目 | `#4a90d9` | 蓝色 |
| 专利技术 | `#e67e22` | 橙色 |
| 行业标准 | `#e67e22` | 橙色 |

---

## 四、内容字数要求

| 字段 | 字数要求（中文字符） |
|------|-------------------|
| 趋势展望每条 | 一两句话（30~60字） |
| 论文摘要 | 50~100字 |
| 论文创新 | 50~100字 |
| 厂商动态摘要 | 50~100字 |
| 开源项目摘要 | 50~100字 |
| 专利摘要 | 50~100字 |
| 专利创新 | 50~100字 |
| 标准目的 | 50~100字 |
| 标准核心内容 | 50~100字 |

---

## 五、日期与链接要求

1. **日期范围**：所有条目的日期必须在发布日往前 **7 天以内**
2. **日期格式**：`📅YYYY-MM-DD`（如 `📅2026-08-17`），不要用模糊格式
3. **链接有效性**：所有来源链接必须可访问
4. **链接格式**：以 `<span>` 纯文本展示（微信会过滤 `<a>` 标签）
5. **DOI 优先**：论文有 DOI 的优先使用 `https://doi.org/...`
6. **禁止来源**：不得使用 `toutiao.com`（今日头条）、`cj.sina.com.cn`（新浪看点自媒体）、企查查/爱企查搜索页 URL

---

## 六、格式一致性检查清单

生成完成后，必须逐项检查：

- [ ] 同一部分内 10 条的 HTML 结构完全一致（标签数量、字段数量、样式属性）
- [ ] 论文部分：顶刊=A2（绿），其他 SCI=B2（蓝），arXiv=C3（橙），评级一致
- [ ] 评级双字符格式正确（A-F × 1-6），无旧版 T1-T4 残留（`re.findall(r">T[1-4]<", html)` 为空）
- [ ] 每条论文标签行包含期刊来源名称（arXiv / Applied Energy / J. Power Sources 等）
- [ ] 所有日期在 7 天以内
- [ ] 所有链接不以 toutiao.com / cj.sina.com.cn 开头
- [ ] 趋势展望在最前面，3~5 条，每条一两句话，无引导语
- [ ] 信源分级说明模块位于趋势展望与"一、"之间，含 AJP-2.1 字样
- [ ] 每条摘要/创新/目的等字段达到 50~100 字
- [ ] 各部分左边框颜色正确（论文蓝色、厂商绿色、专利橙色、标准橙色）

---

## 七、微信公众号推送

### 7.1 推送参数

| 参数 | 值 |
|------|-----|
| AppID | `wx6faba10fc6b42653` |
| AppSecret | `edf800d13ce266ad5c8d7e15a75ea6eb` |
| 标题格式 | `BMS 算法追踪 YYYY-MM-DD`（如 `BMS 算法追踪 2026-08-17`） |
| 作者 | `算法` |
| 封面图 | 两行文字：第一行「BMS 算法追踪」，第二行日期「YYYY-MM-DD」 |

### 7.2 推送流程

```
1. 获取 access_token
   GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}

2. 上传封面图为永久素材
   POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image
   Body: multipart/form-data, field name: "media"

3. 推送草稿
   POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}
   Body: JSON, articles[0].thumb_media_id = 封面图 media_id
```

### 7.3 编码要求（关键坑点）

**必须使用以下编码方式，否则中文会乱码：**

```python
import json, requests

# 序列化时 ensure_ascii=False，然后 encode('utf-8')
payload = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')

# 请求头必须声明 charset=utf-8
headers = {'Content-Type': 'application/json; charset=utf-8'}

# 发送时用 data= 而非 json=
r = requests.post(url, data=payload, headers=headers)

# 读取响应时用 content.decode('utf-8')
result = json.loads(r.content.decode('utf-8'))
```

**错误示例（会导致中文乱码）：**
```python
# 错误1：使用 json= 参数
r = requests.post(url, json=draft_data)  # 中文可能被转为 \uXXXX

# 错误2：使用 r.json() 直接读取
result = r.json()  # 可能因编码问题乱码

# 错误3：不设置 Content-Type charset
headers = {'Content-Type': 'application/json'}  # 缺少 charset=utf-8
```

### 7.4 封面图生成

使用 AI 图像生成工具，参数：
- 尺寸：`900x383`（微信公众号封面推荐比例 2.35:1）或 `square_hd`
- 背景：深蓝色科技风格
- 文字：第一行「BMS 算法追踪」，第二行「YYYY-MM-DD」日期
- 风格：简洁、专业、科技感
- 布局：文字居中聚拢，占画面宽约 60%、高约 50%，勿拉伸至全宽

### 7.5 推送后验证

推送成功后，必须回读草稿验证：
1. 标题正确（含日期）
2. 中文字符数 > 5000
3. H2 标题数量 = 6
4. 来源链接数量 > 50
5. 期刊标签数量 = 10，DOI ≥ 6，arXiv = 4
6. 信源分级说明含 AJP-2.1 且位于"一、"之前
7. 评级徽章计数与生成端一致，且无 T1-T4 残留

### 7.6 完整推送脚本

```python
# -*- coding: utf-8 -*-
import requests, json, re

APPID = 'wx6faba10fc6b42653'
APPSECRET = 'edf800d13ce266ad5c8d7e15a75ea6eb'

# 1. 获取 token
token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
token = requests.get(token_url).json()['access_token']

# 2. 上传封面图
cover_path = 'cover.jpg'
upload_url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image'
with open(cover_path, 'rb') as f:
    files = {'media': ('cover.jpg', f, 'image/jpeg')}
    thumb_media_id = requests.post(upload_url, files=files).json()['media_id']

# 3. 读取 HTML
with open('wechat_content_final.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 4. 推送草稿
draft_url = f'https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}'
draft_data = {
    'articles': [{
        'title': 'BMS 算法追踪 2026-08-17',
        'author': '算法',
        'digest': '',
        'content': content,
        'content_source_url': '',
        'thumb_media_id': thumb_media_id,
        'need_open_comment': 0,
        'only_fans_can_comment': 0,
        'show_cover_pic': 1,
    }]
}
payload = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')
headers = {'Content-Type': 'application/json; charset=utf-8'}
result = json.loads(requests.post(draft_url, data=payload, headers=headers).content.decode('utf-8'))

# 5. 验证
if 'media_id' in result:
    media_id = result['media_id']
    r2 = requests.post(
        f'https://api.weixin.qq.com/cgi-bin/draft/get?access_token={token}',
        json={'media_id': media_id}
    )
    stored = json.loads(r2.content.decode('utf-8'))['news_item'][0]
    print(f"Title: {stored['title']}")
    print(f"Chinese chars: {len(re.findall(r'[\u4e00-\u9fff]', stored['content']))}")
    print(f"H2 count: {len(re.findall(r'<h2', stored['content']))}")
```

---

## 八、踩过的坑与解决方案

### 8.1 编码问题（最严重）

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 推送后中文显示为 `\uXXXX` | `json.dumps` 默认 `ensure_ascii=True` | 使用 `ensure_ascii=False` |
| 响应中文乱码 | `r.json()` 使用了错误编码 | 使用 `r.content.decode('utf-8')` |
| Content-Type 不匹配 | 默认不声明 charset | 显式设置 `application/json; charset=utf-8` |
| Python 脚本中含中文引号 | 中文 `""` 与 Python 字符串引号冲突 | 使用 `\u201c` `\u201d` Unicode 转义 |

### 8.2 微信 HTML 限制

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `<a>` 标签被过滤 | 微信编辑器不支持 `<a>` | 用 `<span>` 纯文本展示 URL |
| 外部 CSS 不生效 | 微信不支持 `<style>` 标签 | 所有样式用 inline style |
| `<script>` 被过滤 | 安全限制 | 不使用 JavaScript |
| section 嵌套深度限制 | 微信渲染限制 | 控制嵌套在 3 层以内 |

### 8.3 格式一致性问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 同一部分内条目格式不统一 | 分批生成导致格式漂移 | 使用统一的模板函数生成所有条目 |
| 论文 #9、#10 与 #1-8 格式不同 | 后期替换时未对齐格式 | 替换时严格使用相同模板 |
| 评级不统一 | 标准不明确 | 按 Admiralty 双维评级：评直接发布方，可靠性不泄漏进可信度 |
| 标签行缺少期刊名 | 原始标签只有主题词 | 第一个标签位改为期刊来源名 |

### 8.4 内容来源问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 日期超出 7 天范围 | 初次搜索时未限制日期 | 生成后统一检查日期范围 |
| 使用了 toutiao.com 链接 | 搜索结果包含今日头条 | 手动替换为可靠媒体来源 |
| 使用了 cj.sina.com.cn 链接 | 新浪看点自媒体混入搜索结果 | 换 finance.sina.com.cn 正式报道或降为 D3 |
| 使用了企查查/爱企查搜索页链接 | 聚合搜索页不稳定不可核验 | 专利一律用 patents.google.com 专利号链接 |
| 链接不可访问 | 来源页面已删除或需登录 | 逐一验证链接可访问性 |
| 专利 ID 重复 | 搜索时返回相同专利 | 去重检查 |

### 8.5 信源评级问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 中电联 DL/GB 征求意见评为 A2 | 误将受委托协会当政府机构 | 征求意见阶段= B2；政府平台正式发布终稿才 = A2 |
| arXiv 论文评为 B2 | 可靠性泄漏进可信度 | 预印本一律 C3（未过同行评审） |
| 企查查转述专利评为 C2 | 转述非一手 | 聚合平台转述 = C3；Google Patents 一手文本 = C2 |

### 8.6 结构问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 趋势展望在最后 | 原始设计在第六部分 | 移动到全文最前面作为"本周趋势展望" |
| 有无意义的引导语 | 自动生成的概述 | 删除引导语，直接展示条目 |
| 封面图格式不符 | 未参考历史文章 | 使用 AI 生成深蓝色背景+两行文字 |

---

## 九、Python 模板函数

以下函数用于统一生成所有条目，确保格式一致（评级参数为 Admiralty 双字符）：

```python
# -*- coding: utf-8 -*-

RATING_COLOR = {"A": "#6abf69", "B": "#4a90d9", "C": "#e67e22",
                "D": "#9b59b6", "E": "#9b59b6", "F": "#95a5a6"}

def rating_color(rating):
    return RATING_COLOR[rating[0]]

def h2(title):
    return f'<h2 style="font-size:19px;color:#111;margin:24px 0 12px 0;padding-bottom:8px;border-bottom:2px solid #4a90d9;font-weight:bold;text-align:left;">{title}</h2>'

def trend_section(num, title, description):
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">{description}</div></section>'

def paper_section(num, title, abstract, innovation, source_url, journal, topic_tag, date, rating='B2'):
    # rating: A2 top-tier / B2 SCI / C3 arXiv
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:{rating_color(rating)};color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">{rating}</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001f4c5{date}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{journal}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{topic_tag}</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cc <b>\u6458\u8981:</b>{abstract}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4a1 <b>\u521b\u65b0:</b>{innovation}</div><div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">{source_url}</span></div></section>'

def vendor_section(num, title, abstract, source_url, tags, date, rating='B2'):
    tag1, tag2 = tags
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:{rating_color(rating)};color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">{rating}</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001f4c5{date}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag1}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag2}</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cc <b>\u6458\u8981:</b>{abstract}</div><div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">{source_url}</span></div></section>'

def opensource_section(num, title, abstract, source_url, tags, date, rating='C2'):
    tag1, tag2 = tags
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:{rating_color(rating)};color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">{rating}</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001f4c5{date}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag1}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag2}</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cc <b>\u6458\u8981:</b>{abstract}</div><div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">{source_url}</span></div></section>'

def patent_section(num, cn_id, title, applicant, abstract, innovation, tags, date, rating='C2'):
    tag1, tag2 = tags
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:{rating_color(rating)};color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">{rating}</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001f4c5{date}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag1}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag2}</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {cn_id} {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cc <b>\u7533\u8bf7\u4eba:</b>{applicant}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cc <b>\u6458\u8981:</b>{abstract}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4a1 <b>\u521b\u65b0:</b>{innovation}</div><div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">https://patents.google.com/patent/{cn_id}/zh</span></div></section>'

def standard_section(num, std_id, title, purpose, core_content, implementation, tags, date, source_url, rating='A2'):
    tag1, tag2 = tags
    return f'<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;"><div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;"><span style="background:{rating_color(rating)};color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">{rating}</span><span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001f4c5{date}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag1}</span><span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">{tag2}</span></div><div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">{num} \u00b7 {std_id} {title}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f3af <b>\u76ee\u7684:</b>{purpose}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4cb <b>\u6838\u5fc3\u5185\u5bb9:</b>{core_content}</div><div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001f4c5 <b>\u5b9e\u65bd:</b>{implementation}</div><div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;;word-break:break-all">{source_url}</span></div></section>'

def footer():
    return '<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;"><div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">\u4e8b\u5b9e\u6838\u67e5\u58f0\u660e\uff1a\u672c\u671f\u5185\u5bb9\u6765\u6e90\u5df2\u6309 Admiralty / NATO AJP-2.1 \u6807\u51c6\u53cc\u7ef4\u8bc4\u7ea7\u6807\u6ce8\uff0cD/E \u7ea7\u4fe1\u6e90\u6761\u76ee\u4ec5\u4f9b\u53c2\u8003\uff0c\u4e0d\u6784\u6210\u6295\u8d44\u5efa\u8bae\u3002</div><div style="font-size:14px;color:#4a90d9;font-weight:bold;">\U0001f50b BMS \u7b97\u6cd5\u8ffd\u8e2a</div><div style="font-size:11px;color:#aaa;margin-top:4px;">\u5173\u6ce8\u7535\u6c60\u7ba1\u7406\u7cfb\u7edf\u524d\u6cbf | \u6bcf\u5468\u66f4\u65b0</div></section>'
```

---

## 十、优化后的完整执行路径

### Step 1: 信息收集（并行搜索）

使用搜索工具并行收集以下 5 类信息，每类 10 条，日期限定在 7 天内：

1. **论文**：6 篇高 IF 期刊（优先 BMS 高相关：Applied Energy, J. Power Sources, Journal of Energy Storage 等）+ 4 篇 arXiv
2. **厂商动态**：搜索 BMS/电池相关厂商新闻，来源限定为新浪财经/东方财富/财联社/人民网/OFweek 桌面版
3. **开源项目**：搜索 GitHub 上 BMS/电池相关项目的最近 release
4. **专利**：搜索 Google Patents 最近公开的 BMS 相关中国专利
5. **标准**：搜索最近发布或实施的电池/BMS 相关标准

### Step 2: 生成 HTML

使用第九节的 Python 模板函数批量生成所有条目，确保格式完全一致。

### Step 3: 格式一致性检查

- 每部分 10 条，结构完全一致
- 评级双字符统一（顶刊=A2, SCI=B2, arXiv=C3），无 T1-T4 残留
- 日期在 7 天内
- 无 toutiao.com / cj.sina.com.cn 链接
- 字数达标（各字段 50~100 字）

### Step 4: 生成封面图

使用 AI 图像生成工具，深蓝色背景，两行文字居中聚拢。

### Step 5: 推送微信公众号

按照第七节的完整脚本推送，注意编码要求（`ensure_ascii=False` + `charset=utf-8`）。

### Step 6: 验证

回读草稿，确认标题、中文字符数、H2 数量、链接数量、期刊标签数量、AJP-2.1 说明模块与评级徽章计数。

---

## 十一、附录：完整配色方案

| 元素 | 色值 | 用途 |
|------|------|------|
| `#6abf69` | 绿色 | A 级信源徽章背景 |
| `#4a90d9` | 蓝色 | B 级信源徽章、论文/开源左边框、链接文字、H2 下划线 |
| `#e67e22` | 橙色 | C 级信源徽章、专利/标准左边框 |
| `#9b59b6` | 紫色 | D/E 级信源徽章 |
| `#95a5a6` | 灰色 | F 级信源徽章（无法判断） |
| `#27ae60` | 深绿色 | 厂商动态左边框 |
| `#d4edda` | 浅绿色 | 主题标签背景 |
| `#155724` | 深绿色 | 主题标签文字 |
| `#e8f5e9` | 浅绿色 | 日期标签背景 |
| `#2e7d32` | 深绿色 | 日期标签文字 |
| `#111` | 近黑色 | 标题文字 |
| `#333` | 深灰色 | 正文文字 |
| `#888` | 灰色 | 来源标签文字 |
| `#f5f5f5` | 浅灰色 | 页脚背景 |
| `#aaa` | 浅灰色 | 页脚副标题 |
