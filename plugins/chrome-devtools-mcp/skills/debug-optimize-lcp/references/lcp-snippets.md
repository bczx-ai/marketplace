# LCP 调试脚本

通过 `evaluate_script` 执行以下 JavaScript，提取页面中的 LCP 证据。

## 识别 LCP 元素

识别 LCP 元素并读取 Performance API 提供的原始计时数据。

```javascript
async () => {
  return await new Promise(resolve => {
    let timer;
    const observer = new PerformanceObserver(list => {
      const entries = list.getEntries();
      const last = entries[entries.length - 1];
      observer.disconnect();
      clearTimeout(timer);
      const rect = last.element?.getBoundingClientRect();
      resolve({
        element: last.element?.tagName,
        id: last.element?.id,
        className: last.element?.className,
        url: last.url,
        currentSrc: last.element?.currentSrc,
        loading: last.element?.loading,
        fetchPriority: last.element?.fetchPriority,
        rect: rect
          ? {top: rect.top, left: rect.left, width: rect.width, height: rect.height}
          : null,
        startTime: last.startTime,
        renderTime: last.renderTime,
        loadTime: last.loadTime,
        size: last.size,
      });
    });
    observer.observe({type: 'largest-contentful-paint', buffered: true});
    timer = setTimeout(() => {
      observer.disconnect();
      resolve(null);
    }, 2000);
  });
};
```

## 检查常见问题

检查 DOM 中常见的 LCP 问题，包括首屏图片懒加载、图片优先级缺失和阻塞渲染的脚本。

```javascript
() => {
  const issues = [];

  // 检查视口内被设置为懒加载的图片。
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    const rect = img.getBoundingClientRect();
    if (rect.bottom > 0 && rect.top < window.innerHeight) {
      issues.push({
        issue: '视口内图片被设置为懒加载',
        element: img.outerHTML.substring(0, 200),
        fix: '移除该图片的 loading="lazy"，它位于首屏并可能是 LCP 元素',
      });
    }
  });

  // 检查缺少 fetchpriority 的 LCP 候选图片。
  document.querySelectorAll('img:not([fetchpriority])').forEach(img => {
    const rect = img.getBoundingClientRect();
    if (
      rect.bottom > 0 &&
      rect.top < window.innerHeight &&
      rect.width * rect.height > 50000
    ) {
      issues.push({
        issue: '首屏大图缺少 fetchpriority',
        element: img.outerHTML.substring(0, 200),
        fix: '为该图片增加 fetchpriority="high"，它尺寸较大且位于首屏',
      });
    }
  });

  // 检查 head 中阻塞渲染的脚本。
  document
    .querySelectorAll(
      'head script:not([async]):not([defer]):not([type="module"])',
    )
    .forEach(script => {
      if (script.src) {
        issues.push({
          issue: 'head 中存在阻塞渲染的脚本',
          element: script.outerHTML.substring(0, 200),
          fix: '增加 async 或 defer 属性，或把脚本移到 body 末尾',
        });
      }
    });

  return {issueCount: issues.length, issues};
};
```
