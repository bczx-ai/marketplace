---
name: devcube
description: "通过 DevCube查询团队项目，并操作发布、配置、运行状态、监控、测试与扫描任务。"
---

# DevCube

所有 DevCube 命令都直接调用 Brain 公共 `PATH` 中的原生 CLI：

```bash
cubelet --config "$CUBELET_CONFIG" <group> <command> [flags]
```

Brain 会根据当前用户已连接的 DevCube App 生成配置文件，并在新 Session 中注入 `CUBELET_CONFIG`。所有命令都必须使用该路径；变量缺失时提示用户先完成 App 连接，不要自行创建、修改、读取或输出认证配置。

## 发现命令

先按需读取当前服务暴露的命令，再选择具体能力：

```bash
cubelet --config "$CUBELET_CONFIG" --help-format json
cubelet --config "$CUBELET_CONFIG" publish --help
cubelet --config "$CUBELET_CONFIG" trace --help
```

主要命令组：

- 发布与配置：`publish`、`config`、`workflow`
- 运行状态：`container`、`vmapp`
- 监控排障：`health`、`jvm`、`log`、`node`、`pod`、`trace`
- 测试与扫描：`case`、`codeTask`、`artifactTask`
- 团队协作：`team`（项目、迭代、事项和看板查询，以及事项创建、更新和文件上传）
- 质量工程：`mantis-test-design`、`mantis-case-generate`、`mantis-auto-generate`、`mantis-auto-run`（写入 `.brain-quality` 与 `tests/**`，不替代上述 CLI 命令组）

## 常用调用

```bash
cubelet --config "$CUBELET_CONFIG" publish status --id 10001 --env dev
cubelet --config "$CUBELET_CONFIG" workflow logs --publish-id 10001
cubelet --config "$CUBELET_CONFIG" container inspect --name demo-service --env dev
cubelet --config "$CUBELET_CONFIG" pod list --app demo-service --start 1776043865402 --end 1776045665402 --env dev
cubelet --config "$CUBELET_CONFIG" log system --app demo-service --start 1776043865402 --end 1776045665402 --level ERROR --env dev
cubelet --config "$CUBELET_CONFIG" codeTask list --name demo-service
cubelet --config "$CUBELET_CONFIG" team projectlist --query 支付 --currentPage 1 --pageSize 20
```

命令输出固定为 JSON envelope：

```json
{"ok":true,"data":{},"error":""}
```

只在 `ok` 为 `true` 时把操作视为成功。失败时向用户说明 `error`，不要猜测或伪造结果。

## 安全规则

- `publish quick`、`publish create`、`workflow run`、配置创建或更新、测试用例写入、扫描任务创建/执行/停止，以及 `team createissue`、`team updateissue`、`team uploadfile` 都属于写操作，执行前必须获得用户明确确认。
- 查询、状态、结果和日志命令可以直接执行，但要限制时间范围和返回规模。
- 文件参数只使用当前项目内的相对路径，不访问项目外文件。
- 保持默认 JSON 输出；只有用户明确要求其它格式时才传 `--output`。
- 只使用 Brain 通过 `CUBELET_CONFIG` 提供的配置文件，不把其中的 token、session 或服务地址写入对话、日志或其它文件。
