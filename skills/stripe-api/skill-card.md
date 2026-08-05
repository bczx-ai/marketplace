## Description: <br>
Stripe API integration with managed OAuth for administering customers, subscriptions, invoices, products, prices, and payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer Stripe resources through Maton-managed OAuth, including customers, subscriptions, invoices, products, prices, payments, and refunds. It is intended for users who need Stripe administration and can verify account context before write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact Stripe financial actions such as charges, refunds, invoice finalization or payment, payment method changes, deletions, and subscription changes. <br>
Mitigation: Require explicit user confirmation that shows the exact endpoint, target resource, object IDs, amounts, test/live mode, and expected financial effect before any write action. <br>
Risk: Requests may be sent to the wrong Stripe account when multiple Maton connections exist or a default connection is used. <br>
Mitigation: Verify the intended Maton-Connection account before each request and include the Maton-Connection header for Stripe API calls. <br>
Risk: Broad OAuth access or stale connections can expose sensitive financial data and administrative capabilities. <br>
Mitigation: Use the least-privileged Stripe or Maton connection available, prefer test mode where possible, and revoke unused connections promptly. <br>


## Reference(s): <br>
- [Stripe skill on ClawHub](https://clawhub.ai/byungkyu/skills/stripe-api) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton](https://maton.ai) <br>
- [API Gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>
- [Stripe API Reference](https://docs.stripe.com/api) <br>
- [Stripe Dashboard](https://dashboard.stripe.com/) <br>
- [Stripe Testing](https://docs.stripe.com/testing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, JavaScript, HTTP endpoint examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Maton-managed Stripe OAuth connection.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
