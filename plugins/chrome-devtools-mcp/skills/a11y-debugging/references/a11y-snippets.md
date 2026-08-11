# 无障碍调试脚本

通过 `evaluate_script` 执行以下 JavaScript。

## 查找缺少标签的表单控件

查找没有关联 `label[for]`、`aria-label`、`aria-labelledby`，且未被 `<label>` 包裹的表单控件。

```javascript
() =>
  Array.from(document.querySelectorAll('input, select, textarea'))
    .filter(element => {
      const hasId =
        element.id && document.querySelector(`label[for="${element.id}"]`);
      const hasAria =
        element.getAttribute('aria-label') ||
        element.getAttribute('aria-labelledby');
      return !hasId && !hasAria && !element.closest('label');
    })
    .map(element => ({
      tag: element.tagName,
      id: element.id,
      name: element.name,
      placeholder: element.placeholder,
    }));
```

## 测量触控目标尺寸

返回元素的 Bounding Box 尺寸。调用 `evaluate_script` 时传入快照中的元素 `uid`。

```javascript
element => {
  const rect = element.getBoundingClientRect();
  return {width: rect.width, height: rect.height};
};
```

## 检查颜色对比度

估算元素文本色与背景色的对比度。调用 `evaluate_script` 时传入元素 `uid`，并按 WCAG AA 标准判断：普通文本至少 4.5:1，大号文本至少 3:1。

该算法经过简化，不处理透明度、渐变或背景图片。生产级审计应使用 Lighthouse 或 `axe-core`。

```javascript
element => {
  function getRGB(colorString) {
    const match = colorString.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    return match
      ? [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])]
      : [255, 255, 255];
  }

  function luminance(red, green, blue) {
    const values = [red, green, blue].map(value => {
      value /= 255;
      return value <= 0.03928
        ? value / 12.92
        : Math.pow((value + 0.055) / 1.055, 2.4);
    });
    return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
  }

  const style = window.getComputedStyle(element);
  const foreground = getRGB(style.color);
  const background = getRGB(style.backgroundColor);
  const foregroundLuminance = luminance(...foreground);
  const backgroundLuminance = luminance(...background);
  const contrastRatio =
    (Math.max(foregroundLuminance, backgroundLuminance) + 0.05) /
    (Math.min(foregroundLuminance, backgroundLuminance) + 0.05);

  return {
    color: style.color,
    background: style.backgroundColor,
    contrastRatio: contrastRatio.toFixed(2),
  };
};
```

## 检查页面全局设置

检查组件审计容易遗漏的页面级无障碍设置。

```javascript
() => ({
  lang:
    document.documentElement.lang ||
    '缺少 lang，Screen Reader 无法确定正确发音规则',
  title: document.title || '缺少 title，用户无法获得页面上下文',
  viewport:
    document.querySelector('meta[name="viewport"]')?.content ||
    '缺少 viewport，同时检查是否错误使用 user-scalable=no',
  reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ? '已启用'
    : '未启用',
});
```
