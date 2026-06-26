## BizNext Public API Leads

Endpoint: GET `/api/public/leads`
Production URL: `https://leadapi.biznext.vn/api/public/leads`
Auth: `X-API-KEY` header only; no query-string keys.
Scope: Read-only leads.

### Tested call shape
```text
GET https://leadapi.biznext.vn/api/public/leads
Header: X-API-KEY: <KEY>
Response: 200 JSON array
Example statuses in sample: Hot, Warm, Contract
Useful fields: createdAt, sale, service, revenue, contractDate, expectedContractDate, status, notes
```

### Operational notes
- Production enforces HTTPS; HTTP returns `400 HTTPS_REQUIRED`.
- Invalid or missing key returns `401 INVALID_SECRET`.
- Limit sensitive auth material from chat output; store key externally or in Hermes script.
