---
name: doc-converter
displayName: "docx"
description: "使用 markitdown 命令将 .pdf、.docx、.xlsx、.pptx 文档转换为 Markdown。"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# Document Converter

This skill converts a document file into Markdown text.

## Activation

Activate when asked to read a file with one of the following extensions:
- .pdf
- .docx
- .xlsx
- .pptx

## Execution

The skill executes the `markitdown` command on the input file path and outputs the resulting Markdown text.

```bash
markitdown "{file_path}"
```
