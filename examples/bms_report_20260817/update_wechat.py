# -*- coding: utf-8 -*-
import json
import os
import re
import requests

APPID = "wx6faba10fc6b42653"
APPSECRET = "edf800d13ce266ad5c8d7e15a75ea6eb"
TITLE = "BMS 算法追踪 2026-08-17"
AUTHOR = "算法"
DRAFT_ID = "_ERri4LMAITQElNOx3CKJO--joRhvOxIHpnsaJTc6vTYDyhQlUUrhxxV81m1x2ie"
THUMB_ID = "_ERri4LMAITQElNOx3CKJAaJVyXr1Flo4AAq1QfodsD1g0oVxx1_FIXLU41EkWxG"
BASE = os.path.dirname(os.path.abspath(__file__))
headers = {"Content-Type": "application/json; charset=utf-8"}

r = requests.get("https://api.weixin.qq.com/cgi-bin/token",
                 params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
                 timeout=30)
token = json.loads(r.content.decode("utf-8")).get("access_token")
if not token:
    raise SystemExit("token failed")
print("token ok")

with open(os.path.join(BASE, "report.html"), encoding="utf-8") as f:
    content = f.read()

update_data = {
    "media_id": DRAFT_ID,
    "index": 0,
    "articles": {
        "title": TITLE,
        "author": AUTHOR,
        "digest": "物理信息AI成为电池状态估计主流范式；储能订单潮延续；新型储能标准密集征求意见。信源评级采用 Admiralty/NATO AJP-2.1 标准。",
        "content": content,
        "thumb_media_id": THUMB_ID,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    },
}
payload = json.dumps(update_data, ensure_ascii=False).encode("utf-8")
r = requests.post(f"https://api.weixin.qq.com/cgi-bin/draft/update",
                  params={"access_token": token}, data=payload, headers=headers, timeout=120)
result = json.loads(r.content.decode("utf-8"))
print("draft/update:", result)
if result.get("errcode") not in (0,):
    raise SystemExit("draft update failed")

# read back and verify
r = requests.post(f"https://api.weixin.qq.com/cgi-bin/draft/get",
                  params={"access_token": token},
                  data=json.dumps({"media_id": DRAFT_ID}).encode("utf-8"), headers=headers,
                  timeout=60)
back = json.loads(r.content.decode("utf-8"))
a = back.get("news_item", [{}])[0]
if not a:
    raise SystemExit(f"read back failed: {back}")
c = a["content"]
cjk = sum(1 for ch in c if "\u4e00" <= ch <= "\u9fff")
checks = {
    "title contains date": "2026-08-17" in a["title"],
    "chinese chars > 5000": cjk > 5000,
    "h2 count == 6": c.count("<h2") == 6,
    "url count > 50": c.count("http") > 50,
    "doi count >= 6": c.count("https://doi.org/") >= 6,
    "arxiv count == 4": c.count("https://arxiv.org/abs/") == 4,
    "legend mentions AJP-2.1": "AJP-2.1" in c,
    "legend before papers": c.find("信源分级说明") < c.find("一、学术论文进展"),
    "badge A2 x4": c.count(">A2<") == 4,
    "badge B2 x13": c.count(">B2<") == 13,
    "badge C2 x26": c.count(">C2<") == 26,
    "badge C3 x6": c.count(">C3<") == 6,
    "badge D3 x1": c.count(">D3<") == 1,
    "no legacy T badges": len(re.findall(r">T[1-4]<", c)) == 0,
    "thumb set": bool(a.get("thumb_media_id")),
}
print(f"read back: title={a['title']!r} cjk={cjk}")
for k, v in checks.items():
    print(("PASS " if v else "FAIL ") + k)
if not all(checks.values()):
    raise SystemExit("VERIFICATION FAILED")
print("ALL CHECKS PASSED")
