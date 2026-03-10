---
name: translate-scanned-medicine-pdf
description: Translate scanned medicine leaflet or packaging-insert PDFs into Chinese with OCR, section reconstruction, and approximate original layout preservation. Use when the source PDF is image-based or tiny-print, especially one-page front/back leaflet artwork, and the user wants a readable Chinese PDF that stays close to the original structure.
---

# Translate Scanned Medicine Pdf

Use this skill for scanned or artwork-style drug leaflet PDFs where normal text extraction is incomplete, the source has dense small print, and the user wants a Chinese translation that roughly preserves the original front/back layout.

## Workflow

1. Inspect the workspace for the target PDF and confirm whether it is text-based or scan-based.
2. Try direct text extraction with PyMuPDF first. If extraction is sparse or obviously incomplete, switch to OCR.
3. Render the page to a high-resolution PNG. For one-page leaflet artwork, OCR the full page and also OCR cropped regions for the front panel, back panel, and any bottom metadata block.
4. Reconstruct the document sections from OCR output instead of trusting raw OCR order blindly. Medicine leaflets usually contain predictable sections such as composition, indications, dosage, warnings, contraindications, adverse reactions, storage, and manufacturer details.
5. Translate into Chinese conservatively. Preserve medical meaning, dosage numbers, timings, contraindications, and storage conditions exactly. Do not invent pharmacology details that are not present.
6. Rebuild a deliverable PDF that keeps the original structure as much as practical. For one-page front/back artwork, prefer a single-page Chinese layout with two main panels plus a simplified metadata block.
7. Validate the rebuilt page visually. Check for clipped text, missing section headers, broken dosage units, and unreadably small font.
8. In the final response, provide the output PDF path and explicitly note that scanned-source OCR should be manually reviewed before regulatory, print, or public use.

## Operating Rules

- Prefer `scripts/ocr_leaflet_regions.py` to extract OCR text from full pages and common leaflet regions.
- Prefer `scripts/render_two_panel_leaflet.py` to render the translated Chinese PDF from a JSON spec.
- Read [references/workflow.md](references/workflow.md) when you need the detailed end-to-end procedure.
- Read [references/translation-checklist.md](references/translation-checklist.md) when the file is a drug leaflet and translation fidelity matters.
- Use [assets/leaflet_spec.example.json](assets/leaflet_spec.example.json) as the starting template for the render spec.

## Decision Guidance

- If the PDF already contains extractable text with intact reading order, skip OCR and translate directly.
- If the artwork is multi-page, process one page at a time and create one render spec per page.
- If exact original typography cannot be reproduced, preserve panel structure and information hierarchy rather than chasing visual perfection.
- If OCR text is ambiguous, keep uncertain manufacturer metadata brief and focus effort on clinically relevant sections first.
- If the user asks for a formal or publishable deliverable, state that the Chinese output is an OCR-based reconstruction and requires human pharmaceutical review.

## Deliverables

Default output set:
- One translated PDF in the workspace.
- Optional intermediate PNGs and OCR text files if they help review or debugging.
- A reusable JSON spec if the page may need revision.
