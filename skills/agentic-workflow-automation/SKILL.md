---
name: agentic-workflow-automation
displayName: "Agentic Workflow Automation"
description: "生成可重用的多步智能体工作流蓝图。用于触发/动作编排、确定性工作流定义及自动化交接。"
version: 0.1.0
tags:
  - ai_agent
license: "Unknown"
---

# Agentic Workflow Automation

## Overview

Build workflow blueprints that can be translated into automation platforms such as n8n or internal orchestrators.

## Workflow

1. Define workflow name, trigger, and ordered steps.
2. Normalize each step into a simple execution contract.
3. Build a blueprint with dependencies and execution order.
4. Export JSON/markdown artifacts for implementation.

## Use Bundled Resources

- Run `scripts/generate_workflow_blueprint.py` for deterministic workflow output.
- Read `references/workflow-blueprint-guide.md` for step design guidance.

## Guardrails

- Keep each step single-purpose.
- Include clear fallback behavior for failed steps.
