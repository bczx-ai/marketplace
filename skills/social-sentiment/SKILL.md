---
name: social-sentiment
displayName: "Social Sentiment"
description: "针对Twitter、Reddit和Instagram的品牌与产品情感分析。监控舆情，追踪品牌声誉，检测公关危机，大规模提取投诉与赞扬——支持分析超7万条帖子，提供批量CSV导出与Python/pandas处理。基于超15亿条索引帖子驱动的社交聆听与品牌监控工具。"
version: "1.4.0"
tags:
  - data_analysis
license: "Unknown"
---

# Social Sentiment

**Analyze brand sentiment from live social conversations at scale.**

Surfaces themes, flags viral complaints, compares competitors. Analyzes 1K-70K posts via bulk CSV + Python.

## Setup

Run `xpoz-setup` skill. Verify: `mcporter call xpoz.checkAccessKeyStatus`

## 4-Step Process

### Step 1: Search Platforms

Queries: (1) `"Brand"` (2) `"Brand" AND (slow OR buggy)` (3) `"Brand" AND (love OR amazing)`

```bash
mcporter call xpoz.getTwitterPostsByKeywords query='"Notion"' startDate="YYYY-MM-DD"
mcporter call xpoz.checkOperationStatus operationId="op_..." # Poll 5s
```

Repeat for Reddit/Instagram. Default: 30 days.

### Step 2: Download CSVs

Use `dataDumpExportOperationId`, poll with `checkOperationStatus` for download URL (up to 64K rows).

### Step 3: Analyze

Python/pandas:

```python
import pandas as pd
df = pd.read_csv('/tmp/twitter-sentiment.csv')

POSITIVE = ['love', 'amazing', 'best', 'recommend']
NEGATIVE = ['hate', 'terrible', 'worst', 'broken']

def classify(text):
    t = str(text).lower()
    pos = sum(1 for k in POSITIVE if k in t)
    neg = sum(1 for k in NEGATIVE if k in t)
    return 'positive' if pos>neg else ('negative' if neg>pos else 'neutral')

df['sentiment'] = df['text'].apply(classify)
```

Extract themes, find viral by engagement. Customize keywords.

### Step 4: Report

```
Sentiment: 72/100 | Posts: 14,832
😊 58% | 😠 24% | 😐 18%

Themes: Performance (2K, 81% neg), UX (1.8K, 72% pos)
Viral: [Top 10]
```

Score: Engagement-weighted, 0-100. Include insights.

## Tips

Download full CSVs | Reddit = honest | Store `data/social-sentiment/` for trends
