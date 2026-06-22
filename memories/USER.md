Làm việc tại FPT Corporation, phụ trách sản phẩm BizNext, đặc biệt BizNext POS. Muốn xây dựng quy trình báo cáo tuần tự động cho BizNext, tích hợp API CRM BizNext (read-only, endpoint /api/public/leads). Thích giao tiếp bằng tiếng Việt. Có kỹ năng kỹ thuật, quan tâm đến tự động hoá và lưu workflow thành skill.
§
BizNext CRM API key: BIZNEXT_API_KEY đã lưu trong hermes config, endpoint /api/public/leads dùng header X-API-KEY
§
For BizNext opportunity reports, always include lead source (`source` field) in new opportunity lists and quick briefings.
§
Keep BizNext reporting skills strictly separated: biznext-reporting (weekly/ad-hoc flexible windows) vs biznext-monthly-report (fixed calendar-month only). Do not conflate them.
§
User: Lê Đạt, FPT Corporation, quản lý sản phẩm BizNext (đặc biệt BizNext POS). Giao tiếp tiếng Việt, trực diện, không cần disclaimer. Kỹ thuật vừa phải, quan tâm automation và lưu workflow thành skill. Ưu tiên actionable steps, không tóm tắt input.
Đang triển khai: báo cáo tuần BizNext tự động (biznext-reporting skill), đánh giá AI trợ lý pháp luật, social listening automation.
Yêu cầu nghiệp vụ: reports phải có field source; biznext-reporting và biznext-monthly-report phải tách biệt.
Mục tiêu sắp tới: triển khai Hermes lên AWS EC2 để chạy 24/7, không phụ thuộc máy local.
Công cụ quen: n8n, Power BI, React, pptxgenjs, LLM prompts.