import csv
import re
import ssl
from html import unescape
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source_extracts"
CSV = OUT / "kaja_pr_candidates.csv"
TXT = OUT / "kaja_article_9374_text.txt"
CTX = ssl.create_default_context()
HEADERS = {"User-Agent": "Mozilla/5.0 Chrome/125 Safari/537.36", "Referer": "https://kaja.re.kr/"}


def fetch(url: str) -> str:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30, context=CTX) as response:
        return response.read().decode("utf-8", errors="ignore")


def strip_tags(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()


def board_links(url: str, label: str):
    html = fetch(url)
    rows = []
    for href, text in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', html, flags=re.I):
        title = strip_tags(text)
        if not title or len(title) < 4:
            continue
        if any(skip in title for skip in ["장바구니", "로그인", "회원가입", "검색", "목록", "이전", "다음"]):
            continue
        if not re.search(r"어라연|전각|체험|언론|보도|인터뷰|관광|서울|문화|외국|럭셔리|트래블|CIEE|대학교", title, re.I):
            continue
        rows.append({"board": label, "title": title, "url": urljoin(url, href)})
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for page in range(1, 5):
        rows.extend(board_links(f"https://kaja.re.kr/front/php/b/board_list.php?board_no=1&page={page}", "notice_board_no_1"))
        rows.extend(board_links(f"https://kaja.re.kr/board/gallery/list.html?board_no=12&page={page}", "gallery_board_no_12"))

    seen = set()
    deduped = []
    for row in rows:
        key = (row["title"], row["url"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    with CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["board", "title", "url"])
        writer.writeheader()
        writer.writerows(deduped)

    article_url = "https://kaja.re.kr/article/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD/1/9374/page/2/"
    TXT.write_text(strip_tags(fetch(article_url)), encoding="utf-8")
    print(f"rows: {len(deduped)}")
    print(CSV)
    print(TXT)


if __name__ == "__main__":
    main()
