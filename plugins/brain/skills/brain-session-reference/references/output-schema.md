# brain-session-reference 输出 Schema

列表模式：

```ts
interface TurnsListOutput {
  session: {
    projectId: string;
    sessionId: string;
    title: string;
    engine?: "claude" | "codex" | "acp";
    createdAt: number;
    lastMessageAt?: number;
  };
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
    nextPage: number | null;
  };
  turns: Array<{
    number: number;
    userMessageId: string;
    timestamp: number;
    preview: string;
    outcome?: "completed" | "stopped" | "failed";
  }>;
}
```

详情模式：

```ts
interface TurnDetailOutput {
  session: TurnsListOutput["session"];
  turn: {
    number: number;
    detail: "dialogue" | "visible" | "full";
    userMessageId: string;
    startedAt: number;
    outcome?: "completed" | "stopped" | "failed";
  };
  messages: Array<{
    id: string;
    role: "user" | "assistant" | "tool_call" | "tool_result" | "system" | "summary";
    timestamp: number;
    content: string;
    images?: Array<{ id: string; fileName?: string; mediaType: string }>;
    toolName?: string;
    toolInput?: Record<string, unknown>;
    toolResult?: Record<string, unknown>;
    toolError?: boolean;
    thinking?: string;
  }>;
}
```

输出永远不包含图片 `data`。Owner、runtime、lease、token/cost、trace 和引擎私有字段都不属于任一输出。
