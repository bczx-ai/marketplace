---
name: bbc-news
displayName: "BBC News"
description: "使用 RSS 订阅获取并展示 BBC 新闻的各版块和地区报道。用户询问 BBC 新闻、英国头条、世界新闻或特定版块（科技、商业、政治、科学、健康、娱乐、英国地区、世界地区）时使用。"
version: 1.0.0
tags:
  - knowledge_management
license: "Unknown"
---

# BBC News

Fetch top stories from BBC News across different sections and regions.

## Quick Start

Fetch top stories:
```bash
python3 scripts/bbc_news.py
```

Fetch from specific section:
```bash
python3 scripts/bbc_news.py uk
python3 scripts/bbc_news.py world
python3 scripts/bbc_news.py technology
```

List all available sections:
```bash
python3 scripts/bbc_news.py --list
```

## Available Sections

### Main Sections
- `top` - Top stories (default)
- `uk` - UK news
- `world` - World news
- `business` - Business news
- `politics` - Politics
- `health` - Health news
- `education` - Education
- `science` - Science & Environment
- `technology` - Technology news
- `entertainment` - Entertainment & Arts

### UK Regional
- `england` - England news
- `scotland` - Scotland news
- `wales` - Wales news
- `northern-ireland` - Northern Ireland news

### World Regions
- `africa` - Africa news
- `asia` - Asia news
- `australia` - Australia news
- `europe` - Europe news
- `latin-america` - Latin America news
- `middle-east` - Middle East news
- `us-canada` - US & Canada news

## Options

**Limit number of stories:**
```bash
python3 scripts/bbc_news.py world --limit 5
```

**JSON output:**
```bash
python3 scripts/bbc_news.py technology --json
```

## Examples

Get top 5 UK stories:
```bash
python3 scripts/bbc_news.py uk --limit 5
```

Get Scotland news in JSON:
```bash
python3 scripts/bbc_news.py scotland --json
```

Get latest technology headlines:
```bash
python3 scripts/bbc_news.py technology --limit 3
```

## Dependencies

Requires `feedparser`:
```bash
pip3 install feedparser
```

## Resources

### scripts/bbc_news.py
Python CLI that fetches and displays BBC News stories from RSS feeds. Supports all major BBC sections and regions, with text and JSON output formats.

### references/feeds.md
Complete list of BBC News RSS feed URLs organized by section and region.
