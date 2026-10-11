#!/usr/bin/env python3
"""
Builds memes.js from every image in the memes/ folder.

  1. Drop all your meme images into the  memes/  folder (next to this file).
  2. Run:   python3 make-memes.py
  3. Upload the whole folder to your host.

Run it again any time you add or remove memes.
Optional: `pip install pillow` first so image sizes are recorded
(this stops the page from jumping around while images load).
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
FOLDER = HERE / "memes"
EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}

try:
    from PIL import Image
except ImportError:
    Image = None


def natural_key(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def main():
    if not FOLDER.is_dir():
        sys.exit("Couldn't find a 'memes' folder next to this script.")

    files = sorted((p for p in FOLDER.iterdir() if p.suffix.lower() in EXTS), key=natural_key)
    if not files:
        sys.exit("The memes/ folder has no images yet.")

    out = []
    for p in files:
        item = {"src": "memes/" + quote(p.name)}
        if Image:
            try:
                with Image.open(p) as im:
                    item["w"], item["h"] = im.size
            except Exception:
                pass
        out.append(item)

    (HERE / "memes.js").write_text(
        "window.MEMES = " + json.dumps(out, indent=1) + ";\n", encoding="utf-8"
    )
    note = "" if Image else "  (install pillow to also record sizes)"
    print(f"Wrote memes.js with {len(out)} memes.{note}")


if __name__ == "__main__":
    main()
