import csv
import os
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    from PIL import Image, ImageStat
except ImportError:
    Image = None
    ImageStat = None


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "source_extracts"
DROPBOX = Path(r"C:\Users\hwaeu\Dropbox")
KAKAO = Path(r"C:\Users\hwaeu\OneDrive\문서\카카오톡 받은 파일")
IMAGE_SCAN_ROOTS = [
    DROPBOX / "♥홈페이지-",
    DROPBOX / "원장님작품",
    DROPBOX / "@어라연",
]

PPTX_FILES = [
    KAKAO / "★2026-전각 캘리그라피 만들기 프로그램 제안서_ 국문.pptx",
    KAKAO / "★2026-전각 캘리그라피 만들기 프로그램 제안서_ 영문.pptx",
    KAKAO / "★어라연전각연구소 기업소개.pptx",
    KAKAO / "★2026 체험관소개_영문.pptx",
]


def safe_name(path: Path) -> str:
    return re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", path.stem)[:80]


def extract_pptx_text(path: Path) -> str:
    if not path.exists():
        return ""

    lines = [f"# {path.name}", ""]
    with zipfile.ZipFile(path) as zf:
        slide_names = sorted(
            (name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)),
            key=lambda item: int(re.search(r"slide(\d+)\.xml", item).group(1)),
        )
        ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        for slide_name in slide_names:
            xml = zf.read(slide_name)
            root = ET.fromstring(xml)
            texts = [node.text.strip() for node in root.findall(".//a:t", ns) if node.text and node.text.strip()]
            if texts:
                slide_no = re.search(r"slide(\d+)\.xml", slide_name).group(1)
                lines.append(f"## slide {slide_no}")
                lines.extend(texts)
                lines.append("")
    return "\n".join(lines)


def image_metrics(path: Path):
    if Image is None:
        return None
    try:
        with Image.open(path) as img:
            img = img.convert("RGB")
            width, height = img.size
            stat = ImageStat.Stat(img.resize((64, 64)))
            r, g, b = stat.mean
            red_bias = r - ((g + b) / 2)
            darkness = 255 - ((r + g + b) / 3)
            aspect = width / height if height else 0
            return {
                "width": width,
                "height": height,
                "megapixels": round((width * height) / 1_000_000, 2),
                "aspect": round(aspect, 3),
                "red_bias": round(red_bias, 2),
                "darkness": round(darkness, 2),
            }
    except Exception:
        return None


def score_image(path: Path, metrics: dict) -> float:
    text = str(path).lower()
    score = 0.0
    score += min(metrics["megapixels"], 8) * 6
    if 0.65 <= metrics["aspect"] <= 1.65:
        score += 10
    if metrics["red_bias"] > 8:
        score += min(metrics["red_bias"], 60) * 0.45
    if metrics["darkness"] > 45:
        score += min(metrics["darkness"], 120) * 0.18
    for keyword in ["전각", "작품", "개인전", "newyork", "뉴욕", "창조", "부활", "seal", "artwork"]:
        if keyword in text:
            score += 14
    for keyword in ["예약", "명부", "map", "캡처", "장부", "카톡", "kakaotalk"]:
        if keyword.lower() in text:
            score -= 10
    return round(score, 2)


def scan_dropbox_images(limit: int = 80):
    rows = []
    if Image is None:
        return rows

    extensions = {".jpg", ".jpeg", ".png", ".webp"}
    for scan_root in IMAGE_SCAN_ROOTS:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in extensions:
                continue
            metrics = image_metrics(path)
            if not metrics:
                continue
            score = score_image(path, metrics)
            rows.append({
                "score": score,
                "path": str(path),
                **metrics,
            })

    rows.sort(key=lambda row: row["score"], reverse=True)
    return rows[:limit]


def copy_top_images(rows, count: int = 24):
    preview_dir = SOURCE_DIR / "image_candidates"
    preview_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    if Image is None:
        return copied

    for idx, row in enumerate(rows[:count], 1):
        src = Path(row["path"])
        target = preview_dir / f"{idx:02d}-{safe_name(src)}{src.suffix.lower()}"
        if src.exists():
            shutil.copy2(src, target)
            copied.append(str(target))
    return copied


def main():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    combined_text = []
    for path in PPTX_FILES:
        text = extract_pptx_text(path)
        if text:
            output = SOURCE_DIR / f"{safe_name(path)}.txt"
            output.write_text(text, encoding="utf-8")
            combined_text.append(text)
    (SOURCE_DIR / "pptx_combined_text.txt").write_text("\n\n".join(combined_text), encoding="utf-8")

    rows = scan_dropbox_images()
    with (SOURCE_DIR / "dropbox_image_candidates.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fieldnames = ["score", "path", "width", "height", "megapixels", "aspect", "red_bias", "darkness"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    copied = copy_top_images(rows)
    (SOURCE_DIR / "copied_image_candidates.txt").write_text("\n".join(copied), encoding="utf-8")

    print(f"pptx extracted: {len(combined_text)}")
    print(f"image candidates: {len(rows)}")
    print(f"copied candidates: {len(copied)}")


if __name__ == "__main__":
    main()
