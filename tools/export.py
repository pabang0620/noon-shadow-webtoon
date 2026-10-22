"""조립된 웹툰(novel-noon-shadow/webtoon/episodes_v2)을 폰용으로 줄여 이 사이트의 ep/ 아래로 옮기고 manifest.json을 만든다.
사용: python3 tools/export.py   (바뀐 회차만 다시 내보낸다)
"""
import json
import os
from pathlib import Path

from PIL import Image

SITE = Path(__file__).resolve().parents[1]
SRC = Path("/home/lee/project/novel-noon-shadow/webtoon/episodes_v2")
QUALITY = 70  # WebP. 같은 화질에 JPEG보다 약 4분의 1 작다(폰 브라우저 모두 지원)
# 작업용 장 키 -> (출간 화 번호, 제목). novel-noon-shadow/TOC.md 기준
CHAPTERS = [
    ("01", 1, "Twelve Bells"), ("02", 2, "Strays"), ("02_5", 3, "Field Notes"), ("03", 4, "First Light"),
    ("04", 5, "Keep the Hour"), ("04_5", 6, "Second Hand"), ("05", 7, "Half Past Noon"), ("06", 8, "Night Shift"),
    ("06_5", 9, "Golden Hour"), ("07", 10, "Half a Beat"), ("08", 11, "Adjourned"), ("09", 12, "Warrant"),
    ("10", 13, "Morning Star"),
]


def export_part(src_dir: Path, dst_dir: Path) -> list[dict]:
    dst_dir.mkdir(parents=True, exist_ok=True)
    images = []
    for i, f in enumerate(sorted(src_dir.glob("*.jpg")), 1):
        out = dst_dir / f"{i:02d}.webp"
        if not out.exists() or out.stat().st_mtime < f.stat().st_mtime:
            Image.open(f).convert("RGB").save(out, quality=QUALITY, method=5)
        with Image.open(out) as im:
            images.append({"f": f"ep/{dst_dir.name}/{out.name}", "w": im.width, "h": im.height})
    for old in dst_dir.glob("*.webp"):  # 조각 수가 줄었으면 남은 옛 조각을 지운다
        if int(old.stem) > len(images):
            old.unlink()
    return images


def main():
    manifest = []
    for key, no, title in CHAPTERS:
        parts = []
        k = 1
        while (SRC / f"ep{key}-{k}").is_dir():
            imgs = export_part(SRC / f"ep{key}-{k}", SITE / "ep" / f"{key}-{k}")
            if imgs:
                parts.append({"k": k, "images": imgs})
            k += 1
        if parts:
            manifest.append({"key": key, "no": no, "title": title, "parts": parts})
    (SITE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(len(p["images"]) for c in manifest for p in c["parts"])
    print(f"화 {len(manifest)}개, 조각 {total}장")


if __name__ == "__main__":
    main()
