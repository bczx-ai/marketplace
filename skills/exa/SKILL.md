---
name: exa
displayName: "Exa"
description: "利用 Exa AI API 实现神经网页搜索与代码上下文检索，需要 EXA_API_KEY，用于查找文档、代码示例、研究论文或公司信息。"
version: 0.0.2
tags:
  - development_programming
license: "Unknown"
---

# Exa - Neural Web Search

Direct API access to Exa's neural search engine.

## Setup

**1. Get your API Key:**
Get a key from [Exa Dashboard](https://dashboard.exa.ai/api-keys).

**2. Set it in your environment:**
```bash
export EXA_API_KEY="your-key-here"
```

## Usage

### Web Search
```bash
bash scripts/search.sh "query" [num_results] [type]
```
*   `type`: auto (default), neural, fast, deep
*   `category`: company, research-paper, news, github, tweet, personal-site, pdf

### Code Context
Finds relevant code snippets and documentation.
```bash
bash scripts/code.sh "query" [num_results]
```

### Get Content
Extract full text from URLs.
```bash
bash scripts/content.sh "url1" "url2"
```
