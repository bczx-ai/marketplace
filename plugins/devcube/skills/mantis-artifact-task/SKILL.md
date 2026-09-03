---
name: mantis-artifact-task
description: "用于操作 Cubelet Mantis 制品扫描任务，包括 artifactTask list、run、status、result、log、stop。"
metadata:
  version: 0.2.0
  openclaw:
    category: "qa"
    domain: "mantis"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet artifactTask --help"
---

# artifactTask

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和读写安全规则。

```bash
cubelet artifactTask <command> [flags]
```

## 真实接口

不要造 `runId`，不要在 CLI 拼报告地址。

| 命令 | 下游接口 | 说明 |
|------|----------|------|
| `list` | `GET /neptune/v1/task/list` | 固定 `q=taskFrom=web`，内部翻页聚合 |
| `create` | `POST /neptune/v1/task` | 创建手动制品扫描任务，复杂字段使用下游 JSON 结构 |
| `run` | `POST /neptune/v1/task/{id}/exec` | 返回下游 `execId` |
| `status` | `GET /neptune/v1/task/{id}/{eid}` | 透传任务状态和下游报告地址 |
| `result` | `GET /neptune/v1/execHis/{id}/detail` | `id` 是 `execId`，内部翻页聚合制品明细 |
| `log` | `GET /neptune/v1/execHis/{id}/detail/log` | `id` 是 `detailId`，不是 `execId` |
| `stop` | `POST /neptune/v1/task/{id}/abort` | 停止任务 |

## 安全规则

- `create`、`run` 和 `stop` 会改变系统状态，执行前必须让用户明确确认。
- `list`、`status`、`result`、`log` 是只读命令。
- 日志原文用 `--output raw`；默认 JSON 更适合机器解析。

## 状态码

| 数值 | 中文名称 |
|------|----------|
| 0 | 待执行 |
| 1 | 进行中 |
| 2 | 执行成功 |
| 3 | 执行失败 |
| 4 | 质量门禁通过 |
| 5 | 质量门禁未通过 |
| 其他 | 未知 |

## Commands

| Command | 说明 |
|---------|------|
| `list` | 查看当前会话可见的手动创建制品扫描任务 |
| `create` | 创建手动制品扫描任务 |
| `run` | 执行已有制品扫描任务，返回 `execId` |
| `status` | 用 `taskId + execId` 查询执行状态 |
| `result` | 用 `execId` 查询本次执行的制品结果 |
| `log` | 用 `detailId` 查询单个制品日志 |
| `stop` | 用 `taskId` 停止任务 |

## 示例

### list

```bash
cubelet artifactTask list
cubelet artifactTask list --name login
```

```json
[
  {
    "taskId": 6001,
    "name": "login-image-scan",
    "productType": "Docker",
    "taskFrom": "web",
    "repoInstanceId": "harbor-prod",
    "planId": 7001,
    "planName": "默认漏洞扫描",
    "scanRange": 1,
    "lastExecId": 8001,
    "lastTaskStatusCode": 2,
    "lastTaskStatus": "执行成功"
  }
]
```

### create

`scan-range=2` 扫描仓库最新制品，必须传 `repo-info`；`scan-range=1` 指定制品，必须传 `product-list`。

```bash
cubelet artifactTask create \
  --name login-image-scan \
  --repo-instance-id harbor-prod \
  --plan-id 7001 \
  --product-type Docker \
  --scan-range 2 \
  --repo-info '[{"name":"devcube"}]'
```

```json
{
  "taskId": 6001,
  "name": "login-image-scan",
  "productType": "Docker",
  "taskFrom": "web",
  "repoInstanceId": "harbor-prod",
  "planId": 7001,
  "scanRange": 2,
  "lastTaskStatusCode": 0,
  "lastTaskStatus": "待执行"
}
```

### run

```bash
cubelet artifactTask run --task-id 6001
```

```json
{
  "taskId": 6001,
  "execId": 8001,
  "message": "artifact scan task accepted"
}
```

### status

```bash
cubelet artifactTask status --task-id 6001 --exec-id 8001
```

```json
{
  "taskId": 6001,
  "execId": 8001,
  "name": "login-image-scan",
  "lastTaskStatusCode": 1,
  "lastTaskStatus": "进行中",
  "scanProductCount": 3,
  "reportUrl": "https://devcube.example/magic/productScan/task/6001/8001"
}
```

### result

```bash
cubelet artifactTask result --exec-id 8001
```

```json
{
  "execId": 8001,
  "products": [
    {
      "detailId": 9001,
      "taskId": 6001,
      "execId": 8001,
      "repoName": "devcube",
      "productName": "login",
      "productVersion": "1.0.0",
      "statusCode": 2,
      "statusName": "执行成功"
    }
  ]
}
```

### log

```bash
cubelet artifactTask log --detail-id 9001
cubelet --output raw artifactTask log --detail-id 9001
```

```json
{
  "detailId": 9001,
  "status": 1,
  "statusName": "进行中",
  "log": "artifact log...",
  "osskey": "b3Nz"
}
```

### stop

```bash
cubelet artifactTask stop --task-id 6001
```

```json
{
  "taskId": 6001,
  "status": "stopping",
  "message": "stop request accepted"
}
```
