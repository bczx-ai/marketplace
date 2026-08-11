---
name: team-issue
description: "需要查询事项基础或完整详情、查询字段选项，或更新事项字段和附件。"
---

# team-issue

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和读写安全规则。

## `getissue`

```bash
cubelet --config "$CUBELET_CONFIG" team getissue --id <事项ID或事项编号>
```

- `--id`：必填。既支持纯数字事项 ID，也支持事项编号，例如 `ZA-T-98054`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" team getissue --id 98054
cubelet --config "$CUBELET_CONFIG" team getissue --id ZA-T-98054
```

## `issuedetail`

更新事项前，先查询完整字段定义和当前值：

```bash
cubelet --config "$CUBELET_CONFIG" team issuedetail \
  --projectid 7803 \
  --project-type-name demand \
  --id 99924
```

从 `tagVoList.pageFieldVoList` 读取实际的 `fieldKey`、`fieldType`、`componentType`、`options` 和 `source`。不要猜测字段 key；`fieldType=5` 的系统字段不能更新。

## `fieldoptions`

当 `issuedetail` 返回的下拉字段 `options` 为空时，使用该字段返回的 `source` 查询可选值：

```bash
cubelet --config "$CUBELET_CONFIG" team fieldoptions \
  --source "/search/select/iteration?search=" \
  --search 迭代
```

## `updateissue`

推荐把待更新的 `fieldKey`/`value` 数组写入当前项目内的 JSON 文件：

```bash
cubelet --config "$CUBELET_CONFIG" team updateissue \
  --projectid 7803 \
  --project-type-name demand \
  --id 99924 \
  --file ./issue-fields.json
```

可选文件参数：

- `--attachment-field-key` 与 `--attachment-file` 配对；CLI 会先上传附件，再更新附件字段。
- `--markdown-field-key` 与 `--markdown-file` 配对；Markdown 文件原文作为富文本字段值。

更新完成后再次调用 `issuedetail`，确认目标字段已经生效。

## 安全规则

- `getissue`、`issuedetail` 和 `fieldoptions` 是只读命令。
- `updateissue` 会修改事项，执行前必须获得用户明确确认。
- `getissue` 会自动区分纯数字 ID 与事项编号。
- 字段 key 和选项值必须来自当前事项的 `issuedetail`/`fieldoptions` 返回，不能硬编码或猜测。
