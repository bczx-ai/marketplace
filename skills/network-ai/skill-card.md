## Description: <br>
Local Python orchestration skill for multi-agent workflows using a shared blackboard file, permission gating, token-budget checks, and persistent project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jovancoding](https://clawhub.ai/user/jovancoding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate local multi-agent work, share task state, gate sensitive operations, and manage project context within a trusted workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local coordination files and audit logs can contain user-provided task context, justification text, or other sensitive content. <br>
Mitigation: Install only in a trusted workspace, avoid secrets or personal data in justifications and blackboard entries, and restrict access to the local data directory. <br>
Risk: Permission grant tokens are advisory workflow signals and do not prove user or agent identity. <br>
Mitigation: Require platform authentication or human approval before honoring grants for sensitive actions such as payments, database access, or file export. <br>
Risk: Persistent project context can influence later agent behavior if untrusted content is injected. <br>
Mitigation: Review project-context.json before injecting it into an agent prompt and avoid force options unless the context source is trusted. <br>


## Reference(s): <br>
- [Network-AI homepage](https://network-ai.org) <br>
- [ClawHub skill page](https://clawhub.ai/jovancoding/skills/network-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON or markdown file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only Python scripts write coordination state, audit logs, grants, and project context files in the workspace.] <br>

## Skill Version(s): <br>
5.15.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
