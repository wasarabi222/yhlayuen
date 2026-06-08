from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import csv
import math
import os


ROOTS = [
    ("newyork", r"C:\Users\hwaeu\Dropbox\@어라연\@@@개인전\5회 뉴욕개인전", 24),
    ("connections2024", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\2024-커넥션스 럭셔리 서울", 24),
    ("connections2023", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\231113-커넥션스 럭셔리 서울 2023 관광박람", 24),
    ("sitm2023", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\2023서울국제트래블마트 행사 사진", 24),
    ("sitm2022", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\2022 서울국제트래블마트", 24),
    ("russia2019", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\190317_주러시아한국문화원", 24),
    ("youtube2017", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\170712_한국문화산업교류재단 해외유튜버초청", 24),
    ("ciee2025", r"C:\Users\hwaeu\Dropbox\★체험관_행사／언론모음\대외행사\2025-CIEE Seoul Center 캘리그라피 체험", 24),
    ("experience2024", r"C:\Users\hwaeu\Dropbox\@2024_체험사진", 24),
    ("exhibitions_old", r"C:\Users\hwaeu\Dropbox\♥홈페이지-\2015-연구소홈피-장서연\2전시회\개인전시회사진", 24),
    ("works_old1", r"C:\Users\hwaeu\Dropbox\♥홈페이지-\웹작품", 24),
    ("works_old2", r"C:\Users\hwaeu\Dropbox\♥홈페이지-\어라연웹작품2", 24),
    ("gallery_old", r"C:\Users\hwaeu\Dropbox\♥홈페이지-\전각아카데미-갤러리", 24),
]

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
OUT = Path(r"C:\Users\hwaeu\OneDrive\문서\yhlayuen\homepage_assets")
REVIEW = OUT / "__review"
FILE_ATTRIBUTE_OFFLINE = 0x1000
MAX_FILE_SIZE = 60 * 1024 * 1024


def fit_thumb(path: Path, size=(220, 160)):
    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        width, height = im.size
        thumb = ImageOps.contain(im, size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", size, (247, 241, 231))
        canvas.paste(thumb, ((size[0] - thumb.width) // 2, (size[1] - thumb.height) // 2))
        return canvas, width, height


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default()
    rows = []

    for slug, root_s, limit in ROOTS:
        root = Path(root_s)
        if not root.exists():
            continue

        files = []
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in IMG_EXTS:
                continue
            stat = path.stat()
            attrs = getattr(stat, "st_file_attributes", 0)
            if attrs & FILE_ATTRIBUTE_OFFLINE:
                continue
            if stat.st_size > MAX_FILE_SIZE:
                continue
            files.append(path)
        files = sorted(files, key=lambda p: p.stat().st_size, reverse=True)
        selected = files[:limit]
        thumbs = []

        for idx, path in enumerate(selected, start=1):
            try:
                thumb, width, height = fit_thumb(path)
                rows.append(
                    {
                        "group": slug,
                        "index": idx,
                        "path": str(path),
                        "name": path.name,
                        "size_kb": round(path.stat().st_size / 1024, 1),
                        "width": width,
                        "height": height,
                        "folder": str(path.parent),
                        "error": "",
                    }
                )

                tile = Image.new("RGB", (240, 205), (251, 247, 239))
                tile.paste(thumb, (10, 10))
                draw = ImageDraw.Draw(tile)
                draw.text((10, 174), f"{idx:02d} {path.name[:28]}", fill=(29, 26, 22), font=font)
                draw.text(
                    (10, 188),
                    f"{width}x{height} {round(path.stat().st_size / 1024)}KB",
                    fill=(107, 75, 53),
                    font=font,
                )
                thumbs.append(tile)
            except Exception as exc:
                rows.append(
                    {
                        "group": slug,
                        "index": idx,
                        "path": str(path),
                        "name": path.name,
                        "size_kb": round(path.stat().st_size / 1024, 1),
                        "width": "",
                        "height": "",
                        "folder": str(path.parent),
                        "error": str(exc),
                    }
                )

        if thumbs:
            cols = 4
            row_count = math.ceil(len(thumbs) / cols)
            sheet = Image.new("RGB", (cols * 240, row_count * 205 + 44), (247, 241, 231))
            draw = ImageDraw.Draw(sheet)
            draw.text((12, 12), f"{slug} - top {len(thumbs)} images by file size", fill=(29, 26, 22), font=font)
            for i, tile in enumerate(thumbs):
                x = (i % cols) * 240
                y = (i // cols) * 205 + 44
                sheet.paste(tile, (x, y))
            sheet.save(REVIEW / f"contact_{slug}.jpg", quality=90)

    with open(REVIEW / "asset_inventory.csv", "w", newline="", encoding="utf-8-sig") as handle:
        fieldnames = ["group", "index", "path", "name", "size_kb", "width", "height", "folder", "error"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows to {REVIEW}")


if __name__ == "__main__":
    main()
