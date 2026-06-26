import urllib.request
import json
from datetime import datetime, date
import os
import ssl

API_URL = os.environ.get("BIZNEXT_API_URL", "https://leadapi.biznext.vn/api/public/leads")
API_KEY = os.environ.get("BIZNEXT_API_KEY", "ffVdNG9cc5H9LoSJvrG1BACJVlpEuTw8")

def fetch_leads():
    headers = {
        "X-API-KEY": API_KEY,
        "Accept": "application/json"
    }
    req = urllib.request.Request(API_URL, headers=headers, method="GET")
    
    ctx = None
    if API_URL.startswith("https"):
        ctx = ssl.create_default_context()
        
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)
    except Exception as e:
        print(f"Lỗi truy cập CRM API: {e}")
        return []

def parse_date(value):
    if not value:
        return None
    value = str(value).strip()
    if not value:
        return None
    try:
        return datetime.strptime(value[:10], "%Y-%m-%d").date()
    except Exception:
        return None

def fmt_number(value):
    try:
        return float(value)
    except Exception:
        return 0.0

def format_currency(value):
    return f"{fmt_number(value):,.0f}".replace(",", ".")

def main():
    print(f"Đang đồng bộ dữ liệu từ CRM ({datetime.today().strftime('%d/%m/%Y %H:%M:%S')})...\n", flush=True)
    leads = fetch_leads()
    if not leads:
        print("Không thể lấy dữ liệu hoặc không có leads nào trên hệ thống.")
        return

    today = date.today()
    leads_today = []
    contracts_today = []

    for item in leads:
        created_at = parse_date(item.get("createdAt"))
        contract_date = parse_date(item.get("contractDate"))
        status = (item.get("status") or "").strip().lower()

        # Check if created today
        if created_at == today:
            leads_today.append(item)
            
        # Check if contract signed today
        if contract_date == today and status in ("contract", "closed"):
            contracts_today.append(item)

    print(f"📊 BÁO CÁO NHANH BIZNEXT CRM NGÀY {today.strftime('%d/%m/%Y')}\n")
    print(f"Tổng quan hôm nay:")
    print(f"- Số cơ hội mới tạo: {len(leads_today)}")
    print(f"- Hợp đồng đã ký mới: {len(contracts_today)}")
    
    total_revenue_today = sum(fmt_number(x.get("revenue")) for x in contracts_today)
    print(f"- Doanh thu hợp đồng hôm nay: {format_currency(total_revenue_today)} đ\n")

    if leads_today:
        print("---")
        print("💡 CHI TIẾT CƠ HỘI MỚI HÔM NAY:")
        for idx, item in enumerate(leads_today, 1):
            name = item.get("name") or "Không tên"
            sale = item.get("sale") or "Chưa giao"
            status_display = item.get("status") or "Mới"
            service = item.get("service") or "Chưa rõ"
            revenue = fmt_number(item.get("revenue"))
            notes = item.get("notes") or ""
            notes_truncated = f" ({notes[:100]}...)" if len(notes) > 100 else (f" ({notes})" if notes else "")
            
            print(f"{idx}. {name} | Sale: {sale}")
            print(f"   - Trạng thái: {status_display} | Dịch vụ: {service}")
            print(f"   - Doanh thu dự kiến: {format_currency(revenue)} đ")
            if notes_truncated:
                print(f"   - Ghi chú:{notes_truncated}")
        print()

    if contracts_today:
        print("---")
        print("🏆 CHI TIẾT HỢP ĐỒNG ĐÃ KÝ HÔM NAY:")
        for idx, item in enumerate(contracts_today, 1):
            name = item.get("name") or "Không tên"
            sale = item.get("sale") or "Chưa giao"
            service = item.get("service") or "Khac"
            revenue = fmt_number(item.get("revenue"))
            notes = item.get("notes") or ""
            notes_truncated = f" ({notes[:100]}...)" if len(notes) > 100 else (f" ({notes})" if notes else "")

            print(f"{idx}. {name} | Sale: {sale}")
            print(f"   - Dịch vụ: {service} | Doanh thu: {format_currency(revenue)} đ")
            if notes_truncated:
                print(f"   - Ghi chú:{notes_truncated}")
        print()

    if not leads_today and not contracts_today:
        print("Hôm nay chưa phát sinh cơ hội mới hoặc hợp đồng mới trên CRM.")

if __name__ == "__main__":
    main()
