## Description: <br>
Google Merchant Center API integration with managed OAuth for reading and administering products, inventories, data sources, promotions, account settings, conversions, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect and manage Google Merchant Center resources through a Maton-authenticated connection. It is intended for Merchant Center administration workflows that may include read operations, reporting, and explicitly approved writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Merchant Center writes can affect live products, inventory, promotions, account settings, and conversions. <br>
Mitigation: Require explicit user approval with specific account and resource identifiers before any create, update, or delete operation. <br>
Risk: Requests may target the wrong Merchant Center account or connection. <br>
Mitigation: Verify the account ID and use the intended connection before approving writes, especially when multiple Google Merchant connections exist. <br>
Risk: The MATON_API_KEY can expose access to connected Merchant Center workflows if mishandled. <br>
Mitigation: Store MATON_API_KEY as a secret, keep it out of logs and chats, rotate it if compromised, and revoke unused Maton or Google connections. <br>
Risk: Overbroad Google Merchant permissions can increase business impact if an agent action is approved incorrectly. <br>
Mitigation: Use least-privilege Merchant Center access and default to read-only checks before proposing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/skills/google-merchant) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Google Merchant API overview](https://developers.google.com/merchant/api/overview) <br>
- [Google Merchant API reference](https://developers.google.com/merchant/api/reference/rest) <br>
- [Products guide](https://developers.google.com/merchant/api/guides/products/overview) <br>
- [Data sources guide](https://developers.google.com/merchant/api/guides/data-sources/overview) <br>
- [Reports guide](https://developers.google.com/merchant/api/guides/reports/overview) <br>
- [Product data specification](https://support.google.com/merchants/answer/7052112) <br>
- [Maton settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, JavaScript, HTTP, and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an authorized Google Merchant Center connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
