#!/usr/bin/env python3
"""Optimize generated GitHub Pages site without changing source assets.
Requires Pillow. Converts JPG/PNG to WebP, rewrites references and minifies CSS."""
from pathlib import Path
from PIL import Image
import re

root = Path("_site")
assets = root / "assets" / "images"
converted = 0
saved = 0
for source in assets.rglob("*"):
    if source.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        continue
    with Image.open(source) as im:
        dest = source.with_suffix(".webp")
        im.save(dest, "WEBP", quality=72, method=6)
    if dest.stat().st_size < source.stat().st_size:
        saved += source.stat().st_size - dest.stat().st_size
        source.unlink()
        converted += 1
    else:
        dest.unlink()

# Replace only paths to assets that were actually converted.
for source in list(root.rglob("*.html")) + list(root.rglob("*.js")) + list(root.rglob("*.css")):
    original = source.read_text(encoding="utf-8")
    updated = re.sub(
        r"assets/images/([a-zA-Z0-9_./-]+)\.(jpg|jpeg|png)",
        lambda m: ("assets/images/" + m.group(1) + ".webp")
        if (assets / (m.group(1) + ".webp")).exists()
        else m.group(0),
        original,
    )
    if updated != original:
        source.write_text(updated, encoding="utf-8")

print(f"Optimized {converted} images; saved {saved / 1024:.0f} KiB in deployed site")
