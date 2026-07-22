---
name: feishu
description: 通过飞书官方 lark-cli 操作消息、文档、云空间、多维表格、电子表格、幻灯片、日历、任务、知识库、邮箱、会议和审批。用户提到飞书、Lark 或飞书开放平台时使用。
---

# 飞书 CLI

使用官方 `lark-cli`。优先使用 `+` 快捷命令，其次使用精选 API 命令，只有前两者不能覆盖时才调用通用 API。

## 准备

1. 运行 `command -v lark-cli`。缺失表示插件 CLI 安装异常，请用户更新或重新安装飞书插件，不要执行系统级安装命令。
2. 确认 `LARKSUITE_CLI_CONFIG_DIR` 已由 Brain 注入。Brain 连接会通过 stdin 配置 App Secret，不在参数中暴露凭据。
3. 运行 `lark-cli auth status`。未登录时请用户从插件详情重新连接；Brain 会自动打开 CLI 输出的用户授权页面。
4. 凭据保存在系统钥匙串和当前连接配置目录；不要读取或复制。

## 调用层级

```bash
lark-cli calendar +agenda
lark-cli im +messages-send --chat-id <chat-id> --text "消息"
lark-cli docs +create --doc-format markdown --content "# 周报"
lark-cli calendar calendars list
lark-cli api GET /open-apis/calendar/v4/calendars
```

用 `lark-cli <service> --help` 查找快捷命令，默认使用 JSON 输出。明确需要机器人或用户身份时使用 `--as bot|user`，不猜测身份。

## 安全

- 查询、搜索和读取可直接执行。
- 发送消息、创建或修改文档/日程/任务、审批操作前确认目标、接收人和内容。
- 删除、撤回、拒绝审批、批量权限变更等高影响操作必须再次确认。
- 不输出 App Secret、用户 Token、聊天或文档中的无关敏感内容。
