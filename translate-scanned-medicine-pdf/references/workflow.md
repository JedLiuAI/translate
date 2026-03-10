# Workflow

## 1. Inspect the source PDF

- Find the target PDF in the workspace.
- Check page count and attempt direct extraction with PyMuPDF.
- If extraction returns only a few lines from a full page, treat it as scan-based.

Suggested commands:
```powershell
python -c "import fitz; doc=fitz.open('file.pdf'); print(doc.page_count); print(doc[0].get_text()[:2000])"
```

## 2. Generate OCR inputs

Use `scripts/ocr_leaflet_regions.py`.

Example:
```powershell
$env:PYTHONPATH="D:\path\to\.pydeps"
python scripts/ocr_leaflet_regions.py file.pdf --page 1 --output-dir work_ocr
```

Outputs:
- full-page PNG
- cropped PNGs for front/back/table regions
- OCR text files for each region
- one JSON index of generated files

## 3. Reconstruct the section order

Do not translate directly from raw OCR line order.

For medicine leaflets, rebuild by section:
- title
- composition
- classification / pharmacologic group
- indications
- dosage and administration
- inhaler instructions or use instructions
- contraindications
- warnings / pregnancy / lactation / pediatric use
- adverse reactions
- overdose
- interactions
- storage
- manufacturer / distributor details

## 4. Translate conservatively

- Preserve all numbers, units, timings, counts, temperatures, and frequency.
- Translate medical meaning, not OCR noise.
- If a line is visibly corrupted and non-clinical, summarize briefly rather than hallucinating exact wording.
- Spend effort first on clinically relevant content, then on artwork metadata.

## 5. Build the render spec

Start from `assets/leaflet_spec.example.json`.

Fill in:
- `front.text`
- `back.text`
- `metadata`

If the page has no bottom metadata block, you can still keep the default simplified table to preserve the visual structure.

## 6. Render the translated PDF

Example:
```powershell
python scripts/render_two_panel_leaflet.py assets\leaflet_spec.example.json
```

The script writes:
- `*_rendered.png`
- `*_rendered.pdf`

## 7. Validate visually

Check:
- no clipped paragraphs
- no missing warnings or dosage lines
- readable font size
- correct panel headings
- no accidental change to drug strength or storage temperature

If text is clipped, reduce body font size in the JSON spec or shorten low-value metadata.
