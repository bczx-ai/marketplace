---
name: playwright-scraper
displayName: "Playwright Scraper"
description: "使用 Playwright 隐身模式抓取网站，绕过机器人检测，支持动态 JavaScript 内容以及可自定义的视口和 User-Agent。"
version: 1.0.0
tags:
  - data_analysis
license: "Unknown"
---

# Playwright Stealth Scraper

A high-performance MCP skill for OpenClaw that bypasses anti-bot measures using Playwright Extra and Stealth plugin.

## Features
- **Stealth Mode**: Uses `puppeteer-extra-plugin-stealth` to mimic real browser behavior.
- **Dynamic Content**: Full JavaScript execution support for SPA and React-based sites.
- **Flexible Options**: Custom viewport and User-Agent spoofing.

## Tools
### stealth_scrape
Scrapes any URL with advanced bot detection bypass.
- `url`: The target website address.

## Installation
Requires Playwright and Chromium to be installed in the skill directory.