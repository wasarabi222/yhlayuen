from pathlib import Path
import csv
import shutil

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source_extracts" / "artwork_candidates"
SHEET = ROOT / "source_extracts" / "artwork_candidates_sheet.jpg"
CSV = ROOT / "source_extracts" / "artwork_candidates.csv"

SOURCE_DIRS = [
    Path(r"C:\Users\hwaeu\Dropbox\♥홈페이지-\2015-연구소홈피-장서연\2전시회\2회-5회"),
    Path(r"C:\Users\hwaeu\Dropbox\♥홈페이지-\어라연웹작품2\자연미\한글1"),
    Path(r"C:\Users\hwaeu\Dropbox\♥홈페이지-\어라연웹작품2\자연미\한문1"),
]


def safe_name(path: Path) -> str:
    return "".join(ch if ch.isalnum() or ch in " ._-" else "_" for ch in path.stem)[:70]


def collect_images():
    rows = []
    for source in SOURCE_DIRS:
        if not source.exists():
            continue
        for path in source.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue
            try:
                with Image.open(path) as img:
                    width, height = img.size
                rows.append({
                    "source": str(path),
                    "name": path.name,
                    "width": width,
                    "height": height,
                    "area": width * height,
                })
            except Exception:
                continue
    rows.sort(key=lambda row: (row["area"], row["name"]), reverse=True)
    return rows[:48]


def make_sheet(rows):
    OUT.mkdir(parents=True, exist_ok=True)
    thumb_w, thumb_h = 260, 210
    label_h = 64
    cols = 4
    rows_count = (len(rows) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows_count * (thumb_h + label_h)), "#f4eee4")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, row in enumerate(rows, 1):
        src = Path(row["source"])
        target = OUT / f"{idx:02d}-{safe_name(src)}{src.suffix.lower()}"
        shutil.copy2(src, target)
        row["candidate"] = str(target)

        with Image.open(src) as img:
            img = img.convert("RGB")
            img.thumbnail((thumb_w - 18, thumb_h - 18))
            x = (idx - 1) % cols * thumb_w
            y = (idx - 1) // cols * (thumb_h + label_h)
            px = x + (thumb_w - img.width) // 2
            py = y + (thumb_h - img.height) // 2
            sheet.paste(img, (px, py))
            label = f"{idx:02d}. {src.name}"[:44]
            draw.text((x + 10, y + thumb_h + 8), label, fill="#211d18", font=font)
            draw.text((x + 10, y + thumb_h + 28), f"{row['width']}x{row['height']}", fill="#6f665d", font=font)

    sheet.save(SHEET, quality=92)
    with CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["candidate", "source", "name", "width", "height", "area"])
        writer.writeheader()
        writer.writerows(rows)
    print(SHEET)
    print(CSV)


if __name__ == "__main__":
    make_sheet(collect_images())
