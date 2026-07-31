---
name: brain-diagnose
description: Diagnose Brain failures from local runtime logs and Session transcript size metadata, then generate a redacted Markdown support report. Use when a user reports Brain crashes, startup or blank-screen failures, Agent/session/tool/terminal/login/update/message-channel errors, slow or oversized long-running Sessions, repeated timeouts, or asks for root-cause analysis or a report for Brain developers. Run only when the user explicitly invokes $brain-diagnose; never invoke it implicitly from symptoms alone.
---

# Brain Diagnose

Diagnose Brain itself. Do not use this Skill for ordinary build failures or bugs in the user's project unless the evidence shows that Brain caused them.

## Workflow

1. Capture the user's symptom, visible error, affected workflow, approximate occurrence time, and reproduction steps from the current message. Do not invent missing details or block on them.
2. Choose the smallest useful lookback window:
   - Use 24 hours when no occurrence time is given.
   - Include at least one hour before and after a known incident.
   - Never exceed 168 hours. Ask for a narrower occurrence time only if a seven-day result is still ambiguous.
3. Collect the bounded evidence summary:

```bash
brain-workspace-server diagnostics --since-hours 24 --max-events 160
```

4. Analyze only the returned JSON and the user's symptom. The command may inspect Session transcript file size and modification time, but never its content. Do not open raw Brain logs, `config.toml`, `auth.json`, Session JSON content, terminal history, or project files to compensate for missing evidence.
5. Read [the report template](references/report-template.md), then generate the final report in the user's language. Default to Chinese.
6. Write the report under the current project as `.brain-diagnostics/brain-diagnostic-YYYYMMDD-HHMMSS.md`.
7. Register the report as a Session file artifact with `brain-workspace-server session-artifacts`. Use a stable non-empty id, a `file://` URI for the absolute report path, and `text/markdown` as the MIME type.
8. Return the leading conclusion, confidence level, and report path. Do not attach or expose raw logs.

## Analysis Rules

- Build a causal chain from the symptom to relevant events. Time proximity alone is not causation.
- Mark the conclusion as `已确认` only when an explicit terminal error or complete causal chain explains the symptom.
- Mark it as `高概率` when multiple consistent signals support one cause but a decisive event is absent.
- Mark it as `证据不足` when logs are absent, truncated, outside the window, contradictory, or unrelated to the symptom.
- Treat expected shutdown signals, disconnect errors adjacent to a normal shutdown, and unrelated updater/network warnings as background unless they explain the reported symptom.
- Treat `sessionTranscripts` as a separate health signal:
  - `search-excluded` means a transcript is larger than 5 MiB and Brain's current message search skips it.
  - `high-risk` means a transcript is larger than 25 MiB; current load, save, and metadata updates may incur costly whole-file reads, JSON parsing, serialization, and atomic rewrites.
  - A large transcript is not a confirmed root cause by size alone. Correlate it with Session open/save/search/refresh/resume latency, timeouts, memory pressure, disk pressure, or matching log errors.
  - Prefer `sessionTranscripts.current` when the user reports a problem in the current Session. It is present only after a complete scan uniquely matches the runtime Session id. Never infer a Session id from anonymous `transcript-*` refs.
  - Treat `scanTruncated=true` or transcript warnings as partial metadata. Disclose the limitation and do not infer that an unlisted large transcript is absent.
- Cite event ids such as `evt-004`; include only the shortest excerpt needed for the conclusion and no more than 12 evidence items.
- Preserve alternatives that remain plausible. State exactly what evidence would distinguish them.
- Separate user workarounds from developer remediation. Do not modify Brain, user configuration, credentials, processes, or project files beyond the report unless the user separately asks for a fix.

## Privacy And Failure Handling

- Treat the collector output as already reduced, not automatically safe to reproduce verbatim. Remove user content, command bodies, unnecessary paths, identifiers, emails, headers, and query values from the report.
- Never include environment-variable dumps, secrets, tokens, cookies, private keys, auth files, config contents, raw Session messages, Session/project ids, or complete raw log files.
- If `collection.truncated` is true, disclose that the evidence is partial. Do not silently raise command limits beyond the documented maximum.
- If the diagnostics command fails or returns no relevant events, still create a report with `证据不足`, the collector failure or empty scope, and the minimal next evidence needed.
- If artifact registration fails, keep the project-local report and state that registration failed.
- Do not upload the report, create an issue, or contact an external system automatically. The user controls onward delivery to Brain developers.

See [the evidence schema](references/evidence-schema.md) when interpreting collection limits, sources, or empty results.
