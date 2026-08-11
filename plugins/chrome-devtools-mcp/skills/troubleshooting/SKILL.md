---
name: troubleshooting
description: 使用 Chrome DevTools MCP 与官方文档排查连接和页面目标问题。`list_pages`、`new_page`、`navigate_page` 调用失败，或 MCP Server 初始化失败时使用。
---

## 排障流程

按以下顺序帮助用户定位并修复 Chrome DevTools MCP 配置问题。

### 第一步：查找并读取配置

先在用户 Workspace 中查找 `.mcp.json`、`gemini-extension.json`、`.claude/settings.json`、`.vscode/launch.json` 或 `.gemini/settings.json`。

找到后检查：

- 参数或 Flag 是否拼写错误。
- 环境变量是否缺失。
- 当前环境是否支持 `--autoConnect`。

只有找不到配置文件时，才要求用户提供配置内容。

### 第二步：识别常见连接错误

阅读文档或建议改配置前，先匹配失败工具的错误消息。

#### `Could not find DevToolsActivePort`

该错误专属于 `--autoConnect`，表示 MCP Server 找不到可调试 Chrome 进程创建的文件，不是通用连接错误。不要立即改用 `--browserUrl`，按以下顺序检查：

1. 请用户确认错误中对应的 Chrome 版本正在运行，例如错误提到 Chrome Canary 时必须启动 Canary。
2. Chrome 已运行时，请用户打开 `chrome://inspect/#remote-debugging` 并启用远程调试。
3. 两项都确认后，只调用一次 `list_pages` 验证连接，不要先重试更复杂的原始命令。
4. `list_pages` 成功即表示问题已解决；仍返回相同错误时，再检查 `--browserUrl` 或沙箱限制。

#### Server 启动但创建新的空 Profile

若 `list_pages` 返回空列表，或 Server 新建 Profile 而没有连接现有 Chrome，检查参数拼写，例如把 `--autoConnect` 错写成 `--autoBronnect`。

#### 缺少工具或只有少量工具

若只看到 `list_pages`、`get_console_message`、`lighthouse_audit`、`take_heapsnapshot` 等少量工具，通常是 MCP Client 强制启用了只读模式。

`chrome-devtools-mcp` 会通过 `readOnlyHint` 标注工具是否修改浏览器状态。要使用 `emulate`、`click`、`navigate_page` 等完整工具，用户必须关闭 MCP Client 的只读模式，例如退出 Gemini CLI 的 Plan Mode 或调整工具安全设置。

#### 扩展程序工具缺失或扩展程序加载失败

1. 检查 MCP Server 配置是否包含 `--categoryExtensions`。
2. 确保 MCP Server 自行启动 Chrome，而不是连接已有实例；Chrome 149 之前通过 `--auto-connect` 或 `--browserUrl` 连接时不能加载扩展程序。

#### 其它常见错误

从失败工具响应或初始化日志中识别：

- `Target closed`
- `Tool not found`，并检查是否使用只提供少量导航和截图工具的 `--slim`
- `ProtocolError: Network.enable timed out`
- `The socket connection was closed unexpectedly`
- `Error [ERR_MODULE_NOT_FOUND]: Cannot find module`
- 沙箱或 Host 校验错误

### 第三步：查阅已知问题

读取 https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md ，根据原始错误匹配已知问题，重点检查：

- macOS Seatbelt 与 Linux 容器沙箱限制。
- WSL 要求。
- `--autoConnect` 的握手、超时和 Chrome 144+ 运行要求。

### 第四步：形成配置方案

根据具体错误、操作系统和 MCP Client 生成配置，并判断是否需要：

- 在 Claude Desktop 等沙箱环境中使用 `--browser-url=http://127.0.0.1:9222`，而不是 `--autoConnect`。
- 在 `chrome://inspect/#remote-debugging` 启用远程调试并接受连接提示。
- 添加 `--logFile <日志绝对路径>` 采集调试日志。
- Windows 上将 `startup_timeout_ms` 提高到例如 `20000`。

无法确认当前配置时，要求用户提供 MCP Server JSON 配置，不要猜测。

### 第五步：运行诊断命令

问题仍不明确时：

- 运行 `npx chrome-devtools-mcp@1.7.0 --help` 验证安装和 Node.js 环境。
- 需要详细日志时，运行 `DEBUG=* npx chrome-devtools-mcp@1.7.0 --logFile=/tmp/cdm-test.log`，再分析错误。

### 第六步：搜索 GitHub 已有问题

官方排障文档没有覆盖时，先检查环境中是否存在 `gh`，然后搜索相似问题：

```bash
gh issue list --repo ChromeDevTools/chrome-devtools-mcp --search "<错误片段>" --state all
```

也可引导用户查看 https://github.com/ChromeDevTools/chrome-devtools-mcp/issues 和 https://github.com/ChromeDevTools/chrome-devtools-mcp/discussions 。
