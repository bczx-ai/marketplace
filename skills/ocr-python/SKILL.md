---
name: ocr-python
displayName: "OCR with python"
description: "{\"answer\":\"用Python PaddleOCR提取图片和扫描PDF中的中英文文本（含发票、合同）。\"}"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# OCR Text Recognition

This skill uses PaddleOCR for text recognition, supporting both Chinese and English.

## Quick Start

### Basic Usage

Perform OCR recognition directly on image or PDF files:

```python
from paddleocr import PaddleOCR

ocr = PaddleOCR(lang='ch')
result = ocr.predict("file_path.jpg")
```

## Dependency Installation

Install dependencies before first use:

```bash
pip3 install paddlepaddle paddleocr
```

## Output Format

Recognition results return JSON containing:
- `rec_texts`: List of recognized text
- `rec_scores`: Confidence score for each text

## Typical Use Cases

1. **PDF Scans**: Use PyMuPDF to extract images first, then OCR
2. **Image Text Recognition**: Perform OCR directly on images
3. **Multi-page PDFs**: Process page by page

## Scripts

Common scripts are located in the `scripts/` directory.
