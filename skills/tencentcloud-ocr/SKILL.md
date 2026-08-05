---
name: tencentcloud-ocr
displayName: "腾讯云文字识别（通用高精度版）"
description: "腾讯云通用文字识别（高精度版）技能包。用户发送/粘贴图片、提供图片URL或要求识别图片文字时自动调用。支持中文、英文、中英混合、数字及特殊符号的检测与识别，返回文字框位置与内容。适用于文字较多、版式复杂、准召率要求高的场景。"
version: "1.0.5"
tags:
  - knowledge_management
license: "Unknown"
---

# 腾讯云通用文字识别（高精度版）(GeneralAccurateOCR)

## 用途

调用腾讯云OCR通用文字识别（高精度版）接口，对图片中的文字进行精准提取。

核心能力：
- **文字识别**：高精度识别图片中的文字内容，返回完整识别文本
- **PDF支持**：支持对PDF文件进行文字识别（单页）
- **单字信息**：可选返回每个单字的位置和置信度信息
- **多语种简历结构化识别**：基于 OCR 结果，对简历进行结构化提取与格式化输出（详见 `references/resume-parsing.md`）

官方文档：https://cloud.tencent.com/document/api/866/37831

## 📚 可用资源

### References（场景化指引）
- `references/resume-parsing.md` - 多语种简历结构化识别指引（处理流程、Prompt模板、输出格式化模板、格式化规则）

## 使用时机

当用户提出以下需求时触发此技能：
- 需要从图片或PDF中提取文字内容
- 需要对各类文档、图片等进行文字识别
- 涉及通用文字OCR识别的任何场景
- 需要从简历图片/PDF中识别并结构化提取简历信息（请参考 `references/resume-parsing.md` 指引）
- 需要对多语种简历进行识别和格式化输出（请参考 `references/resume-parsing.md` 指引）

## 环境要求

- Python 3.6+
- 依赖：`tencentcloud-sdk-python`（通过 `pip install tencentcloud-sdk-python` 安装）
- 环境变量：
  - `TENCENTCLOUD_SECRET_ID`：腾讯云API密钥ID
  - `TENCENTCLOUD_SECRET_KEY`：腾讯云API密钥Key

## 使用方式

运行 `scripts/main.py` 脚本完成文字识别。

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| ImageBase64 | str | 否(二选一) | 图片Base64值，不超过10MB |
| ImageUrl | str | 否(二选一) | 图片URL地址，优先使用 |
| IsPdf | bool | 否 | 是否开启PDF识别，默认false |
| PdfPageNumber | int | 否 | 需要识别的PDF页码，IsPdf为true时有效，默认1 |
| IsWords | bool | 否 | 是否返回单字信息，默认false |
| **UserAgent** | **str** | **否** | **请求来源标识(可选)，不传时自动探测平台** |

### ⚠️ UserAgent参数使用指南

**`--user-agent`参数是可选参数**，不传时脚本会**自动探测当前调用平台**（WorkBuddy / OpenClaw / QClaw / ADP / CodeBuddy），并输出 `skill-<platform>`；无法识别时回退为 `skillother`。用于标识API调用来源，便于按渠道追踪和统计调用次数：

| 调用平台 | 不传时的自动探测结果 | 说明 |
|---------|--------------|------|
| WorkBuddy | `skill-workbuddy` | 自动识别 |
| CodeBuddy | `skill-codebuddy` | 自动识别 |
| OpenClaw | `skill-openclaw` | 自动识别 |
| QClaw | `skill-qclaw` | 自动识别 |
| ADP | `skill-adp` | 自动识别 |
| 未识别 | `skillother` | 兜底 |
| 显式传参 | 原样使用 | 人工覆盖，向后兼容 |

**实现说明**：
- 不传 `--user-agent` 时，脚本通过环境变量 + 进程树回溯自动探测渠道
- SDK 会将其拼接为 `SDK_PYTHON_x.x.x; skill-<platform>` 注入到请求的 `RequestClient` 字段
- cam_access_server 会将此值写入 ES 日志的 `requestClient` 字段，可直接聚合统计
- 探测逻辑异常安全：任何失败回退为 `skillother`，不影响 OCR 主流程

### 输出格式

识别成功后返回 JSON 格式结果：

```json
{
  "raw_text": "识别到的完整文字内容\n第二行文字\n第三行文字",
  "RequestId": "xxx"
}
```

无文字时返回：

```json
{
  "raw_text": "",
  "message": "No text detected in the image.",
  "RequestId": "xxx"
}
```

### 调用示例

```bash
# 基础调用示例（--user-agent 默认为 Skills，可不传）
python scripts/main.py --image-url "https://example.com/document.jpg"

# 使用 Base64 文件调用
python scripts/main.py --image-base64 "/path/to/document.jpg"

# 识别 PDF 文件中的文字
python scripts/main.py --image-url "https://example.com/doc.pdf" \
  --is-pdf true --pdf-page-number 1

# 返回单字信息
python scripts/main.py --image-url "https://example.com/document.jpg" --is-words true
```

## 密钥配置

### Step 1: 获取/购买 OCR 服务

🔗 **[腾讯云文字识别 OCR 购买页](https://buy.cloud.tencent.com/iai_ocr)**

在购买页面中选择 **通用文字识别（高精度版）** 完成购买。

### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

### Step 3: 设置环境变量

**Linux / macOS：**
```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

**Windows (PowerShell)：**
```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
```
