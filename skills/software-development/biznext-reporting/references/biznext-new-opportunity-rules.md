# BizNext New-Opportunity & Windows Report Rules

## 1. Anti-batch `createdAt`
_dataset.current.createdAt_ is not reliable as a creation proxy.
Evidence this session:
- 2026-01-14 appears 51 times
- 2025-08-17 appears 40 times
- 2026-03-16 appears 30 times
- 2025-11-18 appears 29 times

## 2. Contract framing
Use `contractDate` with status in `Contract` / `Closed` for accurate "new contracts in Window".

## 3. ID threshold (current snapshot)
Max ID at time of setup:
- `2026-06-04`: 6737
- `2026-06-05`: 6739

Cron should store `last_max_id` on each run and count only records where `id > last_max_id`.

## 4. Windows: 401 from script without live header
If a script run as `python script.py` returns `401` but the same URL succeeds elsewhere, the header was sent as an empty string. Cause:
- Terminal subprocess does not inherit Hermes `.env` variables unless launched by Hermes runtime.
Workaround:
- Load dotfile explicitly in the script, or
- Always pass the value via variable injection at run time.

## 5. Why we still prefer `contractDate` for "new confirmation"
The CRM sync path likely back-dates imports. `createdAt` cannot differentiate organic lead creation from import batches. Business user expectation of "key hoc moi" aligns more with signed contracts_for_window_ than admission_order.
