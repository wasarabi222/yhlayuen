from pathlib import Path
from PIL import Image, ImageOps
from PIL import ImageDraw, ImageFont
import csv
import math
import re


REVIEW = Path(r"C:\Users\hwaeu\OneDrive\臾몄꽌\yhlayuen\homepage_assets\__review")
OUT = Path(r"C:\Users\hwaeu\OneDrive\臾몄꽌\yhlayuen\homepage_assets")
MAX_SIDE = 2400

SELECTED = [
    ("newyork", 1, "01-hero", "hero / works", 95, "New York exhibition artwork. Strong global artist signal; good for hero crop or featured works."),
    ("newyork", 3, "01-hero", "hero / works", 92, "New York exhibition artwork with strong black, red, and gold contrast."),
    ("newyork", 10, "02-profile-works", "New York exhibition", 90, "Installation/gallery view. Useful for international exhibition timeline."),
    ("newyork", 15, "02-profile-works", "New York exhibition", 82, "Gallery exterior context. Use small in archive/timeline, not hero."),
    ("newyork", 18, "02-profile-works", "New York exhibition", 88, "Object display wall. Good proof of overseas exhibition presentation."),
    ("newyork", 19, "02-profile-works", "New York exhibition", 86, "Large artwork in gallery. Good for works/archive section."),
    ("newyork", 23, "02-profile-works", "New York exhibition", 84, "Object display detail. Useful for archive rhythm."),
    ("works_old1", 1, "02-profile-works", "jeongak detail", 94, "Classic seal object on black. Excellent visual motif for profile site."),
    ("works_old1", 2, "02-profile-works", "jeongak detail", 94, "Round seal object. Strong traditional Korean material detail."),
    ("works_old1", 8, "02-profile-works", "jeongak detail", 92, "Three-dimensional seal block. Useful for craft/art bridge."),
    ("exhibitions_old", 1, "02-profile-works", "early exhibition work", 88, "Soft white work image. Works well with Hanji Ivory UI."),
    ("exhibitions_old", 8, "02-profile-works", "early exhibition work", 88, "Circular installation-like work. Good for contemporary expansion story."),
    ("exhibitions_old", 10, "02-profile-works", "Korean foundation", 86, "Early domestic exhibition room. Use for Phase 1 foundation."),
    ("exhibitions_old", 12, "02-profile-works", "Korean foundation", 84, "Gallery wall view with black works. Good timeline support image."),
    ("russia2019", 7, "03-global-events", "global workshop", 94, "Foreign participant carving. Strong global hands-on culture image."),
    ("russia2019", 14, "03-global-events", "global workshop", 92, "International group at workshop table. Good for global program section."),
    ("russia2019", 17, "03-global-events", "global workshop", 88, "Crowded workshop table. Shows participation and energy."),
    ("russia2019", 22, "03-global-events", "global culture", 84, "Korean culture center portrait moment. Use sparingly as archive proof."),
    ("sitm2023", 2, "03-global-events", "travel mart", 86, "SITM venue/signage. Good evidence image for global travel-mart timeline."),
    ("sitm2023", 7, "03-global-events", "buyer meeting", 90, "Buyer meeting table. Strong B2B global program proof."),
    ("sitm2023", 8, "03-global-events", "buyer meeting", 88, "Consultation scene. Use in global section or archive."),
    ("sitm2023", 17, "03-global-events", "program detail", 86, "Fan/calligraphy close-up from travel mart. Good visual relief."),
    ("sitm2022", 1, "03-global-events", "travel mart", 82, "SITM 2022 venue. Use small for timeline depth."),
    ("sitm2022", 11, "03-global-events", "buyer meeting", 86, "International buyer holding Korean craft. Good global proof."),
    ("sitm2022", 16, "03-global-events", "buyer meeting", 88, "Hands-on buyer consultation scene."),
    ("connections2023", 1, "03-global-events", "luxury travel", 93, "Hand stamping name seals. Very strong luxury travel workshop detail."),
    ("connections2023", 3, "03-global-events", "luxury travel", 90, "Close-up workshop process at Connections Luxury Seoul."),
    ("connections2023", 5, "03-global-events", "luxury travel", 88, "Workshop table with international guests."),
    ("connections2023", 7, "03-global-events", "luxury travel", 84, "Signage explaining Dojang experience in English."),
    ("connections2023", 9, "03-global-events", "luxury travel", 88, "Guided workshop in refined venue. Good for global programs."),
    ("connections2023", 15, "03-global-events", "luxury travel", 90, "Foreign participants holding results. Strong social proof."),
    ("connections2023", 20, "03-global-events", "luxury travel", 82, "Small experience display table. Use as detail image."),
    ("connections2023", 22, "03-global-events", "luxury travel", 88, "Finished result close-up. Strong bridge between experience and memory."),
    ("experience2024", 1, "04-experience", "calligraphy result", 86, "Completed hanging calligraphy. Good for experience card."),
    ("experience2024", 3, "04-experience", "calligraphy process", 88, "Hands writing. Useful as process image."),
    ("experience2024", 5, "04-experience", "calligraphy process", 88, "Close process crop. Good for quiet studio feel."),
    ("experience2024", 14, "04-experience", "calligraphy process", 84, "Participant working with brush. Good secondary card image."),
    ("experience2024", 22, "04-experience", "calligraphy process", 86, "Close-up hand movement. Good for process section."),
    ("youtube2017", 1, "04-experience", "foreign visitors", 86, "Foreign YouTuber group workshop. Useful for global visitor proof."),
    ("youtube2017", 11, "04-experience", "foreign visitors", 86, "Mixed international group experience table."),
    ("youtube2017", 21, "04-experience", "foreign visitors", 88, "Hands-on group table. Strong experience proof."),
    ("youtube2017", 23, "04-experience", "foreign visitors", 86, "Conversation/workshop moment with foreign guests."),
]

SUPPLEMENTAL = [
    (r"C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\c53e59c34238c068\outputs\yhlayuen-pptx-inspect\company\ppt\media\image21.png", "04-experience", "studio mood", 92, "PPT source: transparent calligraphy result with greenery. Excellent warm studio mood."),
    (r"C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\c53e59c34238c068\outputs\yhlayuen-pptx-inspect\company\ppt\media\image54.png", "04-experience", "kits / preparation", 82, "PPT source: prepared kits. Use small; too busy for hero."),
    (r"C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\c53e59c34238c068\outputs\yhlayuen-pptx-inspect\company\ppt\media\image1.png", "05-space-archive", "studio/classroom", 82, "PPT source: classroom/studio scene with director. Use for where-it-happens, not hero."),
    (r"C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\c53e59c34238c068\outputs\yhlayuen-pptx-inspect\program\ppt\media\image16.jpg", "04-experience", "finished seal", 86, "PPT source: finished seal/name cards. Good experience detail."),
    (r"C:\Users\CodexSandboxOffline\.codex\.sandbox\cwd\c53e59c34238c068\outputs\yhlayuen-pptx-inspect\program\ppt\media\image17.jpg", "04-experience", "finished seal", 84, "PPT source: multiple finished seals. Colorful; use small."),
    (r"C:\Users\hwaeu\Dropbox\@?대씪??源?꾩닕?ъ쭊- .jpg", "02-profile-works", "profile portrait", 78, "Dropbox source: formal portrait candidate. Usable, but a newer warm studio portrait would be better."),
    (r"C:\Users\hwaeu\Dropbox\@?대씪???대씪?곗옄?붿긽2.jpg", "02-profile-works", "artist identity", 88, "Dropbox source: self-portrait style engraving image. Strong conceptual profile support."),
]


def slugify(text: str) -> str:
    text = re.sub(r"[\\/:*?\"<>|]+", "-", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text[:120]


def save_web_copy(source: Path, dest: Path):
    with Image.open(source) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        elif im.mode == "L":
            im = im.convert("RGB")

        width, height = im.size
        scale = min(MAX_SIDE / max(width, height), 1.0)
        if scale < 1:
            im = im.resize((round(width * scale), round(height * scale)), Image.Resampling.LANCZOS)

        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, "JPEG", quality=88, optimize=True, progressive=True)
        return im.size


def main():
    inventory = {}
    with open(REVIEW / "asset_inventory.csv", newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            inventory[(row["group"], int(row["index"]))] = row

    rows = []
    for group, index, folder, use_case, score, note in SELECTED:
        source_row = inventory.get((group, index))
        if not source_row:
            continue
        source = Path(source_row["path"])
        out_name = f"{group}-{index:02d}-{slugify(source.stem)}.jpg"
        dest = OUT / folder / out_name
        size = save_web_copy(source, dest)
        rows.append(
            {
                "selected_file": str(dest),
                "source_file": str(source),
                "source_group": group,
                "source_index": index,
                "use_case": use_case,
                "fit_score": score,
                "width": size[0],
                "height": size[1],
                "note": note,
            }
        )

    for i, (source_s, folder, use_case, score, note) in enumerate(SUPPLEMENTAL, start=1):
        source = Path(source_s)
        if not source.exists():
            continue
        out_name = f"supplemental-{i:02d}-{slugify(source.stem)}.jpg"
        dest = OUT / folder / out_name
        size = save_web_copy(source, dest)
        rows.append(
            {
                "selected_file": str(dest),
                "source_file": str(source),
                "source_group": "pptx",
                "source_index": i,
                "use_case": use_case,
                "fit_score": score,
                "width": size[0],
                "height": size[1],
                "note": note,
            }
        )

    manifest = OUT / "selected_assets_manifest.csv"
    with open(manifest, "w", newline="", encoding="utf-8-sig") as handle:
        fieldnames = ["selected_file", "source_file", "source_group", "source_index", "use_case", "fit_score", "width", "height", "note"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    make_selected_contact_sheet(rows)
    print(f"copied {len(rows)} selected assets")
    print(manifest)


def make_selected_contact_sheet(rows):
    font = ImageFont.load_default()
    thumbs = []
    for idx, row in enumerate(rows, start=1):
        path = Path(row["selected_file"])
        if not path.exists():
            continue
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            thumb = ImageOps.contain(im, (220, 150), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (240, 205), (251, 247, 239))
            tile.paste(thumb, ((240 - thumb.width) // 2, 10))
            draw = ImageDraw.Draw(tile)
            draw.text((10, 162), f"{idx:02d} {Path(path).name[:28]}", fill=(29, 26, 22), font=font)
            draw.text((10, 176), f"{row['use_case']} / score {row['fit_score']}", fill=(107, 75, 53), font=font)
            draw.text((10, 190), f"{row['width']}x{row['height']}", fill=(107, 75, 53), font=font)
            thumbs.append(tile)

    if not thumbs:
        return

    cols = 4
    row_count = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 240, row_count * 205 + 44), (247, 241, 231))
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 12), "yhlayuen homepage selected assets", fill=(29, 26, 22), font=font)
    for i, tile in enumerate(thumbs):
        x = (i % cols) * 240
        y = (i // cols) * 205 + 44
        sheet.paste(tile, (x, y))
    sheet.save(REVIEW / "contact_selected_assets.jpg", quality=90)


if __name__ == "__main__":
    main()
