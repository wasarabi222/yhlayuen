import csv
import re
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source_extracts" / "ppt_slide_images"


def rels_for_slide(pptx: Path, slide_number: int):
    with zipfile.ZipFile(pptx) as zf:
        presentation = ET.fromstring(zf.read("ppt/presentation.xml"))
        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        }
        rels = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        slide_ids = presentation.findall(".//p:sldIdLst/p:sldId", ns)
        slide_rel_id = slide_ids[slide_number - 1].attrib[f"{{{ns['r']}}}id"]
        slide_path = "ppt/" + rel_map[slide_rel_id].lstrip("/")
        rels_path = f"{Path(slide_path).parent}/_rels/{Path(slide_path).name}.rels"
        slide_rels = ET.fromstring(zf.read(rels_path))
        image_targets = []
        for rel in slide_rels:
            target = rel.attrib.get("Target", "")
            rel_type = rel.attrib.get("Type", "")
            if "image" not in rel_type:
                continue
            image_targets.append(str((Path(slide_path).parent / target).resolve()).split("pptx_root")[-1])
        return slide_path, image_targets


def normalize_target(slide_path: str, target: str) -> str:
    base = PurePosixPath(slide_path).parent
    joined = base / target
    parts = []
    for part in joined.parts:
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def extract_slide_images(pptx: Path, slide_number: int):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    slide_dir = OUT_DIR / f"{pptx.stem}-slide-{slide_number:02d}-{stamp}"
    slide_dir.mkdir(parents=True)

    rows = []
    with zipfile.ZipFile(pptx) as zf:
        presentation = ET.fromstring(zf.read("ppt/presentation.xml"))
        ns = {
            "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
            "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        }
        pres_rels = ET.fromstring(zf.read("ppt/_rels/presentation.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in pres_rels}
        slide_ids = presentation.findall(".//p:sldIdLst/p:sldId", ns)
        slide_rel_id = slide_ids[slide_number - 1].attrib[f"{{{ns['r']}}}id"]
        slide_path = normalize_target("ppt/presentation.xml", rel_map[slide_rel_id])
        rels_path = f"{PurePosixPath(slide_path).parent}/_rels/{PurePosixPath(slide_path).name}.rels"
        slide_rels = ET.fromstring(zf.read(rels_path))

        image_index = 0
        for rel in slide_rels:
            target = rel.attrib.get("Target", "")
            rel_type = rel.attrib.get("Type", "")
            if "image" not in rel_type:
                continue
            image_path = normalize_target(slide_path, target)
            if image_path not in zf.namelist():
                continue
            image_index += 1
            suffix = Path(image_path).suffix.lower() or ".png"
            output = slide_dir / f"slide{slide_number:02d}-image{image_index:02d}{suffix}"
            output.write_bytes(zf.read(image_path))
            try:
                with Image.open(output) as img:
                    width, height = img.size
                rows.append({
                    "file": str(output),
                    "pptx": str(pptx),
                    "slide": slide_number,
                    "source": image_path,
                    "width": width,
                    "height": height,
                })
            except Exception:
                output.unlink(missing_ok=True)

    return slide_dir, rows


def make_sheet(slide_dir: Path, rows: list[dict]):
    thumb_w, thumb_h = 320, 230
    label_h = 56
    cols = 3
    row_count = max(1, (len(rows) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb_w, row_count * (thumb_h + label_h)), "#f4eee4")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, row in enumerate(rows, 1):
        with Image.open(row["file"]) as img:
            img = img.convert("RGB")
            img.thumbnail((thumb_w - 18, thumb_h - 18))
            x = (idx - 1) % cols * thumb_w
            y = (idx - 1) // cols * (thumb_h + label_h)
            sheet.paste(img, (x + (thumb_w - img.width) // 2, y + (thumb_h - img.height) // 2))
            draw.text((x + 10, y + thumb_h + 8), f"{idx:02d}. {Path(row['file']).name}", fill="#211d18", font=font)
            draw.text((x + 10, y + thumb_h + 28), f"{row['width']}x{row['height']}", fill="#9f332c", font=font)

    sheet_path = slide_dir / "contact-sheet.jpg"
    sheet.save(sheet_path, quality=92)
    csv_path = slide_dir / "images.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["file", "pptx", "slide", "source", "width", "height"])
        writer.writeheader()
        writer.writerows(rows)
    print(sheet_path)
    print(csv_path)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python extract_ppt_slide_images.py <pptx> <slide_number>")
    pptx = Path(sys.argv[1])
    slide_number = int(sys.argv[2])
    slide_dir, rows = extract_slide_images(pptx, slide_number)
    make_sheet(slide_dir, rows)
    print(f"images: {len(rows)}")


if __name__ == "__main__":
    main()
