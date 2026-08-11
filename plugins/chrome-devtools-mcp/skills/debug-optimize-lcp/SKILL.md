---
name: debug-optimize-lcp
description: 使用 Chrome DevTools MCP 调试并优化 Largest Contentful Paint（LCP）。用户询问 LCP、页面加载缓慢、Core Web Vitals、CWV、首屏主图或主要内容显示过慢时使用。
---

## 理解 LCP

Largest Contentful Paint（LCP）衡量页面主要内容变得可见的速度，即从导航开始到视口内最大图片或文本块完成渲染的时间。

- **良好**：不超过 2.5 秒。
- **需要改进**：2.5 至 4.0 秒。
- **较差**：超过 4.0 秒。

LCP 是 Core Web Vitals 指标，直接影响用户体验与搜索排名。移动页面中的 LCP 元素经常是图片。

## 分解 LCP

每个页面的 LCP 可分为四个连续且不重叠的阶段。先确定瓶颈阶段，再决定优化措施。

| 阶段 | 理想占比 | 衡量范围 |
| --- | --- | --- |
| **Time to First Byte（TTFB）** | 约 40% | 导航开始 -> 收到 HTML 第一个字节 |
| **资源加载延迟** | 小于 10% | TTFB -> 浏览器开始加载 LCP 资源 |
| **资源加载时长** | 约 40% | 下载 LCP 资源所需时间 |
| **元素渲染延迟** | 小于 10% | LCP 资源下载完成 -> 元素完成渲染 |

两个“延迟”阶段应尽量接近零。任一延迟占比明显偏高时，优先处理该阶段。

不要在未分解 LCP 前直接压缩图片。若真正瓶颈是渲染延迟，缩小图片只会让节省的时间转移到渲染延迟，并不能改善最终 LCP。

## 调试流程

严格按顺序执行，每一步使用上一步的证据。

开始前确认目标 URL，并固定 Chrome 版本、Viewport、登录态、服务端环境、缓存策略、网络和 CPU 限速。修复前后必须使用相同条件，至少各采集 3 次并比较中位数；对高波动页面增加到 5 次。

### 第一步：录制性能 Trace

1. 使用 `navigate_page` 打开目标 URL。
2. 调用 `performance_start_trace`，设置 `reload: true` 和 `autoStop: true`，完整捕获页面加载和 LCP。
3. 记录输出中的 Insight Set ID，后续分析需要该 ID。

### 第二步：分析 LCP 洞察

从 Trace 输出中查找以下 Insight，并调用 `performance_analyze_insight`，把 Trace 返回值分别传给 `insightSetId` 和 `insightName`：

- **LCPBreakdown**：显示四个 LCP 阶段及各自耗时。
- **DocumentLatency**：识别影响 TTFB 的服务端响应问题。
- **RenderBlocking**：识别阻塞 LCP 元素渲染的资源。
- **LCPDiscovery**：判断浏览器能否尽早发现 LCP 资源。

### 第三步：识别 LCP 元素

读取 [references/lcp-snippets.md](references/lcp-snippets.md)，通过 `evaluate_script` 执行“识别 LCP 元素”脚本，获取元素标签、资源 URL 和原始计时数据。

`url` 指向需要在网络瀑布图中检查的资源；为空时表示 LCP 元素是文本，不需要加载独立资源。

### 第四步：检查网络瀑布图

1. 根据元素类型调用 `list_network_requests`，例如用 `resourceTypes: ["image", "font"]` 过滤。
2. 使用 LCP 资源的请求 ID 调用 `get_network_request` 获取完整详情。

重点检查：

- **开始时间**：与 HTML 文档和首批资源比较。LCP 资源明显较晚开始，表示存在资源加载延迟。
- **持续时间**：持续时间过长通常表示资源过大或服务端响应缓慢。

### 第五步：检查常见 HTML 问题

读取 [references/lcp-snippets.md](references/lcp-snippets.md)，通过 `evaluate_script` 执行“检查常见问题”脚本，检查首屏图片懒加载、缺少 `fetchpriority` 和阻塞渲染的脚本。该脚本检查 LCP 候选图片，必须结合第三步确认的真实 LCP 元素判断，不能把候选结果直接当作根因。

## 优化策略

根据已确认的瓶颈阶段，按以下优先级修复。

### 1. 消除资源加载延迟

目标是低于 LCP 的 10%，让 LCP 资源尽早开始加载。

- LCP 图片由 JavaScript、CSS 或 `data-src` 延迟发现时，改用标准 `<img src>`。
- 不要给 LCP 图片设置 `loading="lazy"`。
- 资源无法从初始 HTML 发现时，增加 `<link rel="preload" fetchpriority="high">`。响应式图片还要正确设置 `imagesrcset` 和 `imagesizes`，跨域资源按需要设置 `crossorigin`，并确认没有重复下载。
- 为 LCP `<img>` 增加 `fetchpriority="high"`。

### 2. 消除元素渲染延迟

目标是低于 LCP 的 10%，资源下载完成后应立即渲染。

- 内联关键 CSS，延后非关键 CSS 和 JavaScript。存在执行顺序依赖时优先使用 `defer`；只对完全独立的脚本使用 `async`。
- 拆分阻塞主线程的长任务。
- 使用 Server-Side Rendering（SSR），确保元素存在于初始 HTML。

### 3. 缩短资源加载时长

- 使用 WebP、AVIF 和响应式图片 `srcset`。
- 通过 CDN 分发。
- 设置合理的 `Cache-Control`。
- 文本 LCP 被 Web Font 阻塞时使用 `font-display: swap`。

### 4. 降低 TTFB

- 减少重定向并优化服务端响应时间。
- 在边缘 CDN 缓存 HTML。

## 验证与模拟

- **验证**：再次使用 `reload: true` 录制 Trace。比较 LCP 总时长、四个阶段的绝对毫秒数、LCP 资源相对 HTML 的启动时间和资源大小，并确认 LCP 元素身份没有意外变化。阶段占比下降但绝对耗时未下降，不算有效改善；同时检查 CLS 等相邻指标没有回退。
- **模拟**：实验室结果与真实用户体验不同。需要模拟低端环境时，在导航和 Trace 前调用 `emulate`，设置 `networkConditions: "Fast 3G"` 和 `cpuThrottlingRate: 4`，并在修复前后保持相同配置。完成后把 `cpuThrottlingRate` 恢复为 `1`，并在不传 `networkConditions` 的调用中关闭网络限速。
- **上线验证**：实验室 Trace 只证明受控条件下的改善。发布后继续通过真实用户监控或 CrUX 数据确认效果。
