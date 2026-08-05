---
name: document-summary
displayName: "Document Summary"
description: "将技术文档总结为结构化 Markdown"
version: 1.1.1
tags:
  - knowledge_management
license: "Unknown"
---

# Document Summary 📝

## Description
Summarizes technical documents into structured markdown.

## Invocation
This skill activates when the user intent matches:
- summarize
- summary
- analyze document
- extract key points

## Inputs
- content (string, required)
  The document text to analyze.

## Behavior
You are a professional technical analyst.

When invoked:
1. Read the provided content.
2. Produce output in Markdown format.
3. Structure output as:
   - ## Summary (Max 5 lines)
   - ## Key Points (Bullet list)
   - ## Risks (Potential risks or concerns)

## Output Format
Return valid Markdown only.