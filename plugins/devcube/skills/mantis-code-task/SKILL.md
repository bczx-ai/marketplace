---
name: mantis-code-task
description: "Cubelet：Mantis 代码扫描任务能力，包括查看、创建、执行、查询状态/结果/日志和停止任务。"
metadata:
  version: 0.1.0
  openclaw:
    category: "qa"
    domain: "mantis"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet codeTask --help"
---

# codeTask

> **PREREQUISITE:** 先阅读 `../shared/SKILL.md`，确认配置文件、全局 flag 和写操作安全规则。

```bash
cubelet codeTask <command> [flags]
```

## Commands

使用前提：

- `cube-api-server` 所在配置中已设置 `cube_api_server.mantis_url`
- 当前会话已具备可访问 Mantis 的登录态
- `list`、`status`、`result`、`log` 是只读命令
- `create`、`run`、`stop` 是写命令，执行前必须确认用户明确要创建、触发或停止扫描任务

| Command | 说明 |
|---------|------|
| `list` | 查看当前会话可见的手动创建代码扫描任务，固定只查 `from=web`，支持按任务名称模糊查询 |
| `create` | 创建代码扫描任务并返回任务基础信息 |
| `run` | 触发已有代码扫描任务执行 |
| `status` | 查询任务执行状态，支持指定执行历史 ID |
| `result` | 查询任务扫描结果，支持指定执行历史 ID |
| `log` | 查询执行日志 |
| `stop` | 停止任务最近一次执行 |

## `list`

常用参数：

- `--name`：非必传；任务名称模糊查询

注意：

- 该命令固定只查询手动创建任务，对应下游查询条件 `from=web`
- 不返回流水线或其他来源自动生成的扫描任务

返回字段：

- `taskId`
- `appId`
- `name`
- `branch`
- `mode`
- `pdfGen`
- `commitBaseId`
- `commitCompareId`

示例：

```bash
cubelet codeTask list
cubelet codeTask list --name login
```

输出示例：

```json
[
  {
    "taskId": 3001,
    "appId": "1001",
    "name": "login-scan",
    "branch": "feature/login",
    "mode": "increment",
    "pdfGen": true,
    "commitBaseId": "1a2b3c4d",
    "commitCompareId": "5e6f7g8h"
  }
]
```

## `create`

常用参数：

- `--app-id`：必传
- `--name`：必传
- `--branch`：必传
- `--mode`：必传；只支持 `total` 或 `increment`
- `--generate-pdf`：非必传；默认 `false`
- `--base-commit-id`：仅 `mode=increment` 时必传
- `--compare-commit-id`：仅 `mode=increment` 时必传

注意：

- 这是写命令，会在 Mantis 中创建新的代码扫描任务
- 增量扫描必须同时提供 `base-commit-id` 和 `compare-commit-id`
- 返回值是任务基础信息，不只返回 `taskId`

示例：

```bash
cubelet codeTask create \
  --app-id 1001 \
  --name login-scan \
  --branch feature/login \
  --mode increment \
  --base-commit-id 1a2b3c4d \
  --compare-commit-id 5e6f7g8h \
  --generate-pdf=true
```

输出示例：

```json
{
  "taskId": 3001,
  "appId": "1001",
  "name": "login-scan",
  "branch": "feature/login",
  "mode": "increment",
  "pdfGen": true,
  "commitBaseId": "1a2b3c4d",
  "commitCompareId": "5e6f7g8h"
}
```

## `run`

常用参数：

- `--task-id`：必传

注意：

- 这是写命令，会实际触发已有扫描任务执行
- 执行时完全复用任务中已保存的 `mode`、`branch`、`commitBaseId`、`commitCompareId`
- CLI 不再暴露覆盖参数，避免把任务定义和任务执行拆成两套状态
- 返回的 `status` 为 Neptune/数据库里的原始数值状态码，直接透传，不做文本翻译

示例：

```bash
cubelet codeTask run --task-id 3001
```

输出示例：

```json
{
  "taskId": 3001,
  "execHisId": 8899,
  "status": 2,
  "statusName": "执行成功",
  "message": "scan task accepted"
}
```

## `status`

常用参数：

- `--task-id`：必传
- `--his-id`：非必传；执行历史 ID，不传时 Neptune 使用最近一次执行

注意：

- 下游真实接口是 `GET /rick/api/scanTask/overview/{taskId}`
- 这里没有统一 `runId`，不要编造一层不存在的映射
- 返回的 `status` 为 Neptune 原始数值状态码
- `reportUrl` 由 Mantis 下游直接返回，CLI 不自行拼接

示例：

```bash
cubelet codeTask status --task-id 3001
cubelet codeTask status --task-id 3001 --his-id 8899
```

输出示例：

```json
{
  "taskId": 3001,
  "hisId": 8899,
  "mode": "increment",
  "status": 1,
  "statusName": "进行中",
  "statusMsg": "进行中",
  "taskName": "login-scan",
  "appName": "login",
  "branch": "feature/login",
  "commitBaseId": "1a2b3c4d",
  "commitCompareId": "5e6f7g8h",
  "reportUrl": "https://devcube.example/magic/codeScan/task/historyDetail?taskId=3001&hisId=8899&tab=scanResult&taskName=login-scan&appName=login",
  "pdfUrl": "https://devcube.example/api/pdfreport/get?componentKey=login"
}
```

## `result`

常用参数：

- `--task-id`：必传
- `--his-id`：非必传；执行历史 ID，不传时 Neptune 使用最近一次执行

注意：

- 下游真实接口同样是 `GET /rick/api/scanTask/overview/{taskId}`
- 该命令只做字段收口，不额外翻译质量门禁状态

示例：

```bash
cubelet codeTask result --task-id 3001 --his-id 8899
```

输出示例：

```json
{
  "taskId": 3001,
  "hisId": 8899,
  "mode": "increment",
  "status": 2,
  "statusName": "执行成功",
  "statusMsg": "执行成功",
  "summary": {
    "blocker": 1,
    "critical": 5,
    "major": 12,
    "minor": 28
  },
  "qualityGates": 2,
  "qualityGatesColumn": "未通过",
  "reportUrl": "https://devcube.example/magic/codeScan/task/historyDetail?taskId=3001&hisId=8899&tab=scanResult&taskName=login-scan&appName=login",
  "pdfUrl": "https://devcube.example/api/pdfreport/get?componentKey=login"
}
```

## `log`

常用参数：

- `--his-id`：必传；执行历史 ID

注意：

- 下游真实接口是 `GET /rick/api/scanTask/history/logs/{hisId}`
- 需要纯日志文本时使用 `--output raw`

示例：

```bash
cubelet codeTask log --his-id 8899
cubelet --output raw codeTask log --his-id 8899
```

输出示例：

```json
{
  "hisId": 8899,
  "status": 2,
  "statusName": "执行成功",
  "log": "scan log...",
  "osskey": "b3Nz"
}
```

## `stop`

常用参数：

- `--task-id`：必传

注意：

- 这是写命令，会停止任务最近一次执行
- 下游真实接口是 `POST /rick/api/scanTask/task/stop/{id}/scan`

示例：

```bash
cubelet codeTask stop --task-id 3001
```

输出示例：

```json
{
  "taskId": 3001,
  "status": "stopping",
  "message": "stop request accepted"
}
```
