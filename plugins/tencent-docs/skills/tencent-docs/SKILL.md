---
name: tencent-docs
description: 通过腾讯文档开放平台 OpenAPI 查询或管理腾讯文档、在线表格、文件、权限和协作者。用户提到腾讯文档、docs.qq.com、在线文档或在线表格 API 操作时使用。
---

# 腾讯文档开放平台

使用随技能提供的 `scripts/tencent_docs.py` 调用腾讯文档 OpenAPI。

## 认证

腾讯文档使用不带 PKCE 的 OAuth2 授权码模式。安装插件后，Brain 要求填写 `Client ID` 和 `Client Secret`，保存时自动打开腾讯文档官方登录页，由用户扫码并确认授权；Brain 在 Server 端换取和刷新 Token，并通过 `TENCENT_DOCS_CONFIG` 投影 `Client ID`、`Access Token` 和 `Open ID`。

1. 确认环境变量 `TENCENT_DOCS_CONFIG` 存在。
2. 缺失时请用户在插件详情中建立腾讯文档连接。
3. 腾讯文档只接受已登记的 HTTPS OAuth 回调地址；开放平台应用中的回调地址必须与当前 Brain Agent 空间公开地址一致。
4. 不读取或输出配置文件内容，不在命令行参数中传递 Token。

## 调用

先从腾讯文档官方文档确认 API 的 method、path、query 和 body，再调用：

```bash
python scripts/tencent_docs.py GET /openapi/v2/files
python scripts/tencent_docs.py POST /openapi/v2/example --query '{"limit":20}' --data '{"name":"示例"}'
```

也可使用项目内 JSON 文件：

```bash
python scripts/tencent_docs.py POST /openapi/v2/example --data-file request.json
```

不要猜测 endpoint 或字段。需要上传、下载或官方文档未覆盖的认证头时，先查官方文档并说明当前脚本是否支持。

## 安全

- 查询列表、读取元数据和内容可直接执行。
- 创建、修改、移动、共享或变更协作者前，展示目标文档和变更摘要并取得确认。
- 删除文档、取消共享、批量改权限等高影响操作必须再次确认。
- 响应中出现 Token、个人信息或敏感正文时，只返回完成任务所需内容。
