# -*- coding: utf-8 -*-
"""
BMS Weekly Report Generator - 2026-07-18
Generates HTML content and pushes to WeChat Official Account draft box.
"""
import json
import requests
import sys
import os

# ============================================================
# CONFIG
# ============================================================
APPID = "wx6faba10fc6b42653"
APPSECRET = "edf800d13ce266ad5c8d7e15a75ea6eb"
TITLE = "BMS \u7b97\u6cd5\u8ffd\u8e2a 2026-07-18"
AUTHOR = "\u7b97\u6cd5"
COVER_IMAGE_PATH = r"c:\Users\tiany\.trae-cn\work\6a5b7a465b16c418624765c1\bms_cover_20260718.jpg"
DATE_STR = "2026-07-18"

# ============================================================
# TIER COLORS
# ============================================================
TIER_COLORS = {
    "T1": "#6abf69",
    "T2": "#4a90d9",
    "T3": "#e67e22",
    "T4": "#9b59b6",
}

# ============================================================
# TEMPLATE FUNCTIONS
# ============================================================

def h2(title, color="#4a90d9"):
    return '<h2 style="font-size:19px;color:#111;margin:24px 0 12px 0;padding-bottom:8px;border-bottom:2px solid %s;font-weight:bold;text-align:left;">%s</h2>' % (color, title)


def trend_item(text):
    return '<div style="font-size:14px;color:#333;line-height:1.8;margin-bottom:10px;padding-left:16px;border-left:3px solid #4a90d9;">%s</div>' % text


def _tag_badge(text):
    return '<span style="background:#d4edda;color:#155724;font-size:11px;padding:1px 6px;border-radius:3px;">%s</span>' % text


def _date_badge(date_str):
    return '<span style="background:#e8f5e9;color:#2e7d32;font-size:11px;padding:1px 6px;border-radius:3px;">\U0001F4C5%s</span>' % date_str


def _tier_badge(tier):
    color = TIER_COLORS.get(tier, "#4a90d9")
    return '<span style="background:%s;color:#fff;font-size:11px;padding:1px 6px;border-radius:3px;">%s</span>' % (color, tier)


def _tag_row(tier, date_str, tags):
    """Build the tag row: tier badge + date badge + tag badges"""
    parts = [_tier_badge(tier), _date_badge(date_str)]
    for t in tags:
        parts.append(_tag_badge(t))
    return '<div style="display:flex;align-items:center;flex-wrap:nowrap;gap:4px;margin-bottom:6px;overflow-x:auto;white-space:nowrap;">%s</div>' % "".join(parts)


def _source_row(url):
    return '<div style="color:#888;font-size:12px;">\u6765\u6e90: <span style="color:#4a90d9;text-decoration:none;word-break:break-all">%s</span></div>' % url


def paper_entry(num, tier, date_str, journal, topic_tags, title, abstract, innovation, url):
    """Generate a paper entry. journal is the first tag (source name)."""
    tags = [journal] + topic_tags
    html = '<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;">'
    html += _tag_row(tier, date_str, tags)
    html += '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">%d \u00b7 %s</div>' % (num, title)
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4CC <b>\u6458\u8981:</b>%s</div>' % abstract
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4A1 <b>\u521b\u65b0:</b>%s</div>' % innovation
    html += _source_row(url)
    html += '</section>'
    return html


def vendor_entry(num, tier, date_str, tags, title, abstract, url):
    html = '<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #27ae60;border-radius:4px;word-break:break-all;">'
    html += _tag_row(tier, date_str, tags)
    html += '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">%d \u00b7 %s</div>' % (num, title)
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4CC <b>\u6458\u8981:</b>%s</div>' % abstract
    html += _source_row(url)
    html += '</section>'
    return html


def opensource_entry(num, tier, date_str, tags, title, abstract, url):
    html = '<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #4a90d9;border-radius:4px;word-break:break-all;">'
    html += _tag_row(tier, date_str, tags)
    html += '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">%d \u00b7 %s</div>' % (num, title)
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4CC <b>\u6458\u8981:</b>%s</div>' % abstract
    html += _source_row(url)
    html += '</section>'
    return html


def patent_entry(num, tier, date_str, tags, title, applicant, abstract, innovation, url):
    html = '<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;">'
    html += _tag_row(tier, date_str, tags)
    html += '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">%d \u00b7 %s</div>' % (num, title)
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F465 <b>\u7533\u8bf7\u4eba:</b>%s</div>' % applicant
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4CC <b>\u6458\u8981:</b>%s</div>' % abstract
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4A1 <b>\u521b\u65b0:</b>%s</div>' % innovation
    html += _source_row(url)
    html += '</section>'
    return html


def standard_entry(num, tier, date_str, tags, title, purpose, core_content, implementation, url):
    html = '<section style="margin-bottom:12px;padding:12px 14px;background:#fff;border-left:3px solid #e67e22;border-radius:4px;word-break:break-all;">'
    html += _tag_row(tier, date_str, tags)
    html += '<div style="font-size:14px;color:#111;font-weight:bold;margin-bottom:6px;line-height:1.5;">%d \u00b7 %s</div>' % (num, title)
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F3AF <b>\u76ee\u7684:</b>%s</div>' % purpose
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F4CC <b>\u6838\u5fc3\u5185\u5bb9:</b>%s</div>' % core_content
    html += '<div style="font-size:13px;color:#333;margin-bottom:6px;line-height:1.7;">\U0001F6E0 <b>\u5b9e\u65bd:</b>%s</div>' % implementation
    html += _source_row(url)
    html += '</section>'
    return html


def footer():
    return '''<section style="background:#f5f5f5;border-radius:8px;padding:16px;margin-top:24px;text-align:center;">
<div style="font-size:12px;color:#888;line-height:1.8;margin-bottom:8px;">\u4e8b\u5b9e\u6838\u67e5\u58f0\u660e\uff1a\u672c\u671f\u5185\u5bb9\u6765\u6e90\u5df2\u6807\u6ce8\uff0cT4\u7ea7\u4fe1\u6e90\u4ec5\u4f9b\u53c2\u8003\uff0c\u4e0d\u6784\u6210\u6295\u8d44\u5efa\u8bae\u3002</div>
<div style="font-size:14px;color:#4a90d9;font-weight:bold;">\U0001F50B BMS \u7b97\u6cd5\u8ffd\u8e2a</div>
<div style="font-size:11px;color:#aaa;margin-top:4px;">\u5173\u6ce8\u7535\u6c60\u7ba1\u7406\u7cfb\u7edf\u524d\u6cbf | \u6bcf\u5468\u66f4\u65b0</div>
</section>'''


# ============================================================
# DATA
# ============================================================

# --- Trends (5 items) ---
TRENDS = [
    "\u4e0d\u786e\u5b9a\u6027\u91cf\u5316\u6210\u4e3a\u7535\u6c60\u9000\u5316\u9884\u6d4b\u7684\u6838\u5fc3\u9700\u6c42\uff0c\u672c\u5468\u591a\u7bc7\u8bba\u6587\u805a\u7126\u6982\u7387\u6027\u7f6e\u4fe1\u533a\u95f4\u8f93\u51fa\uff0c\u63a8\u52a8SOH\u4f30\u8ba1\u4ece\u786e\u5b9a\u6027\u70b9\u9884\u6d4b\u5411\u53ef\u4fe1\u533a\u95f4\u9884\u6d4b\u8f6c\u53d8\uff0c\u4e3aBMS\u5b89\u5168\u51b3\u7b56\u63d0\u4f9b\u91cf\u5316\u4f9d\u636e\u3002",
    "\u591a\u6a21\u6001\u878d\u5408\u4e0e\u8fc1\u79fb\u5b66\u4e60\u7a81\u7834\u8de8\u57dfSOH\u4f30\u8ba1\u74f6\u9888\uff0cIC/IS/\u9012\u5f52\u56fe\u591a\u7279\u5f81\u878d\u5408\u52a0\u4e0aRMMD\u76f8\u5bf9\u9000\u5316\u8fdb\u7a0b\u5bf9\u9f50\uff0c\u6709\u6548\u89e3\u51b3\u8de8\u7535\u6c60\u3001\u8de8\u5de5\u51b5\u3001\u8de8\u6750\u6599\u4f53\u7cfb\u7684\u6cdb\u5316\u96be\u9898\uff0c\u5c11\u91cf\u6807\u7b7e\u5373\u53ef\u5b8c\u6210\u6709\u6548\u9002\u914d\u3002",
    "\u68af\u6b21\u5229\u7528\u4e0e\u7cfb\u7edf\u7ea7\u4f18\u5316\u8986\u76d6\u7535\u6c60\u5168\u751f\u547d\u5468\u671f\uff0c\u4ece\u9000\u5f79\u7535\u6c60\u7ec4\u88c5\u9c81\u68d2\u4f18\u5316\u5230BESS\u7f51\u7edc\u7ecf\u6d4e\u8c03\u5ea6\uff0c\u7814\u7a76\u91cd\u5fc3\u4ece\u5355\u7535\u6c60\u6269\u5c55\u5230\u7cfb\u7edf\u7ea7\u8d44\u6e90\u5206\u914d\u3001\u6210\u672c\u4f18\u5316\u4e0eSoC\u7ea6\u675f\u534f\u540c\u63a7\u5236\u3002",
    "\u70ed\u7ba1\u7406\u5411\u52a8\u6001\u4e3b\u52a8\u63a7\u5236\u4e0e\u5236\u9020\u5de5\u827a\u5efa\u6a21\u6f14\u8fdb\uff0cITSC\u96c6\u6210\u51b7\u5374\u914d\u5408MPC\u5b9e\u73b0\u6beb\u79d2\u7ea7\u70ed\u8c03\u63a7\u5e76\u6700\u5c0f\u5316\u70ed\u68af\u5ea6\uff0c\u7535\u6781\u70ed\u5bfc\u7387\u538b\u5ef6\u5efa\u6a21\u5219\u5c06\u70ed\u7ba1\u7406\u5173\u6ce8\u70b9\u5ef6\u4f38\u81f3\u5236\u9020\u5de5\u827a\u5c42\u9762\u3002",
    "\u7535\u5316\u5b66\u6a21\u578b\u53c2\u6570\u6807\u5b9a\u8ffd\u6c42\u5feb\u901f\u7a33\u5065\u4ee5\u652f\u6491BMS\u6570\u5b57\u5b6a\u751f\uff0cBOLT\u65b9\u6cd5\u6574\u5408\u5019\u9009\u521d\u59cb\u5316\u3001\u6279\u5e76\u884cTRF\u7cbe\u4fee\u3001Numba JIT\u52a0\u901f\u4e0e\u591a\u5de5\u51b5\u4e00\u81f4\u6027\u7b5b\u9009\uff0c\u4e3a\u5728\u7ebf\u53c2\u6570\u66f4\u65b0\u4e0e\u68af\u6b21\u7b5b\u9009\u63d0\u4f9b\u5b9e\u7528\u65b9\u6848\u3002",
]

# --- Papers (10) ---
PAPERS = [
    {
        "num": 1, "tier": "T2", "date": "2026-07-16", "journal": "arXiv",
        "tags": ["SOH\u4f30\u7b97", "\u53ef\u89e3\u91caAI"],
        "title": "TIDE: Trustworthy and Interpretable Battery Degradation Estimation with Contextual Learning and Symbolic Distillation",
        "abstract": "\u63d0\u51faTIDE\u6846\u67b6\uff0c\u7ed3\u5408\u7535\u6c60\u9886\u57df\u77e5\u8bc6\u4e0e\u8fd0\u884c\u6570\u636e\uff0c\u5b9e\u73b0\u53ef\u4fe1\u4e14\u53ef\u89e3\u91ca\u7684\u7535\u6c60\u9000\u5316\u4f30\u8ba1\uff0c\u6574\u4f53\u4f30\u8ba1\u7cbe\u5ea6\u8f83\u57fa\u7ebf\u63d0\u534719.7%\u3002",
        "innovation": "\u5c06\u77e5\u8bc6\u5f15\u5bfc\u5148\u9a8c\u3001\u5355\u8c03\u6b8b\u5dee\u5efa\u6a21\u4e0e\u7b26\u53f7\u84b8\u998f\u7ed3\u5408\uff0c\u5728\u4fdd\u8bc1\u7cbe\u5ea6\u7684\u540c\u65f6\u63d0\u4f9b\u6a21\u578b\u7ea7\u53ef\u89e3\u91ca\u6027\uff0c\u652f\u6301\u667a\u80fd\u4e92\u8054\u7cfb\u7edf\u4e0b\u6e38\u51b3\u7b56\u3002",
        "url": "https://arxiv.org/abs/2607.14640",
    },
    {
        "num": 2, "tier": "T2", "date": "2026-07-16", "journal": "arXiv",
        "tags": ["\u50a8\u80fd\u8c03\u5ea6", "\u5206\u5e03\u5f0f\u63a7\u5236"],
        "title": "A Distributed PI+Reset Scheme for Discrete-Time Economic Dispatch of A Grid-connected BESS Network",
        "abstract": "\u7814\u7a76\u542b\u80fd\u91cf\u8def\u7531\u5668\u7684BESS\u7f51\u7edc\u7ecf\u6d4e\u8c03\u5ea6\u95ee\u9898\uff0c\u8bbe\u8ba1\u5e26\u590d\u4f4d\u673a\u5236\u7684\u5206\u5e03\u5f0fPI\u63a7\u5236\u5668\uff0c\u5728SoC\u7ea6\u675f\u4e0b\u52a0\u901f\u6536\u655b\u5e76\u63d0\u9ad8\u63a7\u5236\u7cbe\u5ea6\uff0c\u9002\u7528\u4e8e\u591a\u7535\u6c60\u50a8\u80fd\u7ad9\u534f\u540c\u8fd0\u884c\u573a\u666f\u3002",
        "innovation": "PI\u63a7\u5236\u5668\u590d\u4f4d\u673a\u5236\u5728\u6bd4\u4f8b\u9879\u53d8\u53f7\u65f6\u4ee4\u79ef\u5206\u9879\u4ece\u96f6\u7d2f\u79ef\uff0c\u517c\u987e\u6536\u655b\u901f\u5ea6\u4e0e\u63a7\u5236\u7cbe\u5ea6\uff0c\u65e0\u663e\u8457\u8d85\u8c03\uff0c\u63d0\u5347\u7cfb\u7edf\u7a33\u5b9a\u6027\u3002",
        "url": "https://arxiv.org/abs/2607.14508",
    },
    {
        "num": 3, "tier": "T2", "date": "2026-07-15", "journal": "arXiv",
        "tags": ["SOH\u4f30\u7b97", "\u4e0d\u786e\u5b9a\u6027\u91cf\u5316"],
        "title": "Predicting BESS Degradation with Uncertainty Quantification: A Probabilistic Framework for Battery Energy Storage Systems",
        "abstract": "\u63d0\u51fa\u6982\u7387\u6027\u7535\u6c60SOH\u9884\u6d4b\u6846\u67b6\uff0c\u7ed3\u5408\u6df1\u5ea6\u5b66\u4e60\u4e0e\u968f\u673a\u9000\u5316\u8f68\u8ff9\u4f20\u64ad\uff0c\u5b9e\u73b0\u7cfb\u7edf\u7ea7\u9000\u5316\u9884\u6d4b\u5e76\u8f93\u51fa95%\u7f6e\u4fe1\u533a\u95f4\u3002",
        "innovation": "\u5c06\u7535\u82af\u7ea7\u9884\u6d4b\u4e0e\u7cfb\u7edf\u62d3\u6251\u53ca\u5b9e\u9645\u8fd0\u884c\u53d8\u5f02\u6027\u96c6\u6210\uff0c\u5f25\u5408\u5b9e\u9a8c\u5ba4\u8001\u5316\u6a21\u578b\u4e0e\u5168\u7cfb\u7edf\u8fd0\u884c\u6570\u636e\u8bc4\u4f30\u4e4b\u95f4\u7684\u5dee\u8ddd\u3002",
        "url": "https://arxiv.org/abs/2607.13709",
    },
    {
        "num": 4, "tier": "T2", "date": "2026-07-14", "journal": "arXiv",
        "tags": ["\u68af\u6b21\u5229\u7528", "\u7535\u6c60\u5206\u7ec4"],
        "title": "Optimal Assembly of Repurposed Lithium-Ion Battery Packs under Cell Heterogeneity and Screening Uncertainty",
        "abstract": "\u63d0\u51fa\u68af\u6b21\u5229\u7528\u7535\u6c60\u7ec4\u88c5\u914d\u7684\u9c81\u68d2\u4f18\u5316\u6846\u67b6\uff0c\u5728\u5bb9\u91cf\u3001DCIR\u548c\u81ea\u653e\u7535\u5f02\u8d28\u6027\u53ca\u6d4b\u91cf\u4e0d\u786e\u5b9a\u6027\u4e0b\u5b9e\u73b010kW/10kWh\u7cfb\u7edf\u6700\u4f18\u7ec4\u88c5\uff0c\u63d0\u5347\u68af\u6b21\u7535\u6c60\u5229\u7528\u4ef7\u503c\u3002",
        "innovation": "\u5c06\u6d4b\u91cf\u4e0d\u786e\u5b9a\u6027\u5efa\u6a21\u4e3a\u6709\u754c\u533a\u95f4\uff0c\u6df7\u5408\u6574\u6570\u7ebf\u6027\u89c4\u5212\u8054\u5408\u4f18\u5316\u7535\u6c60\u5339\u914d\uff0c\u5931\u914d\u76ee\u6807\u8f83\u5355\u6307\u6807\u57fa\u7ebf\u964d\u4f4e76-87%\uff0c\u663e\u8457\u63d0\u5347\u7ec4\u88c5\u8d28\u91cf\u3002",
        "url": "https://arxiv.org/abs/2607.12951",
    },
    {
        "num": 5, "tier": "T2", "date": "2026-07-13", "journal": "arXiv",
        "tags": ["\u7535\u6c60\u8bbe\u8ba1", "\u51e0\u4f55\u5efa\u6a21"],
        "title": "Geometric Scaling of Battery Cells and Its Effect on Key Performance Indicators",
        "abstract": "\u63d0\u51fa\u5706\u67f1\u9502\u79bb\u5b50\u7535\u6c60\u7684\u8f7b\u91cf\u5316\u51e0\u4f55\u7f29\u653e\u6a21\u578b\uff0c\u6620\u5c04\u51e0\u4f55\u4e0e\u7535\u6781\u8bbe\u8ba1\u53d8\u91cf\u5230\u5bb9\u91cf\u3001\u5185\u963b\u3001\u8d28\u91cf\u3001\u4f53\u79ef\u53ca\u80fd\u91cf\u5bc6\u5ea6\u7b49\u5173\u952e\u6307\u6807\u3002",
        "innovation": "\u6a21\u578b\u9a8c\u8bc1\u540e\u7528\u4e8e\u5355\u7535\u6c60\u8bbe\u8ba1\u7a7a\u95f4\u63a2\u7d22\u4e0e\u5168\u5c40\u654f\u611f\u6027\u5206\u6790\uff0c\u8bc6\u522b\u4e3b\u5bfc\u8bbe\u8ba1\u53d8\u91cf\u53ca\u51e0\u4f55\u3001\u8d1f\u8f7d\u4e0e\u80fd\u91cf\u5bc6\u5ea6\u95f4\u7684\u6743\u8861\u5173\u7cfb\u3002",
        "url": "https://arxiv.org/abs/2607.11566",
    },
    {
        "num": 6, "tier": "T2", "date": "2026-07-13", "journal": "arXiv",
        "tags": ["\u70ed\u7ba1\u7406", "\u7535\u6781\u5236\u9020"],
        "title": "Capturing the calendering U-shape in lithium-ion electrode thermal conductivity",
        "abstract": "\u5f00\u53d1\u538b\u5ef6\u611f\u77e5\u7684Zehner-Bauer-Schl\u00fcnder\u6a21\u578b\u6269\u5c55\uff0c\u6355\u6349\u9502\u79bb\u5b50\u7535\u6781\u9762\u5185\u70ed\u5bfc\u7387\u5728\u538b\u5ef6\u8fc7\u7a0b\u4e2d\u7684U\u578b\u975e\u5355\u8c03\u53d8\u5316\u884c\u4e3a\u3002",
        "innovation": "\u7ed3\u5408Knudsen\u4fee\u6b63\u591a\u5b54\u57fa\u7ebf\u4e0e\u538b\u5ef6\u7d22\u5f15\u63a5\u89e6\u8d21\u732e\uff0c27\u79cd\u538b\u5ef6\u72b6\u6001\u4e0b\u5e73\u5747\u7edd\u5bf9\u767e\u5206\u6bd4\u8bef\u5dee\u4ece31.1%\u964d\u81f34.5%\u3002",
        "url": "https://arxiv.org/abs/2607.11521",
    },
    {
        "num": 7, "tier": "T2", "date": "2026-07-12", "journal": "arXiv",
        "tags": ["\u70ed\u7ba1\u7406", "\u6a21\u578b\u9884\u6d4b\u63a7\u5236"],
        "title": "Model Predictive Coolant Allocation for Integrated Tab-Surface Cooling of Battery Cells",
        "abstract": "\u63d0\u51fa\u96c6\u6210\u6781\u8033-\u8868\u9762\u51b7\u5374(ITSC)\u7cfb\u7edf\uff0c\u901a\u8fc7RTI-MPC\u52a8\u6001\u5206\u914d\u51b7\u5374\u6db2\uff0c\u5b9e\u65f6\u8c03\u63a7\u7535\u6c60\u6e29\u5ea6\u5e76\u6700\u5c0f\u5316\u70ed\u68af\u5ea6\u3002",
        "innovation": "RTI-MPC\u57280.0035\u2103\u7edd\u5bf9\u8bef\u5dee\u5185\u590d\u73b0\u975e\u7ebf\u6027MPC\u70ed\u54cd\u5e94\uff0c\u8ba1\u7b97\u6210\u672c\u4ece\u6570\u79d2\u964d\u81f319.3ms\uff0c\u5177\u5907\u5b9e\u65f6\u90e8\u7f72\u6f5c\u529b\u3002",
        "url": "https://arxiv.org/abs/2607.10872",
    },
    {
        "num": 8, "tier": "T2", "date": "2026-07-11", "journal": "arXiv",
        "tags": ["SOH\u4f30\u7b97", "\u751f\u6210\u6a21\u578b"],
        "title": "BattVAE-GP: Generative Modeling of Long-Horizon Battery Degradation with Uncertainty Quantification",
        "abstract": "\u63d0\u51fa\u6df7\u5408\u7269\u7406-\u6982\u7387\u5b66\u4e60\u6846\u67b6\uff0c\u5229\u7528VAE\u4e0e\u591a\u4efb\u52a1\u9ad8\u65af\u8fc7\u7a0b\u6784\u5efa\u7535\u6c60\u9000\u5316\u8f68\u8ff9\u4ee3\u7406\u6a21\u578b\uff0c\u63d0\u4f9b\u4e0d\u786e\u5b9a\u6027\u611f\u77e5\u7684SOH\u4f30\u8ba1\u3002",
        "innovation": "\u5c06DFN/P2D\u7535\u5316\u5b66\u6a21\u578b\u9000\u5316\u6570\u636e\u7f16\u7801\u81f3\u4e8c\u7ef4\u6f5c\u7a7a\u95f4\uff0cGP\u5728\u6f5c\u7a7a\u95f4\u63d2\u503c\u5e76\u63d0\u4f9b\u540e\u9a8c\u4e0d\u786e\u5b9a\u6027\uff0c\u8499\u7279\u5361\u6d1b\u4f20\u64ad\u5b9e\u73b0SOH\u4e0d\u786e\u5b9a\u6027\u4f30\u8ba1\u3002",
        "url": "https://arxiv.org/abs/2607.11943",
    },
    {
        "num": 9, "tier": "T1", "date": "2026-07-15", "journal": "J. Energy Storage",
        "tags": ["SOH\u4f30\u7b97", "RUL\u9884\u6d4b", "\u8fc1\u79fb\u5b66\u4e60"],
        "title": "Multi-modal degradation information fusion with transfer learning for state of health estimation and remaining useful life inference of lithium-ion batteries",
        "abstract": "\u63d0\u51fa\u591a\u6a21\u6001\u8fc1\u79fb\u5b66\u4e60\u6846\u67b6\uff0c\u878d\u5408IC\u3001IS\u53ca\u9012\u5f52\u56fe\u8868\u5f81\u7535\u6c60\u9000\u5316\uff0cSOH\u4f30\u8ba1RMSE\u7ea61.01%\uff0cRUL\u76f8\u5bf9\u8bef\u5dee1.87%\u3002",
        "innovation": "\u53cd\u5411Softmax\u8de8\u6a21\u6001\u6ce8\u610f\u529b\u964d\u4f4e\u9ad8\u76f8\u4f3c\u7279\u5f81\u6743\u91cd\uff0cRMMD\u6309\u76f8\u5bf9\u9000\u5316\u8fdb\u7a0b\u5206\u6bb5\u5bf9\u9f50\uff0c\u51cf\u8f7b\u8de8\u57df\u9636\u6bb5\u9519\u914d\u3002",
        "url": "https://doi.org/10.1016/j.est.2026.123461",
    },
    {
        "num": 10, "tier": "T1", "date": "2026-07-14", "journal": "Applied Energy",
        "tags": ["\u53c2\u6570\u8fa8\u8bc6", "\u7535\u5316\u5b66\u6a21\u578b"],
        "title": "Rapid and robust parameter estimation for electrochemical battery models via BOLT: A batch-optimized local-to-global technique",
        "abstract": "\u63d0\u51faBOLT\u65b9\u6cd5\uff0c\u6574\u5408\u5019\u9009\u521d\u59cb\u5316\u3001\u6279\u5e76\u884cTRF\u5c40\u90e8\u7cbe\u4fee\u3001Numba JIT\u52a0\u901f\u4e0e\u591a\u5de5\u51b5\u4e00\u81f4\u6027\u7b5b\u9009\uff0c\u5b9e\u73b0\u7535\u5316\u5b66\u6a21\u578b\u5feb\u901f\u53c2\u6570\u6807\u5b9a\u3002",
        "innovation": "BOLT(32)\u5728\u4e94\u79cd\u5de5\u51b5\u4e0b\u5b9e\u73b012.4\u00b10.1mV\u5e73\u5747MAE\uff0c\u4ec5\u970020636\u6b21\u6a21\u578b\u8c03\u7528\u548c8.97s/\u6b21\uff0c\u7cbe\u5ea6\u3001\u6548\u7387\u4e0e\u91cd\u590d\u7a33\u5b9a\u6027\u5747\u4f18\u4e8ePSO\u548cGA\u3002",
        "url": "https://doi.org/10.1016/j.apenergy.2026.128307",
    },
]

# --- Vendor News (10) ---
VENDOR_NEWS = [
    {
        "num": 1, "tier": "T2", "date": "2026-07-16",
        "tags": ["\u88c5\u673a\u91cf", "\u5e02\u5360\u7387", "\u4e2d\u6c7d\u534f"],
        "title": "2026\u5e746\u6708\u4e2d\u56fd\u52a8\u529b\u7535\u6c60\u88c5\u673a\u91cfTOP15\u51fa\u7089",
        "abstract": "6\u6708\u56fd\u5185\u52a8\u529b\u7535\u6c60\u88c5\u673a76.5GWh\uff0c\u540c\u6bd4+31.5%\uff1b\u5b81\u5fb7\u65f6\u4ee342.74%\u3001\u6bd4\u4e9a\u8fea18.49%\u5c45\u524d\u4e8c\uff0c\u4e2d\u521b\u65b0\u822a\u53cd\u8d85\u56fd\u8f69\u5347\u81f3\u7b2c\u4e09\uff0c\u78f7\u9178\u94c1\u9502\u5360\u6bd483.3%\u3002",
        "url": "https://auto.sina.cn/2026-07-16/detail-inihyyvw7703846.d.html",
    },
    {
        "num": 2, "tier": "T3", "date": "2026-07-12",
        "tags": ["CATL", "\u6d77\u5916\u5408\u4f5c", "\u5956\u9879"],
        "title": "\u52a8\u529b\u7535\u6c60\u9886\u57df\u552f\u4e00\uff01\u5b81\u5fb7\u65f6\u4ee3\u8363\u83b72026\u5e74\u5927\u4f17\u96c6\u56e2\u5956",
        "abstract": "\u5b81\u5fb7\u65f6\u4ee3\u6210\u4e3a2026\u5e74\u5927\u4f17\u96c6\u56e2\u5956\u4e2d\u52a8\u529b\u7535\u6c60\u9886\u57df\u552f\u4e00\u83b7\u5956\u4f01\u4e1a\uff0c\u4f53\u73b0\u5176\u4e0e\u6d77\u5916\u6574\u8f66\u5382\u4f9b\u5e94\u94fe\u5408\u4f5c\u6301\u7eed\u6df1\u5316\uff0c\u6807\u5fd7\u7740\u4e2d\u56fd\u52a8\u529b\u7535\u6c60\u4f01\u4e1a\u5728\u5168\u7403\u6c7d\u8f66\u4ea7\u4e1a\u94fe\u4e2d\u7684\u4f9b\u5e94\u5730\u4f4d\u8fdb\u4e00\u6b65\u5de9\u56fa\u3002",
        "url": "https://www.catl.com/",
    },
    {
        "num": 3, "tier": "T2", "date": "2026-07-15",
        "tags": ["CATL", "\u8d22\u62a5", "\u5206\u7ea2"],
        "title": "\u5b81\u5fb7\u65f6\u4ee3\uff1a7\u670824\u65e5\u53ec\u5f00\u8463\u4e8b\u4f1a\u5ba1\u8bae\u4e2d\u671f\u4e1a\u7ee9\u53ca\u6d3e\u606f",
        "abstract": "\u5b81\u5fb7\u65f6\u4ee3\u516c\u544a\u5c06\u4e8e7\u670824\u65e5\u4e3e\u884c\u8463\u4e8b\u4f1a\u5ba1\u8bae2026\u5e74\u4e2d\u671f\u4e1a\u7ee9\u5e76\u8003\u8651\u5efa\u8bae\u6d3e\u53d1\u4e2d\u671f\u80a1\u606f\uff0c\u534a\u5e74\u62a5\u62ab\u9732\u7a97\u53e3\u4e34\u8fd1\u3002",
        "url": "https://m.sohu.com/a/1050195975_122014422/",
    },
    {
        "num": 4, "tier": "T2", "date": "2026-07-17",
        "tags": ["CATL", "\u6e2f\u80a1", "\u8d44\u91d1\u6d41\u5411"],
        "title": "\u5b81\u5fb7\u65f6\u4ee3(03750.HK)\uff1a7\u670817\u65e5\u5357\u5411\u8d44\u91d1\u589e\u63016.9\u4e07\u80a1",
        "abstract": "7\u670817\u65e5\u5357\u5411\u8d44\u91d1\u589e\u6301\u5b81\u5fb7\u65f6\u4ee3H\u80a16.9\u4e07\u80a1\uff0c\u8fd15\u65e53\u65e5\u83b7\u589e\u6301\uff0c\u53cd\u6620\u6e2f\u80a1\u8d44\u91d1\u5bf9\u7535\u6c60\u9f99\u5934\u7684\u914d\u7f6e\u52a8\u6001\u3002",
        "url": "https://m.sohu.com/a/1051682488_122123195/",
    },
    {
        "num": 5, "tier": "T3", "date": "2026-07-16",
        "tags": ["BYD", "\u50a8\u80fd", "\u4e1c\u5357\u4e9a"],
        "title": "\u6bd4\u4e9a\u8fea\uff1a2026\u5e747\u67089\u65e5\u6295\u8d44\u8005\u5173\u7cfb\u6d3b\u52a8\u8bb0\u5f55\uff08\u50a8\u80fd\u51fa\u6d77\u4e1c\u5357\u4e9a\uff09",
        "abstract": "\u6bd4\u4e9a\u8fea\u50a8\u80fd\u643a\u5927\u50a8BYD Haohan\u53ca\u6237\u7528Battery-Box LV5.0+/HVE\u7cfb\u5217\u4eae\u76f8\u4e1c\u5357\u4e9a\u5e02\u573a\uff0c\u52a0\u7801\u6d77\u5916\u50a8\u80fd\u5e03\u5c40\uff0c\u6269\u5927\u5728\u5168\u7403\u50a8\u80fd\u5e02\u573a\u7684\u5e02\u5360\u7387\u548c\u54c1\u724c\u5f71\u54cd\u529b\u3002",
        "url": "https://auto.sina.cn/2026-07-16/detail-inihyuqf8046301.d.html",
    },
    {
        "num": 6, "tier": "T2", "date": "2026-07-12",
        "tags": ["\u9502\u7535", "\u51fa\u8d27\u91cf", "\u50a8\u80fd"],
        "title": "\u9502\u7535\u4ea7\u4e1a\u94fe\u53cc\u5468\u62a5\uff1a\u7535\u6c60\u4f01\u4e1a\u6301\u7eed\u65a9\u83b7\u50a8\u80fd\u5927\u5355",
        "abstract": "2026H1\u56fd\u5185\u52a8\u529b\u7535\u6c60\u51fa\u8d27\u7ea6630GWh\u540c\u6bd4+30%\uff0c\u50a8\u80fd\u7535\u6c60\u7ea6485GWh\u540c\u6bd4+80%\uff0c\u4ebf\u7eac\u3001\u745e\u6d66\u5170\u94a7\u7b49\u4e2d\u62a5\u4e1a\u7ee9\u5411\u597d\u3002",
        "url": "https://data.eastmoney.com/report/zw_industry.jshtml?infocode=AP202607121826910146",
    },
    {
        "num": 7, "tier": "T2", "date": "2026-07-15",
        "tags": ["\u50a8\u80fd", "\u4ea7\u80fd", "\u8d44\u6e90\u535a\u5f08"],
        "title": "\u50a8\u80fd\u6269\u5bb9\u6f6e\u8d77\uff0c\u8f66\u7528\u7535\u6c60\u6216\u9762\u4e34\u201c\u8d44\u6e90\u535a\u5f08\u201d",
        "abstract": "\u5b81\u5fb7\u3001\u4ebf\u7eac\u3001\u6b23\u65fa\u8fbe\u3001\u8fdc\u666f\u3001\u695a\u80fd\u3001\u8702\u7a9d\u7b49\u5bc6\u96c6\u5b98\u5ba3\u5927\u989d\u50a8\u80fd\u8ba2\u5355\uff0c\u50a8\u80fd\u4e1a\u52a1\u8fdb\u5165\u96c6\u4e2d\u5151\u73b0\u671f\uff0c\u4e0e\u8f66\u7528\u7535\u6c60\u4e89\u593a\u8d44\u6e90\u3002",
        "url": "https://www.escn.com.cn/news/show-2262354.html",
    },
    {
        "num": 8, "tier": "T2", "date": "2026-07-14",
        "tags": ["CATL", "\u4e13\u5229", "\u6b63\u6781"],
        "title": "\u5b81\u5fb7\u65f6\u4ee3\u83b7\u65b0\u53d1\u660e\u4e13\u5229\u6388\u6743\uff0c\u63d0\u5347\u7535\u6c60\u5faa\u73af\u5bb9\u91cf\u4fdd\u6301\u7387",
        "abstract": "\u5b81\u5fb7\u65f6\u4ee3\u83b7\u201c\u6b63\u6781\u6781\u7247\u53ca\u5176\u5236\u5907\u65b9\u6cd5\u3001\u7535\u6c60\u3001\u7528\u7535\u8bbe\u5907\u201d\u53d1\u660e\u4e13\u5229\u6388\u6743\uff0c\u52a9\u529b\u5faa\u73af\u5bff\u547d\u4e0e\u5bb9\u91cf\u4fdd\u6301\u7387\u63d0\u5347\u3002",
        "url": "https://m.sohu.com/a/1050378421_122066678/",
    },
    {
        "num": 9, "tier": "T1", "date": "2026-07-13",
        "tags": ["\u7535\u6c60\u56de\u6536", "\u653f\u7b56", "\u5de5\u4fe1\u90e8"],
        "title": "\u5de5\u4fe1\u90e8\u7b49\u516d\u90e8\u95e8\u5370\u53d1\u300a\u65b0\u80fd\u6e90\u6c7d\u8f66\u5e9f\u65e7\u52a8\u529b\u7535\u6c60\u56de\u6536\u7ba1\u7406\u6682\u884c\u529e\u6cd5\u300b",
        "abstract": "\u5de5\u4fe1\u90e8\u3001\u53d1\u6539\u59d4\u3001\u751f\u6001\u73af\u5883\u90e8\u7b49\u516d\u90e8\u95e8\u8054\u5408\u5370\u53d1\u52a8\u529b\u7535\u6c60\u56de\u6536\u7ba1\u7406\u6682\u884c\u529e\u6cd5\uff0c\u660e\u786e\u56de\u6536\u4e3b\u4f53\u4e0e\u8d23\u4efb\uff0c\u89c4\u8303\u56de\u6536\u6d41\u7a0b\u3002",
        "url": "https://m.sohu.com/a/1050684649_121106902/",
    },
    {
        "num": 10, "tier": "T2", "date": "2026-07-12",
        "tags": ["\u50a8\u80fd", "\u8ba2\u5355", "\u94a0\u7535"],
        "title": "\u4e00\u5468\u50a8\u80fd\u4f01\u4e1a\uff1a\u8fdc\u666f/\u9633\u5149/\u745e\u6d66/\u6b23\u65fa\u8fbe/\u5b81\u5fb7/\u695a\u80fd\u7b49\u52a8\u6001",
        "abstract": "\u6c47\u603b\u4e00\u5468\u50a8\u80fd\u4f01\u4e1a\u7b7e\u7ea6\u4e0e\u8ba2\u5355\uff0c\u542b\u6bd4\u4e9a\u8feaMasdar 11.275GWh\u3001\u5b81\u5fb7\u5929\u6052\u94a0\u75359\u6708\u4ea4\u4ed8\u7b49\u5173\u952e\u8282\u70b9\u3002",
        "url": "https://finance.sina.com.cn/wm/2026-07-12/doc-inihqzxm4272944.shtml",
    },
]

# --- Open Source (10) ---
OPEN_SOURCE = [
    {
        "num": 1, "tier": "T3", "date": "2026-07-18",
        "tags": ["BMS", "\u5b66\u4e60\u8d44\u6e90", "Python"],
        "title": "MG-Seo17/BMS-Portfolio",
        "abstract": "\u7535\u6c60\u7ba1\u7406\u7cfb\u7edf\uff08BMS\uff09\u5b66\u4e60\u7b14\u8bb0\u4e0e\u9879\u76ee\u96c6\u5408\uff0cPython\u5b9e\u73b0\uff0c7\u670818\u65e5\u65b0\u589e\u5185\u5bb9\u66f4\u65b0\u3002",
        "url": "https://github.com/MG-Seo17/BMS-Portfolio/releases",
    },
    {
        "num": 2, "tier": "T3", "date": "2026-07-18",
        "tags": ["BESS", "\u80fd\u91cf\u7ba1\u7406", "\u50a8\u80fd"],
        "title": "Marinalizm/BESS-energy-management-system",
        "abstract": "300MW\u7535\u6c60\u50a8\u80fd\u7cfb\u7edf\uff08BESS\uff09\u5b9e\u65f6\u76d1\u63a7\u4e0e\u80fd\u91cf\u7ba1\u7406\u7cfb\u7edf\uff0cJava\u5b9e\u73b0\uff0c\u542bHIL\u4eff\u771f\u4e0eSCADA\uff0c7\u670818\u65e5\u91cd\u5927\u66f4\u65b0\u3002",
        "url": "https://github.com/Marinalizm/BESS-energy-management-system/releases",
    },
    {
        "num": 3, "tier": "T3", "date": "2026-07-16",
        "tags": ["SOC\u4f30\u7b97", "PINN", "LSTM"],
        "title": "MMRezAkp/PINNMirai",
        "abstract": "\u57fa\u4e8e\u7269\u7406\u4fe1\u606f\u795e\u7ecf\u7f51\u7edc(PINN)+LSTM\u8fc1\u79fb\u5b66\u4e60\u7684\u7535\u6c60SOC\u4f30\u7b97\uff0c\u9762\u5411\u4e30\u7530Mirai\u71c3\u6599\u7535\u6c60\u6df7\u52a8\u8f66\u578b\uff0cMIT\u534f\u8bae\u3002",
        "url": "https://github.com/MMRezAkp/PINNMirai/releases",
    },
    {
        "num": 4, "tier": "T3", "date": "2026-07-16",
        "tags": ["LFP", "SOC", "\u78f7\u9178\u94c1\u9502"],
        "title": "MahathiSGit/LFP-battery-soc-estimation",
        "abstract": "\u78f7\u9178\u94c1\u9502(LFP)\u7535\u6c60SOC\u4f30\u7b97\u9879\u76ee\uff0c7\u670816\u65e5\u63a8\u9001\u66f4\u65b0\uff0c\u5305\u542b\u591a\u79cd\u4f30\u7b97\u7b97\u6cd5\u5b9e\u73b0\u4e0e\u5bf9\u6bd4\u3002",
        "url": "https://github.com/MahathiSGit/LFP-battery-soc-estimation/releases",
    },
    {
        "num": 5, "tier": "T3", "date": "2026-07-15",
        "tags": ["EV", "Simulink", "SOC"],
        "title": "rohit3481/EV-Powertrain-Performance-Analysis-MATLAB-Simulink",
        "abstract": "\u57fa\u4e8eMATLAB/Simulink\u7684\u7535\u52a8\u6c7d\u8f66\u52a8\u529b\u603b\u6210\u4eff\u771f\uff0c\u542b\u7535\u6c60SOC\u4f30\u7b97\u3001\u80fd\u91cf\u5206\u6790\u4e0e\u5236\u52a8\u56de\u9988\u8bc4\u4f30\uff0c7\u670815\u65e5\u66f4\u65b0\u3002",
        "url": "https://github.com/rohit3481/EV-Powertrain-Performance-Analysis-MATLAB-Simulink",
    },
    {
        "num": 6, "tier": "T3", "date": "2026-07-18",
        "tags": ["\u7535\u6c60\u6570\u636e", "\u8d44\u6e90\u6c47\u603b"],
        "title": "nikamhritik/awesome-battery-data",
        "abstract": "\u7535\u6c60\u5f00\u6e90\u6570\u636e\u3001\u5efa\u6a21\u5de5\u5177\u4e0e\u5206\u6790\u8d44\u6e90\u7efc\u5408\u6c47\u603b\u6e05\u5355\uff0c7\u670818\u65e5\u66f4\u65b0\u6536\u5f55\uff0c\u8986\u76d6\u591a\u79cd\u7535\u6c60\u7c7b\u578b\u4e0e\u573a\u666f\u3002",
        "url": "https://github.com/nikamhritik/awesome-battery-data/releases",
    },
    {
        "num": 7, "tier": "T3", "date": "2026-07-18",
        "tags": ["BESS", "\u57fa\u51c6\u6d4b\u8bd5", "AI"],
        "title": "Pixeltruth/bess-benchmark",
        "abstract": "\u7535\u6c60\u50a8\u80fd\u4e0e\u5bb6\u5ead\u80fd\u6e90\u7ba1\u7406\u57fa\u7840\u6a21\u578b\u57fa\u51c6\u8bc4\u6d4b\u6846\u67b6\uff0c\u591a\u771f\u5b9e\u573a\u666f\u6307\u6807\uff0cMIT\u534f\u8bae\uff0c7\u670818\u65e5\u66f4\u65b0\u3002",
        "url": "https://github.com/Pixeltruth/bess-benchmark/releases",
    },
    {
        "num": 8, "tier": "T3", "date": "2026-07-15",
        "tags": ["\u7535\u6c60\u5b89\u5168", "\u8def\u5f84\u89c4\u5212", "\u65e0\u4eba\u673a"],
        "title": "Violet030zzz/Energy-aware-UAV-Delivery-Route-Planning",
        "abstract": "\u8003\u8651\u7535\u6c60\u5b89\u5168\u7ea6\u675f\u7684\u65e0\u4eba\u673a\u914d\u9001\u8def\u5f84\u89c4\u5212\u4eff\u771f\uff0c\u5bf9\u6bd4Dijkstra\u4e0eA*\u7b97\u6cd5\u5e76\u8bc4\u4f30\u8fd4\u822a\u80fd\u91cf\u4f59\u91cf\uff0cPython\u5b9e\u73b0\u3002",
        "url": "https://github.com/Violet030zzz/Energy-aware-UAV-Delivery-Route-Planning/releases",
    },
    {
        "num": 9, "tier": "T3", "date": "2026-07-18",
        "tags": ["\u7535\u6c60\u63a7\u5236", "\u50a8\u80fd", "\u667a\u80fd\u5bb6\u5c45"],
        "title": "EmmaVriezen/HA-battery-controller-SBSE",
        "abstract": "\u901a\u8fc7SMA Sunny Boy Smart Energy\u6df7\u5408\u9006\u53d8\u5668\u63a7\u5236\u7535\u6c60\u7684Home Assistant\u81ea\u52a8\u5316\u7ec4\u4ef6\uff0cApache-2.0\u534f\u8bae\uff0c7\u670818\u65e5\u66f4\u65b0\u3002",
        "url": "https://github.com/EmmaVriezen/HA-battery-controller-SBSE/releases",
    },
    {
        "num": 10, "tier": "T3", "date": "2026-07-18",
        "tags": ["EV", "\u5145\u7535", "\u7eed\u822a\u53ef\u89c6\u5316"],
        "title": "lohithaketha01/Visualization-Tool-for-Electric-Vehicle-Charge-and-Range-Analysis",
        "abstract": "\u7535\u52a8\u6c7d\u8f66\u5145\u7535\u4e0e\u7eed\u822a\u5206\u6790\u53ef\u89c6\u5316\u5de5\u5177\uff0c\u652f\u6301\u591a\u7ef4\u5ea6\u6570\u636e\u5c55\u793a\u4e0e\u4ea4\u4e92\u5206\u6790\uff0c7\u670818\u65e5\u66f4\u65b0\u3002",
        "url": "https://github.com/lohithaketha01/Visualization-Tool-for-Electric-Vehicle-Charge-and-Range-Analysis",
    },
]

# --- Patents (10) ---
PATENTS = [
    {
        "num": 1, "tier": "T3", "date": "2026-07-17",
        "tags": ["SOC\u4f30\u7b97", "\u56fd\u6c11\u6280\u672f", "\u82af\u7247\u5382\u5546"],
        "title": "\u7535\u6c60SOC\u9884\u6d4b\u65b9\u6cd5\u548c\u88c5\u7f6e",
        "applicant": "\u56fd\u6c11\u6280\u672f\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u57fa\u4e8e\u80fd\u91cf\u5b88\u6052\u5b9a\u5f8b\uff0c\u901a\u8fc7\u9884\u6d4b\u672a\u6765\u95f4\u9694\u5185\u91c7\u6837\u70b9\u7684\u6e29\u5ea6\u548c\u963b\u6297\uff0c\u8ba1\u7b97\u7126\u8033\u70ed\uff0c\u4ece\u800c\u9ad8\u7cbe\u5ea6\u9884\u6d4b\u7535\u6c60SOC\u3002",
        "innovation": "\u5c06\u672a\u6765\u6e29\u5ea6/\u963b\u6297\u9884\u6d4b\u4e0e\u7126\u8033\u70ed\u8ba1\u7b97\u7ed3\u5408\uff0c\u65b9\u6848\u7b80\u5355\u6613\u884c\uff0cSOC\u9884\u6d4b\u7cbe\u5ea6\u663e\u8457\u63d0\u5347\u3002",
        "url": "https://patents.google.com/patent/CN116184203B",
    },
    {
        "num": 2, "tier": "T3", "date": "2026-07-17",
        "tags": ["SOC\u663e\u793a", "\u5b81\u5fb7\u65f6\u4ee3"],
        "title": "\u786e\u5b9a\u7535\u6c60\u5305\u7684\u663e\u793a\u8377\u7535\u72b6\u6001SOC\u7684\u65b9\u6cd5\u4e0e\u88c5\u7f6e",
        "applicant": "\u5b81\u5fb7\u65f6\u4ee3\u65b0\u80fd\u6e90\u79d1\u6280\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u901a\u8fc7\u83b7\u53d6\u5b9e\u9645SOC\u4e0e\u663e\u793aSOC\uff0c\u4fee\u6b63\u663e\u793a\u7cbe\u5ea6\uff0c\u63d0\u5347\u7535\u6c60\u7ba1\u7406\u9886\u57df\u7528\u6237\u4f53\u9a8c\uff0c\u907f\u514d\u8868\u663e\u7535\u91cf\u8df3\u53d8\u5f15\u53d1\u7528\u6237\u7126\u8651\u3002",
        "innovation": "\u533a\u5206\u5b9e\u9645\u4e0e\u663e\u793aSOC\u5e76\u8fdb\u884c\u52a8\u6001\u4fee\u6b63\uff0c\u89e3\u51b3\u8868\u663e\u4e0e\u771f\u5b9e\u7535\u91cf\u504f\u5dee\u95ee\u9898\uff0c\u63d0\u5347\u6574\u8f66BMS\u7cfb\u7edf\u53ef\u9760\u6027\u3002",
        "url": "https://patents.google.com/patent/CN202180085513A",
    },
    {
        "num": 3, "tier": "T3", "date": "2026-07-17",
        "tags": ["BMS\u82af\u7247", "\u5b81\u5fb7\u65f6\u4ee3"],
        "title": "\u7535\u6c60\u63a7\u5236\u82af\u7247\u3001\u7535\u6c60\u7ba1\u7406\u7cfb\u7edf\u3001\u7535\u6c60\u88c5\u7f6e\u53ca\u7528\u7535\u88c5\u7f6e",
        "applicant": "\u5b81\u5fb7\u65f6\u4ee3\u65b0\u80fd\u6e90\u79d1\u6280\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u6d89\u53ca\u7535\u6c60\u63a7\u5236\u82af\u7247\u53ca\u542b\u8be5\u82af\u7247\u7684BMS\u3001\u7535\u6c60\u88c5\u7f6e\u4e0e\u7528\u7535\u88c5\u7f6e\u7684\u96c6\u6210\u8bbe\u8ba1\u65b9\u6848\u3002",
        "innovation": "\u5c06\u63a7\u5236\u82af\u7247\u4e0eBMS\u7cfb\u7edf\u786c\u4ef6\u6df1\u5ea6\u96c6\u6210\uff0c\u63d0\u5347\u7535\u6c60\u7ba1\u7406\u53ef\u9760\u6027\u4e0e\u96c6\u6210\u5ea6\u3002",
        "url": "https://patents.google.com/patent/CN202620605074U",
    },
    {
        "num": 4, "tier": "T3", "date": "2026-07-17",
        "tags": ["SOH\u4f30\u7b97", "\u5b87\u901a\u5ba2\u8f66", "\u5546\u7528\u8f66"],
        "title": "\u4e00\u79cd\u8f66\u8f86\u7535\u6c60SOH\u9884\u6d4b\u65b9\u6cd5\u53ca\u7cfb\u7edf",
        "applicant": "\u5b87\u901a\u5ba2\u8f66\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u901a\u8fc7\u591a\u53c2\u6570\u62df\u5408\u65b9\u5f0f\u9884\u6d4b\u8f66\u8f86\u7535\u6c60\u5065\u5eb7\u72b6\u6001\uff08SOH\uff09\uff0c\u63d0\u5347\u7535\u6c60\u5bff\u547d\u8bc4\u4f30\u51c6\u786e\u6027\u3002",
        "innovation": "\u591a\u53c2\u6570\u8054\u5408\u62df\u5408\u5efa\u6a21\uff0c\u9488\u5bf9\u5546\u7528\u8f66\u573a\u666f\u4f18\u5316SOH\u9884\u6d4b\uff0c\u63d0\u5347\u8fd0\u8425\u8f66\u8f86\u7535\u6c60\u7ba1\u7406\u3002",
        "url": "https://patents.google.com/patent/CN116660763B",
    },
    {
        "num": 5, "tier": "T3", "date": "2026-07-17",
        "tags": ["\u7535\u6c60\u5747\u8861", "\u5b81\u5fb7\u65f6\u4ee3"],
        "title": "\u5747\u8861\u7535\u8def\u548c\u5747\u8861\u7cfb\u7edf",
        "applicant": "\u5b81\u5fb7\u65f6\u4ee3\u65b0\u80fd\u6e90\u79d1\u6280\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u63d0\u4f9b\u4e00\u79cd\u7535\u6c60\u5747\u8861\u7535\u8def\u4e0e\u5747\u8861\u7cfb\u7edf\uff0c\u7528\u4e8e\u89e3\u51b3\u7535\u6c60\u5355\u4f53\u95f4\u4e00\u81f4\u6027\u5dee\u5f02\u95ee\u9898\uff0c\u63d0\u5347\u7535\u6c60\u7ec4\u6574\u4f53\u6027\u80fd\u4e0e\u5faa\u73af\u5bff\u547d\u3002",
        "innovation": "\u4f18\u5316\u5747\u8861\u7535\u8def\u62d3\u6251\u7ed3\u6784\uff0c\u63d0\u9ad8\u5747\u8861\u6548\u7387\u4e0e\u80fd\u91cf\u5229\u7528\u7387\uff0c\u964d\u4f4e\u80fd\u8017\u635f\u8017\uff0c\u5ef6\u957f\u7535\u6c60\u7ec4\u4f7f\u7528\u5bff\u547d\u3002",
        "url": "https://patents.google.com/patent/CN202521120464U",
    },
    {
        "num": 6, "tier": "T3", "date": "2026-07-14",
        "tags": ["\u7535\u6c60\u70ed\u7ba1\u7406", "\u6bd4\u4e9a\u8fea"],
        "title": "\u7535\u6c60\u5305\u7684\u6362\u70ed\u7ec4\u4ef6\u548c\u7535\u6c60\u5305\u3001\u8f66\u8f86",
        "applicant": "\u6bd4\u4e9a\u8fea\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u63d0\u4f9b\u4e00\u79cd\u7535\u6c60\u5305\u6362\u70ed\u7ec4\u4ef6\uff0c\u4f18\u5316\u7535\u6c60\u5305\u5185\u90e8\u70ed\u4ea4\u6362\u7ed3\u6784\uff0c\u63d0\u5347\u6563\u70ed\u6548\u7387\uff0c\u964d\u4f4e\u70ed\u5931\u63a7\u98ce\u9669\u3002",
        "innovation": "\u6539\u8fdb\u6362\u70ed\u7ec4\u4ef6\u7ed3\u6784\u8bbe\u8ba1\uff0c\u589e\u5f3a\u70ed\u7ba1\u7406\u80fd\u529b\uff0c\u964d\u4f4e\u70ed\u5931\u63a7\u98ce\u9669\uff0c\u63d0\u5347\u7535\u6c60\u5305\u8fd0\u884c\u5b89\u5168\u6027\u4e0e\u5bff\u547d\u3002",
        "url": "https://patents.google.com/patent/CN202211049751A",
    },
    {
        "num": 7, "tier": "T3", "date": "2026-07-14",
        "tags": ["\u7535\u6c60\u5b89\u5168", "\u7edd\u7f18", "\u6bd4\u4e9a\u8fea"],
        "title": "\u7edd\u7f18\u819c\u3001\u7535\u82af\u3001\u7535\u6c60\u7ec4\u4ef6\u3001\u7535\u6c60\u5305\u4ee5\u53ca\u7528\u7535\u8bbe\u5907",
        "applicant": "\u6bd4\u4e9a\u8fea\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u6d89\u53ca\u7535\u82af\u7edd\u7f18\u819c\u53ca\u542b\u8be5\u7edd\u7f18\u819c\u7684\u7535\u6c60\u7ec4\u4ef6\u3001\u7535\u6c60\u5305\u7ed3\u6784\uff0c\u63d0\u5347\u7535\u6c14\u5b89\u5168\u3002",
        "innovation": "\u4f18\u5316\u7edd\u7f18\u819c\u6750\u6599\u4e0e\u7ed3\u6784\uff0c\u589e\u5f3a\u7535\u82af\u95f4\u7edd\u7f18\u6027\u80fd\uff0c\u964d\u4f4e\u77ed\u8def\u98ce\u9669\u3002",
        "url": "https://patents.google.com/patent/CN202521340083U",
    },
    {
        "num": 8, "tier": "T3", "date": "2026-07-17",
        "tags": ["\u7535\u6c60\u5b89\u5168\u8bca\u65ad", "\u4e0a\u6c7d\u96c6\u56e2"],
        "title": "\u52a8\u529b\u7535\u6c60\u7684\u5f02\u5e38\u68c0\u6d4b\u65b9\u6cd5\u548c\u88c5\u7f6e\u3001\u5b58\u50a8\u4ecb\u8d28\u53ca\u8ba1\u7b97\u673a\u7a0b\u5e8f\u4ea7\u54c1",
        "applicant": "\u4e0a\u6d77\u6c7d\u8f66\u96c6\u56e2\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u63d0\u4f9b\u52a8\u529b\u7535\u6c60\u5f02\u5e38\u68c0\u6d4b\u65b9\u6cd5\u4e0e\u88c5\u7f6e\uff0c\u63d0\u5347\u52a8\u529b\u7535\u6c60\u5f02\u5e38\u68c0\u6d4b\u7684\u51c6\u786e\u6027\u4e0e\u65f6\u6548\u6027\u3002",
        "innovation": "\u57fa\u4e8e\u6570\u636e\u9a71\u52a8\u7684\u5f02\u5e38\u68c0\u6d4b\u7b97\u6cd5\uff0c\u5b9e\u73b0\u5bf9\u52a8\u529b\u7535\u6c60\u8fd0\u884c\u5f02\u5e38\u7684\u5b9e\u65f6\u8bc6\u522b\u4e0e\u9884\u8b66\u3002",
        "url": "https://patents.google.com/patent/CN122410340A",
    },
    {
        "num": 9, "tier": "T3", "date": "2026-07-17",
        "tags": ["\u6545\u969c\u8bca\u65ad", "\u5927\u6a21\u578b", "\u4e0a\u6c7d\u96c6\u56e2"],
        "title": "\u4e00\u79cd\u8f66\u8f86\u6545\u969c\u8bca\u65ad\u65b9\u6cd5\u3001\u88c5\u7f6e\u53ca\u8bbe\u5907",
        "applicant": "\u4e0a\u6d77\u6c7d\u8f66\u96c6\u56e2\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u57fa\u4e8e\u5927\u6a21\u578b\u8d4b\u80fd\u7684\u8f66\u8f86\u6545\u969c\u8bca\u65ad\u65b9\u6cd5\uff0c\u5b9e\u73b0\u8f66\u8f86\u6545\u969c\u7cbe\u51c6\u8bca\u65ad\u3002",
        "innovation": "\u5f15\u5165\u5927\u8bed\u8a00\u6a21\u578b\u8fdb\u884c\u6545\u969c\u8bed\u4e49\u89e3\u6790\u4e0e\u63a8\u7406\uff0c\u63d0\u5347\u8bca\u65ad\u667a\u80fd\u5316\u6c34\u5e73\u3002",
        "url": "https://patents.google.com/patent/CN122411361A",
    },
    {
        "num": 10, "tier": "T3", "date": "2026-07-11",
        "tags": ["\u7535\u6c60\u5b89\u5168\u8bca\u65ad", "\u81ea\u653e\u7535", "\u4e2d\u56fd\u6c7d\u7814"],
        "title": "\u4e00\u79cd\u57fa\u4e8e\u529b\u5b66\u591a\u7279\u5f81\u5b66\u4e60\u7684\u52a8\u529b\u7535\u6c60\u81ea\u653e\u7535\u5f02\u5e38\u8bc6\u522b\u65b9\u6cd5",
        "applicant": "\u4e2d\u56fd\u6c7d\u8f66\u5de5\u7a0b\u7814\u7a76\u9662\u80a1\u4efd\u6709\u9650\u516c\u53f8",
        "abstract": "\u57fa\u4e8e\u529b\u5b66\u591a\u7279\u5f81\u5b66\u4e60\u8bc6\u522b\u52a8\u529b\u7535\u6c60\u81ea\u653e\u7535\u5f02\u5e38\uff0c\u63d0\u5347\u7535\u6c60\u5b89\u5168\u8bca\u65ad\u7cbe\u5ea6\u3002",
        "innovation": "\u5c06\u529b\u5b66\u7279\u5f81\u4e0e\u673a\u5668\u5b66\u4e60\u7ed3\u5408\u7528\u4e8e\u81ea\u653e\u7535\u5f02\u5e38\u8bc6\u522b\uff0c\u5f00\u8f9f\u7535\u6c60\u8bca\u65ad\u65b0\u7ef4\u5ea6\u3002",
        "url": "https://patents.google.com/patent/CN122365011A",
    },
]

# --- Standards (10) ---
STANDARDS = [
    {
        "num": 1, "tier": "T1", "date": "2026-07-18",
        "tags": ["\u52a8\u529b\u7535\u6c60", "\u5f3a\u5236\u6027\u56fd\u6807", "\u70ed\u6269\u6563"],
        "title": "GB 38031-2025\u300a\u7535\u52a8\u6c7d\u8f66\u7528\u52a8\u529b\u84c4\u7535\u6c60\u5b89\u5168\u8981\u6c42\u300b",
        "purpose": "\u63d0\u5347\u7535\u52a8\u6c7d\u8f66\u52a8\u529b\u84c4\u7535\u6c60\u5b89\u5168\u6c34\u5e73\uff0c\u89c4\u8303\u5355\u4f53\u53ca\u7535\u6c60\u5305\u5b89\u5168\u6d4b\u8bd5\u8981\u6c42\uff0c\u964d\u4f4e\u70ed\u5931\u63a7\u4e8b\u6545\u98ce\u9669\u3002",
        "core_content": "\u65b0\u589e\u5feb\u5145\u5faa\u73af\u540e\u5b89\u5168\u6d4b\u8bd5\uff0c\u4fee\u8ba2\u70ed\u6269\u6563\u6d4b\u8bd5\uff0c\u660e\u786e\u5f85\u6d4b\u7535\u6c60\u6e29\u5ea6\u53caSOC\u8981\u6c42\uff0c\u5f3a\u5316\u5bb9\u91cf\u4fdd\u6301\u7387\u9608\u503c\u3002",
        "implementation": "\u65b0\u7533\u62a5\u8f66\u578b\u5fc5\u987b\u901a\u8fc7\u65b0\u6807\u68c0\u6d4b\uff0c\u5426\u5219\u65e0\u6cd5\u83b7\u5de5\u4fe1\u90e8\u4ea7\u54c1\u516c\u544a\uff0c\u5f3a\u5236\u6267\u884c\uff0c\u8001\u8f66\u578b\u540c\u6b65\u7eb3\u5165\u76d1\u7ba1\u3002",
        "url": "https://auto.sina.cn/2026-07-18/detail-iniiemqp8337482.d.html",
    },
    {
        "num": 2, "tier": "T1", "date": "2026-07-15",
        "tags": ["\u7535\u52a8\u6c7d\u8f66", "\u6574\u8f66\u5b89\u5168", "\u5f3a\u5236\u6027\u56fd\u6807"],
        "title": "GB 18384-2025\u300a\u7535\u52a8\u6c7d\u8f66\u5b89\u5168\u8981\u6c42\u300b",
        "purpose": "\u89c4\u8303\u7535\u52a8\u6c7d\u8f66\u6574\u8f66\u7535\u6c14\u5b89\u5168\u8981\u6c42\uff0c\u4e0e\u52a8\u529b\u7535\u6c60\u65b0\u6807\u534f\u540c\u4fdd\u969c\u8f66\u8f86\u5b89\u5168\u3002",
        "core_content": "\u8986\u76d6\u6574\u8f66\u7535\u6c14\u5b89\u5168\u3001\u529f\u80fd\u5b89\u5168\u53ca\u7535\u6c60\u7cfb\u7edf\u5b89\u5168\u534f\u540c\u8981\u6c42\u3002",
        "implementation": "\u4e0eGB 38031-2025\u540c\u6b65\u751f\u6548\uff0c\u6240\u6709\u65b0\u7533\u62a5\u8f66\u578b\u987b\u540c\u6b65\u6ee1\u8db3\u4e24\u9879\u5f3a\u5236\u56fd\u6807\u3002",
        "url": "https://www.163.com/dy/article/L22OCP5U05119VAC.html",
    },
    {
        "num": 3, "tier": "T2", "date": "2026-07-15",
        "tags": ["\u50a8\u80fd", "\u5e76\u7f51\u5b89\u5168", "\u56fd\u9645\u6807\u51c6\u63a5\u8f68"],
        "title": "GB/T 46957-2025\u300a\u7535\u529b\u50a8\u80fd\u7cfb\u7edf \u5e76\u7f51\u50a8\u80fd\u7cfb\u7edf\u5b89\u5168\u901a\u7528\u89c4\u8303\u300b",
        "purpose": "\u4e3a\u5e76\u7f51\u50a8\u80fd\u7cfb\u7edf\u5efa\u7acb\u5168\u751f\u547d\u5468\u671f\u5b89\u5168\u7ba1\u7406\u6846\u67b6\uff0c\u7edf\u4e00\u4e0d\u540c\u6280\u672f\u8def\u7ebf\u98ce\u9669\u8bc6\u522b\u4e0e\u8bc4\u4f30\u65b9\u6cd5\u3002",
        "core_content": "\u7b49\u540c\u91c7\u7528IEC 62933-5-1:2024\uff0c\u8986\u76d6\u5371\u9669\u6e90\u8fa8\u8bc6\u3001\u98ce\u9669\u8bc4\u4f30\u3001\u98ce\u9669\u5e94\u5bf9\u3001\u7cfb\u7edf\u6d4b\u8bd5\u7b49\u5168\u94fe\u6761\u5b89\u5168\u7ba1\u7406\u8981\u6c42\u3002",
        "implementation": "\u78f7\u9178\u94c1\u9502\u3001\u6db2\u6d41\u3001\u94a0\u79bb\u5b50\u3001\u538b\u7f29\u7a7a\u6c14\u7b49\u6280\u672f\u8def\u7ebf\u5747\u987b\u9075\u5faa\u540c\u4e00\u5957\u98ce\u9669\u903b\u8f91\u3002",
        "url": "https://www.163.com/dy/article/L22OCP5U05119VAC.html",
    },
    {
        "num": 4, "tier": "T1", "date": "2026-07-14",
        "tags": ["\u79fb\u52a8\u7535\u6e90", "\u5145\u7535\u5b9d", "\u5f3a\u5236\u6027\u56fd\u6807"],
        "title": "GB 47372-2026\u300a\u79fb\u52a8\u7535\u6e90\u5b89\u5168\u6280\u672f\u89c4\u8303\u300b",
        "purpose": "\u63d0\u5347\u79fb\u52a8\u7535\u6e90\u5728\u9ad8\u6e29\u3001\u8fc7\u5145\u3001\u6324\u538b\u7b49\u6ee5\u7528\u573a\u666f\u4e0b\u7684\u5b89\u5168\u9632\u62a4\u80fd\u529b\u3002",
        "core_content": "\u65b0\u589e\u5faa\u73af\u8001\u5316\u540e\u6790\u9502\u68c0\u6d4b\uff0c\u7981\u6b62\u68af\u6b21\u5229\u7528\u7535\u6c60\uff0c\u660e\u786e\u4e5d\u9879\u6807\u8bc6\u4fe1\u606f\u8981\u6c42\u3002",
        "implementation": "\u8bbe12\u4e2a\u6708\u8fc7\u6e21\u671f\uff0c\u8986\u76d6\u5145\u7535\u5b9d\u4e0e\u6237\u5916\u50a8\u80fd\u7535\u6e90\uff0c\u8fc7\u6e21\u671f\u5185\u4f01\u4e1a\u52a0\u901f\u5408\u89c4\u3002",
        "url": "https://blog.csdn.net/Microtest_CS/article/details/160221464",
    },
    {
        "num": 5, "tier": "T2", "date": "2026-07-13",
        "tags": ["\u9502\u79bb\u5b50\u7535\u6c60", "\u8d28\u91cf\u7ba1\u7406", "\u751f\u4ea7\u7ba1\u63a7"],
        "title": "GB/T 47292.4-2026\u300a\u9502\u79bb\u5b50\u7535\u6c60\u751f\u4ea7\u8d28\u91cf\u7ba1\u7406 \u7b2c4\u90e8\u5206\uff1a\u7535\u6c60\u7ec4\u8fc7\u7a0b\u7ba1\u63a7\u4e0e\u6210\u54c1\u6d4b\u8bd5\u300b",
        "purpose": "\u89c4\u8303\u9502\u79bb\u5b50\u7535\u6c60\u7ec4\u751f\u4ea7\u8fc7\u7a0b\u8d28\u91cf\u7ba1\u63a7\u4e0e\u6210\u54c1\u6d4b\u8bd5\uff0c\u63d0\u5347\u4ea7\u54c1\u4e00\u81f4\u6027\u3002",
        "core_content": "\u8986\u76d6\u52a8\u529b\u578b\u3001\u50a8\u80fd\u578b\u3001\u6d88\u8d39\u578b\u7535\u6c60\u7ec4\uff0c\u89c4\u5b9a\u5173\u952e\u5de5\u5e8f\u5408\u683c\u7387\u53ca\u8bbe\u5907\u7efc\u5408\u6548\u7387\u5206\u7ea7\u3002",
        "implementation": "\u4f01\u4e1a\u987b\u6309\u6807\u51c6\u5efa\u7acb\u8d28\u91cf\u7ba1\u7406\u4f53\u7cfb\uff0c\u6700\u4f4e\u9700\u6ee1\u8db3C\u7ea7\u8d28\u91cf\u6307\u6807\u8981\u6c42\u3002",
        "url": "https://news.sohu.com/a/977490805_120588350",
    },
    {
        "num": 6, "tier": "T1", "date": "2026-07-17",
        "tags": ["\u7535\u529b\u5b89\u5168", "\u50a8\u80fd\u4f5c\u4e1a", "\u5f3a\u5236\u6027\u6807\u51c6\u4fee\u8ba2"],
        "title": "\u56fd\u5bb6\u80fd\u6e90\u5c40\u7535\u529b\u5b89\u5168\u5de5\u4f5c\u89c4\u7a0b\u4fee\u8ba2\u5f81\u6c42\u610f\u89c1\uff08GB 26164.1-2010\u3001GB 26861-2011\uff09",
        "purpose": "\u4fee\u8ba2\u7535\u529b\u5b89\u5168\u5de5\u4f5c\u89c4\u7a0b\uff0c\u9002\u5e94\u65b0\u80fd\u6e90\u4e0e\u50a8\u80fd\u8bbe\u65bd\u63a5\u5165\u540e\u7684\u5b89\u5168\u4f5c\u4e1a\u9700\u6c42\uff0c\u4fdd\u969c\u4eba\u8eab\u4e0e\u8bbe\u5907\u5b89\u5168\u3002",
        "core_content": "\u6d89\u53ca\u70ed\u529b\u4e0e\u673a\u68b0\u90e8\u5206\u3001\u7535\u529b\u5b89\u5168\u5de5\u4f5c\u89c4\u7a0b\uff0c\u5f3a\u5316\u50a8\u80fd\u7535\u7ad9\u5b89\u5168\u4f5c\u4e1a\u89c4\u8303\uff0c\u8986\u76d6\u65b0\u578b\u7535\u529b\u7cfb\u7edf\u5168\u573a\u666f\u3002",
        "implementation": "\u5904\u4e8e\u5f3a\u5236\u6027\u6807\u51c6\u5236\u4fee\u8ba2\u8ba1\u5212\u516c\u5f00\u5f81\u6c42\u610f\u89c1\u9636\u6bb5\uff0c\u540e\u7eed\u5c06\u5f62\u6210\u65b0\u7248\u5f3a\u5236\u56fd\u6807\u3002",
        "url": "https://www.nea.gov.cn/sjzz/aqs/",
    },
    {
        "num": 7, "tier": "T2", "date": "2026-07-12",
        "tags": ["\u50a8\u80fd\u7535\u7ad9", "\u8bbe\u8ba1\u89c4\u8303", "\u56fd\u5bb6\u6807\u51c6"],
        "title": "GB 51048-2025\u300a\u7535\u5316\u5b66\u50a8\u80fd\u7535\u7ad9\u8bbe\u8ba1\u6807\u51c6\u300b",
        "purpose": "\u65f6\u969410\u5e74\u4fee\u8ba2\u50a8\u80fd\u7535\u7ad9\u8bbe\u8ba1\u89c4\u8303\uff0c\u9002\u5e94\u65b0\u578b\u7535\u529b\u7cfb\u7edf\u50a8\u80fd\u5efa\u8bbe\u9700\u6c42\uff0c\u63d0\u5347\u7535\u7ad9\u5b89\u5168\u4e0e\u7ecf\u6d4e\u6027\u3002",
        "core_content": "\u5141\u8bb8\u50a8\u80fd\u7535\u6c60\u7c07\u4e24\u5c42\u5e03\u7f6e\uff0c\u4f18\u5316\u7535\u7ad9\u5e03\u5c40\u4e0e\u6d88\u9632\u5b89\u5168\u8bbe\u8ba1\u8981\u6c42\uff0c\u63d0\u9ad8\u5730\u9762\u5229\u7528\u7387\u3002",
        "implementation": "2026\u5e744\u67081\u65e5\u8d77\u5b9e\u65bd\uff0c\u539f2014\u7248\u540c\u65f6\u5e9f\u6b62\uff0c\u65b0\u5efa\u50a8\u80fd\u7535\u7ad9\u987b\u6309\u65b0\u6807\u8bbe\u8ba1\u6267\u884c\u3002",
        "url": "https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=51048",
    },
    {
        "num": 8, "tier": "T1", "date": "2026-07-11",
        "tags": ["\u7535\u52a8\u81ea\u884c\u8f66", "\u9502\u7535\u6c60", "\u5f3a\u5236\u6027\u56fd\u6807"],
        "title": "GB 43854-2024\u300a\u7535\u52a8\u81ea\u884c\u8f66\u7528\u9502\u79bb\u5b50\u84c4\u7535\u6c60\u5b89\u5168\u6280\u672f\u89c4\u8303\u300b",
        "purpose": "\u89c4\u8303\u7535\u52a8\u81ea\u884c\u8f66\u7528\u9502\u79bb\u5b50\u84c4\u7535\u6c60\u5b89\u5168\uff0c\u964d\u4f4e\u7535\u52a8\u81ea\u884c\u8f66\u706b\u707e\u98ce\u9669\uff0c\u4fdd\u969c\u4eba\u6c11\u7fa4\u4f17\u751f\u547d\u8d22\u4ea7\u5b89\u5168\u3002",
        "core_content": "\u89c4\u5b9a\u5355\u4f53\u7535\u6c60\u4e0e\u7535\u6c60\u7ec4\u5b89\u5168\u6d4b\u8bd5\u9879\u76ee\uff0c\u5305\u62ec\u8fc7\u5145\u3001\u77ed\u8def\u3001\u70ed\u6ee5\u7528\u7b49\u591a\u9879\u5f3a\u5236\u6027\u8bd5\u9a8c\u8981\u6c42\u3002",
        "implementation": "\u5df2\u5f3a\u5236\u5b9e\u65bd\uff0c\u5e02\u573a\u76d1\u7ba1\u6301\u7eed\u52a0\u5f3a\uff0c\u4e0e\u52a8\u529b\u7535\u6c60\u65b0\u6807\u5f62\u6210\u4e24\u8f6e/\u56db\u8f6e\u5168\u8986\u76d6\u7684\u5b89\u5168\u6807\u51c6\u4f53\u7cfb\u3002",
        "url": "https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=43854",
    },
    {
        "num": 9, "tier": "T3", "date": "2026-07-11",
        "tags": ["\u94a0\u79bb\u5b50\u7535\u6c60", "\u50a8\u80fd", "\u56e2\u4f53\u6807\u51c6"],
        "title": "T/CIAPS 0052-2026\u300a\u50a8\u80fd\u7528\u94a0\u79bb\u5b50\u7535\u6c60\u6280\u672f\u8981\u6c42\u300b",
        "purpose": "\u89c4\u5b9a\u50a8\u80fd\u7528\u94a0\u79bb\u5b50\u7535\u6c60\u53ca\u6a21\u5757\u3001\u7535\u6c60\u7c07\u6280\u672f\u8981\u6c42\uff0c\u652f\u6491\u94a0\u7535\u50a8\u80fd\u4ea7\u4e1a\u5316\u8fdb\u7a0b\uff0c\u7edf\u4e00\u6280\u672f\u6307\u6807\u3002",
        "core_content": "\u8986\u76d6\u94a0\u79bb\u5b50\u7535\u6c60\u672f\u8bed\u5b9a\u4e49\u3001\u7535\u6027\u80fd\u3001\u5b89\u5168\u6027\u80fd\u53ca\u6d4b\u8bd5\u65b9\u6cd5\uff0c\u89c4\u8303\u4ea7\u54c1\u8d28\u91cf\u7ba1\u63a7\u3002",
        "implementation": "\u7531\u5316\u5b66\u4e0e\u7269\u7406\u7535\u6e90\u884c\u4e1a\u534f\u4f1a\u53d1\u5e03\uff0c\u94a0\u7535\u50a8\u80fd\u9879\u76ee\u4f9d\u6b64\u6267\u884c\u6280\u672f\u9a8c\u6536\u3002",
        "url": "https://www.escn.com.cn/news/show-2159265.html",
    },
    {
        "num": 10, "tier": "T3", "date": "2026-07-15",
        "tags": ["\u6210\u672c\u6838\u7b97", "\u52a8\u529b\u7535\u6c60", "\u50a8\u80fd\u7535\u6c60"],
        "title": "\u300a\u52a8\u529b\u548c\u50a8\u80fd\u7535\u6c60\u6210\u672c\u6838\u7b97\u6a21\u578b\u901a\u5219\u300b\u56e2\u4f53\u6807\u51c6\u7814\u5236",
        "purpose": "\u5efa\u7acb\u52a8\u529b\u4e0e\u50a8\u80fd\u7535\u6c60\u5355\u4f53\u3001\u6a21\u7ec4\u3001\u7cfb\u7edf\u7684\u6210\u672c\u6838\u7b97\u7edf\u4e00\u6a21\u578b\u4e0e\u8ba1\u7b97\u8981\u6c42\u3002",
        "core_content": "\u89c4\u5b9a\u6210\u672c\u6784\u6210\u3001\u8ba1\u7b97\u65b9\u6cd5\u4e0e\u53e3\u5f84\uff0c\u8986\u76d6\u52a8\u529b\u4e0e\u50a8\u80fd\u4e24\u7c7b\u7535\u6c60\u5168\u94fe\u6761\u3002",
        "implementation": "\u5df2\u5217\u5165\u7814\u5236\u8ba1\u5212\uff0c\u8fdb\u5165\u8d77\u8349\u9636\u6bb5\uff0c\u540e\u7eed\u53d1\u5e03\u4e3a\u56e2\u4f53\u6807\u51c6\u3002",
        "url": "https://www.escn.com.cn/news/show-2262353.html",
    },
]


# ============================================================
# BUILD HTML
# ============================================================

def build_html():
    parts = []

    # Trends section
    parts.append(h2("\u672c\u5468\u8d8b\u52bf\u5c55\u671b", "#4a90d9"))
    for t in TRENDS:
        parts.append(trend_item(t))

    # Papers section
    parts.append(h2("\u4e00\u3001\u5b66\u672f\u8bba\u6587\u8fdb\u5c55", "#4a90d9"))
    for p in PAPERS:
        parts.append(paper_entry(
            p["num"], p["tier"], p["date"], p["journal"],
            p["tags"], p["title"], p["abstract"], p["innovation"], p["url"]
        ))

    # Vendor News section
    parts.append(h2("\u4e8c\u3001\u5382\u5546\u52a8\u6001", "#27ae60"))
    for v in VENDOR_NEWS:
        parts.append(vendor_entry(
            v["num"], v["tier"], v["date"], v["tags"],
            v["title"], v["abstract"], v["url"]
        ))

    # Open Source section
    parts.append(h2("\u4e09\u3001\u5f00\u6e90\u9879\u76ee\u4e0e\u6570\u636e\u96c6", "#4a90d9"))
    for o in OPEN_SOURCE:
        parts.append(opensource_entry(
            o["num"], o["tier"], o["date"], o["tags"],
            o["title"], o["abstract"], o["url"]
        ))

    # Patents section
    parts.append(h2("\u56db\u3001\u4e13\u5229\u6280\u672f", "#e67e22"))
    for p in PATENTS:
        parts.append(patent_entry(
            p["num"], p["tier"], p["date"], p["tags"],
            p["title"], p["applicant"], p["abstract"], p["innovation"], p["url"]
        ))

    # Standards section
    parts.append(h2("\u4e94\u3001\u884c\u4e1a\u6807\u51c6", "#e67e22"))
    for s in STANDARDS:
        parts.append(standard_entry(
            s["num"], s["tier"], s["date"], s["tags"],
            s["title"], s["purpose"], s["core_content"], s["implementation"], s["url"]
        ))

    # Footer
    parts.append(footer())

    return "".join(parts)


# ============================================================
# WECHAT API FUNCTIONS
# ============================================================

def get_access_token():
    """Get WeChat access token"""
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (APPID, APPSECRET)
    r = requests.get(url)
    result = json.loads(r.content.decode('utf-8'))
    if 'access_token' in result:
        print("[OK] Got access token: %s..." % result['access_token'][:20])
        return result['access_token']
    else:
        print("[ERROR] Failed to get access token: %s" % result)
        sys.exit(1)


def upload_cover_image(token, image_path):
    """Upload cover image as permanent material"""
    url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % token
    with open(image_path, 'rb') as f:
        files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
        r = requests.post(url, files=files)
    result = json.loads(r.content.decode('utf-8'))
    if 'media_id' in result:
        print("[OK] Uploaded cover image, media_id: %s" % result['media_id'])
        return result['media_id']
    else:
        print("[ERROR] Failed to upload cover image: %s" % result)
        sys.exit(1)


def push_draft(token, title, content, thumb_media_id, author):
    """Push draft to WeChat draft box"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=%s" % token
    draft_data = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": "BMS\u7b97\u6cd5\u8ffd\u8e2a\u5468\u62a5 | \u5b66\u672f\u8bba\u6587\u00b7\u5382\u5546\u52a8\u6001\u00b7\u5f00\u6e90\u9879\u76ee\u00b7\u4e13\u5229\u6280\u672f\u00b7\u884c\u4e1a\u6807\u51c6",
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    payload = json.dumps(draft_data, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(url, data=payload, headers=headers)
    result = json.loads(r.content.decode('utf-8'))
    if 'media_id' in result:
        print("[OK] Draft pushed successfully, draft media_id: %s" % result['media_id'])
        return result['media_id']
    else:
        print("[ERROR] Failed to push draft: %s" % result)
        sys.exit(1)


def verify_draft(token, draft_media_id):
    """Read back and verify the draft"""
    url = "https://api.weixin.qq.com/cgi-bin/draft/get?access_token=%s" % token
    data = {"media_id": draft_media_id}
    payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    r = requests.post(url, data=payload, headers=headers)
    result = json.loads(r.content.decode('utf-8'))

    if 'news_item' not in result:
        print("[ERROR] Failed to read draft back: %s" % result)
        return False

    article = result['news_item'][0]
    content = article['content']
    title = article['title']

    # Count checks
    h2_count = content.count('<h2')
    url_count = content.count('https://')
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    journal_badges = content.count('arXiv') + content.count('Applied Energy') + content.count('J. Energy Storage')

    print("\n========== VERIFICATION ==========")
    print("Title: %s" % title)
    print("Title contains date: %s" % ("2026-07-18" in title))
    print("H2 count: %d (expected 6)" % h2_count)
    print("URL count: %d (expected >50)" % url_count)
    print("Chinese chars: %d (expected >5000)" % chinese_chars)
    print("Journal badge count: %d (expected 10)" % journal_badges)
    print("==================================\n")

    all_pass = True
    if "2026-07-18" not in title:
        print("[FAIL] Title does not contain date")
        all_pass = False
    if h2_count != 6:
        print("[FAIL] H2 count is %d, expected 6" % h2_count)
        all_pass = False
    if url_count < 50:
        print("[FAIL] URL count is %d, expected >50" % url_count)
        all_pass = False
    if chinese_chars < 5000:
        print("[FAIL] Chinese chars is %d, expected >5000" % chinese_chars)
        all_pass = False
    if journal_badges < 10:
        print("[FAIL] Journal badge count is %d, expected 10" % journal_badges)
        all_pass = False

    if all_pass:
        print("[ALL CHECKS PASSED]")
    return all_pass


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("BMS Weekly Report Generator - 2026-07-18")
    print("=" * 60)

    # Step 1: Build HTML content
    print("\n[Step 1] Building HTML content...")
    content = build_html()
    print("[OK] HTML content built, length: %d chars" % len(content))

    # Save HTML to file for inspection
    html_path = r"c:\Users\tiany\.trae-cn\work\6a5b7a465b16c418624765c1\bms_report_20260718.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("[OK] HTML saved to: %s" % html_path)

    # Step 2: Get access token
    print("\n[Step 2] Getting WeChat access token...")
    token = get_access_token()

    # Step 3: Upload cover image
    print("\n[Step 3] Uploading cover image...")
    thumb_media_id = upload_cover_image(token, COVER_IMAGE_PATH)

    # Step 4: Push draft
    print("\n[Step 4] Pushing draft to WeChat...")
    draft_media_id = push_draft(token, TITLE, content, thumb_media_id, AUTHOR)

    # Step 5: Verify
    print("\n[Step 5] Verifying draft...")
    verify_draft(token, draft_media_id)

    print("\n" + "=" * 60)
    print("DONE! Draft pushed to WeChat Official Account.")
    print("Draft media_id: %s" % draft_media_id)
    print("=" * 60)


if __name__ == "__main__":
    main()
