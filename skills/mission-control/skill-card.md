## Description: <br>
Mission Control is a Kanban-style task management dashboard for AI assistants that lets users manage work items through a CLI or dashboard UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdsthomas](https://clawhub.ai/user/rdsthomas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent operators use Mission Control to set up and operate a GitHub-backed Kanban workflow where tasks, subtasks, comments, status changes, webhook events, and cron controls coordinate agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles broad GitHub credentials for repository and dashboard operations. <br>
Mitigation: Use a dedicated least-privilege GitHub token, avoid shared browser profiles, and review setup steps before allowing repository writes. <br>
Risk: Webhook exposure and persistent agent wakeups can trigger automated agent work from task changes. <br>
Mitigation: Configure a real webhook secret, restrict dashboard and repository access, and review tasks before moving them into an execution state. <br>
Risk: Cron control and gateway access can affect recurring automation. <br>
Mitigation: Install only when a webhook-driven automation system is intended, protect gateway tokens, and limit who can access the dashboard and gateway. <br>
Risk: The optional CORS proxy can increase exposure if published broadly. <br>
Mitigation: Avoid exposing the CORS proxy publicly and use it only for the documented cross-origin setup that requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rdsthomas/skills/mission-control) <br>
- [README](README.md) <br>
- [Mission Control Skill Reference](SKILL.md) <br>
- [How Mission Control Works](docs/HOW-IT-WORKS.md) <br>
- [Prerequisites](docs/PREREQUISITES.md) <br>
- [Gateway Setup Guide](docs/gateway-setup.md) <br>
- [Troubleshooting](docs/TROUBLESHOOTING.md) <br>
- [Mission Control Configuration Reference](assets/examples/CONFIG-REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and code or file references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, task-management, troubleshooting, and configuration guidance for an agent-operated dashboard workflow.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
