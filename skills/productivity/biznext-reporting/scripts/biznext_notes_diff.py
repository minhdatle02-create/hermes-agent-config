from __future__ import annotations

import json
import os
import urllib.request
from datetime import datetime
from typing import Any

API_URL = os.environ.get(
    "BIZNEXT_API_URL",
    "https://leadapi.biznext.vn/api/public/leads",
)

BASE_DIR = os.path.join(
    os.environ.get("USERPROFILE", os.path.expanduser("~")),
    "AppData", "Local", "hermes", "cron", "output",
)
CACHE_PATH = os.path.join(BASE_DIR, "biznext_notes_history.json")


def load_api_key() -> str:
    env_path = os.path.join(
        os.environ.get("USERPROFILE", os.path.expanduser("~")),
        "AppData", "Local", "hermes", ".env",
    )
    if not os.path.exists(env_path):
        return ""
    with open(env_path, "r", errors="ignore") as f:
        for raw in f:
            line = raw.strip()
            prefix = "BIZNEXT_API_KEY="
            if line.startswith(prefix):
                return line[len(prefix):].strip()
    return ""


def fetch_leads(api_key: str) -> list[dict[str, Any]]:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["X-API-KEY"] = api_key
    req = urllib.request.Request(API_URL, headers=headers, method="GET")
    ctx = None
    import ssl
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def load_cache() -> dict[str, dict[str, str]]:
    if not os.path.exists(CACHE_PATH):
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8", errors="ignore") as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(cache: dict[str, dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def main() -> None:
    api_key = load_api_key()
    if not api_key:
        print("Missing BIZNEXT_API_KEY")
        return

    leads = fetch_leads(api_key)
    fetched_at = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    old_cache = load_cache()

    changes: list[dict[str, str]] = []
    new_cache: dict[str, dict[str, str]] = {}

    for lead in leads:
        lead_id = str(lead.get("id") or "").strip()
        if not lead_id:
            continue
        notes = (lead.get("notes") or "").strip()
        entry = {
            "notes": notes,
            "fetchedAt": fetched_at,
            "name": (lead.get("name") or "").strip(),
            "sale": (lead.get("sale") or "").strip(),
            "status": (lead.get("status") or "").strip(),
        }
        new_cache[lead_id] = entry

        old = old_cache.get(lead_id)
        if not old:
            # First time seen this ID in cache — ignore as change to avoid initial noise
            continue

        old_notes = (old.get("notes") or "").strip()
        if old_notes != notes:
            changes.append(
                {
                    "id": lead_id,
                    "name": entry["name"],
                    "sale": entry["sale"],
                    "old": old_notes,
                    "new": notes,
                    "status": entry["status"],
                }
            )

    save_cache(new_cache)

    print(f"Fetched: {len(leads)}")
    print(f"Cache entries: {len(new_cache)}")
    print(f"Notes changed: {len(changes)}")
    for c in changes:
        print("\nID:", c["id"])
        print("Name:", c["name"])
        print("Sale:", c["sale"])
        print("Status:", c["status"])
        print("[Old]:", c["old"])
        print("[New]:", c["new"])


if __name__ == "__main__":
    main()
