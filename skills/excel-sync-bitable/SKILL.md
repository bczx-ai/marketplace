---
name: excel-sync-bitable
displayName: "飞书多维表格-Excel同步"
description: "Excel/CSV与飞书表格（多维表格/电子表格）双向转换工具。支持：1. 导入Excel到多维表格（创建新表或同步到现有表）；2. 从多维表格/电子表格导出数据为CSV或Excel格式。自动识别URL类型，智能推断字段类型。"
version: 2.0.0
tags:
  - office_productivity
license: "Unknown"
---

# Excel ↔ Feishu Base

Use `scripts/excel_sync_bitable.py`. Require an explicit `--apply` before any Base write.

## Preconditions

- Confirm the input file, Base URL, target table and business-key column.
- Run `lark-cli auth status` if the user identity or permission is uncertain.
- Use a Base URL, not a guessed token. The script resolves it with `base +url-resolve`.

## Commands

Preview a keyed sync (no write):

```powershell
python scripts/excel_sync_bitable.py sync --input .\orders.xlsx --url "https://example.feishu.cn/base/..." --key "订单号"
```

Apply the reviewed sync and read back its keys:

```powershell
python scripts/excel_sync_bitable.py sync --input .\orders.xlsx --url "https://example.feishu.cn/base/..." --key "订单号" --apply
```

Handle source columns that do not exist in the target Base:

```powershell
# Show missing fields and their inferred types (default; no write)
python scripts/excel_sync_bitable.py sync --input .\orders.xlsx --url "https://example.feishu.cn/base/..." --key "订单号"

# Intentionally ignore absent columns
python scripts/excel_sync_bitable.py sync --input .\orders.xlsx --url "https://example.feishu.cn/base/..." --key "订单号" --missing-fields skip --apply

# Create absent text/number/datetime/checkbox fields, then import
python scripts/excel_sync_bitable.py sync --input .\orders.xlsx --url "https://example.feishu.cn/base/..." --key "订单号" --missing-fields create --apply
```

Create a Base from a workbook:

```powershell
python scripts/excel_sync_bitable.py create --input .\orders.xlsx --app-name "订单数据" --table-name "订单" --apply
```

Export one Base table:

```powershell
python scripts/excel_sync_bitable.py export --url "https://example.feishu.cn/base/..." --table-name "订单" --output .\orders.xlsx
```

## Safety rules

- `sync` updates only records whose business key matches exactly; it does not delete remote records.
- Stop on blank or duplicate keys in either the source or target table.
- For absent source columns, default to a no-write prompt with inferred types; explicitly choose `--missing-fields skip` or `--missing-fields create --apply`.
- Treat preview counts as approval material. Use `--apply` only after the user has confirmed the target and counts.
- The current implementation supports text, number, date/time and checkbox fields. Handle select, user, attachment, link, formula and lookup fields with a field-specific workflow instead of guessing values.
