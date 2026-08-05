---
name: feishu-bitable
displayName: "feishu-bitable"
description: "使用提供的应用凭证管理飞书多维表格，支持列出表格以及添加记录或任务。"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# Feishu Bitable Skill

操作飞书多维表格（Bitable/Base）记录。

## 功能
- 列出 Base 内的表
- 向表中新增记录/任务

## 使用方式
该技能目前主要作为库/模板使用：

```javascript
const { addRecord } = require('./add_task');
// addRecord(appToken, tableId, fields)
```

## 配置
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
