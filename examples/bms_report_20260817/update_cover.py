# -*- coding: utf-8 -*-
import json
import os
import requests

APPID = "wx6faba10fc6b42653"
APPSECRET = "edf800d13ce266ad5c8d7e15a75ea6eb"
TITLE = "BMS 算法追踪 2026-08-17"
AUTHOR = "算法"
DRAFT_ID = "_ERri4LMAITQElNOx3CKJO--joRhvOxIHpnsaJTc6vTYDyhQlUUrhxxV81m1x2ie"
BASE = os.path.dirname(os.path.abspath(__file__))
headers = {"Content-Type": "application/json; charset=utf-8"}

r = requests.get("https://api.weixin.qq.com/cgi-bin/token",
                 params={"grant_type": "client_credential", "appid": APPID, "secret": APPSECRET},
                 timeout=30)
token = json.loads(r.content.decode("utf-8")).get("access_token")
if not token:
    raise SystemExit("token failed")

with open(os.path.join(BASE, "cover_final.jpg"), "rb") as f:
    up = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
        files={"media": ("cover_final.jpg", f, "image/jpeg")}, timeout=60)
res = json.loads(up.content.decode("utf-8"))
print("upload:", res)
new_thumb = res.get("media_id")
if not new_thumb:
    raise SystemExit("cover upload failed")

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
        "thumb_media_id": new_thumb,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    },
}
payload = json.dumps(update_data, ensure_ascii=False).encode("utf-8")
r = requests.post(f"https://api.weixin.qq.com/cgi-bin/draft/update",
                  params={"access_token": token}, data=payload, headers=headers, timeout=120)
print("draft/update:", json.loads(r.content.decode("utf-8")))

r = requests.post(f"https://api.weixin.qq.com/cgi-bin/draft/get",
                  params={"access_token": token},
                  data=json.dumps({"media_id": DRAFT_ID}).encode("utf-8"), headers=headers, timeout=60)
back = json.loads(r.content.decode("utf-8"))
a = back.get("news_item", [{}])[0]
print(f"thumb now: {a.get('thumb_media_id')}")
print("THUMB UPDATED OK" if a.get("thumb_media_id") == new_thumb else "THUMB MISMATCH")
