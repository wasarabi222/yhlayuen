from pathlib import Path
import re


SITE = Path("yhlayuen_site")


def resolve_ref(html: Path, ref: str) -> Path:
    return (html.parent / ref).resolve()


def main():
    refs = []
    missing = []
    html_files = sorted(SITE.glob("*.html"))

    for html in html_files:
        text = html.read_text(encoding="utf-8")
        page_refs = []
        page_refs.extend(re.findall(r'src="([^"]+)"', text))
        page_refs.extend(re.findall(r'href="([^"]+\.css)"', text))
        page_refs.extend(re.findall(r'<script[^>]+src="([^"]+)"', text))
        page_refs.extend(re.findall(r'href="([^"]+\.html(?:#[^"]+)?)"', text))
        refs.extend((html, ref) for ref in page_refs)

        for ref in page_refs:
            if ref.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_ref = ref.split("#", 1)[0]
            path = resolve_ref(html, path_ref)
            if not path.exists():
                missing.append((str(html), ref, str(path)))

    print(f"checked refs: {len(refs)}")
    print(f"missing: {len(missing)}")
    for html, ref, path in missing:
        print(f"{html}: {ref} -> {path}")

    assets = list((SITE / "assets").glob("*"))
    print(f"assets: {len(assets)}")
    print(f"html pages: {len(html_files)}")
    print(f"index: {(SITE / 'index.html').exists()}")
    print(f"about: {(SITE / 'about.html').exists()}")
    print(f"css: {(SITE / 'styles.css').exists()}")
    print(f"js: {(SITE / 'script.js').exists()}")


if __name__ == "__main__":
    main()
