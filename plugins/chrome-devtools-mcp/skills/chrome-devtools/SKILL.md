---
name: chrome-devtools
description: 通过 Chrome DevTools MCP 高效完成网页调试、故障排查和浏览器自动化。用户要求调试网页、自动操作浏览器、分析性能或检查网络请求时使用；不适用于启用了 `--slim` 的 MCP 配置。
---

## 核心概念

**浏览器生命周期**：首次调用工具时自动启动浏览器，并使用持久化 Chrome Profile。通过 MCP Server 配置中的命令行参数调整行为；可运行 `npx chrome-devtools-mcp@1.7.0 --help` 查看参数。

额外工具需要显式启用：

- 扩展程序工具需要 `--categoryExtensions`。
- 内存工具需要 `--memoryDebugging`。

**页面选择**：工具作用于当前选中的页面。先用 `list_pages` 查看页面，再用 `select_page` 切换上下文。

**元素交互**：用 `take_snapshot` 获取页面结构及元素 `uid`，再把 `uid` 传给交互工具。页面变化后若找不到元素，重新获取快照，不要继续使用旧 `uid`。

## 工作流程

### 与页面交互前

1. 使用 `navigate_page` 或 `new_page` 导航。
2. 已知目标内容时，使用 `wait_for` 等待加载完成。
3. 使用 `take_snapshot` 理解页面结构。
4. 使用快照中的 `uid` 调用 `click`、`fill` 等工具。

### 高效获取数据

- 对截图、快照和 Trace 等大输出使用 `filePath` 参数。
- 使用 `pageIdx`、`pageSize` 分页，并用 `types` 等参数过滤。
- 输入操作无需返回新快照时，设置 `includeSnapshot: false`。

### 选择工具

- **自动化和交互**：优先使用 `take_snapshot`，文本结构更快，也更适合稳定定位。
- **视觉检查**：用户需要确认实际画面时使用 `take_screenshot`。
- **补充信息**：无障碍树未包含所需数据时使用 `evaluate_script`。

### 并行调用

可以并行执行相互独立的查询，但必须保持有依赖的顺序：导航 -> 等待 -> 快照 -> 交互。

### 测试 Chrome 扩展程序

开始前确认工具列表中存在 `install_extension`、`list_extensions` 等扩展程序工具。若不存在，停止操作并说明 MCP Server 必须增加 `--categoryExtensions`，修改后还需重启 MCP Server 或宿主应用。

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@1.7.0", "--categoryExtensions"]
    }
  }
}
```

1. 使用 `install_extension` 安装已解压的扩展程序目录。
2. 从响应或 `list_extensions` 获取扩展程序 ID。
3. 使用 `trigger_extension_action` 打开弹出窗口或侧边栏。
4. 使用带 `serviceWorkerId` 的 `evaluate_script` 检查 Service Worker 状态或触发后台行为。
5. 导航到扩展程序生效页面，并用 `take_snapshot` 验证内容脚本是否正确注入或修改页面。

## 排障

若 `chrome-devtools-mcp` 无法满足需求，引导用户使用 Chrome DevTools UI：

- https://developer.chrome.com/docs/devtools
- https://developer.chrome.com/docs/devtools/ai-assistance

启动 `chrome-devtools-mcp` 或 Chrome 失败时，参考 https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md 。
