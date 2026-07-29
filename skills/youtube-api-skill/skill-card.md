## Description: <br>
YouTube Data API integration with managed OAuth for searching videos, managing playlists, accessing channel data, and interacting with comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to work with YouTube through Maton-managed OAuth, including searches, channel and video lookups, playlists, comments, subscriptions, and account-scoped write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton-managed OAuth can perform account-changing YouTube actions such as playlist, comment, subscription, rating, and deletion operations. <br>
Mitigation: Install only if you trust Maton to broker OAuth access, confirm the intended YouTube connection before use, and approve write actions only after checking the exact target and effect. <br>


## Reference(s): <br>
- [ClawHub YouTube Skill](https://clawhub.ai/byungkyu/skills/youtube-api-skill) <br>
- [YouTube Data API Overview](https://developers.google.com/youtube/v3) <br>
- [YouTube Data API Search](https://developers.google.com/youtube/v3/docs/search/list) <br>
- [YouTube Data API Playlists](https://developers.google.com/youtube/v3/docs/playlists) <br>
- [YouTube Data API Comments](https://developers.google.com/youtube/v3/docs/comments) <br>
- [YouTube Data API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with CLI commands, API endpoint examples, code snippets, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected YouTube OAuth account.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
