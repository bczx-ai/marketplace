---
name: habit-tracker
displayName: "Habit Tracker"
description: "结合打卡、提醒与进度可视化养成习惯"
version: 1.0.0
tags:
  - office_productivity
license: "Unknown"
---

# Habit Tracker

Build lasting habits through conversation. Track streaks, get reminders, celebrate progress.

## What it does

Creates and tracks daily/weekly habits, maintains streak counts, sends optional reminders, and visualizes your progress over time. Simple accountability through your AI assistant.

## Usage

**Create habits:**
```
"New habit: meditate daily"
"Track reading 30 minutes"
"Add habit: gym 3x per week"
```

**Log completions:**
```
"Did meditation"
"Completed reading"
"Hit the gym today"
```

**Check progress:**
```
"How are my habits?"
"Meditation streak"
"Weekly habit summary"
```

**Set reminders:**
```
"Remind me to meditate at 7am"
"Habit reminder at 9pm"
```

## Habit Types

- **Daily**: Must complete every day for streak
- **Weekly**: Complete X times per week
- **Custom**: Define your own cadence

## Streak Rules

- Miss a day = streak resets (daily habits)
- Miss weekly target = week doesn't count
- Say "skip [habit] today" to pause without breaking streak (limited uses)

## Tips

- Start with 1-2 habits, add more as they stick
- Ask "habit insights" for pattern analysis
- Say "archive [habit]" to stop tracking without deleting history
- Morning check: "What habits do I need to do today?"
- All data stored locally
