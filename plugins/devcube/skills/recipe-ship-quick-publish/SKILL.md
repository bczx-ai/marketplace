---
name: recipe-ship-quick-publish
description: "快速发布一个应用到指定环境，并在需要时等待终态或回查发布状态。"
---

# Quick Publish an Application

> **PREREQUISITE:** 执行该 recipe 前加载 [ship-publish](../ship-publish/SKILL.md)、[ship-workflow](../ship-workflow/SKILL.md)、[ship-container](../ship-container/SKILL.md)、[ship-vmapp](../ship-vmapp/SKILL.md)。

把单应用快速发布到指定环境。

## Steps

1. 如需先预览，执行：`cubelet --config "$CUBELET_CONFIG" publish quick --app APP --branch BRANCH --env ENV --dry-run`
2. 确认要真正执行后，运行：`cubelet --config "$CUBELET_CONFIG" publish quick --app APP --branch BRANCH --env ENV --wait`
3. 如果不想阻塞等待，改用：`cubelet --config "$CUBELET_CONFIG" publish quick --app APP --branch BRANCH --env ENV --wait=false`
4. 当使用 `--wait=false` 时，拿到 `publish_id` 后继续查询：`cubelet --config "$CUBELET_CONFIG" publish status --id PUBLISH_ID --env ENV`
5. 如果结果显示流程阶段失败，继续查：`cubelet --config "$CUBELET_CONFIG" workflow logs --publish-id PUBLISH_ID`
6. 如果是容器运行态问题，继续查：`cubelet --config "$CUBELET_CONFIG" container inspect --name SERVICE_NAME --env ENV` 和 `cubelet --config "$CUBELET_CONFIG" container logs --name SERVICE_NAME --env ENV`
7. 如果是虚拟机发布，改查：`cubelet --config "$CUBELET_CONFIG" vmapp inspect --name SERVICE_NAME --env ENV` 和 `cubelet --config "$CUBELET_CONFIG" vmapp logs --name SERVICE_NAME --env ENV`

> [!CAUTION]
> 这是写操作流程。除 `--dry-run` 外，其余发布命令都应在用户确认后执行。
