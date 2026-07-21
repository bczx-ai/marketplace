---
name: mantis-test-case-library
description: "需要通过 Brain DevCube 应用连接管理 Mantis 测试管理用例库，包括查询/创建用例库、查看目录树、新增目录、导入 Excel/XMind 用例，或批量新增用例并关联需求。"
---

# case

> **PREREQUISITE:** 先阅读 [DevCube 公共规则](../devcube/SKILL.md)，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet --config "$CUBELET_CONFIG" case <command> [flags]
```

## Commands

使用前提：

- `cube-api-server` 所在配置中已设置 `cube_api_server.mantis_url`
- 当前会话已具备可访问 Mantis 的登录态

| Command | 说明 |
|---------|------|
| `librarySearch` | 查询指定项目下当前用户可见的测试用例库 |
| `libraryAdd` | 在指定项目下创建新的测试用例库 |
| `folderTree` | 查看指定用例库的目录树 |
| `folderAdd` | 在用例库目录树下新增目录 |
| `addBatchAndRelateDemand` | 批量新增用例并关联需求 |
| `import` | 将本地 `.xlsx` 或 `.xmind` 测试用例文件同步导入到指定用例库 |

## 安全规则

- 写命令包括：`libraryAdd`、`folderAdd`、`addBatchAndRelateDemand`、`import`
- 执行任何写命令前，必须确认用户明确授权本次写入
- 本文中的 `8143`、`323600757682245`、`323600757727301`、`326087293272133`、`101782` 和 `agent-*` 名称是已验证返回示例；除非用户明确要求使用这些值，否则只能用于理解返回结构，不能原样执行
- 写命令的项目 ID、用例库 ID、目录 ID、需求 ID、用例名称必须来自用户输入或本次查询/创建返回

## 推荐调用流程

1. `librarySearch`：按 `projectId` 查询用例库；如用户给了名称，用 `--name` 缩小结果
2. `folderTree`：用目标用例库 ID 查看目录树
3. 选择已有目录，或执行 `folderAdd` 创建目录
4. `addBatchAndRelateDemand`：把目录节点 ID 写入 payload 的 `parentNodeId`

注意：用例不能直接挂在用例库根下。`parentNodeId` 应使用 `folderTree` 返回的已有目录 `data.children[].id`，或 `folderAdd` 返回的 `data.id`。

## 返回读取规则

`cubelet` 命令输出统一是 envelope：

- `ok`：布尔值；只有 `true` 才继续读取业务字段
- `error`：错误文本；`ok=false` 时优先把它反馈给用户
- `data`：业务数据；agent 后续取值必须从这里取

常用取值：

| 场景 | JSON path | 用途 |
|------|-----------|------|
| 查询用例库后定位目标库 | `data[]` | 未带 `--name` 时可能返回多条，必须按 `name` 匹配目标库 |
| 按名称查询后取用例库 ID | `data[0].id` | 传给 `case import --library`；如果是纯数字字符串，也可作为 `folderTree --libraryId` 和新增 payload 的 `libraryId` |
| 创建用例库后取新用例库 ID | `data.id` | 后续导入或查看目录树 |
| 查看目录树后取根目录 ID | `data.id` | 作为 `case folderAdd --parentId` 创建一级目录；不要把用例直接挂到用例库根下 |
| 查看目录树后取子目录 ID | `data.children[].id` | 作为新增用例 payload 的 `parentNodeId`，表示新增到指定目录 |
| 新增目录后取目录 ID | `data.id` | 作为 `addBatchAndRelateDemand` payload 的 `parentNodeId` |
| 新增并关联需求后确认数量 | `data.caseCount` | 本次请求新增的用例数量汇总 |
| 新增并关联需求后确认需求 ID | `data.relateDemandIds` | 本次请求关联的需求 ID 列表 |
| 导入后确认导入数量 | `data.imported` | 成功导入数量 |

注意：`addBatchAndRelateDemand` 当前不返回新建用例 ID，只返回本次请求汇总；不要从返回中推断具体 case ID。

## `librarySearch`

- `--projectId`：项目 ID，必传
- `--name`：非必传；用例库名称模糊查询
- `--share`：非必传；按共享状态过滤

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case librarySearch --projectId 8143
cubelet --config "$CUBELET_CONFIG" case librarySearch --projectId 8143 --name lq0001
cubelet --config "$CUBELET_CONFIG" case librarySearch --projectId 8143 --share=true
```

返回示例：`cubelet --config "$CUBELET_CONFIG" case librarySearch --projectId 8143`。返回数量会随项目变化，agent 不能按固定位置判断目标库。

```json
{
  "data": [
    {
      "id": "323600757682245",
      "name": "lq0001",
      "projectId": "8143",
      "share": false
    },
    {
      "id": "321136154517573",
      "name": "导入用例",
      "projectId": "8143",
      "share": false
    }
  ],
  "error": "",
  "ok": true
}
```

返回示例：`cubelet --config "$CUBELET_CONFIG" case librarySearch --projectId 8143 --name lq0001`

```json
{
  "data": [
    {
      "id": "323600757682245",
      "name": "lq0001",
      "projectId": "8143",
      "share": false
    }
  ],
  "error": "",
  "ok": true
}
```

Agent 取值：

- 未带 `--name` 时先在 `data[]` 中按 `name` 找目标库；不要默认使用 `data[0]`
- 带 `--name lq0001` 后，`data[0].id` 是目标用例库 ID：`323600757682245`
- `data[0].projectId`：项目 ID，例如 `8143`
- `data[0].share`：是否共享

## `libraryAdd`

- `--projectId`：必传
- `--name`：必传
- `--share`：非必传；是否共享，默认 `false`
- `--description`：非必传；用例库描述

注意：

- 这是写命令，执行前必须确认用户明确要创建用例库
- 不要原样使用示例名称；按用户目标项目和命名创建

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case libraryAdd --projectId 8143 --name agent示例用例库
cubelet --config "$CUBELET_CONFIG" case libraryAdd --projectId 8143 --name agent示例用例库 --share --description "agent 创建示例"
```

返回字段形态示例；`data.id` 由后端生成：

```json
{
  "data": {
    "id": "326000000000001",
    "name": "agent示例用例库",
    "projectId": "8143",
    "share": false
  },
  "error": "",
  "ok": true
}
```

Agent 取值：

- `data.id`：新建用例库 ID
- `data.name`：新建用例库名称
- `data.projectId`：项目 ID
- `data.share`：是否共享

## `folderTree`

- `--libraryId`：必传；用例库数字 ID

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case folderTree --libraryId 323600757682245
```

返回示例：`cubelet --config "$CUBELET_CONFIG" case folderTree --libraryId 323600757682245`

```json
{
  "data": {
    "children": [
      {
        "descendantsTotal": 3,
        "id": 323600818372677,
        "libraryId": 323600757682245,
        "name": "x",
        "nodeType": "folder",
        "parentId": 323600757727301,
        "siblingOrder": 1
      },
      {
        "children": [
          {
            "descendantsTotal": 1,
            "id": 325740307968069,
            "libraryId": 323600757682245,
            "name": "1111",
            "nodeType": "folder",
            "parentId": 325700786344006,
            "siblingOrder": 3
          }
        ],
        "descendantsTotal": 2,
        "id": 325700786344006,
        "libraryId": 323600757682245,
        "name": "目录",
        "nodeType": "folder",
        "parentId": 323600757727301,
        "siblingOrder": 3
      }
    ],
    "descendantsTotal": 11,
    "id": 323600757727301,
    "libraryId": 323600757682245,
    "name": "lq0001",
    "nodeType": "root",
    "parentId": 0,
    "siblingOrder": 33
  },
  "error": "",
  "ok": true
}
```

Agent 取值：

- `data.id`：当前返回树根节点 ID，例如 `323600757727301`；用于 `case folderAdd --parentId` 创建一级目录
- `data.libraryId`：用例库 ID，例如 `323600757682245`
- `data.children[].id`：子目录节点 ID；要新增到子目录时用作 `parentNodeId`
- `data.children[].name`：子目录名称

## `folderAdd`

- `--libraryId`：必传；用例库数字 ID
- `--parentId`：必传；父目录节点 ID，可使用 `folderTree` 返回的 `data.id` 创建一级目录，或使用 `data.children[].id` 创建子目录
- `--name`：必传；目录名称

注意：

- 这是写命令，会实际新增目录
- 执行前必须确认用户明确要创建目录
- 用例不能直接挂在用例库根下；新增用例前先用 `folderTree` 选择已有目录，或用 `folderAdd` 创建目录
- `folderAdd` 固定创建 `nodeType=folder`
- 不要原样使用示例中的 `agent-folderAdd-20260710`，除非用户明确要求

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case folderAdd --libraryId 323600757682245 --parentId 323600757727301 --name agent-folderAdd-20260710
```

返回示例：`cubelet --config "$CUBELET_CONFIG" case folderAdd --libraryId 323600757682245 --parentId 323600757727301 --name agent-folderAdd-20260710`

```json
{
  "data": {
    "id": 326087293272133,
    "libraryId": 323600757682245,
    "name": "agent-folderAdd-20260710",
    "nodeType": "folder",
    "parentId": 323600757727301
  },
  "error": "",
  "ok": true
}
```

Agent 取值：

- `data.id`：新目录节点 ID，例如 `326087293272133`；后续作为 `addBatchAndRelateDemand` payload 的 `parentNodeId`
- `data.libraryId`：用例库 ID
- `data.parentId`：父目录节点 ID
- `data.name`：目录名称
- `data.nodeType`：应为 `folder`

## `addBatchAndRelateDemand`

- `--payload`：非必传；直接传 `AddBatchAndRelateDemandReq` JSON
- `--file`：非必传；本地 JSON 文件路径，文件内容会写入 `payload`

注意：

- `--payload` 和 `--file` 至少传一个；同时传时以 `--payload` 为准
- 这是写命令，会实际新增用例并写入需求关联
- 执行前必须确认用户明确要新增用例并关联需求
- 请求 JSON 顶层字段使用 Mars 外部接口格式：`libraryId`、`parentNodeId`、`marsCaseGptDTOS`、`relateDemandIds`
- `parentNodeId` 必须是目录节点 ID；从 `folderTree` 的 `data.children[].id` 取已有目录，或从 `folderAdd` 的 `data.id` 取新目录
- 不要原样使用示例 payload；必须替换为用户目标用例、目录和需求 ID

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case addBatchAndRelateDemand --file ./cases-relate-demand.json
cubelet --config "$CUBELET_CONFIG" case addBatchAndRelateDemand --payload '{"libraryId":323600757682245,"parentNodeId":326087293272133,"marsCaseGptDTOS":[{"name":"agent-folderAdd目录下新增用例-20260710","priority":"P1","steps":{"type":"text","text":{"description":"在新建目录下新增用例","expected_results":"用例新增成功"}}}],"relateDemandIds":[101782]}'
```

返回示例：`cubelet --config "$CUBELET_CONFIG" case addBatchAndRelateDemand --payload ...`

```json
{
  "data": {
    "caseCount": 1,
    "libraryId": 323600757682245,
    "parentNodeId": 326087293272133,
    "relateDemandIds": [
      101782
    ]
  },
  "error": "",
  "ok": true
}
```

Agent 取值：

- `data.libraryId`：本次写入的用例库 ID，例如 `323600757682245`
- `data.parentNodeId`：本次写入的目录节点 ID，例如 `326087293272133`
- `data.caseCount`：本次新增用例数量
- `data.relateDemandIds`：本次关联需求 ID 列表

注意：返回里没有新建 case ID；如果后续必须拿 case ID，需要通过其他查询能力按用例库/目录/名称再查。

## `import`

- `--projectId`：必传；用于映射 Mantis 请求头 `spaceid`
- `--file`：必传；本地文件路径，只支持 `.xlsx` 和 `.xmind`
- `--library`：必传；目标用例库 ID，使用 Mars 返回的字符串 ID

注意：

- 这是写命令，会实际向目标用例库写入用例
- 执行前必须确认用户明确要导入文件
- 当前只支持**同步导入**
- 当前**不支持**：`--parent`、`--dry-run`、`--async`、`case import status`

示例：

```bash
cubelet --config "$CUBELET_CONFIG" case import --projectId 8143 --file ./cases.xlsx --library 323600757682245
cubelet --config "$CUBELET_CONFIG" case import --projectId 8143 --file ./login.xmind --library 323600757682245
```

返回示例：

```json
{
  "data": {
    "format": "excel",
    "imported": 12,
    "libraryId": "323600757682245"
  },
  "error": "",
  "ok": true
}
```

Agent 取值：

- `data.libraryId`：目标用例库 ID
- `data.format`：导入格式，`excel` 或 `xmind`
- `data.imported`：成功导入数量
