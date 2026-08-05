## Description: <br>
Salesforce CRM API integration with managed OAuth for querying, managing, and mutating Salesforce records through Maton CLI or API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM administrators use this skill to query Salesforce data, inspect sObject schemas, manage OAuth connections, and perform approved CRUD, composite, and batch operations through Maton. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate Salesforce CRM records through create, update, delete, composite, and batch operations. <br>
Mitigation: Default to SOQL or GET requests first, verify the exact connection, sObject type, record IDs, and intended effect, then require explicit approval before any write operation. <br>
Risk: MATON_API_KEY and Salesforce OAuth connections can grant access to CRM data and administrative actions. <br>
Mitigation: Use the narrowest Salesforce permissions available, keep the API key out of logs and shared files, rotate exposed keys, and revoke unused connections promptly. <br>
Risk: Batch and composite requests can affect multiple Salesforce records in a single call. <br>
Mitigation: Prefer sandbox orgs for destructive or bulk work, enumerate every affected record before execution, and use transaction controls such as allOrNone when appropriate. <br>


## Reference(s): <br>
- [ClawHub Salesforce Skill](https://clawhub.ai/byungkyu/skills/salesforce-api) <br>
- [Salesforce REST API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest.htm) <br>
- [SOQL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm) <br>
- [SOSL Reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_sosl.htm) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI, Python, JavaScript, HTTP endpoint, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Salesforce OAuth connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
