---
name: feishu
description: 飞书官方 Skill 总入口。用户泛化提到飞书、Lark、飞书开放平台或跨多个飞书业务域时使用；单一业务对象优先转到对应的 lark-* 官方 Skill。
---

# 飞书官方 Skills 入口

本 Plugin 内置与 `lark-cli 1.0.82` 匹配的 27 个官方 Skill。先读取 `../lark-shared/SKILL.md`，再按业务对象读取最具体的 Skill；不要用本入口替代领域说明。

## 路由

| 对象 | Skill |
|---|---|
| 消息、群聊、联系人 | `lark-im`、`lark-contact` |
| 文档、云盘、知识库、Markdown | `lark-doc`、`lark-drive`、`lark-wiki`、`lark-markdown` |
| 多维表格、电子表格、幻灯片、白板 | `lark-base`、`lark-sheets`、`lark-slides`、`lark-whiteboard` |
| 日历、任务、审批、考勤、OKR | `lark-calendar`、`lark-task`、`lark-approval`、`lark-attendance`、`lark-okr` |
| 邮箱、会议、妙记、智能纪要 | `lark-mail`、`lark-vc`、`lark-note`、`lark-minutes`、`lark-vc-agent` |
| 妙搭应用、事件、OpenAPI | `lark-apps`、`lark-event`、`lark-openapi-explorer` |
| 站会与会议总结 | `lark-workflow-standup-report`、`lark-workflow-meeting-summary` |

## Brain 环境

- `LARKSUITE_CLI_CONFIG_DIR` 由 Brain 注入，应用凭据和用户授权从 Plugin 连接入口管理。
- 不执行系统级安装、`lark-cli update`、`npx skills add` 或 `lark-cli config init`。
- `lark-cli` 缺失或连接失效时，请用户更新、重新安装或重新连接飞书 Plugin。
