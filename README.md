# BMS Weekly Report Generator

A skill for generating weekly BMS (Battery Management System) technology tracking reports and pushing them to WeChat Official Account draft box.

## Features

- 6 sections: Trends, Papers, Vendor News, Open Source, Patents, Standards
- 6+4 paper composition: 6 high-IF journal papers + 4 arXiv preprints
- Source grading system (T1-T4) with color-coded badges
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

## Usage

Invoke when user asks to generate/publish/update the BMS weekly report or says "BMS 算法追踪".

## Latest Updates (2026-08-02)

- Added pitfalls 17-23 based on production experience
- OFweek mobile URL 403 handling
- IEEE DOI format correction (arnumber != DOI suffix)
- Elsevier DOI year mismatch guidance
- Google Patents timeout handling
- MIIT.gov.cn 403 handling
- Cover image text layout guidance
- Unicode corruption scan refinement

## License

MIT
