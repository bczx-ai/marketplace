---
name: report-generator
displayName: "Generate responsive HTML pages suitable for reporting, supporting resizing and screenshot capture."
description: "根据指定模板生成结构化报告 HTML，适用于用户需要从原始内容创建报告、幻灯片或摘要卡片时调用。"
version: 1.0.1
tags:
  - office_productivity
license: "Unknown"
---

# Report Generator Skill
 
 This skill generates a beautifully formatted HTML report based on a clean, minimal business template style (Light & Concise).

## Capabilities

1. **Refine Content**: Structures raw text into a 4-quadrant format (Goal, Q1-Q4 details, Summary).
2. **Generate HTML**: Creates a responsive HTML file.
3. **Screenshot**: (Instruction) Guides the agent to convert the HTML to an image using the browser tool.

## Usage

### 1. Prepare Data

You need to extract the following information from the user's input:

- **title**: Report Title
- **goal**: One-sentence goal (Top section)
- **q1** to **q4**: Four main sections, each containing:
  - `title`: Short title (e.g., "稳交付")
  - `subtitle`: Explanatory subtitle
  - `slogan`: Catchy slogan
  - `items`: List of bullet points (Array of strings)
- **summary**: Array of 4 keywords for the bottom summary

### 2. Run Generation Script

Execute the python script with the JSON data:

```bash
python3 scripts/generate.py --output "workspace/reports" --data '{"title": "...", ...}'
```

### 3. Convert to Image (Agent Action)

After the script returns the `html_path`, use the **browser** tool to screenshot it:

1. Open the file: `file://<html_path>`
2. Take a screenshot of the full page.

## Example Data Structure

```json
{
  "title": "2024 Q3 述职报告",
  "goal": "构建可规模化的非平台件能力体系",
  "q1": {
    "title": "稳交付",
    "subtitle": "解决扛量问题",
    "slogan": "保交付，争第一",
    "items": ["保障核心需求上线", "降低事故概率"]
  },
  "q2": { ... },
  "q3": { ... },
  "q4": { ... },
  "summary": ["稳定性", "增长", "效率", "反馈"]
}
```
