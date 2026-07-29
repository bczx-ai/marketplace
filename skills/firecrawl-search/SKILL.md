---
name: firecrawl-search
displayName: "Firecrawl Search"
description: "通过 Firecrawl API 进行网页搜索与抓取。适用于搜索网络、抓取网站（包括重度JS页面）、爬取全站或从网页提取结构化数据。需要配置 FIRECRAWL_API_KEY 环境变量。"
version: 1.0.0
tags:
  - data_analysis
license: "Unknown"
---

# Firecrawl

Web search and scraping via Firecrawl API.

## Prerequisites

Set `FIRECRAWL_API_KEY` in your environment or `.env` file:
```bash
export FIRECRAWL_API_KEY=fc-xxxxxxxxxx
```

## Quick Start

### Search the web
```bash
firecrawl_search "your search query" --limit 10
```

### Scrape a single page
```bash
firecrawl_scrape "https://example.com"
```

### Crawl an entire site
```bash
firecrawl_crawl "https://example.com" --max-pages 50
```

## API Reference

See [references/api.md](references/api.md) for detailed API documentation and advanced options.

## Scripts

- `scripts/search.py` - Search the web with Firecrawl
- `scripts/scrape.py` - Scrape a single URL
- `scripts/crawl.py` - Crawl an entire website
