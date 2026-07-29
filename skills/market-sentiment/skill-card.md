## Description: <br>
Market Sentiment analyzes CSV market breadth, trend, volume, and emotion data to produce a 0-100 sentiment score, market state, and planner suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cqdev-ai](https://clawhub.ai/user/cqdev-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to score market sentiment from selected CSV market data, inspect dimension breakdowns and trends, and pass a market-state parameter into stock-planner workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market state, position, threshold, or planner suggestions may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis aids and make investment decisions only after independent review. <br>
Risk: The analyzer can write JSON to a user-specified --output path. <br>
Mitigation: Review output paths before running commands to avoid overwriting or placing files in unintended locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cqdev-ai/skills/market-sentiment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-formatted sentiment reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes user-provided CSV market data; can write JSON output when an --output path is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
