---
name: ocr-local
displayName: "OCR - Local (No API Key)"
description: "使用 Tesseract.js OCR 从图像中提取文本（100%本地运行，无需API密钥）。支持中文（简繁体）和英文。"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# OCR - Image Text Recognition (Local)

Extract text from images using Tesseract.js. **100% local run, no API key required.** Supports Chinese and English.

## Quick start

```bash
node {baseDir}/scripts/ocr.js /path/to/image.jpg
node {baseDir}/scripts/ocr.js /path/to/image.png --lang chi_sim
node {baseDir}/scripts/ocr.js /path/to/image.jpg --lang chi_tra+eng
```

## Options

- `--lang <langs>`: Language codes (default: chi_sim+eng)
  - `chi_sim` - Simplified Chinese
  - `chi_tra` - Traditional Chinese  
  - `eng` - English
  - Combine with `+`: `chi_sim+eng`

- `--json`: Output as JSON instead of plain text

## Examples

```bash
# Recognize Chinese screenshot
node {baseDir}/scripts/ocr.js screenshot.png

# Recognize English document
node {baseDir}/scripts/ocr.js document.jpg --lang eng

# Mixed Chinese + English
node {baseDir}/scripts/ocr.js mixed.png --lang chi_sim+eng
```

## Notes

- First run downloads language data (~20MB per language)
- Subsequent runs are cached locally
- Works best with clear, high-contrast images
- For handwritten text, accuracy may vary
