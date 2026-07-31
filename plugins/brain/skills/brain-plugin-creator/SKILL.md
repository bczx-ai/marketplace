---
name: brain-plugin-creator
description: 创建、扩展、校验和发布 Brain 原生 Plugin。需要新建 Brain Plugin、修改 .codex-plugin/plugin.json 或 brain.json、添加 Agents/Skills/Commands/Apps/App Templates/Assets/Hooks/Rules/MCP/CLI 组件、同步 Codex 与 Claude Marketplace catalog，或执行发布前检查时使用。
---

# Brain Plugin Creator

以当前 Brain Plugin 规范创建可安装、可更新且可被 Codex 与 Claude Code 发现的插件。

## 工作流

1. 读取目标仓库的 `AGENTS.md`、`CLAUDE.md` 和贡献说明，检查未提交改动。
2. 目标为 Brain 主仓库时，先读取 `docs/design-docs/plugin-market.md` 和当前 runtime validator；否则完整读取 [references/plugin-spec.md](references/plugin-spec.md)。
3. 新建插件时运行脚手架；扩展已有插件时直接检查现有 canonical metadata。
4. 只创建实际使用的组件目录，同时更新 `brain.json` 和至少一个宿主 manifest；官方发布默认同时维护 Codex 与 Claude manifest。
5. CLI Plugin 先依据官方文档确认安装制品、登录命令、配置目录和认证状态命令，再声明 App、App Template、CLI 及使用方的 `requires`。
6. 同步目标 Marketplace 中实际存在的 catalog。Brain 官方市场同时维护 `.agents/plugins/marketplace.json` 与 `.claude-plugin/marketplace.json`。
7. 运行本 Skill 的校验器，再运行目标仓库已有的测试。检查 diff 中没有 credential、私钥、带凭据 URL 或同版本内容重发。
8. 涉及 CLI 或认证时完成真实安装、认证和新 Agent 会话验收；只有用户明确要求时才 commit、push、创建 MR 或发布。

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
- 向 Marketplace 中已有的 Codex、Claude catalog 追加本地 source 条目；
- 在目标目录或 catalog 已存在同名条目时停止，不覆盖内容。

## 扩展插件

- 以 `brain.json` 和首选宿主 manifest 为业务真源；至少提供 `.codex-plugin/plugin.json` 或 `.claude-plugin/plugin.json`。
- 同时提供双 manifest 时保持 `name` 一致；Codex manifest 优先提供展示 metadata，Hook 和 MCP 声明必须通过 Brain runtime 的一致性校验。
- 受控包根目录只保留支持的组件、双 manifest、`brain.json`、`LICENSE` 和 `CHANGELOG.md`；不创建空目录。
- 图标优先使用唯一的 `assets/icon.svg|jpg|png|webp`，大小不超过 5 MiB；声明路径时必须指向包内可读取的普通文件。
- 在 `brain.json.components` 声明实际组件及同包依赖，引用必须指向包内现存内容。
- 同时提供双 manifest 时保持 `version` 一致；CLI Plugin 的两份 manifest 都声明 `interface.capabilities` 中的 `CLI`。
- CLI 的 `command` 是 Agent 调用名：Unix target 的 `file` 与它相同，Windows target 使用 `<command>.exe`、`.cmd` 或 `.bat`。Skill 等使用方通过 `requires: ["cli:<command>"]` 声明依赖。
- `cli_oauth` 必须引用同包 `components.cli` 中的命令，并同时提供 App 和 App Template。`components.apps[].templates`、`app.json.templates` 与 `components.appTemplates` 双向一致，避免安装后没有连接入口。
- 不加入 lifecycle/install script，不为单一实现增加 manager 或 wrapper。
- 内容发生变化时递增 SemVer；同一版本的内容、CLI URL、size 或 SHA-256 不得改变。
- 默认官方来源的 `brain-official:brain` 在 Codex catalog 中使用 `REQUIRED`；其它 Plugin 使用 `AVAILABLE`。两者的 `authentication` 都为 `ON_INSTALL`，其它来源的 `REQUIRED` 不会获得系统权限。
- 新增权限、网络范围、Hook、MCP、App credential 或 CLI 时，按目标仓库安全规则补充检查和用户确认。

## 校验

```bash
python3 scripts/brain_plugin.py validate <plugin-root> \
  --marketplace-root <marketplace-root> \
  --source-scope public
python3 scripts/brain_plugin.py verify-cli <plugin-root> \
  --source-scope public \
  --target darwin-x64
python3 scripts/brain_plugin.py self-test
```

`public` source 的 CLI 只允许 HTTPS；Controller `private` source 和个人 Marketplace 使用 `private` 或 `personal`，允许经过网络边界校验的 HTTP/HTTPS。

`verify-cli` 下载所选 target，校验 size、SHA-256 和 tar.gz/zip 精确普通文件入口，但不执行制品。重复 `--target` 可一次校验多个平台；不传时校验声明的全部 target。

校验器只做可移植的发布前检查，不代替 Brain runtime validator。目标是 Brain 主仓库时，还要运行与 `server/src/services/plugins/manifest.ts`、Marketplace normalizer 和 installer 相关的测试。

Skill 自身有改动时，如环境提供 `skill-creator`，再运行其 `quick_validate.py`。

## CLI 与认证验收

1. 使用 `verify-cli` 验证当前平台制品，再通过 Brain 安装 Plugin；不要用手工复制到 `$BRAIN_HOME/cli` 代替安装验收。
2. 从安装完成后的 App 连接入口发起认证，确认浏览器自动打开或二维码可扫描，并等待连接状态进入 `connected`。有配置字段的 Template 会先要求用户保存配置；无字段的 `cli_oauth` 可直接开始，`private` network 不额外请求确认。
3. 结束安装前已存在的 Agent 进程，创建新的 Codex 和 Claude 会话，在会话内执行 `command -v <command>`（Windows 使用 `where <command>`）并运行官方认证状态命令。
4. 在新会话内执行一次不会修改上游数据的真实查询。只看到“已连接”、本地文件存在或旧 Agent 能运行命令，都不算验收通过。
