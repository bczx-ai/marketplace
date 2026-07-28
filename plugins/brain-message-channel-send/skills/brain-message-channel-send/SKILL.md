---
name: brain-message-channel-send
description: 当 Brain 消息渠道任务生成需要原生交付给飞书或个人微信发起用户的项目内图片或文件时，使用本 Skill 发送附件。
---

仅为当前消息渠道任务生成或选中的附件调用 `brain-workspace-server message-channel-send`。

示例：

```bash
brain-workspace-server message-channel-send --image /absolute/project/chart.png
brain-workspace-server message-channel-send --file /absolute/project/report.pdf
brain-workspace-server message-channel-send \
  --image /absolute/project/chart.png \
  --file /absolute/project/report.pdf
```

规则：

- `--image` 接受 PNG、JPEG、GIF 或 WebP；发送多个附件时可以重复使用 `--image` 或 `--file`。
- 只使用项目内路径，并优先使用绝对路径以避免歧义。
- 不要设置 `BRAIN_SESSION_ID`，Brain 会自动注入当前 Session。
- 不要传递收件人、项目、网关或回复标识；命令会从当前活动渠道回合推导来源会话。
- 普通助手正文会自动发送。只用该命令发送附件，成功后正常回复一次即可。
- 命令成功时会输出已发送附件数。失败时优先修复本地路径或格式问题；无法修复时简短说明附件发送失败。
- 不要用 Markdown 链接、Session Artifacts 或直接调用渠道 Provider API 替代该命令。
