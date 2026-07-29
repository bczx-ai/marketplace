## Description: <br>
Square API integration with managed OAuth for administering supported Square resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Square administrators use this skill to inspect and manage supported Square resources including locations, merchants, payments, refunds, customers, orders, catalog, inventory, invoices, team members, loyalty, checkout links, cards, payouts, bank accounts, and terminal checkouts. It is intended for users who need Square administration and can apply least-privileged OAuth scopes and explicit approval for write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform sensitive Square business and financial changes when directed. <br>
Mitigation: Require explicit confirmation before any payment, refund, customer, order, catalog, invoice, card, terminal, or other write operation, including the exact endpoint, account, resource ID, and expected consequence. <br>
Risk: Broad Square OAuth scopes or the wrong connected account could expose or change more data than intended. <br>
Mitigation: Use the least-privileged Square account and OAuth scopes available, verify the Maton connection ID before actions, and revoke unused connections promptly. <br>
Risk: Exposure of MATON_API_KEY could allow unauthorized use of the integration. <br>
Mitigation: Keep MATON_API_KEY secret, do not log or share it, and rotate it immediately if compromised. <br>


## Reference(s): <br>
- [ClawHub Square Skill](https://clawhub.ai/byungkyu/skills/squareup) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [Square API Overview](https://developer.squareup.com/docs) <br>
- [Square API Reference](https://developer.squareup.com/reference/square) <br>
- [Square Payments API](https://developer.squareup.com/reference/square/payments-api) <br>
- [Square Orders API](https://developer.squareup.com/reference/square/orders-api) <br>
- [Square Catalog API](https://developer.squareup.com/reference/square/catalog-api) <br>
- [Square Inventory API](https://developer.squareup.com/reference/square/inventory-api) <br>
- [Square Invoices API](https://developer.squareup.com/reference/square/invoices-api) <br>
- [Square Terminal API](https://developer.squareup.com/reference/square/terminal-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API endpoint examples, JSON request bodies, and Python or JavaScript code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Square OAuth connection; write operations require explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
