---
name: recipe-ship-troubleshoot-publish
description: "定位发布失败或超时问题，按状态、流程日志、容器日志和 vmapp 日志逐层排查。"
metadata:
  version: 0.1.0
  openclaw:
    category: "recipe"
    domain: "devops"
    requires:
      bins:
        - cubelet
      skills:
        - ship-publish
        - ship-workflow
        - ship-container
        - ship-vmapp
---

# Troubleshoot a Publish

> **PREREQUISITE:** 执行该 recipe 前加载 `ship-publish`、`ship-workflow`、`ship-container`、`ship-vmapp`。

按“状态 -> 流程日志 -> 运行态日志”的顺序排查发布异常。

## Steps

1. 先查总体状态：`cubelet publish status --id PUBLISH_ID --env ENV`
2. 如果失败点在代码编译、打包、流程阶段，读取流程日志：`cubelet workflow logs --publish-id PUBLISH_ID --output raw`
3. 如果状态里已经给出服务名，容器应用继续查：`cubelet container inspect --name SERVICE_NAME --env ENV`
4. 容器应用需要运行态日志时执行：`cubelet container logs --name SERVICE_NAME --env ENV --output raw`
5. 虚拟机应用继续查：`cubelet vmapp inspect --name SERVICE_NAME --env ENV`
6. 需要虚拟机日志时执行：`cubelet vmapp logs --name SERVICE_NAME --env ENV --output raw`
7. 只有在用户明确要求“重试当前阶段”时，才执行：`cubelet workflow run --publish-id PUBLISH_ID`

## Decision Rules

- 先读状态和日志，不要一上来就重跑流程
- 看构建/流程问题优先 `workflow logs`
- 看部署后访问或实例问题优先 `container inspect` / `vmapp inspect`
- 看运行态报错优先 `container logs` / `vmapp logs`

> [!CAUTION]
> `cubelet workflow run` 是写操作，只能在用户明确允许重试时执行。
