## Description: <br>
Apollo provides managed Apollo.io API access for searching and enriching people and companies and managing contacts, accounts, and sales sequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and revenue-operations users use this skill through an agent to prospect, enrich leads, and manage Apollo contacts, accounts, and sequences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access business-sensitive Apollo data such as contacts, accounts, opportunities, sequences, and email data. <br>
Mitigation: Install only for agents intended to use the connected Apollo account and avoid exposing returned sales data unnecessarily. <br>
Risk: Create, update, delete, and sequence actions can change Apollo records or outreach. <br>
Mitigation: Confirm the target resource and intended effect with the user before executing write operations. <br>
Risk: Person and email enrichment may consume Apollo credits. <br>
Mitigation: Confirm enrichment requests when credit use matters and keep batch sizes intentional. <br>
Risk: Multiple active Apollo connections can route requests to the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one Apollo connection is available. <br>


## Reference(s): <br>
- [ClawHub Apollo release](https://clawhub.ai/byungkyu/skills/apollo-api) <br>
- [Apollo API Overview](https://docs.apollo.io/reference) <br>
- [Search People](https://docs.apollo.io/reference/people-api-search.md) <br>
- [Enrich Person](https://docs.apollo.io/reference/people-enrichment.md) <br>
- [Search Organizations](https://docs.apollo.io/reference/organization-search.md) <br>
- [Enrich Organization](https://docs.apollo.io/reference/organization-enrichment.md) <br>
- [Create Contact](https://docs.apollo.io/reference/create-a-contact.md) <br>
- [Apollo LLM Reference](https://docs.apollo.io/llms.txt) <br>
- [Related API Gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline HTTP, Python, JavaScript, shell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; write operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
