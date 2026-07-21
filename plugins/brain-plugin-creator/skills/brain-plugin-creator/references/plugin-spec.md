# Brain Plugin 发布规范

本参考描述 Brain 1.0.16 起的原生 Plugin 公共约束。Brain 主仓库的 `docs/design-docs/plugin-market.md` 和 runtime validator 是最终真源；两者与本文冲突时，以当前代码为准。

## 目录

- [真源与目录](#真源与目录)
- [Plugin manifest](#plugin-manifest)
- [Brain manifest](#brain-manifest)
- [组件映射](#组件映射)
- [Marketplace catalog](#marketplace-catalog)
- [安全与版本](#安全与版本)
- [发布检查](#发布检查)

## 真源与目录

Brain 官方 Marketplace 固定使用 Git 仓库。Brain 原生 Plugin 提供 `brain.json`，并至少提供一个宿主 manifest：

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json  # 可选；官方发布默认同时提供
  brain.json
```

九个内容目录都可选，只创建实际使用的目录；CLI 是第十类组件，只在 `brain.json` 中声明：

```text
agents/           skills/           commands/
apps/             app-templates/    assets/
hooks/            rules/            mcp/
```

CLI 二进制不进入 Git 包。`brain.json` 声明对象存储 URL、size 和 SHA-256，Brain 只下载当前平台 target。

同时存在双 manifest 时，Codex manifest 优先提供展示 metadata，两个 `name` 必须一致。Brain 还会分别解析并比较两边的 Hook 和 MCP 声明；其它宿主专用 metadata 可以不同。

## Plugin manifest

官方 Plugin 必须提供稳定小写 slug 和 SemVer：

```json
{
  "name": "sample-plugin",
  "version": "1.0.0",
  "description": "插件用途。",
  "author": { "name": "发布者" },
  "skills": "./skills",
  "interface": {
    "displayName": "Sample Plugin",
    "shortDescription": "用于市场卡片的简短描述",
    "longDescription": "用于详情页的完整描述。",
    "developerName": "发布者",
    "category": "开发工具",
    "capabilities": ["Skills"]
  }
}
```

仅在对应配置真实存在时声明 `skills`、`hooks`、`mcpServers` 或其它路径。图标使用 `interface.logo`，回退 `composerIcon`；第三方插件只能使用包内不超过 1 MiB 的 PNG、JPEG 或 WebP，经过审查的 Brain 内置插件可使用 SVG。

## Brain manifest

`brain.json` 只描述原生 manifest 无法表达的组件和安全约束：

```json
{
  "$schema": "https://brain.zhonganinfo.com/schemas/plugin-extension/v1.json",
  "schemaVersion": 1,
  "publisherId": "publisher",
  "compatibility": { "brain": ">=1.0.16" },
  "components": {
    "skills": [
      { "key": "sample", "requires": ["cli:sample"] }
    ]
  }
}
```

`publisherId` 必须稳定且使用 slug。`schemaVersion` 不代替 Plugin version。`requires` 当前只做格式校验，不执行跨 Plugin 依赖求解。Schema 是闭合的，不要添加未定义字段。

`compatibility.brain` 当前会被解析，但尚未执行版本范围判断；当前 Brain compatibility 主要依据本机是否存在所需 CLI target。

## 组件映射

| `brain.json.components` | 包内位置 | 说明 |
| --- | --- | --- |
| `agents[].key` | `agents/<key>.md` 或 `agents/<key>/AGENT.md` | 由宿主原生发现 |
| `skills[].key` | `skills/<key>/SKILL.md` | 保留其 references/scripts/assets 子树 |
| `commands[].key` | `commands/<key>.md` 或 `.toml` | 由宿主原生发现 |
| `apps[].key` | `apps/<key>/app.json` | 可声明 `templates` 和同包依赖 |
| `appTemplates[]` | `app-templates/<key>/template.json` | 认证仅支持 Brain 定义的公共类型 |
| `assets[]` | `assets/<relative-path>` | `detail.html` 只能使用安全静态 HTML |
| `hooks[].key` | `hooks/<key>.json` | manifest 还需声明 Hook 配置 |
| `rules[].key` | `rules/<key>.mdc` 或 `.md` | 由宿主原生发现 |
| `mcp[]` | manifest `mcpServers` 配置 | 支持安全的 stdio、http/streamable-http 与 SSE |
| `cli[]` | `brain.json` target metadata | 不提交二进制 |

需要由官方 CLI 完成浏览器或扫码登录时，App Template 使用 `auth.kind=cli_oauth`：

```json
{
  "auth": {
    "kind": "cli_oauth",
    "configDirEnv": "EXAMPLE_CONFIG_DIR",
    "commands": [{
      "command": "example",
      "args": ["auth", "login", { "valueFrom": "config.hostname" }],
      "stdinFrom": "secret.app_secret",
      "timeoutSeconds": 600
    }]
  }
}
```

命令只能是 executable token 和参数数组，不经过 shell。动态参数只能引用非 secret 的 `config.<field>`，secret 只能通过 `stdinFrom` 传入；配置目录环境变量不能覆盖系统、Brain、Agent、Git、Node、动态链接器或 SSH 关键变量。登录命令会进入权限摘要，成功退出后连接才可用。

不支持 PKCE 的标准授权码服务使用 `auth.kind=oauth2`；支持 PKCE S256 时使用 `oauth2_pkce`。两者都由 Brain 自动打开授权页、校验一次性 state、在 Server 端换取并刷新 Token。少数官方服务需要固定登录参数或 GET Token 请求时，可声明 `authorizationParams` 和 `tokenMethod`：

```json
{
  "auth": {
    "kind": "oauth2",
    "authorizationEndpoint": "https://identity.example/authorize",
    "authorizationParams": { "scope": "all" },
    "tokenEndpoint": "https://identity.example/token",
    "tokenMethod": "GET",
    "clientIdField": "client_id",
    "clientSecretField": "client_secret"
  }
}
```

`client_id`、`redirect_uri`、`response_type`、`state` 和 PKCE 参数由 Brain 管理，不能放入 `authorizationParams`。CLI 配置可使用 `auth.access_token`；服务在 Token 响应中返回外部账号 ID 时，还可使用 `auth.identity.external_id`。

不要创建 LSP、lifecycle/install script 或其它未知自动发现目录。Brain 安装器只保留经过校验的受支持内容。

远程 MCP 必须使用无凭据、无 fragment 的固定 HTTPS URL。静态 headers 不能包含 `Authorization`、Cookie、Host 或其它敏感、hop-by-hop header；需要认证时使用 AppConnection。

CLI target 只支持 `darwin-arm64`、`darwin-x64`、`win32-x64`。每个 target 必须包含 `file`、无凭据且无 fragment 的 `url`、1-128 MiB 的整数 `size` 和 64 位小写十六进制 `sha256`；Windows 文件扩展名只能是 `.exe`、`.cmd` 或 `.bat`。`public` source 只允许 HTTPS，Controller `private` source 和个人 Marketplace 允许 HTTP 或 HTTPS。

## Marketplace catalog

Marketplace 至少提供以下一个 catalog；Brain 官方市场同时维护两者：

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
```

Codex catalog 示例：

```json
{
  "name": "brain-official",
  "interface": { "displayName": "Brain 官方市场" },
  "plugins": [
    {
      "name": "sample-plugin",
      "source": { "source": "local", "path": "./plugins/sample-plugin" },
      "category": "开发工具",
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      }
    }
  ]
}
```

Controller 同时读取两份 catalog，并按 Plugin name 合并，Codex 条目优先；个人市场按配置的格式或 Codex 优先级读取第一份可用 catalog，不合并。官方 Claude catalog 保留同名、同 source 的兼容条目。`source.path` 相对 Marketplace 根目录、以 `./` 开头且不能越界。新条目追加到现有列表，除非仓库明确规定排序。

## 安全与版本

- 禁止 symlink、hardlink、特殊文件、绝对路径、`..` 和越出 Plugin 根目录的引用。
- manifest 和组件文件不得包含 access token、private key、用户 credential 或带凭据 URL。
- Hook 安装时不执行；新增或改变 Hook、MCP、CLI、network scope、OAuth scope 都属于权限变化。
- stdio MCP 使用 executable token 与参数数组，不使用 shell command string。
- 远程 MCP 和 CLI 使用固定、安全的 URL；App secret 和 OAuth token 只保存在 Server 拥有的本地 `0600` 文件中，不进入 catalog、公开 RPC、事件或日志。
- Plugin 内容变化必须递增 SemVer。相同 version 但内容摘要变化会被视为可变重发并拒绝自动更新。
- `requires` 缺少当前平台 target 时，只禁用依赖组件，不伪装为可用。

## 发布检查

1. 检查仓库说明、工作树和目标分支，避免覆盖他人改动。
2. 确认 name、目录名、catalog entry 和所有现存 manifest 的 name 一致。
3. 确认 SemVer 已按变更递增，`publisherId` 未变化。
4. 确认每个 `brain.json.components` 声明都有包内实现，且没有空目录。
5. 确认所有现存 catalog 都包含条目；Codex catalog 的 category 和 policy 完整，官方 Claude catalog source 一致。
6. 搜索 credential、私钥和带凭据 URL；按 source scope 检查 CLI URL，并检查 size 上限、SHA-256 与不可变 URL。
7. 运行 `brain_plugin.py validate`、各 Skill 校验和仓库测试。
8. review staged diff 后再提交；只有用户明确要求时 push、创建 MR 或 release。
