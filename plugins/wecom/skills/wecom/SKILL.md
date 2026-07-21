---
name: wecom
description: 通过企业微信官方 wecom-cli 查询或管理消息、通讯录、文档、智能表格、待办、会议和日程。用户提到企业微信、WeCom、企业通讯录、企业微信文档或需要用企业微信 CLI 执行操作时使用。
---

# 企业微信 CLI

使用官方 `wecom-cli`，不要自行拼接企业微信 OpenAPI 请求。

## 准备

1. 运行 `command -v wecom-cli`。缺失时告知用户先执行 `npm install -g @wecom/cli`。
2. 确认 `WECOM_CLI_CONFIG_DIR` 已由 Brain 注入。缺失或 `wecom-cli auth show --auth-status` 返回 `unauthorized` 时，请用户从插件详情重新连接；Brain 会自动打开二维码页面。
3. 用 `wecom-cli --help`、`wecom-cli <category> --help` 和 `wecom-cli <category> <method> --help` 查看当前版本能力与参数。

不要自行运行登录流程，不要读取、打印或迁移 CLI 凭据。

## 调用

命令格式：

```bash
wecom-cli <category> <method> '<json_args>'
```

优先使用帮助输出确认 method 和 JSON 字段。示例：

```bash
wecom-cli contact get_userlist '{}'
wecom-cli doc create_doc '{"doc_type":3,"doc_name":"项目周报"}'
```

## 安全

- 查询、搜索、读取可直接执行。
- 发送消息、创建或修改文档、待办、会议、日程前，先向用户确认目标、接收人和关键内容。
- 删除、取消、批量修改或扩大可见范围前必须再次确认。
- 不把机器人 Secret、会话凭据或完整敏感消息写入项目文件、日志或回复。

输出应概括结果并保留关键 ID；除非用户明确要求，不回显完整通讯录或聊天内容。
