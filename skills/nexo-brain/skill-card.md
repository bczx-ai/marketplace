## Description: <br>
Runtime core for NEXO Desktop. Provides local memory, Deep Sleep, Evolution support-ticket mode, skills, watchdog, and MCP tools for the desktop product. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wazionapps](https://clawhub.ai/user/wazionapps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and NEXO Desktop users use this skill to install the NEXO runtime, configure its local MCP server, and enable local memory, session continuity, watchdog, and support-ticket workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an external runtime that provides a local MCP server. <br>
Mitigation: Install only when the NEXO Desktop runtime and MCP integration are intended for the workflow, and review the npm package source before use. <br>
Risk: The runtime stores persistent local memory and may create support or improvement tickets. <br>
Mitigation: Review NEXO privacy behavior and retention settings so local memory and ticket handling match the user's expectations. <br>


## Reference(s): <br>
- [NEXO Desktop homepage](https://nexo-desktop.com) <br>
- [ClawHub skill page](https://clawhub.ai/wazionapps/skills/nexo-brain) <br>
- [npm package](https://www.npmjs.com/package/nexo-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance for installing an external local runtime and configuring a local MCP server.] <br>

## Skill Version(s): <br>
7.38.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
