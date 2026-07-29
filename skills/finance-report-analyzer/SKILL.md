---
name: finance-report-analyzer
displayName: "Finance Report Analyzer"
description: "分析上传的Excel/PDF文件中的财务数据，生成带有迷你趋势图的交互式报告，支持输出为PDF、DOCX、Markdown等格式。"
version: 1.1.0
tags:
  - data_analysis
license: "Unknown"
---

# Finance Report Analyzer

Generate financial analysis reports from uploaded Excel/PDF files with inline SVG sparkline trend charts and multi-format output.

## Quick Start

```bash
python3 scripts/generate_report.py input.xlsx -o pdf --company "公司名" --ticker "000001.SZ"
```

## Output Formats

`-o` flag controls output. **HTML is always generated** as the base; other formats convert from HTML.

| Flag | Output | Requires |
|------|--------|----------|
| `-o html` | HTML only | (built-in) |
| `-o pdf` | HTML + PDF (default) | wkhtmltopdf or chromium |
| `-o doc` | HTML + DOCX | pandoc |
| `-o md` | HTML + Markdown | pandoc or markdownify |

## Workflow

### Step 1: Acquire Data File

Try in order:

1. **Feishu chat file attachment** — Download via API:
   ```bash
   # Get token
   TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
     -H 'Content-Type: application/json' \
     -d '{"app_id":"APP_ID","app_secret":"APP_SECRET"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
   # Get file_key from message
   curl -s "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}" -H "Authorization: Bearer $TOKEN"
   # Download
   curl -s "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file" \
     -H "Authorization: Bearer $TOKEN" -o /tmp/data.xlsx
   ```
   Get app credentials: read `channels.feishu.appId`/`appSecret` from openclaw.json.

2. **Feishu Doc/Bitable link** — Use feishu_doc/feishu_bitable tools
3. **Local file** — Use directly
4. **Pasted text** — Parse and save as xlsx

### Step 2: Generate Report

```bash
python3 scripts/generate_report.py /tmp/data.xlsx -o pdf \
  --company "百济神州-U" --ticker "688235.SH" --output-dir /tmp/reports
```

### Step 3: Web Search Enhancement (Optional)

Search for industry benchmarks:
```
web_search("{company} 行业对比 市场份额 {year}")
```

### Step 4: Deliver File via Feishu API

The `message` tool may send paths as text. Use direct Feishu API to send real file messages:

```bash
# 1. Upload file to get file_key
UPLOAD=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type=stream' \
  -F "file_name=report.html" \
  -F "file=@/path/to/report.html")
FILE_KEY=$(echo "$UPLOAD" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

# 2. Send file message to chat
curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"CHAT_ID\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## Report Features

- **Sparkline trend charts**: Each metric row has an inline SVG showing the trend (solid=actual, dashed=forecast)
- **Forecast markers**: Predicted values marked with ⟡ symbol and yellow background
- **Color coding**: Green=positive, Red=negative
- **Responsive**: Works on mobile and desktop
- **Print-ready**: CSS print styles included

## Metric Definitions

See [references/metrics.md](references/metrics.md) for financial metric calculations.
