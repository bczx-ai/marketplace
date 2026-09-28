---
name: invoice
zh_name: "发票账单页面"
zh_description: "可打印的发票页面，含收付双方信息、明细表、税额拆分、合计与付款说明，适合发票、账单与结算单"
description: |
  A printable invoice page — sender + recipient block, line items table,
  tax breakdown, totals, and payment instructions. Use when the brief
  mentions "invoice", "bill", "billing statement", or "发票".
triggers:
  - "invoice"
  - "bill"
  - "billing statement"
  - "发票"
  - "账单"
od:
  mode: prototype
  platform: desktop
  scenario: finance
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
    sections: [color, typography, layout, components]
  example_prompt: "Create an invoice from a freelance design studio billing a client for a brand identity project — three line items, 10% retainer, 9% sales tax."
  example_prompt_i18n:
    zh-CN: "为一家自由设计工作室开一张发票，向客户收取品牌识别项目费用——三行明细、10% 预付款、9% 销售税。"
---

# Invoice Skill

Produce a single-page printable invoice.

## Workflow

1. Read DESIGN.md.
2. Layout:
   - Top band: studio brand on the left, "INVOICE" + number + date + due date on the right.
   - Two columns: From (sender) / Bill to (recipient) with addresses.
   - Project ref + payment-terms strip.
   - Line items table: description / qty / unit / amount.
   - Right-aligned totals block: subtotal, retainer, tax, total due.
   - Payment instructions (bank, wire, ACH).
   - Thank-you note + signature line.
3. Print stylesheet @media print to remove backgrounds.

## Output contract

```
<artifact identifier="invoice-name" type="text/html" title="Invoice">
<!doctype html>...</artifact>
```
