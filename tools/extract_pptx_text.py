from pathlib import Path
from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET


PPTX = Path(r"C:\Users\hwaeu\OneDrive\臾몄꽌\移댁뭅?ㅽ넚 諛쏆? ?뚯씪\??026-?꾧컖 罹섎━洹몃씪??留뚮뱾湲??꾨줈洹몃옩 ?쒖븞?? ?곷Ц.pptx")
OUT = Path(r"C:\Users\hwaeu\OneDrive\臾몄꽌\yhlayuen\yhlayuen_mockup\source_notes")


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines = []
    with ZipFile(PPTX) as zf:
        slide_names = sorted(
            [name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml")],
            key=slide_number,
        )
        for slide_name in slide_names:
            root = ET.fromstring(zf.read(slide_name))
            texts = []
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    text = node.text.strip()
                    if text:
                        texts.append(text)
            if texts:
                lines.append(f"## Slide {slide_number(slide_name)}")
                lines.extend(texts)
                lines.append("")
    (OUT / "english_pptx_text.md").write_text("\n".join(lines), encoding="utf-8")
    print(OUT / "english_pptx_text.md")


if __name__ == "__main__":
    main()
