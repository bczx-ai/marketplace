---
name: tencent-meeting
description: 通过腾讯会议官方 tmeet CLI 查询和管理会议、参会记录、录制、智能纪要及转写内容。用户提到腾讯会议、VooV Meeting、会议预约、录制下载或会议纪要时使用。
---

# 腾讯会议 CLI

使用官方 `tmeet`，以 CLI 当前帮助为命令真源。

## 准备

1. 运行 `command -v tmeet`。缺失时告知用户执行 `npm install -g @tencentcloud/tmeet`。
2. 运行 `tmeet auth status` 检查登录。未登录时运行 `tmeet auth login`；无浏览器环境使用 `tmeet auth login --no-browser`，把授权 URL 交给用户完成 OAuth2 设备授权。
3. 凭据由 CLI 加密保存在本机，不读取或复制其配置。需要隔离时使用官方 `TMEET_CLI_CONFIG_DIR`。
4. 执行前用 `tmeet --help` 和子命令 `--help` 确认参数。

## 工作流

- 查询会议前先确认时间范围、用户或会议 ID，并处理 `next_page_token` 分页直到满足请求。
- 获取录制或纪要时先列出候选项，再按明确的会议或录制 ID 查询。
- 默认保留结构化输出；只提取完成任务所需字段。

## 安全

- 会议、参会、录制和纪要查询可直接执行。
- 创建、修改、取消会议或变更参会人前，展示主题、时间、时区和参会人并取得确认。
- 下载录制、转写或纪要前说明文件落盘位置；不得上传到未获授权的位置。
- 不输出 Access Token、Refresh Token 或本地凭据。怀疑凭据泄露时建议用户执行 `tmeet auth logout`。
