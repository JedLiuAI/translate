from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz

try:
    from rapidocr_onnxruntime import RapidOCR
except ImportError as exc:
    raise SystemExit("rapidocr_onnxruntime is required. Install it before running this script.") from exc


def ocr_image(ocr: RapidOCR, image_path: Path) -> list[str]:
    result, _ = ocr(str(image_path))
    if not result:
        return []
    return [item[1] for item in result]


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PDF pages and OCR common leaflet regions.")
    parser.add_argument("pdf", help="Input PDF path")
    parser.add_argument("--page", type=int, default=1, help="1-based page number")
    parser.add_argument("--zoom", type=float, default=2.0, help="Render zoom factor")
    parser.add_argument("--output-dir", default="ocr_output", help="Directory for PNG and text outputs")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    page = doc[args.page - 1]
    pix = page.get_pixmap(matrix=fitz.Matrix(args.zoom, args.zoom), alpha=False)
    full_png = out_dir / f"page_{args.page}.png"
    pix.save(full_png)

    rects = {
        "full": None,
        "front": (0.08, 0.05, 0.40, 0.55),
        "back": (0.40, 0.05, 0.72, 0.55),
        "table": (0.14, 0.50, 0.82, 0.94),
    }

    from PIL import Image

    image = Image.open(full_png)
    ocr = RapidOCR()
    payload: dict[str, object] = {
        "pdf": str(pdf_path.resolve()),
        "page": args.page,
        "image": str(full_png.resolve()),
        "regions": {},
    }

    for name, rel in rects.items():
        if rel is None:
            region_path = full_png
        else:
            x0 = int(image.width * rel[0])
            y0 = int(image.height * rel[1])
            x1 = int(image.width * rel[2])
            y1 = int(image.height * rel[3])
            crop = image.crop((x0, y0, x1, y1))
            crop = crop.resize((crop.width * 2, crop.height * 2))
            region_path = out_dir / f"page_{args.page}_{name}.png"
            crop.save(region_path)
        lines = ocr_image(ocr, region_path)
        (out_dir / f"page_{args.page}_{name}.txt").write_text("\n".join(lines), encoding="utf-8")
        payload["regions"][name] = {
            "image": str(region_path.resolve()),
            "text": str((out_dir / f"page_{args.page}_{name}.txt").resolve()),
            "line_count": len(lines),
        }

    spec_path = out_dir / f"page_{args.page}_ocr_index.json"
    spec_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(spec_path.resolve())


if __name__ == "__main__":
    main()
