---
name: shared
description: "Use when agent 需要使用 Cubelet CLI 的共享前置说明，包括配置、服务连通性、全局 flag、输出格式和读写安全规则。"
metadata:
  version: 0.1.1
  openclaw:
    category: "devops"
    requires:
      bins:
        - cubelet
    cliHelp: "cubelet --help"
---

# cubelet - Shared Reference

## 安装 cubelet

cubelet 安装方式：

```bash
npm install -g @agents/cubelet --registry=https://codebase.zhonganinfo.com/api/v4/packages/npm/
```

## 前置条件

- `cubelet` 默认按常规用户配置目录读取配置文件。
- 优先读取 `$XDG_CONFIG_HOME/cube/config.yaml`；如果 `XDG_CONFIG_HOME` 未设置，则读取 `~/.config/cube/config.yaml`。
- 只有在拿不到 home 目录等极少数场景下，才回退到相对路径 `conf/config.yaml`。
- 如需使用非默认配置，始终通过 `--config <PATH>` 显式指定。
- 当前实现依赖配置中的 `cubelet.server_url`、`x-usercenter-session`、`x-service-name`、轮询超时等字段。
- `cube-api-server` 必须可访问；如果服务不可达，命令会返回网络或连接错误。

## 认证与配置

当前二进制暴露的命令集中没有 `login` / `logout`。认证上下文通过配置文件提供，而不是运行时交互登录。

常见字段：

- `cubelet.server_url`：`cube-api-server` 地址
- `cubelet.front_url`：Cube 前端地址；当 `BRAIN_SESSION_ID` 存在且非空时，发布相关命令会通过 `brain-workspace-server session-artifacts --payload ...` 上报发布单页面链接
- `cubelet.x-usercenter-session`：当前用户会话
- `cubelet.x-service-name`：服务名请求头
- `cubelet.request_timeout`：单次请求超时，单位秒
- `cubelet.poll_interval`：轮询间隔，单位秒
- `cubelet.poll_timeout`：等待发布终态的超时，单位秒

## 全局 Flags

| Flag | 说明 |
|------|------|
| `--config <PATH>` | 指定配置文件路径 |
| `--quiet` | 关闭进度输出，适合脚本调用 |
| `--output <json\|raw>` | 输出格式，默认 `json`；`raw` 主要用于日志命令 |
| `--help-format <json\|text>` | 根命令帮助输出格式 |

## 命令分组

```bash
cubelet <group> <command> [flags]
```

当前主要能力分组：

- `publish`：创建发布单、快速发布、查询状态
- `config`：配置创建、查询、版本管理
- `workflow`：执行当前流程阶段、读取流程日志
- `container`：容器服务详情与日志
- `vmapp`：虚拟机应用详情与日志
- `case`：Mantis 测试管理，用例库查询/创建、目录树、目录新增、批量新增用例并关联需求、Excel/XMind 导入
- `codeTask`：代码扫描任务查询、创建、执行、状态/结果/日志读取与停止
- `artifactTask`：制品扫描任务查询、执行、状态/结果/日志读取与停止

## 读写安全规则

以下命令会修改系统状态，执行前必须向用户确认：

- `cubelet publish quick`
- `cubelet publish create`
- `cubelet workflow run`
- `cubelet config create`
- `cubelet config create-version`
- `cubelet case libraryAdd`
- `cubelet case folderAdd`
- `cubelet case addBatchAndRelateDemand`
- `cubelet case import`
- `cubelet codeTask create`
- `cubelet codeTask run`
- `cubelet codeTask stop`
- `cubelet artifactTask create`
- `cubelet artifactTask run`
- `cubelet artifactTask stop`
- `cubelet team createissue`
- `cubelet team updateissue`
- `cubelet team uploadfile`

以下命令默认视为只读：

- `cubelet publish status`
- `cubelet config list`
- `cubelet config versions`
- `cubelet workflow logs`
- `cubelet container inspect`
- `cubelet container logs`
- `cubelet vmapp inspect`
- `cubelet vmapp logs`
- `cubelet case librarySearch`
- `cubelet case folderTree`
- `cubelet codeTask list`
- `cubelet codeTask status`
- `cubelet codeTask result`
- `cubelet codeTask log`
- `cubelet artifactTask list`
- `cubelet artifactTask status`
- `cubelet artifactTask result`
- `cubelet artifactTask log`
- `cubelet team kanbanlist`
- `cubelet team kanbandatas`
- `cubelet team projectlist`
- `cubelet team projectmenus`
- `cubelet team parentandchildren`
- `cubelet team iterationlist`
- `cubelet team getissue`
- `cubelet team issuedetail`
- `cubelet team fieldoptions`
- `cubelet team userlist`
- `cubelet team tasktypelist`

## 使用约定

- 默认优先使用 `--output json`，便于后续解析。
- 只有在明确需要原始日志文本时，才对日志类命令使用 `--output raw`。
- 多行配置内容优先使用 `--file` 或 `--config-file`，不要把大段 YAML 直接塞进命令行。
- 使用 `--config-content`、`--data` 这类内联内容时，注意 shell 引号转义。

## 快速自检

```bash
cubelet --help
cubelet publish --help
cubelet config --help
```
