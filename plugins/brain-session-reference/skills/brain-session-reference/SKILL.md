---
name: brain-session-reference
description: 当用户消息包含 brain-session 引用或要求使用另一段 Brain 会话作为上下文时，使用本 Skill 读取被引用会话。
---

使用 `brain-workspace-server turns` 检查 Brain Session 引用，不要加载或修改来源 Session。

流程：

1. 从用户消息的 Markdown 链接中提取每个完整的 `brain-session://...` href，不要从可见链接标题推测 ID。
2. 多个引用按消息中的出现顺序处理。
3. 先列出来源 Session 的用户回合：

```bash
brain-workspace-server turns 'brain-session://project-id/encoded-session-id' --page 1 --page-size 20
```

4. 根据用户回合预览，只选择与当前请求有关的回合；相关回合尚未出现时再读取 `pagination.nextPage`。
5. 以满足任务所需的最小详细级别读取选中回合：
   - `dialogue`：用户、助手、系统和摘要正文，以及图片元数据。
   - `visible`：在 dialogue 基础上增加工具调用、参数、结果和错误；这是默认值。
   - `full`：在 visible 基础上增加已持久化的助手 thinking；只有历史推理确有必要时才使用。

```bash
brain-workspace-server turns 'brain-session://project-id/encoded-session-id' 3 --detail dialogue
```

6. 使用选中的上下文回答当前请求；除非用户明确要求，不要复述完整来源会话。

规则：

- 每个命令都是对调用时已持久化内容的只读快照。
- 来源回合可能仍在运行，读取可选 `outcome` 字段，不要假设已经完成。
- 单个引用失败时简短说明并继续处理其它引用和当前消息上下文。
- 传给 shell 时始终完整引用 Session reference。
- 精确参数见 `references/cli.md`，稳定输出字段见 `references/output-schema.md`。
