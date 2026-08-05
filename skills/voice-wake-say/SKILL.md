---
name: voice-wake-say
displayName: "Voice Wake Say"
description: "在 macOS 上，当用户输入表明语音唤醒/语音识别（例如，以 “User talked via voice recognition on <device>” 开头的消息）时，使用内置的 `say` 命令朗读回复。"
version: 1.0.1
tags:
  - design_multimedia
license: "Unknown"
---

# Voice Wake Say

## Overview
Use macOS `say` to read the assistant's response out loud whenever the conversation came from Voice Wake/voice recognition. Do **not** use the `tts` tool (it calls cloud providers).

## When to Use `say` (CHECK EVERY MESSAGE INDIVIDUALLY)

**IF** the user message STARTS WITH: `User talked via voice recognition`
- **Step 1:** Acknowledge with `say` first (so the user knows you heard them)
- **Step 2:** Then perform the task
- **Step 3:** Optionally speak again when done if it makes sense

**IF** the user message does NOT start with that exact phrase
- THEN: Do NOT use `say`. Text-only response only.

**Critical:**
- Check EACH message individually — context does NOT carry over
- The trigger phrase must be at the VERY START of the message
- For tasks that take time, acknowledge FIRST so the user knows you're working

## Workflow
1) Detect Voice Wake context
- Trigger ONLY when the latest user/system message STARTS WITH `User talked via voice recognition`
- If the message instructs "repeat prompt first", keep that behavior in the response.

2) Prepare spoken text
- Use the final response text as the basis.
- Strip markdown/code blocks; if the response is long or code-heavy, speak a short summary and mention that details are on screen.

3) Speak with `say` (local macOS TTS)
```bash
printf '%s' "$SPOKEN_TEXT" | say
```

Optional controls (use only if set):
```bash
printf '%s' "$SPOKEN_TEXT" | say -v "$SAY_VOICE"
printf '%s' "$SPOKEN_TEXT" | say -r "$SAY_RATE"
```

## Failure handling
- If `say` is unavailable or errors, still send the text response and note that TTS failed.
