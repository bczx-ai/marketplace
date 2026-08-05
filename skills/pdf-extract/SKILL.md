---
name: pdf-extract
displayName: Pdf Extract
description: 从PDF文件中提取文本供大模型处理
version: 1.0.0
tags:
  - office_productivity
license: Unknown
---

# PDF Extract

Extract text from PDF files for LLM processing. Uses `pdftotext` from the poppler-utils package to convert PDF documents into plain text.

## Commands

```bash
# Extract all text from a PDF
pdf-extract "document.pdf"

# Extract text from specific pages
pdf-extract "document.pdf" --pages 1-5
```

## Install

```bash
sudo dnf install poppler-utils
```
