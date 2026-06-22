import requests, json, os
from datetime import datetime, timedelta, timezone
from pathlib import Path

API_URL = "https://leadapi.biznext.vn/api/public/leads"
API_KEY=os.env...Y", "").strip()
if not API_KEY:
    print("ERROR: missing BIZNEXT_API_KEY")
    raise SystemExit(1)

yesterday_vn = datetime.now(timezone(timedelta(hours=7))).date() - timedelta(days=1)
yesterday_str = yesterday_vn.isoformat()
print("YESTERDAY (VN):", yesterday_str)

headers = {"X-API-KEY": API_KEY}
r = requests.get(API_URL, headers=headers, timeout=30)
print("STATUS:", r.status_code)
if r.status_code != 200:
    print(r.text[:1000])
    raise SystemExit(1)
data = r.json()
if not isinstance(data, list):
    print("UNEXPECTED RESPONSE TYPE:", type(data))
    raise SystemExit(1)
print("TOTAL:", len(data))

new_leads, contracts = [], []
for x in data:
    if x.get("createdAt") and str(x["createdAt"]) == yesterday_str:
        new_leads.append(x)
    if x.get("contractDate") and str(x["contractDate"]) == yesterday_str:
        contracts.append(x)

print("New leads yesterday:", len(new_leads))
print("Contracts yesterday:", len(contracts))

out_path = Path(r"C:\Users\DatLM6\AppData\Local\hermes\cron\output\biznext_yesterday.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
payload = {
    "date": yesterday_str,
    "total": len(data),
    "new_leads_count": len(new_leads),
    "contracts_count": len(contracts),
    "new_leads": [
        {k: x.get(k) for k in ("id","name","sale","status","service","source","createdAt","expectedContractDate","revenue","notes")}
        for x in sorted(new_leads, key=lambda x: x.get("id", 0))
    ],
    "contracts": [
        {k: x.get(k) for k in ("id","name","sale","status","service","source","contractDate","expectedContractDate","revenue","notes")}
        for x in sorted(contracts, key=lambda x: x.get("id", 0))
    ],
}
out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved report to:", out_path)
