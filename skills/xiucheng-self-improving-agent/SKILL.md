---
name: xiucheng-self-improving-agent
displayName: Self Improving Agent
description: 自我改进的智能体系统，分析对话质量，识别改进机会，持续优化回复策略。
version: 1.0.0
tags:
  - ai_agent
license: MIT
---

# Self-Improving Agent

An intelligent self-improvement system for OpenClaw agents that analyzes conversation quality and continuously optimizes performance.

## Features

- 📊 **Quality Analysis**: Evaluates conversation effectiveness
- 🎯 **Improvement Tracking**: Identifies areas for enhancement
- 📝 **Learning Log**: Records insights and lessons learned
- 📈 **Weekly Reports**: Generates improvement summaries
- 🔄 **Strategy Optimization**: Adapts response patterns over time

## Installation

```bash
clawhub install self-improving-agent
```

## Usage

### Automatic Analysis
The skill automatically analyzes conversations after each session.

### Manual Improvement Logging
```python
from self_improving import SelfImprovingAgent

sia = SelfImprovingAgent()
sia.log_improvement("Need to be more concise in technical explanations")
```

### Generate Weekly Report
```python
report = sia.generate_weekly_report()
print(report)
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| improvement_log | ./improvement_log.md | Learning log file |
| soul_file | ./SOUL.md | Personality anchor file |
| auto_analyze | true | Auto-analyze conversations |

## Integration

Works best with:
- `memory-manager`: For tracking improvement history
- Custom agent personalities (SOUL.md)

## License

MIT License - Help agents get better every day!
