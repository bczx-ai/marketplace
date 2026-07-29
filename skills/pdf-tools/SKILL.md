---
name: pdf-tools
displayName: "PDF Tools"
description: "查看、提取、编辑和处理 PDF 文件。支持文本提取、文本编辑（叠加和替换）、合并、拆分、旋转页面及获取元数据。适用于阅读内容、添加/编辑文本、重组页面、合并文件或提取信息等 PDF 文档操作。"
version: 0.1.0
tags:
  - office_productivity
license: "Unknown"
---

# PDF Tools

Tools for viewing, extracting, and editing PDF files using Python libraries (pdfplumber and PyPDF2).

## Quick Start

All scripts require dependencies:
```bash
pip3 install pdfplumber PyPDF2
```

## Core Operations

### Extract Text

Extract text from PDF (all pages or specific pages):
```bash
scripts/extract_text.py document.pdf
scripts/extract_text.py document.pdf -p 1 3 5
scripts/extract_text.py document.pdf -o output.txt
```

### Get PDF Info

View metadata and structure:
```bash
scripts/pdf_info.py document.pdf
scripts/pdf_info.py document.pdf -f json
```

### Merge PDFs

Combine multiple PDFs into one:
```bash
scripts/merge_pdfs.py file1.pdf file2.pdf file3.pdf -o merged.pdf
```

### Split PDF

Split into individual pages:
```bash
scripts/split_pdf.py document.pdf -o output_dir/
```

Split by page ranges:
```bash
scripts/split_pdf.py document.pdf -o output_dir/ -m ranges -r "1-3,5-7,10-12"
```

### Rotate Pages

Rotate all pages or specific pages:
```bash
scripts/rotate_pdf.py document.pdf -o rotated.pdf -r 90
scripts/rotate_pdf.py document.pdf -o rotated.pdf -r 180 -p 1 3 5
```

### Edit Text

Add text overlay on a page:
```bash
scripts/edit_text.py document.pdf -o edited.pdf --overlay "New Text" --page 1 --x 100 --y 700
scripts/edit_text.py document.pdf -o edited.pdf --overlay "Watermark" --page 1 --x 200 --y 400 --font-size 20
```

Replace text (limited, works best for simple cases):
```bash
scripts/edit_text.py document.pdf -o edited.pdf --replace "Old Text" "New Text"
```

**Note:** PDF text editing is complex due to the format. The overlay method is more reliable than replacement.

## Workflow Patterns

### Viewing PDF Content

1. Get basic info: `scripts/pdf_info.py file.pdf`
2. Extract text to preview: `scripts/extract_text.py file.pdf -p 1`
3. Extract full text if needed: `scripts/extract_text.py file.pdf -o content.txt`

### Reorganizing PDFs

1. Split into pages: `scripts/split_pdf.py input.pdf -o pages/`
2. Merge selected pages: `scripts/merge_pdfs.py pages/page_1.pdf pages/page_3.pdf -o reordered.pdf`

### Extracting Sections

1. Get page count: `scripts/pdf_info.py document.pdf`
2. Split by ranges: `scripts/split_pdf.py document.pdf -o sections/ -m ranges -r "1-5,10-15"`

## Advanced Usage

For detailed library documentation and advanced patterns, see [references/libraries.md](references/libraries.md).

## Notes

- Page numbers are **1-indexed** in all scripts (page 1 = first page)
- Text extraction works best with text-based PDFs (not scanned images)
- Rotation angles: 90, 180, 270, or -90 (counterclockwise)
- All scripts validate file existence before processing
