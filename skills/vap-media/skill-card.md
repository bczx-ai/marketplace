## Description: <br>
VAP Media API skill for image, video, music, and media editing through VAP using VAP product keys with current Media API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elestirelbilinc-sketch](https://clawhub.ai/user/elestirelbilinc-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images, videos, and music, and to edit or enhance media through VAP Media API endpoints with a VAP API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and generated or edited media are sent to VAP's external service. <br>
Mitigation: Use this skill only when VAP Media API processing is intended, and avoid private prompts, proprietary media URLs, or sensitive images, audio, or video unless that processing is acceptable under the user's VAP account and API key. <br>
Risk: The skill requires a bearer API key for VAP Media API access. <br>
Mitigation: Store VAP_API_KEY securely, pass it through the environment, and avoid exposing it in shared prompts, logs, shell history, or user-visible output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elestirelbilinc-sketch/skills/vap-media) <br>
- [VAP Developer Hub](https://vapagent.com/developer/) <br>
- [VAP Media API Key](https://vapagent.com/developer/?key=media#keys) <br>
- [VAP Room and Media Plans](https://vapagent.com/new-dashboard/?billing=monthly#plans) <br>
- [VAP AI](https://vapagent.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and VAP_API_KEY; returns media URLs after polling VAP generation or operation endpoints.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
