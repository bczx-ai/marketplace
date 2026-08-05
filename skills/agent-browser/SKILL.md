---
name: agent-browser
displayName: Agent Browser
description: 用于 AI 代理的浏览器自动化 CLI。当用户需要与网站交互（包括浏览页面、填写表单、点击按钮、截图等）时使用。
version: 1.0.0
tags:
  - ai_agent
license: Unknown
---

# agent-browser

Fast browser automation CLI for AI agents. Chrome/Chromium via CDP with
accessibility-tree snapshots and compact `@eN` element refs.

Install: `npm i -g agent-browser && agent-browser install`

## Start here

This file is a discovery stub, not the usage guide. Before running any
`agent-browser` command, load the actual workflow content from the CLI:

```bash
agent-browser skills get core             # start here — workflows, common patterns, troubleshooting
agent-browser skills get core --full      # include full command reference and templates
```

The CLI serves skill content that always matches the installed version,
so instructions never go stale. The content in this stub cannot change
between releases, which is why it just points at `skills get core`.

## Specialized skills

Load a specialized skill when the task falls outside browser web pages:

```bash
agent-browser skills get electron          # Electron desktop apps (VS Code, Slack, Discord, Figma, ...)
agent-browser skills get slack             # Slack workspace automation
agent-browser skills get dogfood           # Exploratory testing / QA / bug hunts
agent-browser skills get vercel-sandbox    # agent-browser inside Vercel Sandbox microVMs
agent-browser skills get agentcore         # AWS Bedrock AgentCore cloud browsers
```

Run `agent-browser skills list` to see everything available on the
installed version.

## Why agent-browser

- Fast native Rust CLI, not a Node.js wrapper
- Works with any AI agent (Cursor, Claude Code, Codex, Continue, Windsurf, etc.)
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency
- Accessibility-tree snapshots with element refs for reliable interaction
- Sessions, authentication vault, state persistence, video recording
- Specialized skills for Electron apps, Slack, exploratory testing, cloud providers
