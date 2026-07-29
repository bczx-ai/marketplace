---
name: cnfinancialscraper
displayName: "全能金融爬虫（新增网页操作+舆情监控功能）"
description: "中国金融机构数据爬取工具 v4.4.0。全量金融机构名单（1540+家，36大类）、A股报告爬取（年报+券商研报+公告）、\n产品解析（基金/ETF/FOF/股票/债券）、新闻资讯、反爬+双语展示、金融文档分析整理。\n\n🆕 v4.4.0: 新增东方财富数据爬虫（基金净值/龙虎榜/北向资金/热门股票）、巨潮资讯官方公告爬虫、\n金融监管机构爬虫（央行/证监会/金监总局）、海外机构扩展至 250+（新增主权基金/PE/做市商）、\n文档导出全面添加原文链接、修复 12 个 Bug。\n\nv4.3.1: 全网舆情爬虫（对话式）— 用户用自然对话指定 1+ 个机构（基金公司/上市公司/地方政府/证券公司/\n银行/保险/信托/私募/外资/期货/理财子公司/金融租赁等），从权威媒体 / 财经垂直 / 地方媒体 / 自媒体 /\n国际媒体 5 大类共 48+ 站点爬取正面新闻+舆情，支持对话式触发、Word/Excel/CSV/JSON 导出、对话提示反馈、\n情感/严重度分级（4档舆情+3档利好）、定时任务（schedule_crawl_task 派发）、URL+标题双维去重、\n浏览器自动化兜底。\n\n触发词 (含 v4.4.0 新增)：爬取机构、机构名单、网页爬取、产品解析、公告下载、券商研报、批量爬取、公司批量、\n文档分析、整理文档、文档对比、基金分析、净值查询、定时爬取、自动爬取、打包ZIP、\n压缩摘要、报告生成、撰写报告、研报生成、图表生成、文件解析、金融写作、\n全网舆情、舆情监测、舆情爬取、新闻舆情、爬取正面、负面新闻、利空舆情、\n对话式舆情、增加自定义目标、舆情定时、东方财富、龙虎榜、北向资金、监管政策、\n央行政策、证监会公告、巨潮资讯、基金净值排行"
version: 1.0.28
tags:
  - data_analysis
license: "Unknown"
---

# cn-financial-scraper v4.4.0 — 全网舆情 + 金融数据 + 监管机构爬虫

> 全量机构名单 (国内1330家/27大类 + 海外250+家/12大类) | A股报告 | 券商研报 | 公告下载 | 产品解析 |
> **🆕 v4.4.0 东方财富/巨潮资讯/监管机构爬虫** | 反爬+双语展示 | 浏览器自动化 | 海外金融机构 | 金融术语翻译
>
> **v4.4.0 更新 (2026-07-28):**
> - ✅ 修复 12 个 Bug（含崩溃级 mcp_server fetch_latest、AnnouncementManager.search 缺失）
> - ✅ 新增东方财富爬虫（基金净值/龙虎榜/北向资金/热门股票）
> - ✅ 新增巨潮资讯爬虫（A 股官方公告检索）
> - ✅ 新增金融监管机构爬虫（央行/证监会/金监总局）
> - ✅ 海外机构扩展至 250+（新增主权基金 8 家、PE 8 家、做市商 7 家、监管机构 15 家）
> - ✅ 文档导出（Word/PPT/Excel）全部添加原文链接
> - ✅ 中文字体修复（Word/Excel/PPT 宋体 universal 字体）
> - ✅ 代码质量优化（删除死代码、修复重复逻辑、补充异常处理）

## 对话触发 — 一句话上手

✅ **任意 Agent 均可通过自然语言触发。无需记忆命令。**

```
帮我爬一下某上市公司最近7天的舆情
某基金公司最近3天的负面新闻，并导出 Excel
看下某基金公司今天的正面新闻并生成 Word
爬一下某基金公司、某银行、某保险公司过去3天的负面新闻
每天早上9点爬取银行板块舆情
哪些媒体可用？哪些目标？
新增自定义目标 某基金公司
看看某地方金融监督管理局过去一周的金融政策
```

> 💡 在对话窗口输入「**帮助 / help / 怎么用**」会再次展示完整指南（包含 API & MCP）。

## 一键启动（推荐零基础上手）

**Windows 用户**：直接双击 `run_sentiment.bat`，或在命令行运行：

```bash
python run_sentiment.py                          # 交互式对话
python run_sentiment.py "贵州茅台最近7天的舆情"     # 直接命令行
```

脚本会自动检测环境，缺失依赖时会提示一键安装。详见 [run_sentiment.py](run_sentiment.py)。

---

---

## 🆕 v4.3.1 全网舆情爬虫 — 功能清单

| 能力 | 说明 |
|------|------|
| **5 大媒体源，48+ 站点** | authoritative / financial_vertical / local_media / self_media / international |
| **12 大类目标机构** | 基金公司 / 上市公司 / 地方政府 / 证券公司 / 商业银行 / 保险 / 信托 / 私募 / 外资 / 期货 / 理财子公司 / 金融租赁 |
| **正面新闻 vs 舆情 分类** | 关键词驱动 + 严重度分级（4档舆情 + 3档利好）|
| **多机构单/多个** | 同时爬取多家，自动去重 |
| **多格式导出** | 对话提示 / Word / Excel / CSV / JSON |
| **对话式 API** | 自然语言 → 自动解析 intent + 参数 |
| **定时任务** | 与 v4.0 schedule_crawl_task 协同 |
| **浏览器兜底** | v4.2 browser_scraper 反爬严格时启用 |
| **数据持久化** | data/sentiment_snapshots/ 全量快照 |

---

## 🗞️ 媒体源库（按需启用）

| 类别 | 代表站点 |
|------|----------|
| **authoritative** | 人民日报 / 新华社 / 新华网财经 / 经济日报 / 中证报 / 上证报 / 证券时报 / 证券日报 / 金融时报 |
| **financial_vertical** | 财联社 / 华尔街见闻 / 第一财经 / 财新 / 21世纪经济报道 / 经济观察报 / 每日经济新闻 / 36氪 / 投中网 / 虎嗅 / 集思录 |
| **local_media** | 北京日报 / 解放日报 / 南方都市报 / 广州日报 / 深圳特区报 / 南方周末 / 扬子晚报 / 新京报 / 钱江晚报 / 中国基金报 |
| **self_media** | 新浪财经微博 / 微信公众号（搜狗） / 今日头条 / 百家号 / 雪球 / 东方财富股吧 / 知乎 / 小红书 / B站财经 / 抖音财经 |
| **international** | Reuters / Bloomberg / FT / WSJ / 路透中文 / 日经中文 / HKET 香港经济日报 |

---

## 🎯 目标机构库

| 类别 | 数量 | 关注方向 |
|------|------|---------|
| fund_company (基金公司) | 160 | 净值/分红/募集/清盘 |
| listed_company (上市公司) | 5000+ | 年报/增持/回购/退市/处罚/问询 |
| local_government (地方政府) | 11 (示例) + 自定义 | 金融政策/开放/改革 |
| securities (证券公司) | 93 | 评级/投行/承销 |
| commercial_bank (商业银行) | 250 | 利率/普惠/反洗钱/挤兑 |
| insurance (保险公司) | 72 | 理赔/销售误导 |
| trust_company (信托) | 67 | 延期兑付/规模 |
| private_fund (私募) | 64 | 清盘/跑路 |
| foreign_institution (外资) | 60 | QFII/合规 |
| futures (期货) | 117 | 穿仓/强平 |
| wealth_management (理财子) | 23 | 破净/回撤 |
| leasing_consumer_finance (租赁/消金/汽车金融) | 115 | 暴力催收/高利贷 |

---

## ⚡ 快速上手（Python）

```python
from scripts import crawl_sentiment, chat_handle, export_sentiment, SentimentChatParser

# 1) 最简单：爬取 + 导出对话
result = chat_handle("帮我爬一下某上市公司最近7天的舆情")
print(result["reply"])

# 2) 多机构 + 多类别筛选
from scripts import crawl_sentiment
snap = crawl_sentiment(
    targets=["某基金公司", "某上市公司"],
    categories=None,                              # 用 targets 优先
    source_categories=["authoritative", "financial_vertical"],
    days=7, positive_only=False, negative_only=False,
    max_articles=80,
)
print(f"共 {len(snap.articles)} 条 | 正面 {snap.positive_count()} | 舆情 {snap.negative_count()}")

# 3) 导出 Word+Excel+JSON+CSV
outputs = export_sentiment(snap, fmt="all")
for k, v in outputs.items():
    print(k, v)
```

---

## 🔧 完整 API 与 MCP 工具

### Python API（`scripts.*`）

| 函数 | 功能 |
|------|------|
| `crawl_sentiment(targets, categories, sources, source_categories, days, positive_only, negative_only, max_articles)` | 一键爬取舆情 |
| `chat_handle(text)` | 自然语言 → 自动执行 |
| `SentimentChatParser().parse(text)` | 仅解析 → {intent, params} |
| `list_sentiment_targets()` | 查看目标库 |
| `list_sentiment_sources(category)` | 查看媒体源 |
| `add_custom_sentiment_target(category, name, aliases)` | 新增自定义目标 |
| `export_sentiment(snapshot, fmt="all")` | 导出 word/excel/csv/json/dialog |

### MCP 工具（Claude Code 直接调用）

| 工具 | 功能 |
|------|------|
| 🆕 `crawl_global_sentiment` | 一键爬取 (单/多机构+多媒体+情感筛选) |
| 🆕 `export_sentiment_report` | 导出已有快照为 Word/Excel/CSV/JSON/对话 |
| 🆕 `list_sentiment_targets` | 查看目标库 |
| 🆕 `list_sentiment_sources` | 查看媒体源 |
| 🆕 `add_sentiment_target` | 新增自定义目标 |
| `schedule_crawl_task` (扩展) | 增加 `action="crawl_sentiment"` 或 `"crawl_sentiment_export"` 模式 |

---

## 🤖 定时任务样例

通过 Claude 对话直接说：
- "每天早上 9 点爬取银行的舆情"
- "每周一早上爬一下保险公司的舆情并导出 Excel"

也可以显式用 MCP：

```python
# 等价于「每天早上 9 点爬一下银行的舆情并导出全部格式」
schedule_crawl_task(
    name="每日银行舆情",
    frequency="daily",                 # 频率
    action="crawl_sentiment_export",   # 🆕 舆情+导出
    sentiment_categories=["commercial_bank"],
    sentiment_source_categories=["authoritative", "financial_vertical"],
    sentiment_days=1,
    sentiment_negative_only=True,
    sentiment_export_format="all",
)
```

---

## 📋 任务清单 — 详细使用指南

> 当用户输入「帮助 / help / 怎么用 / 你能做什么」时，会自动呈现以下内容：

```
🆕 cn-financial-scraper 全网舆情爬虫 v4.3.1 — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
我能做：根据您的对话，全网爬取基金公司、上市公司、地方政府、证券公司、银行、保险、信托等机构的
正面新闻与舆情，并把结果以对话/Word/Excel/CSV/JSON 反馈给您，也可以设置定时任务。

🗞️ 爬取哪些机构的什么信息？
  · 目标类型 (12 大类)：
    fund_company / listed_company / local_government / securities
    / commercial_bank / insurance / trust_company / private_fund
    / foreign_institution / futures / wealth_management / leasing_consumer_finance
  · 信息类型：标题 / 内容简介 / 发布平台 / 发布时间 / 页面连接  — 已自动结构化
  · 情感分类：positive 正面 / negative 舆情 / neutral 中性
  · 严重等级：低度关注 / 中度舆情 / 高危舆情（负面）/ 低度利好 / 中度利好 / 重大利好（正面）

📰 爬哪些媒体？
  · authoritative        — 央媒 & 证券媒体
  · financial_vertical   — 财经垂直
  · local_media          — 地方媒体
  · self_media           — 自媒体
  · international        — 国际媒体

▶️ 对话示例 — 直接复制即可
  · 帮我爬一下某上市公司最近7天的舆情
  · 某基金公司最近3天的负面新闻，并导出 Excel
  · 看下某基金公司今天的正面新闻并生成 Word
  · 每天早上9点爬取银行板块舆情
  · 哪些媒体可用？哪些目标？
  · 新增自定义目标 某基金公司
  · 爬取所有媒体的 某上市公司 过去24小时舆情，导出 Word/Excel

🔧 完整 API / MCP 工具
  · crawl_global_sentiment( 单/多机构, days, 媒体类别, fmt )
  · export_sentiment_report( snapshot_id, fmt )
  · list_sentiment_targets / list_sentiment_sources
  · add_sentiment_target( category, name, aliases )
  · schedule_crawl_task( frequency, sentiment_targets=..., action=crawl_sentiment_export )

📂 产物落盘
  · 快照      : data/sentiment_snapshots/<snapshot_id>.json
  · Word/Excel: data/sentiment_exports/<snapshot_id>.{docx,xlsx}
  · 索引      : data/sentiment_snapshots/index.json
  · 自定义目标: data/sentiment_custom_targets.json

⚠️ 注意事项
  · 浏览器自动化 v4.2 已作为兜底，反爬严格时自动启用
  · 去重：URL + 标题双维指纹，跨调用生效
  · 调度：基于 schedule 库，关闭进程后失效；重启后可从 data/scheduled_tasks.json 自动恢复
```

---

## 提高爬取成功率

1. **零依赖即用**：核心舆情功能无需任何 pip 安装，`python run_sentiment.py` 直接运行
2. **推荐安装**：`python setup_env.py --recommended`（HTML 解析 + Word/Excel 导出）
3. **全功能安装**：`python setup_env.py --full`（含 Playwright 浏览器自动化）
4. **使用代理**：`set_proxy("http://your-proxy:port")` 应对 IP 黑名单
5. **利用现有降级链**：核心 API 自动回退，无需手动干预
6. **开启缓存**：`use_cache=True`（默认开启）
7. **浏览器自动化**：`pip install playwright && playwright install chromium` 处理动态渲染
8. **遇到错误先查 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**：错误码速查表 + 9 大场景解法

## MCP 工具完整列表

通过 MCP 协议暴露 **35 个工具**：

| 工具 | 功能 |
|------|------|
| `query_institution` | 查询机构名单 |
| `scrape_webpage` | 爬取指定 URL |
| `scrape_institution` | 按机构名爬取官网 |
| `parse_financial_product` | 解析基金/ETF/股票/债券页面 |
| `crawl_financial_news` | 最新金融新闻 |
| `search_announcements` | 搜索公告 |
| `download_announcement` | 下载公告 PDF |
| `query_broker_reports` | 券商研报查询 |
| `get_company_reports` | 上市公司综合报告 |
| `parse_document` | PDF/Word/Excel 解析 |
| `export_stock_report` | 导出 PPT/PDF/Word/Excel |
| `batch_crawl_institutions` | 批量爬取机构 |
| `search_report_index` | 全量报告索引搜索 |
| `analyze_document` | 深度分析金融文档 |
| `organize_documents` | 批量整理文档目录 |
| `compare_documents` | 多文档并排对比 |
| `get_stock_realtime` | A 股实时行情 |
| `get_fund_nav_history` | 基金历史净值 |
| `crawl_cls_telegraph` | 财联社 7x24 电报 |
| `get_convertible_bond_data` | 可转债数据 |
| `schedule_crawl_task` | 创建定期爬取任务（v4.3.1 已扩展舆情模式）|
| `list_scheduled_tasks` | 查看所有定时任务 |
| `cancel_scheduled_task` | 取消/暂停/恢复 |
| `batch_crawl_and_package` | 批量爬取+自动打包ZIP |
| `compress_crawl_results` | 压缩为2-3页摘要 |
| `parse_file_enhanced` | 增强文件解析（PPT/HTML/Markdown）|
| `analyze_file_deep` | 深度文件分析 |
| `generate_research_report` | 生成研究报告 |
| `export_research_report` | 导出报告为Word/PPT/HTML/PDF |
| `quick_crawl_summary` | 一键快速爬取+摘要 |
| 🆕 `crawl_global_sentiment` | 一键全网舆情爬取 |
| 🆕 `export_sentiment_report` | 导出舆情快照 |
| 🆕 `list_sentiment_targets` | 查看目标库 |
| 🆕 `list_sentiment_sources` | 查看媒体源 |
| 🆕 `add_sentiment_target` | 新增自定义目标 |

---

## 详细文档

完整功能说明、6个实战场景、27类机构清单、进阶配置、能力边界、FAQ 故障排除、MCP 工具表、v4.3.1 舆情入门均见 [README.md](README.md)。
