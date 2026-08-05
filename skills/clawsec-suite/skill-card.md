## Description: <br>
ClawSec suite manager with embedded advisory-feed monitoring, cryptographic signature verification, approval-gated malicious-skill response, and guided setup for additional security skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
AGPL-3.0-or-later <br>


## Use Case: <br>
Developers and security operators use this skill to monitor ClawSec advisories for OpenClaw skill installs, verify signed advisory and feed artifacts, set up optional hook or cron checks, and run guarded skill installs that require explicit approval for risky actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable persistent OpenClaw advisory monitoring through a hook or optional cron job. <br>
Mitigation: Review the setup preflight output and enable hook or cron automation only when persistent monitoring is intended. <br>
Risk: Advisory checks fetch remote feed and catalog metadata unless local paths are pinned. <br>
Mitigation: Use the signed feed and checksum verification defaults, and pin local feed paths when remote access is not desired. <br>
Risk: Unsigned feed mode weakens feed verification. <br>
Mitigation: Use CLAWSEC_ALLOW_UNSIGNED_FEED only as a temporary migration bypass and restore signed-feed verification promptly. <br>
Risk: The suite may recommend removal or block installation when advisories match installed or requested skills. <br>
Mitigation: Keep destructive responses approval-gated and require explicit second confirmation after advisory details are shown. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/davida-ps/skills/clawsec-suite) <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawSec skill catalog](https://clawsec.prompt.security/skills/index.json) <br>
- [ClawSec advisory feed](https://clawsec.prompt.security/advisories/feed.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce advisory-match alerts, setup instructions, and approval-gated install or removal guidance.] <br>

## Skill Version(s): <br>
0.1.16 (source: SKILL.md frontmatter, artifact/skill.json, CHANGELOG released 2026-07-14, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
