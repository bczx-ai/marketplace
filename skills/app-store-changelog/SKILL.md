---
name: app-store-changelog
displayName: "App Store Changelog"
description: "通过收集并汇总自上个 Git 标签（或指定引用）以来的所有用户相关变更，生成面向用户的 App Store 更新说明。当需要根据 Git 历史或标签生成完整的更新日志、App Store“新版特性”文本或更新说明时使用。"
version: 1.0.1
tags:
  - development_programming
license: "Unknown"
---

# App Store Changelog

## Overview
Generate a comprehensive, user-facing changelog from git history since the last tag, then translate commits into clear App Store release notes.

## Workflow

### 1) Collect changes
- Run `scripts/collect_release_changes.sh` from the repo root to gather commits and touched files.
- If needed, pass a specific tag or ref: `scripts/collect_release_changes.sh v1.2.3 HEAD`.
- If no tags exist, the script falls back to full history.

### 2) Triage for user impact
- Scan commits and files to identify user-visible changes.
- Group changes by theme (New, Improved, Fixed) and deduplicate overlaps.
- Drop internal-only work (build scripts, refactors, dependency bumps, CI).

### 3) Draft App Store notes
- Write short, benefit-focused bullets for each user-facing change.
- Use clear verbs and plain language; avoid internal jargon.
- Prefer 5 to 10 bullets unless the user requests a different length.

### 4) Validate
- Ensure every bullet maps back to a real change in the range.
- Check for duplicates and overly technical wording.
- Ask for clarification if any change is ambiguous or possibly internal-only.

## Output Format
- Title (optional): "What’s New" or product name + version.
- Bullet list only; one sentence per bullet.
- Stick to storefront limits if the user provides one.

## Resources
- `scripts/collect_release_changes.sh`: Collect commits and touched files since last tag.
- `references/release-notes-guidelines.md`: Language, filtering, and QA rules for App Store notes.
