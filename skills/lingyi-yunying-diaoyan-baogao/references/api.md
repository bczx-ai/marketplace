# Social Research Report API 调用契约

面向 Skill 的社媒调研报告接口：采集社媒素材 → LLM 分析 → 返回 Markdown 报告正文。

> ## ⚠️ 真实行为校正（2026-07-10 实测，与本文件下方原始文档有出入，以本节为准）
>
> 以下结论由真实 key 联调实测坐实，下方 §3–§9 为服务端原始文档（保留参考），不一致处以本节为准：
>
> 1. **创建请求体必须用嵌套 `platforms`**（对象，每平台含 `accounts`/`keywords`/`accounts_content_limit`/
>    `keywords_content_limit`）。下方 §4 表格里的扁平 `accounts:[]`/`keywords:[]`/`platforms:["douyin"]`
>    **不被接受**（422 detail 为空，已实测）。
> 2. **deferred 模式 = 创建时不传 `analysis` 字段**（省略即可）。**不要**显式传
>    `analysis:{prompt_mode:"deferred"}`，服务端会 422 拒（已实测）。deferred 流程：
>    `capturing → awaiting_prompt`（content=null，无草稿）→ resume 补 user_prompt → `analyzing → completed`。
> 3. **custom 模式 = 创建时传 `analysis:{user_prompt:...}`**（§4 第一个示例形态正确）。流程：
>    `capturing → analyzing → completed`，**不经 awaiting_prompt**，content 直返 Markdown。
> 4. **resume body 只认 `{"user_prompt":"..."}`**，带 `prompt_mode` 字段会被 422 拒。
>    resume 仅对 `awaiting_prompt` 状态的任务有效；对运行中任务返 409「not resumable」。
> 5. **stage 真实枚举**：`capturing` / `analyzing`（内部别名 GENERATING_REPORT）/ `awaiting_prompt`
>    / `completed` / `failed`。`completed` 时 `next_action=done`、`content` 有值。
> 6. **422 响应 detail 永远为 null**（不告诉你缺哪个字段），需对照本节 1/2/4 自查。
> 7. 鉴权层正常（带 key GET 返业务 404，不带 key 返 401）；URL 必须含 `/services` 前缀：
>    `https://claw.lingyishuke.com/services/api/v1/social-analytics/social-research-report`。
> 8. **skill 侧不动用外部 LLM 网关**（zeroone01/OpenRouter 与本服务是独立鉴权，不认 LY_API_KEY）。
>    所有 LLM 工作（现造分析+生成报告）由服务端用其自有 key 完成，skill 只需 LY_API_KEY。

## 1. 接口列表

前缀：`/api/v1/social-analytics/social-research-report`

```text
POST   /                              创建任务
GET    /{task_id}                     查询任务
POST   /{task_id}/resume              继续任务（补充 prompt）
POST   /{task_id}/retry               重试失败任务
```

返回的 `task_id` 用于后续轮询、继续、重试。

## 2. 鉴权

```http
Authorization: <API_KEY>
```

兼容 `Bearer ` 前缀。`POST /` 和 `POST /{task_id}/resume` 还需 `Content-Type: application/json`。

创建、继续、重试前校验账号余额，可用点数须大于 0，否则 **402**。

## 3. 响应格式

成功时 `data` 结构：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `task_id` | string | 任务 ID |
| `status` | string | 底层状态 |
| `stage` | string | **优先看这个** |
| `next_action` | string | **决定下一步动作** |
| `content` | string \| null | 完成后的 Markdown 报告正文 |
| `error_message` | string \| null | 失败原因 |
| `warning_message` | string \| null | 非阻断警告 |

优先看 `stage` 和 `next_action`，不要只用 `status=COMPLETED` 判断可读。

### 3.1 stage / next_action

| stage | 说明 |
| --- | --- |
| `capturing` | 采集中 |
| `awaiting_prompt` | 采集完成，等待补充 prompt |
| `analyzing` | 生成报告中 |
| `completed` | 完成，可读 `content` |
| `failed` | 失败 |

| next_action | 动作 |
| --- | --- |
| `poll` | 继续 GET 轮询 |
| `resume` | 调 `/resume` |
| `retry` | 可调 `/retry` |
| `done` | 读取 `content` |

完成条件：`stage=completed` 且 `next_action=done`。

## 4. 创建任务

```http
POST /api/v1/social-analytics/social-research-report
```

### 请求体

| 字段 | 类型 | 必填 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `brand` | string | 是 | - | 品牌名 |
| `selling_points` | string \| null | 否 | null | 卖点 |
| `background_context` | string \| null | 否 | null | 背景 |
| `accounts` | string[] | 否 | `[]` | 账号来源，见下方格式 |
| `keywords` | string[] | 否 | `[]` | 搜索关键词 |
| `notes_limit` | int | 否 | `5` | 每个账号/关键词采集条数，1–20 |
| `analysis` | object \| null | 否 | null | 不传等价于先采集后补 prompt |
| `platforms` | string[] | 否 | `["douyin","wx_video"]` | 采集平台白名单 |

`accounts` 和 `keywords` 至少提供一个，采集上限：账号 ≤ 200，关键词 ≤ 200。

`analysis`：

| 字段 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- |
| `prompt_mode` | string | `deferred` | `deferred` 先采集后补 prompt；`custom` 创建时带 prompt |
| `user_prompt` | string \| null | null | 调研需求；传入后自动走 `custom` |

规则：传了 `user_prompt` 即 `custom`；`prompt_mode=custom` 时必须带 `user_prompt`。

### 示例：带 prompt 直接分析

```json
{
  "brand": "零一万物",
  "selling_points": "面向企业的 AI 原生生产力工具，强调高质量内容生成、自动化调研和私域增长",
  "background_context": "希望调研小红书/抖音/微信视频号上的 AI 工具、企业服务、内容营销相关账号与关键词，输出可用于市场策略会的社媒调研报告。",
  "platforms": {
    "douyin": {
      "accounts": [
        "AI产品经理张三",
        "企业增长研究所"
      ],
      "keywords": [
        "AI办公工具",
        "企业服务营销",
        "内容自动化"
      ],
      "accounts_content_limit": 5,
      "keywords_content_limit": 5
    },
    "wx_video": {
      "accounts": [
        "零一增长实验室",
        "B端营销观察"
      ],
      "keywords": [
        "AI营销",
        "视频号获客",
        "私域增长"
      ],
      "accounts_content_limit": 5,
      "keywords_content_limit": 5
    }
  },
  "analysis": {
    "user_prompt": "请重点分析竞品内容定位、爆款选题、用户痛点、常见转化话术，并给出我们品牌未来 30 天的内容选题建议。"
  },
  "output_format": "markdown_text"
}
```

### 示例：先采集后补 prompt

```json
{
  "brand": "示例品牌",
  "accounts": ["douyin:https://v.douyin.com/xxx"],
  "keywords": ["通勤好物"],
  "analysis": { "prompt_mode": "deferred" }
}
```

### 成功响应

```json
{
  "task_id": "ana_xxx",
  "status": "QUEUED",
  "stage": "capturing",
  "next_action": "poll",
  "content": null,
  "error_message": null,
  "warning_message": null
}
```

### 常见错误

| 状态 | 场景 |
| --- | --- |
| 400 | 无有效账号/关键词 |
| 401 | API Key 无效 |
| 402 | 余额不足 |
| 422 | 请求体校验失败 |
| 502 | 服务内部异常 |

## 5. 查询任务

```http
GET /api/v1/social-analytics/social-research-report/{task_id}
```

### 等待 prompt

```json
{
  "task_id": "ana_xxx",
  "status": "PENDING",
  "stage": "awaiting_prompt",
  "next_action": "resume",
  "content": null
}
```

### 完成

```json
{
  "task_id": "ana_xxx",
  "status": "COMPLETED",
  "stage": "completed",
  "next_action": "done",
  "content": "# 社媒调研报告\n\n..."
}
```

`content` 仅在 `stage=completed` 时有值。

## 6. 继续任务

```http
POST /api/v1/social-analytics/social-research-report/{task_id}/resume
```

仅当 `next_action=resume` 时调用。复用已采集数据，不重新采集。

```json
{
  "user_prompt": "请基于采集素材输出调研报告，重点分析爆款选题、平台差异和执行建议。"
}
```

成功后 `stage=analyzing`，`next_action=poll`，继续轮询。

## 7. 重试任务

```http
POST /api/v1/social-analytics/social-research-report/{task_id}/retry
```

无 body。仅当 `next_action=retry` 时调用。

`stage=awaiting_prompt` 时不能 retry，应调 `/resume`。

## 8. 推荐调用流程

1. `POST /` 创建，保存 `task_id`
2. 循环 `GET /{task_id}`（间隔 3–10 秒），按 `next_action` 行动：
   - `poll` → 继续轮询
   - `resume` → `POST /{task_id}/resume`
   - `retry` → 按需 `POST /{task_id}/retry`
   - `done` → 读取 `content`
3. 完成条件：`stage=completed` 且 `next_action=done`

## 9. curl 示例

```bash
curl -X POST "$BASE_URL/api/v1/social-analytics/social-research-report" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "示例品牌",
    "accounts": ["douyin:雅培官方"],
    "keywords": ["通勤好物"],
    "notes_limit": 5,
    "analysis": { "user_prompt": "分析内容机会和执行建议。" }
  }'

curl "$BASE_URL/api/v1/social-analytics/social-research-report/$TASK_ID" \
  -H "Authorization: $API_KEY"

curl -X POST "$BASE_URL/api/v1/social-analytics/social-research-report/$TASK_ID/resume" \
  -H "Authorization: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_prompt":"请输出调研报告，重点分析爆款选题和执行建议。"}'

curl -X POST "$BASE_URL/api/v1/social-analytics/social-research-report/$TASK_ID/retry" \
  -H "Authorization: $API_KEY"
```