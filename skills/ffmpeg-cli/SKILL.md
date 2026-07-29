---
name: ffmpeg-cli
displayName: "FFmpeg CLI"
description: "使用 FFmpeg 命令行处理视频和音频，进行转码、剪切、合并、提取音频、生成缩略图、制作 GIF、调整速度、应用滤镜、添加字幕和水印。"
version: 1.0.0
tags:
  - design_multimedia
license: "Unknown"
---

# FFmpeg CLI

## Quick Reference

| Task | Command |
|------|---------|
| Cut video | `{baseDir}/scripts/cut.sh -i <input> -s <start> -e <end> -o <output>` |
| Merge clips | `{baseDir}/scripts/merge.sh -o <output> <file1> <file2> ...` |
| Extract audio | `{baseDir}/scripts/extract-audio.sh -i <video> -o <output.mp3>` |
| Generate thumbnail | `{baseDir}/scripts/thumb.sh -i <video> -t <timestamp> -o <out.jpg>` |
| Create GIF | `{baseDir}/scripts/gif.sh -i <video> -s <start> -e <end> -o <out.gif>` |
| Convert format | `{baseDir}/scripts/convert.sh -i <input> -o <output.mp4>` |
| Change speed | `{baseDir}/scripts/speed.sh -i <input> -r <0.5-2.0> -o <output>` |
| Add watermark | `{baseDir}/scripts/watermark.sh -i <video> -w <image> -o <output>` |

## Scripts

### cut.sh - Cut video segment
```bash
{baseDir}/scripts/cut.sh -i video.mp4 -s 00:01:30 -e 00:02:45 -o clip.mp4
```

### merge.sh - Concatenate videos
```bash
{baseDir}/scripts/merge.sh -o merged.mp4 part1.mp4 part2.mp4 part3.mp4
```

### extract-audio.sh - Pull audio track
```bash
{baseDir}/scripts/extract-audio.sh -i video.mp4 -o audio.mp3
```

### thumb.sh - Extract frame as image
```bash
{baseDir}/scripts/thumb.sh -i video.mp4 -t 00:00:15 -o frame.jpg
```

### gif.sh - Convert clip to GIF
```bash
{baseDir}/scripts/gif.sh -i video.mp4 -s 00:00:10 -e 00:00:15 -o clip.gif
```

### convert.sh - Transcode to new format
```bash
{baseDir}/scripts/convert.sh -i input.avi -o output.mp4
```

### speed.sh - Adjust playback speed
```bash
{baseDir}/scripts/speed.sh -i video.mp4 -r 2.0 -o fast.mp4  # 2x speed
{baseDir}/scripts/speed.sh -i video.mp4 -r 0.5 -o slow.mp4  # 0.5x speed
```

### watermark.sh - Overlay image watermark
```bash
{baseDir}/scripts/watermark.sh -i video.mp4 -w logo.png -o output.mp4
```

## Notes

- All scripts support common video formats (mp4, avi, mov, mkv, webm, etc.)
- Output quality is optimized for balanced file size and clarity
- Use `-h` or no args to see script usage
