from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

PAGE_SIZE = (1868, 2060)
BG = (243, 243, 243)
PANEL_BORDER = (226, 194, 206)
TEXT = (40, 40, 40)
BLUE = (10, 73, 148)
YELLOW = (241, 209, 47)
WHITE = (255, 255, 255)


def get_font(size: int, bold: bool = False):
    candidates = [
        ("C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc"),
        ("C:/Windows/Fonts/simhei.ttf" if bold else "C:/Windows/Fonts/simsun.ttc"),
    ]
    for font_path in candidates:
        if Path(font_path).exists():
            return ImageFont.truetype(font_path, size=size)
    raise FileNotFoundError("No suitable Chinese font found.")


def wrap_text(draw, text, font, width):
    lines = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        current = ""
        for char in paragraph:
            test = current + char
            if draw.textlength(test, font=font) <= width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = char
        if current:
            lines.append(current)
    return lines


def draw_wrapped(draw, box, text, font, fill, line_spacing=3):
    x0, y0, x1, y1 = box
    lines = wrap_text(draw, text, font, x1 - x0)
    y = y0
    for line in lines:
        if y > y1:
            break
        draw.text((x0, y), line, font=font, fill=fill)
        y += font.size + line_spacing


def draw_table(draw, metadata: dict[str, str]):
    x0, y0, x1, y1 = 260, 1370, 1515, 1935
    draw.rounded_rectangle((x0, y0, x1, y1), radius=22, outline=(110, 110, 110), width=2, fill=WHITE)
    header_h = 48
    draw.rounded_rectangle((x0, y0, x1, y0 + header_h), radius=22, fill=BLUE)
    draw.rectangle((x0, y0 + 20, x1, y0 + header_h), fill=BLUE)

    split1 = [x0, x0 + 210, x0 + 355, x0 + 535, x0 + 720, x0 + 880, x1]
    split2 = [x0, x0 + 220, x0 + 370, x0 + 570, x0 + 760, x0 + 930, x1]
    for s in split1[1:-1]:
        draw.line((s, y0, s, y0 + 180), fill=(140, 140, 140), width=1)
    for s in split2[1:-1]:
        draw.line((s, y0 + 180, s, y0 + 320), fill=(140, 140, 140), width=1)
    draw.line((x0, y0 + 90, x1, y0 + 90), fill=(140, 140, 140), width=1)
    draw.line((x0, y0 + 180, x1, y0 + 180), fill=(140, 140, 140), width=1)
    draw.line((x0, y0 + 320, x1, y0 + 320), fill=(140, 140, 140), width=1)

    obs_x0, obs_y0, obs_x1, obs_y1 = 1540, 1370, 1765, 1935
    draw.rounded_rectangle((obs_x0, obs_y0, obs_x1, obs_y1), radius=18, outline=(140, 140, 140), width=2, fill=WHITE)
    draw.rounded_rectangle((obs_x0, obs_y0, obs_x1, obs_y0 + header_h), radius=18, fill=YELLOW)
    draw.rectangle((obs_x0, obs_y0 + 20, obs_x1, obs_y0 + header_h), fill=YELLOW)
    draw.line((obs_x0, obs_y0 + 320, obs_x1, obs_y0 + 320), fill=(140, 140, 140), width=1)
    draw.rounded_rectangle((obs_x0, obs_y1 - 42, obs_x1, obs_y1), radius=12, fill=(60, 60, 60))

    font_h = get_font(20, bold=True)
    font_s = get_font(16)
    font_c = get_font(19)
    headers = ["产品", "版本", "条码", "内部编码", "日期", "备注"]
    for i, text in enumerate(headers[:-1]):
        draw.text((split1[i] + 10, y0 + 12), text, font=font_h, fill=WHITE)
    draw.text((obs_x0 + 12, obs_y0 + 12), headers[-1], font=font_h, fill=(60, 60, 60))

    values = [
        metadata.get("product", ""),
        metadata.get("version", ""),
        metadata.get("barcode", ""),
        metadata.get("internal_code", ""),
        metadata.get("date", ""),
        metadata.get("comments", ""),
    ]
    value_boxes = [
        (split1[0] + 10, y0 + 58),
        (split1[1] + 10, y0 + 58),
        (split1[2] + 10, y0 + 58),
        (split1[3] + 10, y0 + 58),
        (split1[4] + 10, y0 + 58),
        (obs_x0 + 14, obs_y0 + 70),
    ]
    for (tx, ty), value in zip(value_boxes, values):
        draw.multiline_text((tx, ty), value, font=font_c, fill=TEXT, spacing=4)

    headers2 = ["尺寸", "颜色", "字体", "材质", "公司"]
    keys2 = ["dimensions", "colors", "fonts", "material", "company"]
    for i, (head, key) in enumerate(zip(headers2, keys2)):
        draw.text((split2[i] + 10, y0 + 192), head, font=font_h, fill=BLUE)
        draw.multiline_text((split2[i] + 10, y0 + 230), metadata.get(key, ""), font=font_s, fill=TEXT, spacing=4)

    sign_heads = ["批准人", "市场总监", "设计者"]
    sign_values = [metadata.get("approver", ""), metadata.get("marketing", ""), metadata.get("designer", "")]
    sign_x = [x0, x0 + 335, x0 + 670]
    for sx in sign_x[1:]:
        draw.line((sx, y0 + 320, sx, y1), fill=(140, 140, 140), width=1)
    bar_y = y0 + 330
    for sx, head, val in zip(sign_x, sign_heads, sign_values):
        right = sx + 335 if sx < sign_x[-1] else x1
        draw.rounded_rectangle((sx, bar_y, right, bar_y + 34), radius=12, fill=BLUE)
        draw.text((sx + 12, bar_y + 6), head, font=get_font(18, bold=True), fill=WHITE)
        draw.multiline_text((sx + 12, bar_y + 58), val, font=font_c, fill=TEXT, spacing=4)

    draw.text((obs_x0 + 30, obs_y1 - 34), metadata.get("purchase_order", "采购订单"), font=get_font(16, bold=True), fill=WHITE)


def render(spec_path: Path) -> Path:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    image = Image.new("RGB", PAGE_SIZE, BG)
    draw = ImageDraw.Draw(image)

    body_font = get_font(int(spec.get("body_font_size", 12)))
    title_font = get_font(int(spec.get("title_font_size", 20)), bold=True)
    small_font = get_font(18)
    front = spec["front"]
    back = spec["back"]
    metadata = spec.get("metadata", {})

    draw.text((160, 60), spec.get("top_note_1", "1. 说明书尺寸：100 × 170 mm"), font=small_font, fill=(90, 90, 90))
    draw.text((160, 90), spec.get("top_note_2", "2. 正反面印刷"), font=small_font, fill=(90, 90, 90))
    draw.line((150, 135, 670, 135), fill=(190, 190, 190), width=2)
    draw.line((150, 126, 150, 144), fill=(190, 190, 190), width=2)
    draw.line((670, 126, 670, 144), fill=(190, 190, 190), width=2)
    draw.text((380, 110), "100 mm", font=get_font(16), fill=(90, 90, 90))
    draw.line((120, 210, 120, 1110), fill=(190, 190, 190), width=2)
    draw.line((111, 210, 129, 210), fill=(190, 190, 190), width=2)
    draw.line((111, 1110, 129, 1110), fill=(190, 190, 190), width=2)
    draw.text((70, 640), "170 mm", font=get_font(16), fill=(90, 90, 90))

    front_box = (150, 175, 730, 1250)
    back_box = (750, 175, 1330, 1250)
    for box in (front_box, back_box):
        draw.rectangle(box, outline=PANEL_BORDER, width=2, fill=WHITE)

    draw.text((355, 1265), front.get("label", "正面"), font=get_font(18), fill=(90, 90, 90))
    draw.text((960, 1265), back.get("label", "背面"), font=get_font(18), fill=(90, 90, 90))

    draw.text((180, 195), front.get("header", "患者用药信息"), font=title_font, fill=TEXT)
    draw.text((630, 195), front.get("brand", "OPKO"), font=title_font, fill=TEXT)
    draw.text((775, 195), back.get("header", "禁忌症 / 注意事项"), font=title_font, fill=TEXT)
    draw.text((1230, 195), back.get("brand", "OPKO"), font=title_font, fill=TEXT)

    draw_wrapped(draw, (180, 235, 700, 1215), front.get("text", ""), body_font, TEXT, line_spacing=int(spec.get("line_spacing", 3)))
    draw_wrapped(draw, (775, 235, 1300, 1215), back.get("text", ""), body_font, TEXT, line_spacing=int(spec.get("line_spacing", 3)))
    draw_table(draw, metadata)

    out_base = spec_path.with_suffix("")
    png_path = out_base.with_name(out_base.name + "_rendered.png")
    pdf_path = out_base.with_name(out_base.name + "_rendered.pdf")
    image.save(png_path)

    doc = fitz.open()
    page = doc.new_page(width=PAGE_SIZE[0], height=PAGE_SIZE[1])
    page.insert_image(page.rect, filename=str(png_path))
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a translated two-panel medicine leaflet PDF from JSON.")
    parser.add_argument("spec", help="Path to JSON render spec")
    args = parser.parse_args()
    print(render(Path(args.spec)).resolve())


if __name__ == "__main__":
    main()
