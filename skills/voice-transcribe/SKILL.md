---
name: voice-transcribe
displayName: "Voice Transcribe"
description: "使用 OpenAI 的 gpt-4o-mini-transcribe 模型转录音频文件，支持词汇提示和文本替换，需安装 uv（https://docs.astral.sh/uv/）。"
version: 1.0.1
tags:
  - design_multimedia
license: "Unknown"
---

# voice-transcribe

transcribe audio files using openai's gpt-4o-mini-transcribe model.

## when to use

when receiving voice memos (especially via whatsapp), just run:
```bash
uv run /Users/darin/clawd/skills/voice-transcribe/transcribe <audio-file>
```
then respond based on the transcribed content.

## fixing transcription errors

if darin says a word was transcribed wrong, add it to `vocab.txt` (for hints) or `replacements.txt` (for guaranteed fix). see sections below.

## supported formats

- mp3, mp4, mpeg, mpga, m4a, wav, webm, ogg, opus

## examples

```bash
# transcribe a voice memo
transcribe /tmp/voice-memo.ogg

# pipe to other tools
transcribe /tmp/memo.ogg | pbcopy
```

## setup

1. add your openai api key to `/Users/darin/clawd/skills/voice-transcribe/.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```

## custom vocabulary

add words to `vocab.txt` (one per line) to help the model recognize names/jargon:
```
Clawdis
Clawdbot
```

## text replacements

if the model still gets something wrong, add a replacement to `replacements.txt`:
```
wrong spelling -> correct spelling
```

## notes

- assumes english (no language detection)
- uses gpt-4o-mini-transcribe model specifically
- caches by sha256 of audio file
