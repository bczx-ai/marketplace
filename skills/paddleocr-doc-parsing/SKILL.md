---
name: paddleocr-doc-parsing
displayName: "PaddleOCR Document Parsing"
description: "使用此技能从 PDF 和文档图像中提取结构化的 Markdown/JSON，表格单元格级精确，公式转为 LaTeX，提取图像、印章、图表等。"
version: 3.0.0
tags:
  - office_productivity
license: "Apache-2.0"
---

# PaddleOCR Document Parsing

## When to Use This Skill

**Use this skill for**:

- Documents with tables (invoices, financial reports, spreadsheets)
- Documents with mathematical formulas (academic papers, scientific documents)
- Documents with charts and diagrams
- Multi-column layouts (newspapers, magazines, brochures)
- Complex document structures requiring layout analysis

## Usage

### Basic Document Parsing

From URL:

```bash
paddleocr api \
  --model_type doc_parsing \
  --file_url "https://example.com/report.pdf"
```

From local file:

```bash
paddleocr api \
  --model_type doc_parsing \
  --file_path "./document.pdf"
```

### Common Options

```bash
# With specific model
paddleocr api \
  --model_type doc_parsing \
  --model PP-StructureV3 \
  --file_path "./report.pdf"

# Disable preprocessing (faster, for flat/well-oriented images)
paddleocr api \
  --model_type doc_parsing \
  --file_path "./document.pdf" \
  --use_doc_unwarping False \
  --use_doc_orientation_classify False

# With page ranges
paddleocr api \
  --model_type doc_parsing \
  --file_path "./large.pdf" \
  --page_ranges "1-5,10,15-20"

# Save result and resources
paddleocr api \
  --model_type doc_parsing \
  --file_url "https://..." \
  --output result.json \
  --save_resources ./resources

# Prettify markdown output
paddleocr api \
  --model_type doc_parsing \
  --file_path "./document.pdf" \
  --prettify_markdown True
```

### Output Format

```json
{
  "jobId": "job-xxx",
  "pages": [
    {
      "markdownText": "# Title\n\nContent...",
      "markdownImages": {
        "img1": "https://...",
        "img2": "https://..."
      },
      "outputImages": {
        "layout1": "https://..."
      }
    }
  ]
}
```

## Important Notes

**Preprocessing options**: For flat, well-oriented images (screenshots, properly scanned documents), you can disable preprocessing for faster results:

```bash
paddleocr api --model_type doc_parsing --file_path "./document.pdf" --use_doc_unwarping False --use_doc_orientation_classify False
```

Keep preprocessing enabled when:
- The input is a photo of a curved or folded document
- The document has significant perspective distortion
- Orientation is uncertain (rotated 90/180/270 degrees)

**Display complete results**: Always show the full extracted content to users. Do not truncate with "..." unless content exceeds 10,000 characters. When multiple pages are processed, summarize if needed but provide complete results when explicitly requested.

**Handle errors gracefully**: When the CLI returns an error, inform the user of the specific issue rather than silently failing. Common errors:
- Authentication: `PADDLEOCR_ACCESS_TOKEN` invalid or missing
- Quota: API rate limit exceeded
- No content detected: Document may be blank or contain no extractable text

## CLI Reference

Run `paddleocr api --help` for all options.

For full documentation, see: [PaddleOCR Official Documentation](https://www.paddleocr.ai/latest/en/version3.x/inference_deployment/serving/paddleocr_official_api/cli.html)
