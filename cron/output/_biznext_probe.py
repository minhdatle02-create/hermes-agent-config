import os, requests
from datetime import datetime, timedelta, timezone

API_URL = "https://leadapi.biznext.vn/api/public/leads"
API_KEY = os.environ.get("BIZNEXT_API_KEY", "").strip()
if not API_KEY:
    print("ERROR: missing BIZNEXT_API_KEY")
    raise SystemExit(1)

yesterday_vn = datetime.now(timezone(timedelta(hours=7))).date() - timedelta(days=1)
yesterday_str = yesterday_vn.isoformat()
print("YESTERDAY (VN):", yesterday_str)

headers = {"X-API-KEY": API_KEY}
r = requests.get(API_URL, headers=headers, timeout=30)
print("STATUS:", r.status_code)
text = r.text
print(text[:400])
