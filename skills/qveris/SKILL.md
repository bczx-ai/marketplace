---
name: qveris
displayName: "Qveris"
description: "通过 QVeris API 搜索并执行动态工具，需要时查找并调用外部 API/工具（如天气、搜索、数据检索、股票交易分析等），需提供 QVERIS_API_KEY 环境变量。"
version: 0.1.0
tags:
  - ai_agent
license: "Unknown"
---

# QVeris Tool Search & Execution

QVeris provides dynamic tool discovery and execution - search for tools by capability, then execute them with parameters.

## Setup

Requires environment variable:
- `QVERIS_API_KEY` - Get from https://qveris.ai

## Quick Start

### Search for tools
```bash
uv run scripts/qveris_tool.py search "weather forecast API"
```

### Execute a tool
```bash
uv run scripts/qveris_tool.py execute openweathermap_current_weather --search-id <id> --params '{"city": "London", "units": "metric"}'
```

## Script Usage

```
scripts/qveris_tool.py <command> [options]

Commands:
  search <query>     Search for tools matching a capability description
  execute <tool_id>  Execute a specific tool with parameters

Options:
  --limit N          Max results for search (default: 5)
  --search-id ID     Search ID from previous search (required for execute)
  --params JSON      Tool parameters as JSON string
  --max-size N       Max response size in bytes (default: 20480)
  --json             Output raw JSON instead of formatted display
```

## Workflow

1. **Search**: Describe the capability needed (not specific parameters)
   - Good: "weather forecast API"
   - Bad: "get weather for London"

2. **Select**: Review tools by `success_rate` and `avg_execution_time`

3. **Execute**: Call tool with `tool_id`, `search_id`, and `parameters`

## Example Session

```bash
# Find weather tools
uv run scripts/qveris_tool.py search "current weather data"

# Execute with returned tool_id and search_id
uv run scripts/qveris_tool.py execute openweathermap_current_weather \
  --search-id abc123 \
  --params '{"city": "Tokyo", "units": "metric"}'
```

## Use Cases

- **Weather Data**: Get current weather, forecasts for any location
- **Stock Market**: Query stock prices, historical data, earnings calendars
- **Search**: Web search, news retrieval
- **Data APIs**: Currency exchange, geolocation, translations
- **And more**: QVeris aggregates thousands of API tools
