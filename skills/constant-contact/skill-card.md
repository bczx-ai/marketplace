## Description: <br>
Constant Contact API integration with managed OAuth for reading and administering contacts, email campaigns, contact lists, tags, custom fields, segments, bulk operations, and marketing analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, support teams, and developers use this skill to inspect and administer Constant Contact account data through Maton-managed OAuth. It supports guided read, write, bulk, campaign, and analytics workflows while requiring explicit approval before write or send actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write-capable Constant Contact actions can create, update, delete, or bulk-modify contacts, lists, tags, custom fields, segments, campaigns, and marketing analytics data. <br>
Mitigation: Default to read-only checks first, retrieve the target resource, show the exact identifiers and intended effect, and wait for explicit approval before any write or bulk action. <br>
Risk: Campaign send and schedule operations can deliver external email and may be irreversible once executed. <br>
Mitigation: Preview the campaign and verify recipients, sender address, subject, content, and schedule before requesting final confirmation. <br>
Risk: When multiple Constant Contact OAuth connections exist, an omitted connection selector can target the default account instead of the intended account. <br>
Mitigation: Use the Maton-Connection header for the intended connection, especially before any write, bulk, send, or schedule action. <br>


## Reference(s): <br>
- [ClawHub Constant Contact skill](https://clawhub.ai/byungkyu/skills/constant-contact) <br>
- [Constant Contact V3 API Overview](https://developer.constantcontact.com/api_guide/getting_started.html) <br>
- [Constant Contact API Reference](https://developer.constantcontact.com/api_reference/index.html) <br>
- [Constant Contact Technical Overview](https://developer.constantcontact.com/api_guide/v3_technical_overview.html) <br>
- [Constant Contact Contacts Overview](https://developer.constantcontact.com/api_guide/contacts_overview.html) <br>
- [Constant Contact Email Campaigns Guide](https://developer.constantcontact.com/api_guide/email_campaigns_get_started.html) <br>
- [Constant Contact Contact Lists Overview](https://v3.developer.constantcontact.com/api_guide/lists_overview.html) <br>
- [Maton API key settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline HTTP, JSON, Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and explicit user approval before write, bulk, send, or schedule operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
