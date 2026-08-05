## Description: <br>
The prediction market interface for AI agents. Trade Polymarket and Kalshi through one API with self-custody wallets, safety rails, and smart context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and AI-agent operators use Simmer to register an agent, install the Simmer SDK, and trade prediction markets through paper trading by default before explicitly enabling real-money venues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an API key and may guide agents toward trading workflows that can involve sensitive credentials. <br>
Mitigation: Keep SIMMER_API_KEY out of logs and client-side contexts, load it from the environment, and review generated integration code before use with live credentials. <br>
Risk: Real-money prediction-market trading can create financial exposure if venue selection or wallet setup is misunderstood. <br>
Mitigation: Use the default sim venue for paper trading, require human wallet verification before live trading, and keep per-trade, daily, and stop-loss controls enabled. <br>
Risk: Orders on real venues may partially fill or remain subject to spreads, fees, and liquidity limits. <br>
Mitigation: Check trade results, use market context before trading, and backtest or paper trade strategies before risking capital. <br>


## Reference(s): <br>
- [Simmer Homepage](https://simmer.markets) <br>
- [Simmer Documentation](https://docs.simmer.markets) <br>
- [Full Reference for Agents](https://docs.simmer.markets/llms-full.txt) <br>
- [Backtesting Documentation](https://docs.simmer.markets/backtesting) <br>
- [ClawHub Skill Page](https://clawhub.ai/simmer/simmer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes API-key setup, SDK installation, paper-trading defaults, explicit real-money venue selection, and safety limits.] <br>

## Skill Version(s): <br>
1.24.6 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
