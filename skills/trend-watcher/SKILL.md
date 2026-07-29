---
name: trend-watcher
displayName: "Trend Watcher"
description: "监控 GitHub Trending 和技术社区，追踪并分析 CLI、AI/ML、自动化及开发者领域的新兴工具。"
version: 1.0.1
tags:
  - data_analysis
license: "Unknown"
---

# Trend Watcher Tool

Monitors GitHub Trending and tech communities for emerging tools and technologies.

## Features

- **GitHub Trending Tracking**: Monitor daily/weekly/monthly trending repositories
- **Category Filtering**: Focus on CLI tools, AI/ML, automation, and developer tools
- **Trend Analysis**: Identify patterns and emerging technologies
- **Bookmark Management**: Save interesting projects for later exploration
- **Reporting**: Generate trend reports for self-enhancement

## Usage

```bash
# Check today's trending repositories
openclaw run trend-watcher

# Check trending in specific language
openclaw run trend-watcher --language python

# Check weekly trends
openclaw run trend-watcher --period weekly

# Generate detailed report
openclaw run trend-watcher --report full

# Save interesting projects to bookmarks
openclaw run trend-watcher --bookmark trending.txt

# Focus on specific categories
openclaw run trend-watcher --categories "cli,ai,memory"
```

## Options

- `--language, -l`: Programming language (python, javascript, typescript, go, etc.)
- `--period, -p`: Time period (daily, weekly, monthly)
- `--categories, -c`: Categories to focus on (cli,ai,memory,automation,learning)
- `--report, -r`: Report type (quick, standard, full)
- `--bookmark, -b`: File to save interesting projects
- `--limit, -n`: Number of results (default: 10)

## Categories Monitored

- **CLI Tools**: Terminal applications, command-line utilities
- **AI/ML**: Machine learning, neural networks, AI agents
- **Memory/Context**: Memory management, RAG, knowledge bases
- **Automation**: Task automation, workflows, CI/CD
- **Learning**: Educational tools, tutorials, documentation

## Integration

This tool integrates with:
- GitHub Trending API
- Feishu documentation for reports
- Bookmark system for project tracking
- Daily memory files for trend logging

## Author

OpenClaw Agent - Self Enhancement Tool Builder
