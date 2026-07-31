---
name: brain-skill-creator
description: 创建、扩展、校验和发布符合 Brain Skill Marketplace 规范的独立 Skill。需要向 Marketplace 仓库的 skills/技能名/ 新增或更新 SKILL.md、补齐 displayName/version/tags/license、维护 agents/references/scripts/assets、检查图标和安全边界，或执行发布前检查时使用。
---

# Brain Skill Creator

按照当前 Skill Marketplace 规范创建可发现、可预览、可安装和可更新的独立 Skill。

## 工作流

1. 读取目标仓库的 `AGENTS.md`、`CLAUDE.md` 和贡献说明，检查未提交改动。
2. 目标为 Brain 主仓库时，读取 `docs/design-docs/plugin-market.md` 和 `cloud/internal/usecase/marketplace_catalog.go` 的当前 Skill parser；其它仓库完整读取 [Skill 市场规范](references/skill-market-spec.md)。
3. 检查是否已有同名 Skill。新建时优先使用环境提供的 `skill-creator` 脚手架生成基础目录，再补充 Marketplace metadata；更新时保留现有资源，只修改需求涉及的内容。
4. 官方 Marketplace 固定写入 `skills/<name>/`，目录名与 frontmatter `name` 完全一致。只创建实际使用的 `agents/`、`references/`、`scripts/` 和 `assets/`。
5. 使用六个受控 frontmatter 字段：`name`、`displayName`、`description`、`version`、`tags`、`license`。不要添加未知字段。
6. 让 `description` 同时说明能力和触发场景；`SKILL.md` 只保留核心流程，详细规范、长示例和领域资料放入一层 `references/`。
7. 校验名称、SemVer、分类、图标、目录边界、文件类型、凭据和包体积。目标为 Brain 主仓库时运行对应 Controller Skill Marketplace 测试。
8. 内容变化时递增 SemVer。只有用户明确要求时才提交、推送、创建 MR 或发布。

## 创建与更新

- 名称使用小写字母、数字和连字符，保持简短且动作明确；不要为了兼容市场放宽基础 Skill 的命名质量。
- `displayName` 使用用户可识别的名称；`description` 把所有触发条件放在 frontmatter，不新增重复的“使用场景”章节。
- `tags` 只使用规范允许的固定分类，第一个分类作为目录主分类。通常选择一到三个，不堆叠弱相关分类。
- `license` 使用明确的 SPDX 标识；来源无法确认时先查明，不猜测许可证。
- `agents/openai.yaml` 只写真实需要的 UI metadata；`default_prompt` 必须显式包含 `$<skill-name>`。
- 图标可选。提供时只保留一个 `assets/icon.svg|jpg|png|webp`，不要生成多份候选图标。
- 不创建 `README.md`、`CHANGELOG.md`、安装说明或无用途的空目录。

## 校验

1. 确认 `SKILL.md` frontmatter 从文件第一行开始且正确闭合。
2. 确认目录名、`name`、界面 metadata 中的 Skill 引用一致。
3. 检查包内没有 symlink、hardlink、特殊文件、凭据、私钥或带凭据 URL。
4. 运行目标仓库已有的 Skill Marketplace 测试；通用 `quick_validate.py` 若拒绝 Marketplace 专用字段，不用删除这些字段，改用 Marketplace parser 校验。
5. 检查 staged diff，确认版本已递增且没有把 Skill 目录外内容带入制品。

涉及字段长度、分类、图标和制品上限时，以 [Skill 市场规范](references/skill-market-spec.md) 为准。
