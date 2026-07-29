---
name: daily-digest
displayName: "Daily Digest"
description: "生成每日摘要，将存储记忆文件中的决策、经验教训、行动和问题整理成带日期的日记条目。"
version: 1.0.0
tags:
  - knowledge_management
license: "Unknown"
---

# daily-digest Skill

Purpose: Generate a daily digest from memory and interactions, stored as journals/digest/digest-YYYY-MM-DD.md.

Usage:
- Run the digest_daily.py script to generate today's digest.
- Optional: integrate with clawdbot to run automatically via a cron job or a scheduler.

Notes:
- The script reads memory/YYYY-MM-DD.md and optionally memory/YYYY-MM-DD.md from yesterday to extract decisions, lessons, actions, and questions.
- It also provides a placeholder summary when no structured entries exist in memory.
