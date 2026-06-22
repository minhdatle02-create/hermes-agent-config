---
name: biznext-reporting
description: >
  Build on-demand or scheduled CRM-backed reporting for BizNext by flexible time window.
  Use this for weekly/ad-hoc reports, quick new-opportunity briefings,
  or any lead analysis not tied to calendar month boundaries.
  For fixed monthly reports, use biznext-monthly-report instead.
toolsets:
  - terminal
  - file
  - web
---

# BizNext Reporting

Build and ship reports from the BizNext CRM into a workbook or other format.
This skill is class-level: it covers any BizNext sales/lead reporting need.

## Step 1: Confirm the report contract

Before scripting, confirm with the user:
- output format (default: Excel)
- schedule model (default: run on demand)
- distribution channel (Telegram when chat is configured)
- KPIs to compute from CRM data
- time window: by default use current month unless the user specifies a different week/month
- REQUIRED from BizNext CRM API (`/api/public/leads`) MUST include `source` field in every new opportunity / quick briefing output.
Reason: sales ops needs lead channel attribution for each new opportunity.

## Step 2: Authenticate and probe the CRM

Use the Public API Leads endpoint:
- Production: `https://leadapi.biznext.vn/api/public/leads`
- Auth header: `X-API-KEY`
- Response: JSON array
- Rate limit applies; therefore probe with a small fetch first, not multiple parallel calls.
- Store the key in Hermes config: `hermes config set BIZNEXT_API_KEY <key>`. It is written to `~/.hermes/.env` and
  kept out of chat. Do NOT ask the user to re-send the key in later sessions.
- Windows env caveat: running a script via `python script.py` does not automatically inherit the Hermes-loaded env
  unless the Hermes runtime loads it. If you get `401`, verify the header value is set inside the script before
  relying on `os.environ`.

### New-opportunity definition (anti-batch)
Prefer `contractDate == window_date` with status in `Contract`/`Closed` for new contracts, but ALSO include `source`
field in rows. For “new leads” use `createdAt` carefully (anti-batch).

### Verification
After auth succeeds, record `max id` from the dataset so future “newness” checks can use an ID floor.

## Pitfalls
- NEVER reuse partial output if the CRM call fails. If production returns 400/401/429/500, stop and report the exact status and body, do not synthesize report data.
- Do not synthesize CRM numbers when auth fails. 401 = broken header or expired key; 400/429 = request issue. Stop and surface the exact reason.
- Avoid creating base64/encoded blobs of the workbook in chat; send or return the file path instead.
- Do not guess missing source files. If the user asks for source material that is not found, ask for the exact path.
- Telegram delivery: emit bullet lists with `key: value` lines, not tables. Telegram auto-rewrites pipe tables into row-group bullets, which loses structure.
- REQUIRED: output for new opportunities MUST contain at least columns: ID, Name, Sale, Status, Service, Source, ContractDate, ExpectedContractDate, Revenue, Notes.

## Step 3: Notes change detection
Support check cập nhật ghi chú mới:
- Cache file: `~/AppData/Local/hermes/cron/output/biznext_notes_history.json`
- Trigger by user: “kiểm tra cập nhật ghi chú”, “check notes update”
- Output: list các `id` có `notes` khác với cache cũ, kèm `[Old]` / `[New]`
- Không báo gì nếu không có thay đổi
- Cache is updated on every fetch/session
- On initial run, build cache without notifying; only report changes on subsequent runs

## Step 4: Generate output
Default output locations:
- `~/AppData/Local/hermes/cron/output/BizNext_weekly_<YYYYMMDD>.xlsx`

Default workbook sheets:
1. Summary (Tong_quat)
2. Cơ hội mới (Co_hoi_moi) — MUST include: ID, Ten, Sale, Trang thai, Dich vu, Nguon, Ngay tao, Ngay HD, Ngay du kien HD, Doanh thu (VND), Ghi chu
3. Theo sale (Theo_sale)
4. Theo dich vu (Theo_dich_vu)
5. Trang thai (Trang_thai)
6. Nguồn cơ hội (Nguon_co_hoi) — MUST show source name, volume, and % of dataset
7. Follow list (Follow_list) — MUST include: ID, Ten, Sale, Trang thai, Dich vu, Nguon, Ngay tao, Ngay du kien HD, Ghi chu

## Report template (text briefing for Telegram/Chat)
```
Báo cáo nhanh tuần trước (<DD/MM> – <DD/MM>):

Tổng quan
- Dataset: <TOTAL> leads
- Confirmed contracts trong tuần: <COUNT>
- Doanh thu hợp đồng: <REVENUE>đ
- Follow đang active: <COUNT>

Cơ hội mới (new opportunities)
1. <ID> — <Ten> — <Sale>
   - Trạng thái: <Status>
   - Dịch vụ: <Service>
   - Nguồn: <Source>
   - Ngày HD: <Date>
   - Doanh thu: <Revenue>đ
   - Ghi chú: <Notes>

...

Nguồn cơ hội (dataset toàn bộ)
- <Source>: <Count> (<Percent>%)

Follow list cần đẩy
- <ID>: <Ten> — <Sale> — <Status> — <Service> — <Source> — <Context>

Ghi chú có cập nhật mới
- <ID> (<Tên> — <Sale>):
  [Cũ]: <Old notes>
  [Mới]: <New notes>
```

Rules:
- Keep this exact section structure.
- Prioritize confirmed contracts first, then follow list.
- Revenue in VND with thousand separators.
- Source MUST be present for every opportunity and follow entry.
- If a field is missing, show empty/None, do not synthesize.

## Step 5: Delivery
Preferred delivery is Telegram when `TELEGRAM_HOME_CHANNEL` is configured.
If Telegram is not configured, return the file path and instruct the user to run:
`hermes config set TELEGRAM_HOME_CHANNEL <chat_id>`

## Step 5b: Fixed Monthly Calendar Report

For fixed calendar-month reports, use the standalone `biznext-monthly-report`
skill. It runs a monthly Excel workbook generation script against the same
CRM Public API Leads endpoint.

**Trigger:** monthly report, calendar month rollup, BizNext month summary.

**Output sheets:**
1. `Tong_quan` — total leads, contracts, revenue, pending follow-ups
2. `Lead_theo_sale` — lead count, contracts, follow-ups, revenue per sale
3. `Co_hoi_trang_thai` — opportunity counts by status
4. `Doanh_thu_dich_vu` — revenue and contract counts by service
5. `Follow_list` — filtered follow-up leads

**Script:** `python scripts/report.py` after setting `API_KEY`, `REPORT_YEAR`,
`REPORT_MONTH`, and `API_URL` at the top of the script.

**Dependency:** `openpyxl`.

See standalone `biznext-monthly-report` for full configuration and daily
digest options.

## Session references
See `references/biznext-crm-api.md` for endpoint details and filtering constraints.
See `references/biznext-new-opportunity-rules.md` for anti-batch rules Window deduction and daily report logic.
