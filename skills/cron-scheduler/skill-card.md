## Description: <br>
Create, list, modify, and remove scheduled cron jobs to automate system tasks using simplified cron syntax and manage output logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picaye](https://clawhub.ai/user/picaye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and power users use this skill to inspect existing cron jobs and prepare scheduled task changes for recurring backups, cleanup, monitoring, notifications, and other system automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron jobs can persist scheduled commands after the conversation ends and may run with a minimal environment. <br>
Mitigation: Review the exact cron line before installation, use absolute paths, redirect output, and periodically audit or remove scheduled jobs that are no longer needed. <br>
Risk: Crontab edits can remove or alter existing scheduled tasks, especially when pattern-based deletion is used. <br>
Mitigation: Back up the current crontab, require explicit approval before applying changes, and avoid broad deletion patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/picaye/cron-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron expressions, crontab commands, log-check commands, and operational reminders for scheduled jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
