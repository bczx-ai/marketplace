---
name: nano-pdf
displayName: Nano Pdf
description: 使用nano-pdf CLI通过自然语言指令编辑PDF
version: 1.0.0
tags:
  - office_productivity
license: Unknown
---

# nano-pdf

Use `nano-pdf` to apply edits to a specific page in a PDF using a natural-language instruction.

## Quick start

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
```

Notes:
- Page numbers are 0-based or 1-based depending on the tool’s version/config; if the result looks off by one, retry with the other.
- Always sanity-check the output PDF before sending it out.
