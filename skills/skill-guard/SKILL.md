---
name: skill-guard
displayName: "skill-guard"
description: "在安装前扫描 ClawHub 技能的安全漏洞。从 ClawHub 安装新技能时使用，可检测提示词注入、恶意软件负载、硬编码密钥及其他威胁。使用 mcp-scan 预检包裹 clawhub 安装过程。"
version: 1.0.2
tags:
  - development_programming
license: "Unknown"
---

# skill-guard

**The only pre-install security gate for ClawHub skills.**

## Why skill-guard?

| | **VirusTotal** (ClawHub built-in) | **skillscanner** (Gen Digital) | **skill-guard** |
|---|---|---|---|
| **When it runs** | After publish (server-side) | On-demand lookup | **Before install (client-side)** |
| **What it checks** | Malware signatures | Their database | **Actual skill content** |
| **Prompt injections** | ❌ | ❌ | ✅ |
| **Data exfiltration URLs** | ❌ | ❌ | ✅ |
| **Hidden instructions** | ❌ | ❌ | ✅ |
| **AI-specific threats** | ❌ | ❌ | ✅ |
| **Install blocking** | ❌ | ❌ | ✅ |

**VirusTotal** catches known malware binaries — but won't flag `<!-- IGNORE PREVIOUS INSTRUCTIONS -->`.

**skillscanner** checks if Gen Digital has reviewed it — but can't scan new or updated skills.

**skill-guard** uses [mcp-scan](https://github.com/invariantlabs-ai/mcp-scan) (Invariant Labs, acquired by Snyk) to analyze what's actually in the skill, catches AI-specific threats, and blocks install if issues are found.

## The Problem

Skills can contain:
- 🎭 **Prompt injections** — hidden "ignore previous instructions" attacks
- 💀 **Malware payloads** — dangerous commands disguised in natural language  
- 🔑 **Hardcoded secrets** — API keys, tokens in plain text
- 📤 **Data exfiltration** — URLs that leak your conversations, memory, files
- ⛓️ **Toxic flows** — instructions that chain into harmful actions

**One bad skill = compromised agent.** Your agent trusts skills implicitly.

## The Solution

```bash
# Instead of: clawhub install some-skill
./scripts/safe-install.sh some-skill
```

skill-guard:
1. **Downloads to staging** (`/tmp/`) — never touches your real skills folder
2. **Scans with mcp-scan** — Invariant/Snyk's security scanner for AI agents
3. **Blocks or installs** — clean skills get installed, threats get quarantined

## What It Catches

Real example — skill-guard flagged this malicious skill:

```
● [E004]: Prompt injection detected (high risk)
● [E006]: Malicious code pattern detected  
● [W007]: Insecure credential handling
● [W008]: Machine state compromise attempt
● [W011]: Third-party content exposure
```

VirusTotal: 0/76 engines. **mcp-scan caught what antivirus missed.**

## Usage

```bash
# Secure install (recommended)
./scripts/safe-install.sh <skill-slug>

# With version
./scripts/safe-install.sh <skill-slug> --version 1.2.3

# Force overwrite
./scripts/safe-install.sh <skill-slug> --force
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Clean | Skill installed ✓ |
| `1` | Error | Check dependencies/network |
| `2` | Threats found | Skill quarantined in `/tmp/`, review before deciding |

## When Threats Are Found

Skill stays in `/tmp/skill-guard-staging/skills/<slug>/` (quarantined). You can:
1. **Review** — read the scan output, inspect the files
2. **Install anyway** — `mv /tmp/skill-guard-staging/skills/<slug> ~/.openclaw/workspace/skills/`
3. **Discard** — `rm -rf /tmp/skill-guard-staging/`

## Requirements

- `clawhub` CLI — `npm i -g clawhub`
- `uv` — `curl -LsSf https://astral.sh/uv/install.sh | sh`

## Why This Matters

Your agent has access to your files, messages, maybe your whole machine. One malicious skill can:
- Read your secrets and send them elsewhere
- Modify your agent's behavior permanently  
- Use your identity to spread to other systems

**Trust, but verify.** Scan before you install.
