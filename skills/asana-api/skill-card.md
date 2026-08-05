## Description: <br>
Asana API integration with managed OAuth for accessing tasks, projects, workspaces, users, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Asana work items, track projects, inspect workspace and user data, and integrate Asana workflows through Maton-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers access to an Asana account through Maton and uses MATON_API_KEY for authentication. <br>
Mitigation: Install only when the publisher and Maton broker are trusted, keep MATON_API_KEY out of logs, and verify authentication state before use. <br>
Risk: Write actions can create, update, or delete Asana resources, including tasks, projects, workspaces, users, and webhooks. <br>
Mitigation: Confirm the target resource and intended effect with the user before any create, update, delete, or webhook operation. <br>
Risk: Webhook targets can send Asana event data to external or private endpoints. <br>
Mitigation: Use only intentional, reachable webhook targets and avoid private or internal URLs unless that exposure is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/asana-api) <br>
- [API Gateway Skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Asana API Documentation](https://developers.asana.com) <br>
- [Asana API Reference](https://developers.asana.com/reference) <br>
- [Asana LLM Reference](https://developers.asana.com/llms.txt) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Code, Configuration] <br>
**Output Format:** [Markdown with CLI, HTTP, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an authorized Asana OAuth connection.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
