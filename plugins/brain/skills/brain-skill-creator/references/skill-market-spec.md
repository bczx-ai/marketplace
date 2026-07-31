# Brain Skill 市场规范

本文记录公共 Skill Marketplace 的可移植发布约束。Brain 主仓库的当前 Controller parser 是最终真源；冲突时以 `cloud/internal/usecase/marketplace_catalog.go` 为准。

## 目录与制品

官方 Marketplace 只扫描仓库根目录的以下结构：

```text
skills/
  sample-skill/
    SKILL.md
    agents/openai.yaml       # 可选
    references/              # 可选
    scripts/                 # 可选
    assets/icon.svg          # 可选
```

- 目录名必须与 frontmatter `name` 完全一致。
- 同一来源不能出现重复名称；任一候选 Skill 无效会使本次同步失败并保留上次可用目录。
- 单个 Skill 制品只包含该 Skill 目录，压缩包不得超过 25 MiB。
- `SKILL.md` 不得超过 2 MiB，frontmatter 不得超过 64 KiB。
- 禁止 symlink、hardlink、特殊文件、路径越界和隐藏的凭据文件。

## Frontmatter

frontmatter 使用闭合 Schema，只允许以下六个字段：

```yaml
---
name: sample-skill
displayName: 示例技能
description: 创建并校验示例内容。用户要求处理示例任务或检查相关产物时使用。
version: 1.0.0
tags:
  - development_programming
license: MIT
---
```

| 字段 | 约束 |
| --- | --- |
| `name` | 小写字母或数字开头，只含小写字母、数字、`.`、`_`、`-`，最多 128 字符；新 Skill 优先使用不超过 64 字符的连字符名称 |
| `displayName` | 必填，去除首尾空白后 1-128 个字符 |
| `description` | 必填，去除首尾空白后 1-2000 个字符，同时描述能力和触发场景 |
| `version` | 必填 SemVer，可带 prerelease 和 build metadata；发布内容变化必须递增，推荐不加 `v` 前缀 |
| `tags` | 最多 16 个，不得重复，只能使用固定分类；第一个分类作为目录主分类 |
| `license` | 必填，去除首尾空白后 1-128 个字符，优先使用 SPDX 标识 |

允许的分类：

```text
office_productivity
content_creation
development_programming
data_analysis
design_multimedia
ai_agent
knowledge_management
business_operations
education_learning
```

Marketplace frontmatter 比 Codex 基础 Skill metadata 多四个发布字段。只接受 `name` 和 `description` 的通用校验器可能拒绝合法市场文件；不要因此删除 `displayName`、`version`、`tags` 或 `license`。

## 图标

- 图标可选，自动发现路径为 `assets/icon.svg`、`assets/icon.jpg`、`assets/icon.png` 或 `assets/icon.webp`。
- `assets/` 最多只能有一个 `icon.*` 候选。
- 图标必须是可解析的普通文件，大小为 1 字节到 5 MiB；不限制像素宽高。
- 不使用外部 URL、data URL、symlink 或扩展名与内容不一致的文件。

## 内容设计

- `SKILL.md` 使用命令式表达，只保留 Agent 执行任务所需的核心流程，建议少于 500 行。
- 详细规则和长资料放到 `references/`，从 `SKILL.md` 直接链接，避免多层引用。
- 重复且需要确定性的操作才放入 `scripts/`；脚本必须可直接运行并经过最小真实测试。
- 输出模板和静态资源放入 `assets/`；不要加入项目历史、发布日志、脚手架占位文件或重复说明。
- `agents/openai.yaml` 的 `short_description` 保持简短，`default_prompt` 显式引用 `$<skill-name>`；图标字段只在对应文件真实存在时声明。

## 安全与发布检查

1. 读取目标仓库约束并检查工作树，避免覆盖已有改动。
2. 确认六个 frontmatter 字段完整、无未知字段，目录名和 `name` 一致。
3. 检查分类、SemVer、许可证、图标格式和容量边界。
4. 搜索 access token、Cookie、private key、用户 credential、`.env` 和带凭据 URL。
5. Brain 主仓库执行：

```bash
cd cloud
go test ./internal/usecase -run MarketplaceSkill
```

6. 检查实际 Marketplace 同步诊断和 Skill 文件预览；失败同步不能用不完整结果替换上次可用目录。
7. 审查 staged diff 后再提交；只有用户明确要求时才推送或发布。
