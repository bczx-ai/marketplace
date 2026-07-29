## Description: <br>
Researches the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search to produce a ranked, clustered brief with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use Last30days to gather recent social, market, code, and web evidence for trend scans, competitor comparisons, launch reactions, and person or company profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, profile targets, handles, and retrieved snippets may be sent to AISA and public-source APIs. <br>
Mitigation: Use the skill only with data approved for those services, configure AISA_API_KEY deliberately, and restrict sources when needed. <br>
Risk: Workspace or parent .claude/last30days.env files can affect API keys, source selection, and runtime behavior. <br>
Mitigation: Review local configuration files before running the skill and set LAST30DAYS_CONFIG_DIR when a separate configuration location is needed. <br>
Risk: Optional YouTube transcript enrichment can make direct YouTube requests. <br>
Mitigation: Leave LAST30DAYS_YOUTUBE_TRANSCRIPTS disabled unless direct YouTube transcript fetching is acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/last30days) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API Reference](https://aisa.one/docs/api-reference) <br>
- [AIsa Model Guide](https://aisa.one/docs/guides/models) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON] <br>
**Output Format:** [Markdown brief by default, or structured JSON with query plan, ranked candidates, clusters, per-source items, provider runtime, and source errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save a requested Markdown or JSON file when --save-dir is used; fail-soft output may include source-level errors.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
