import csv
import re
import ssl
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source_extracts" / "kaja_global_candidates"
SHEET = ROOT / "source_extracts" / "kaja_global_candidates_sheet.jpg"
CSV = ROOT / "source_extracts" / "kaja_global_candidates.csv"

PAGES = [
    ("HUFS seal 2025-06-27", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/811956/"),
    ("CIEE fan 2025-07-10", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/811972/categoryno/1/"),
    ("Kwangwoon language institute 2025-09-26", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/812028/"),
    ("Korea University Korean Center 2023-01-18", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/167308/"),
    ("Korea University mood lamp 2023-02-09", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/167314/"),
    ("Ocean Tour foreign visitors 2018", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/930"),
    ("Sejong language academy 2025-03-13", "https://kaja.re.kr/article/%EA%B0%95%EC%A2%8C%EC%9D%98%EB%A2%B0/12/811893/"),
]

CTX = ssl.create_default_context()
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
    "Referer": "https://kaja.re.kr/",
}


def fetch(url: str) -> bytes:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30, context=CTX) as response:
        return response.read()


def page_image_urls(url: str) -> list[str]:
    html = fetch(url).decode("utf-8", errors="ignore")
    urls = set()
    for attr in re.findall(r"""(?:src|href)=["']([^"']+\.(?:jpg|jpeg|png|webp)(?:\?[^"']*)?)["']""", html, re.I):
        attr = unescape(attr).strip()
        if any(skip in attr.lower() for skip in ["blank", "icon", "btn_", "logo", "ico_", "rating", "spinner"]):
            continue
        urls.add(urljoin(url, attr))
    return sorted(urls)


def file_name(page_label: str, index: int, image_url: str) -> str:
    parsed = urlparse(image_url)
    suffix = Path(parsed.path).suffix.lower() or ".jpg"
    label = re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", page_label)[:44]
    original = re.sub(r"[^0-9A-Za-z가-힣._-]+", "_", Path(parsed.path).stem)[:36]
    return f"{label}-{index:02d}-{original}{suffix}"


def download_images():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for label, page_url in PAGES:
        for idx, image_url in enumerate(page_image_urls(page_url), 1):
            target = OUT / file_name(label, idx, image_url)
            try:
                data = fetch(image_url)
                target.write_bytes(data)
                with Image.open(target) as img:
                    width, height = img.size
                if width < 220 or height < 160:
                    target.unlink(missing_ok=True)
                    continue
                rows.append({
                    "label": label,
                    "page_url": page_url,
                    "image_url": image_url,
                    "file": str(target),
                    "width": width,
                    "height": height,
                })
            except Exception as error:
                print(f"skip {image_url}: {error}")
    return rows


def make_sheet(rows):
    thumb_w, thumb_h = 300, 220
    label_h = 70
    cols = 3
    rows_count = max(1, (len(rows) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows_count * (thumb_h + label_h)), "#f4eee4")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, row in enumerate(rows, 1):
        with Image.open(row["file"]) as img:
            img = img.convert("RGB")
            img.thumbnail((thumb_w - 18, thumb_h - 18))
            x = (idx - 1) % cols * thumb_w
            y = (idx - 1) // cols * (thumb_h + label_h)
            sheet.paste(img, (x + (thumb_w - img.width) // 2, y + (thumb_h - img.height) // 2))
            draw.text((x + 10, y + thumb_h + 6), f"{idx:02d}. {row['label']}"[:44], fill="#211d18", font=font)
            draw.text((x + 10, y + thumb_h + 26), Path(row["file"]).name[:42], fill="#6f665d", font=font)
            draw.text((x + 10, y + thumb_h + 44), f"{row['width']}x{row['height']}", fill="#9f332c", font=font)

    sheet.save(SHEET, quality=92)
    with CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "page_url", "image_url", "file", "width", "height"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"images: {len(rows)}")
    print(SHEET)
    print(CSV)


if __name__ == "__main__":
    make_sheet(download_images())
