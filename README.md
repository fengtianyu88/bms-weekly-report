# BMS Weekly Report Generator

A skill for generating weekly BMS (Battery Management System) technology tracking reports and pushing them to WeChat Official Account draft box.

## Features

- 6 sections: Trends, Papers, Vendor News, Open Source, Patents, Standards
- 6+4 paper composition: 6 high-IF journal papers + 4 arXiv preprints
- Source rating per **Admiralty / NATO AJP-2.1**: dual-character rating (Source Reliability A–F × Information Credibility 1–6, e.g. `B2`) with color-coded badges
- WeChat Official Account draft box integration
- Post-push verification with read-back checking
- Cover image generation with AI

## Report Structure

1. **本周趋势展望** (3-5 trend items)
2. **一、学术论文进展** (10 papers: 6 journal + 4 arXiv)
3. **二、厂商动态** (10 vendor news items)
4. **三、开源项目与数据集** (10 GitHub projects)
5. **四、专利技术** (10 patents)
6. **五、行业标准** (10 standards)

A source-grading legend block (Admiralty AJP-2.1) is inserted between the trends section and Section 一.

## Usage

Invoke when user asks to generate/publish/update the BMS weekly report or says "BMS 算法追踪".

## Documentation

- `SKILL.md` — skill definition (rating rules, HTML templates, pitfalls, checklist)
- `docs/SPEC.zh-CN.md` — full Chinese requirements spec & implementation guide (v2.0, migrated from the former `bms-weekly-report-skill` repo)

## Latest Updates

**2026-08-17**
- Adopted Admiralty/NATO AJP-2.1 dual-character source rating (A–F × 1–6), replacing legacy T1-T4 tiers
- Full rating audit: 吉利 entry re-sourced to 财联社/新浪财经 editorial (B2), CATL patent link switched to Google Patents first-hand, 海辰 patent relay downgraded to C3
- Merged the former private `bms-weekly-report-skill` repo into this repo (spec doc migrated to `docs/SPEC.zh-CN.md` with Admiralty grading)
- New pitfalls: CEC consultation-notice grading (B2 not A2), cj.sina.com.cn is self-media, aggregator search-page links forbidden

**2026-08-02**
- Added pitfalls 17-23 based on production experience (OFweek 403, IEEE DOI format, Elsevier DOI year mismatch, Google Patents timeout, MIIT 403, cover layout, Unicode scan refinement)

## License

MIT
