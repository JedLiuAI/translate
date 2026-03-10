# translate

这个仓库用于存放可复用的 Codex / OpenClaw 技能，当前主要用于 PDF 翻译相关流程。

## 当前技能

### `translate-scanned-medicine-pdf`

这个技能适用于以下场景：

- 将扫描版药品说明书 PDF 翻译为中文
- 对小字、图片型、无法直接抽取正文的药品说明书做 OCR
- 在尽量保留原始正反双栏结构的前提下，重建可阅读的中文 PDF

## 技能内容

- `SKILL.md`：说明技能在什么情况下触发，以及整体处理流程
- `scripts/ocr_leaflet_regions.py`：把 PDF 页面渲染成图片，并对常见说明书区域做 OCR
- `scripts/render_two_panel_leaflet.py`：根据 JSON 规格重建中文版双栏说明书 PDF
- `references/`：包含工作流说明和翻译检查清单
- `assets/leaflet_spec.example.json`：用于生成版面的示例配置文件

## 基本流程

1. 对扫描版 PDF 做 OCR，提取各区域文字。
2. 根据 OCR 结果重组说明书的段落和章节。
3. 将药品相关内容翻译为中文。
4. 按接近原始结构的方式生成新的中文 PDF。

## 说明

- 这个流程主要面向扫描件或印刷稿式样的药品说明书。
- 由于结果依赖 OCR，正式用于注册、印刷或公开发布前，仍然建议人工复核。
