---
name: brain-plugin-creator
description: 创建、扩展、校验和发布 Brain 原生 Plugin。需要新建 Brain Plugin、修改 .codex-plugin/plugin.json 或 brain.json、添加 Agents/Skills/Commands/Apps/App Templates/Assets/Hooks/Rules/MCP/CLI 组件、同步 Codex 与 Claude Marketplace catalog，或执行发布前检查时使用。
---

# Brain Plugin Creator

以当前 Brain Plugin 规范创建可安装、可更新且可被 Codex 与 Claude Code 发现的插件。

## 工作流

1. 读取目标仓库的 `AGENTS.md`、`CLAUDE.md` 和贡献说明，检查未提交改动。
2. 如果在 Brain 主仓库开发，先读取 `docs/design-docs/plugin-market.md` 和当前 runtime validator；否则完整读取 [references/plugin-spec.md](references/plugin-spec.md)。
3. 新建插件时运行脚手架；扩展已有插件时直接检查现有 canonical metadata。
4. 只创建实际使用的组件目录，同时更新 `.codex-plugin/plugin.json`、`brain.json` 和 `.claude-plugin/plugin.json` 兼容投影。
5. 同步 `.agents/plugins/marketplace.json` 与 `.claude-plugin/marketplace.json`。Codex catalog 是官方市场的 canonical catalog。
6. 运行本 Skill 的校验器，再运行目标仓库已有的测试。检查 diff 中没有 credential、私钥、带凭据 URL 或同版本内容重发。
7. 只有用户明确要求时才 commit、push、创建 MR 或发布。

## 新建插件

从 Skill 根目录运行：

```bash
python3 scripts/brain_plugin.py create <marketplace-root> <plugin-name> \
  --display-name "Plugin Name" \
  --description "插件用途和触发场景" \
  --publisher-id <publisher-id> \
  --author "发布者名称" \
  --category "分类"
```

默认生成一个与 Plugin 同名的 starter Skill。创建不含 Skill 的骨架时增加 `--without-skill`，随后按规范添加实际组件；不要保留无用途的空插件。

脚手架会：

- 创建 `.codex-plugin/plugin.json`、`.claude-plugin/plugin.json` 和 `brain.json`；
- 为默认 Skill 创建最小有效 `SKILL.md`；
- 向两个 catalog 追加一致的本地 source 条目；
- 在目标目录或 catalog 已存在同名条目时停止，不覆盖内容。

## 扩展插件

- 以 `.codex-plugin/plugin.json` 和 `brain.json` 为业务真源。
- 将 Claude manifest 作为确定性兼容投影；共享字段不要分叉。
- 在 `brain.json.components` 声明实际组件及同包依赖，引用必须指向包内现存内容。
- 不创建空目录，不加入 lifecycle/install script，不为单一实现增加 manager 或 wrapper。
- 内容发生变化时递增 SemVer；同一版本的内容、CLI URL、size 或 SHA-256 不得改变。
- 新增权限、网络范围、Hook、MCP、App credential 或 CLI 时，按目标仓库安全规则补充检查和用户确认。

## 校验

```bash
python3 scripts/brain_plugin.py validate <plugin-root> --marketplace-root <marketplace-root>
python3 scripts/brain_plugin.py self-test
```

校验器只做可移植的发布前检查，不代替 Brain runtime validator。目标是 Brain 主仓库时，还要运行与 `server/src/services/plugins/manifest.ts`、Marketplace normalizer 和 installer 相关的测试。

Skill 自身有改动时，如环境提供 `skill-creator`，再运行其 `quick_validate.py`。
