---
name: kokoro-tts
displayName: "Kokoro TTS"
description: "使用本地Kokoro TTS引擎将文本转换为语音。当用户要求“说”某些内容、请求语音消息或希望将文本转为语音时使用。"
version: 0.1.0
tags:
  - design_multimedia
license: "Unknown"
---

# Kokoro TTS

This skill allows you to generate high-quality AI speech using a local or remote Kokoro-TTS instance.

## Configuration

The skill uses the `KOKORO_API_URL` environment variable to locate the API.

- **Default:** `http://localhost:8880/v1/audio/speech`
- **To Configure:** Add `KOKORO_API_URL=http://your-server:port/v1/audio/speech` to your `.env` file or environment.

## Usage

To generate speech, run the included Node.js script.

### Command

```bash
node skills/kokoro-tts/scripts/tts.js "<text>" [voice] [speed]
```

- **text**: The text to speak. Wrap in quotes.
- **voice**: (Optional) The voice ID. Defaults to `af_heart`.
- **speed**: (Optional) Speech speed (0.25 to 4.0). Defaults to `1.0`.

### Example

```bash
node skills/kokoro-tts/scripts/tts.js "Hello Ed, this is Theosaurus speaking." af_nova
```

### Output

The script will output a single line starting with `MEDIA:` followed by the path to the generated MP3 file. OpenClaw will automatically pick this up and send it as an audio attachment.

Example Output:
`MEDIA: media/tts_1706745000000.mp3`

## Available Voices

Common choices:
- `af_heart` (Default, Female, Warm)
- `af_nova` (Female, Professional)
- `am_adam` (Male, Deep)
- `bf_alice` (British Female)

For a full list, see [references/voices.md](references/voices.md) or query the API.
