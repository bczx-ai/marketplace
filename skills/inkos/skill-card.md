## Description: <br>
InkOS is a story creation and translation AI agent with Studio Chat, CLI, and TUI support for long-form fiction, short fiction, scripts, storyboards, interactive projects, fan works, covers, research-assisted writing, and multilingual EPUB/PDF/TXT/Markdown translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[narcooo](https://clawhub.ai/user/narcooo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, translators, and creative-tooling agents use InkOS to plan, generate, revise, audit, translate, and export narrative projects while preserving persistent story state and review artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags anti-detect rewriting as a misuse concern. <br>
Mitigation: Use InkOS for legitimate drafting, editing, translation, and review workflows; do not use anti-detect mode to bypass AI-content detection or integrity checks. <br>
Risk: InkOS can store manuscripts, project settings, logs, memory, and service secrets on disk. <br>
Mitigation: Keep project directories private, prefer environment-variable based secrets, and treat Studio service settings and local secret files as sensitive. <br>
Risk: Custom or aggregator provider URLs can receive API keys and project content. <br>
Mitigation: Configure only trusted provider endpoints and avoid untrusted proxy base URLs. <br>
Risk: Studio provides a local web interface with project access. <br>
Mitigation: Keep Studio bound to localhost and do not expose its port through a proxy. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/narcooo/skills/inkos) <br>
- [InkOS homepage](https://github.com/Narcooo/inkos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and structured CLI guidance with shell command examples, JSON-capable command results, and generated project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include manuscripts, translations, review reports, prompts, images when providers are configured, exports, state files, logs, and local Studio/TUI interactions.] <br>

## Skill Version(s): <br>
2.7.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
