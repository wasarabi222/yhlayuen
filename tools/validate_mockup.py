from pathlib import Path
import re


html = Path("yhlayuen_mockup/index.html")
text = html.read_text(encoding="utf-8")
srcs = re.findall(r'src="([^"]+)"', text)
missing = []

for src in srcs:
    path = (html.parent / src).resolve()
    if not path.exists():
        missing.append((src, str(path)))

print(f"image refs: {len(srcs)}")
print(f"missing: {len(missing)}")
for src, path in missing:
    print(f"{src} -> {path}")
print(f"css exists: {Path('yhlayuen_mockup/styles.css').exists()}")
