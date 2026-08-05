---
name: demo-video
displayName: "Demo Video Creator"
description: "通过自动化浏览器交互与捕获帧来创建产品演示视频。当用户需要录制Web应用的演示、操作指南、产品展示或交互视频时使用。支持通过Playwright CDP屏幕录制实现高质量捕获，并使用FFmpeg进行视频编码。"
version: 1.0.0
tags:
  - design_multimedia
license: "Unknown"
---

# Demo Video Creator

Create polished product demo videos by automating browser interactions.

## Overview

1. **Plan** the demo sequence (pages, interactions, timing)
2. **Record** frames using Playwright CDP screencast
3. **Encode** to video with FFmpeg

## Quick Start

### Prerequisites

- Clawdbot browser running (`browser action=start profile=clawd`)
- App accessible via browser (localhost or remote)
- FFmpeg installed for encoding

### Recording Workflow

1. Start the Clawdbot browser if not running
2. Navigate to the app manually or via `browser action=open`
3. Customize `scripts/record-demo.js` for the target app
4. Run: `node scripts/record-demo.js`
5. Encode: `bash scripts/frames-to-video.sh`

## Planning a Demo

See `references/demo-planning.md` for guidance on:
- Structuring demo sequences
- Timing and pacing
- Interaction patterns
- What makes demos compelling

## Scripts

### `scripts/record-demo.js`

Template Playwright script that:
- Connects to Clawdbot browser via CDP
- Starts screencast capture (JPEG frames)
- Executes demo sequence (navigation, clicks, hovers, typing)
- Saves frames to output directory

**Customize for each demo:**
- `DEMO_SEQUENCES` array - define pages and interactions
- `OUTPUT_DIR` - where to save frames
- `FRAME_SKIP` - skip every Nth frame (lower = more frames)

### `scripts/frames-to-video.sh`

FFmpeg encoding script with presets:
- `mp4` - H.264, good quality/size balance (default)
- `gif` - Animated GIF for embedding
- `webm` - VP9, smaller files

Usage: `./frames-to-video.sh [input_dir] [output_name] [format]`

## Interaction Patterns

```javascript
// Navigation
await page.goto('http://localhost/dashboard');
await page.waitForTimeout(2000);

// Click element
await page.locator('button:has-text("Create")').click();
await page.waitForTimeout(500);

// Hover (show tooltips, hover states)
await page.locator('.card').first().hover();
await page.waitForTimeout(1000);

// Type text
await page.locator('input[placeholder="Search"]').fill('query');
await page.waitForTimeout(500);

// Press key
await page.keyboard.press('Enter');
await page.keyboard.press('Escape');

// Scroll
await page.evaluate(() => window.scrollBy(0, 300));
```

## Tips

- **Timing**: 2s on page load, 0.5-1s between interactions, 1.5s to show results
- **Frame skip**: Use 3-5 for smooth video, 8-10 for smaller files
- **Quality**: 85-90 JPEG quality balances size and clarity
- **Resolution**: Browser window size determines output resolution
- **Loops**: GIFs should loop seamlessly - end where you started
