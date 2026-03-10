# translate

This repository stores reusable Codex/OpenClaw skills for PDF translation workflows.

## Included skill

### `translate-scanned-medicine-pdf`

Use this skill when you need to:

- translate scanned medicine leaflet PDFs into Chinese
- OCR tiny-print or image-based drug inserts
- rebuild a readable Chinese PDF while keeping the original two-panel layout as much as possible

## What the skill contains

- `SKILL.md`: trigger conditions and operating workflow
- `scripts/ocr_leaflet_regions.py`: render PDF pages and OCR common leaflet regions
- `scripts/render_two_panel_leaflet.py`: rebuild a Chinese two-panel leaflet PDF from a JSON spec
- `references/`: workflow and translation checklist
- `assets/leaflet_spec.example.json`: starter render spec

## Typical workflow

1. OCR the scanned PDF into region text.
2. Reconstruct the leaflet sections from OCR output.
3. Translate the medically relevant content into Chinese.
4. Render a new PDF that stays close to the original structure.

## Notes

- This workflow is intended for scan-based or artwork-style medicine leaflets.
- OCR-based medical translations should be manually reviewed before regulatory, print, or public use.
