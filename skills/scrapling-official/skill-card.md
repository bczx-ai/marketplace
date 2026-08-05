## Description: <br>
Scrape web pages using Scrapling with anti-bot bypass, stealth headless browsing, spiders, adaptive scraping, and JavaScript rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d4vinci](https://clawhub.ai/user/d4vinci) <br>

### License/Terms of Use: <br>
BSD 3-Clause <br>


## Use Case: <br>
Developers and agents use this skill to plan and run Scrapling-based web scraping, crawling, JavaScript rendering, adaptive parsing, and spider workflows. It is intended for authorized scraping tasks where built-in web fetching is insufficient or protected/dynamic pages require Scrapling capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Anti-bot, stealth browser, proxy, and Cloudflare-related capabilities can be misused against sites where scraping is not authorized. <br>
Mitigation: Use the skill only for authorized targets, respect site terms and robots.txt, avoid paywalls or authenticated areas without permission, and prefer the least invasive fetch mode that works. <br>
Risk: Large or concurrent crawls can create excessive request volume. <br>
Mitigation: Apply crawl delays and rate limits, enable robots.txt enforcement for spiders, and keep concurrency appropriate for the target site. <br>
Risk: Scraped pages may contain prompt injection or hidden content intended to manipulate agents. <br>
Mitigation: Use AI-targeted/main-content extraction for command-line or MCP scraping workflows and review extracted content before relying on it. <br>
Risk: Persistent browser sessions, crawl checkpoints, and development caches may retain scraped content or session state locally. <br>
Mitigation: Close persistent sessions when finished and clear local crawl data or development caches that may contain sensitive or stale content. <br>


## Reference(s): <br>
- [Scrapling documentation](https://scrapling.readthedocs.io/en/latest/index.html) <br>
- [ClawHub skill page](https://clawhub.ai/d4vinci/skills/scrapling-official) <br>
- [Scrapling MCP Server](references/mcp-server.md) <br>
- [Fetchers basics](references/fetching/choosing.md) <br>
- [StealthyFetcher](references/fetching/stealthy.md) <br>
- [Getting started with spiders](references/spiders/getting-started.md) <br>
- [Proxy management and handling blocks](references/spiders/proxy-blocking.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to produce local scraping outputs such as Markdown, HTML, text, JSON, crawl checkpoints, or cached responses.] <br>

## Skill Version(s): <br>
0.4.11 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
