---
name: image-ocr
displayName: "Image Ocr"
description: "使用 Tesseract OCR 从图像中提取文本。"
version: 1.0.0
tags:
  - design_multimedia
license: "Unknown"
---

# Image OCR

Extract text from images using Tesseract OCR. Supports multiple languages and image formats including PNG, JPEG, TIFF, and BMP.

## Commands

```bash
# Extract text from an image (default: English)
image-ocr "screenshot.png"

# Extract text with a specific language
image-ocr "document.jpg" --lang eng
```

## Install

```bash
sudo dnf install tesseract
```
