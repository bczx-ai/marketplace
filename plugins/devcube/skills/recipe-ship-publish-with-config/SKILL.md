---
name: recipe-ship-publish-with-config
description: "发布应用时附带配置文件或内联配置，并在需要时独立维护配置版本。"
---

# Publish with Config

> **PREREQUISITE:** 执行该 recipe 前加载 `ship-publish`、`ship-config`。

在发布时附带配置，或先独立管理配置再发布。

## Steps

1. 如果配置是多行文本，优先准备本地文件，如 `./application.yaml`
2. 预览发布请求：`cubelet --config "$CUBELET_CONFIG" publish quick --app APP --branch BRANCH --env ENV --config-file ./application.yaml --config-label application.yaml --dry-run`
3. 需要真正发布时，执行：`cubelet --config "$CUBELET_CONFIG" publish quick --app APP --branch BRANCH --env ENV --config-file ./application.yaml --config-label application.yaml --wait`
4. 如果只想建单不立即执行，把上一步改成：`cubelet --config "$CUBELET_CONFIG" publish create --app APP --branch BRANCH --env ENV --config-file ./application.yaml --config-label application.yaml`
5. 若用户想独立维护配置生命周期，先创建配置：`cubelet --config "$CUBELET_CONFIG" config create --app APP --env ENV --file ./application.yaml --label application.yaml`
6. 后续变更配置内容时，创建新版本：`cubelet --config "$CUBELET_CONFIG" config create-version --config-id CONFIG_ID --file ./application.yaml`

## Notes

- 使用 `--config-file` 或 `--config-content` 时，必须带 `--config-label`
- 多行 YAML/Properties 内容优先走文件，不要把大段内容直接塞进命令行
- `publish` 和 `config create*` 都是写操作，执行前需要确认
