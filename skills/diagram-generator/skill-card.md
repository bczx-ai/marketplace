## Description: <br>
Generate and edit Draw.io, Mermaid, and Excalidraw diagrams through the mcp-diagram-generator MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewyin](https://clawhub.ai/user/matthewyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to create or revise architecture, network topology, flowchart, swimlane, UML, data model, and whiteboard diagrams for documentation, presentations, and collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the mcp-diagram-generator MCP server and may run it through npx when configured that way. <br>
Mitigation: Review the MCP server configuration before use and approve the package source expected for the environment. <br>
Risk: The skill can create .diagram-config.json and diagram output files in the workspace. <br>
Mitigation: Use it in workspaces where diagram configuration and generated files are expected, and review generated paths before committing changes. <br>


## Reference(s): <br>
- [Format Selection Guide](references/format-selection-guide.md) <br>
- [Interactive Intake Guide](references/interaction-intake-guide.md) <br>
- [JSON Schema Guide](references/json-schema-guide.md) <br>
- [Layout And Quality Guide](references/layout-quality-guide.md) <br>
- [Network Topology Examples](references/network-topology-examples.md) <br>
- [Architecture Diagram Playbook](references/playbook-architecture.md) <br>
- [Excalidraw Playbook](references/playbook-excalidraw.md) <br>
- [Flowchart Playbook](references/playbook-flowchart.md) <br>
- [Network Topology Playbook](references/playbook-network-topology.md) <br>
- [Swimlane Playbook](references/playbook-swimlane.md) <br>
- [UML And Data Model Playbook](references/playbook-uml.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON diagram specifications, configuration snippets, and generated .drawio, .mmd, or .excalidraw files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May initialize .diagram-config.json and write diagram outputs under configured workspace directories.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
