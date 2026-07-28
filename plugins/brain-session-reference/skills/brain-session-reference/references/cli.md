# brain-session-reference CLI

列出归一化用户回合：

```bash
brain-workspace-server turns '<session-reference>' --page 1 --page-size 20
```

读取一个从 1 开始计数的回合：

```bash
brain-workspace-server turns '<session-reference>' <num> --detail dialogue
brain-workspace-server turns '<session-reference>' <num> --detail visible
brain-workspace-server turns '<session-reference>' <num> --detail full
```

参数：

- `<session-reference>` 是完整 Markdown href：`brain-session://<project_id>/<encoded-session-id>`。
- `--page` 默认为 `1`，必须是不小于 `1` 的整数。
- `--page-size` 默认为 `20`，必须是 `1` 到 `100` 的整数。
- `<num>` 是可选的、从 1 开始计数的正整数；省略时进入列表模式。
- `-d, --detail` 默认为 `visible`，可选值为 `dialogue`、`visible` 和 `full`。

成功时命令向 stdout 精确输出一个 JSON 对象。失败时以非零状态退出，保持 stdout 为空，并向 stderr 写入 `turns failed:` 错误。
