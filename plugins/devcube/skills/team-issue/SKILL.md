---
name: team-issue
description: "需要查询 Team 事项、发现可编辑字段和动态选项、创建根或子事项，或更新普通字段、Markdown 富文本及其本地图片和附件引用。"
---

# Team 事项

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)。创建、更新和上传会修改真实数据，执行前必须向用户确认目标项目、事项和变更内容。

## 查询事项

按数字 ID 或事项编号做简要查询：

```bash
cubelet --config "$CUBELET_CONFIG" team getissue --id <事项ID或编号>
```

查询完整详情、字段定义和当前值：

```bash
cubelet --config "$CUBELET_CONFIG" team issuedetail \
  --projectid <项目ID> \
  --project-type-name <组件typeName> \
  --id <事项ID>
```

从 `tagVoList[].pageFieldVoList[]` 读取：

- `fieldKey`：更新字段键。
- `fieldType`：值为 `5` 时禁止更新。
- `componentType`：字段组件类型。
- `value`：当前值。
- `options`：非空时从中选择完整选项对象。
- `source`：`options` 为空时用于动态查询。

不要从 `pageRule` 或 `pageDisplayRule` 推断可编辑字段，以 `pageFieldVoList` 为准。

## 查询动态选项

仅当目标字段 `options` 为空且 `source` 非空时调用：

```bash
cubelet --config "$CUBELET_CONFIG" team fieldoptions \
  --source '<source>' \
  --search <关键字>
```

只使用详情返回的 `/search/select/...` 相对地址，不自行构造外部 URL。

## 创建事项

先调用 `team projectmenus --projectid <项目ID>` 获取：

- 第一层 `type=1` 的 `typeName`，用于 `--project-type-name`。
- 对应 `children[].id`，用于 `--task-type-id`。

创建子事项时，再查询父事项允许创建的子事项类型：

```bash
cubelet --config "$CUBELET_CONFIG" team parentandchildren --id <父事项ID>
```

只使用返回 `children` 中允许的 `task-type-id`。创建前查询可指派人员：

```bash
cubelet --config "$CUBELET_CONFIG" team userlist \
  --search <姓名或账号关键字> \
  --currentPage 1 \
  --pageSize 100
```

使用完整人员 JSON 创建事项：

```bash
cubelet --config "$CUBELET_CONFIG" team createissue \
  --projectid <项目ID> \
  --project-type-name <typeName> \
  --name <名称> \
  --task-type-id <类型ID> \
  --assignee '<人员JSON>' \
  [--parentid <父事项ID>]
```

不传 `--parentid` 时创建根事项。只有用户明确要求从父事项继承附件时，才传 `--attachments '<附件JSON数组>'`。

如需按名称或创建人搜索事项类型，可使用只读命令：

```bash
cubelet --config "$CUBELET_CONFIG" team tasktypelist \
  --name <类型名称> \
  --creator <创建人> \
  --currentPage 1 \
  --pageSize 10
```

## 更新普通字段

优先使用当前项目内的 JSON 文件，避免 shell 转义问题。文件可为 `itemValues` 数组或包含该数组的对象：

```json
[
  {
    "fieldKey": "fieldkey891",
    "value": {
      "id": 2277,
      "name": "IT内部需求"
    }
  }
]
```

```bash
cubelet --config "$CUBELET_CONFIG" team updateissue \
  --projectid <项目ID> \
  --project-type-name <typeName> \
  --id <事项ID> \
  --file ./issue-fields.json
```

`updateissue` 会先查询详情，拒绝不存在的字段和 `fieldType=5` 字段。下拉、单选、人员等对象字段应传接口返回的完整选项对象，不要只传显示名称。

## 更新 Markdown 富文本

`componentType=team-rich` 使用 Markdown 原文。更新前扫描 Markdown 中的图片和附件引用，包括：

- `![说明](path)` 图片。
- `[附件](path)` 链接。
- Markdown 中 HTML 标签的本地 `src` 或 `href`。

保留已经是 `http://`、`https://`、`data:`、`mailto:` 或 `#` 锚点的引用。将其他引用按 Markdown 文件所在目录解析为当前项目内的本地文件；文件不存在时停止，不要提交带失效本地路径的富文本。

对每个本地引用先上传：

```bash
cubelet --config "$CUBELET_CONFIG" team uploadfile --file <本地文件路径>
```

从返回的 `data.url` 取得远程地址，将 Markdown 中对应目标完整替换为该 URL。同一本地文件只上传一次，所有重复引用复用同一 URL。全部上传成功并确认 Markdown 中不再存在本地文件引用后，再执行更新：

```bash
cubelet --config "$CUBELET_CONFIG" team updateissue \
  --projectid <项目ID> \
  --project-type-name <typeName> \
  --id <事项ID> \
  --markdown-field-key <fieldKey> \
  --markdown-file ./description.md
```

任一上传失败时，不执行 `updateissue`。不要把图片同时写入事项的附件字段，除非用户明确要求它也作为附件展示。

## 追加附件

`componentType=team-upload` 使用当前项目内的本地文件：

```bash
cubelet --config "$CUBELET_CONFIG" team updateissue \
  --projectid <项目ID> \
  --project-type-name <typeName> \
  --id <事项ID> \
  --attachment-field-key <fieldKey> \
  --attachment-file ./detail.xlsx
```

命令会先调用文件上传接口，再保留已有附件并追加新附件，最后更新事项。不要手工伪造下载 URL、`uid` 或上传状态。普通字段、一个 Markdown 字段和一个附件可以在同一次 `updateissue` 中组合更新。

## 标准顺序

```text
projectlist
-> projectmenus
-> getissue / issuedetail
-> parentandchildren（仅创建子事项）
-> userlist / tasktypelist / fieldoptions / uploadfile（按需）
-> createissue / updateissue（确认后执行）
-> issuedetail（验证结果）
```

## 安全规则

- `getissue`、`issuedetail`、`fieldoptions`、`parentandchildren`、`userlist` 和 `tasktypelist` 是只读命令。
- `createissue`、`updateissue` 和 `uploadfile` 会修改真实数据，执行前必须获得用户明确确认。
- `getissue` 会自动区分纯数字 ID 与事项编号。
- 字段 key、组件类型、事项类型和选项值必须来自当前项目或事项的查询结果，不能硬编码或猜测。
- 文件只允许来自当前项目，不能读取或上传项目外文件。

## 错误处理

- 返回 `Unauthorized`：让用户检查 DevCube App 连接，不读取或输出配置中的认证信息。
- 返回 `unknown flag`：确认当前 App 连接指向已加载最新 capabilities 的 API Server。
- 字段不存在或 `fieldType=5`：停止更新，重新读取 `issuedetail`。
- 动态选项为空：检查是否使用了字段原始 `source` 和合适的 `search`。
