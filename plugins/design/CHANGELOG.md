# Changelog

## 1.0.1

- 随设计平台扩展 0.4.97 发布，参考文件支持项目内直接选择。
- 设计系统优先约束颜色和字体，修订保留原稿，完善新稿登记和失效引用重新关联。
- 幻灯片模板支持完整多页预览，修复两个模板预览内容缺失。
- 工作台仅打开明确入口或已登记设计，模板与设计系统详情返回时保留列表位置。
- 压缩模板图片和扩展归档，保留本地字体；插件包含 333 个技能和 4 条规则。

## 1.0.0

- 首个正式版本，随设计平台扩展 0.4.96 发布。
- 插件简介与详情重写，新增详情页截图。
- 333 个技能全部补齐中文说明（`zh_description`），重写 75 条模板化说明；修复 `frame-product-promo-30s` 的 frontmatter 格式。
- 两条规则的说明改为书面表达。

## 0.1.3

- 修正 8 个 Skill 自检说明中的占位符关键词误报，保持校验意图不变；Plugin validator 现在可正确区分检查规则与残留占位文本。

## 0.1.2

- 新增 `deck-framework`：上游 daemon deck framework directive 的逐字移植（1920×1080 骨架 + SLOT 契约），作为未选模板时幻灯片创建的默认种子。Skill 总数 333。
- 重写 `html-ppt-pitch-deck` / `html-ppt-product-launch` / `html-ppt-course-module` / `html-ppt-tech-sharing` 正文：以目录内 `example.html` 为种子、工作台预实例化文件为工作文件，移除指向 html-ppt 母仓库布局的失效引用。

## 0.1.1

- 补齐 Open Design Community 官方套件：22 个幻灯片视觉体系（花术 / fs / hps / ve）、16 个原型（含 WebGL）、17 个 HyperFrames frame。Skill 总数 332。

## 0.1.0

- 从 Open Design commit `d954bee805b4f1bdf8767cc9aa3da95c1d097e36` 导入 276 个 Skill。
- 上游根许可证为 Apache-2.0；各 Skill 自带的许可证文件保持原路径分发。
- 将 3 个 `SKILL.md` 中会触发发布校验的字面占位标记改为等义描述。
- 将 `review-animations` 的 `disable-model-invocation` 设为 `false`，使其可投影给 Codex、Claude 与 OpenCode Agent。
