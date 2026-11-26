#!/usr/bin/env python3
"""Lighter WebP copies of every photo in images/ for srcset: a phone (900px) and a laptop (1600px) width,
plus a full-size WebP. Same picture, only resized and re-encoded. Run after adding a photo; commit the results.
Netlify's build (build.py) only copies them, so it needs no image library.

Usage: python3 tools/make_webp.py
"""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "images")
SIZES = (900, 1600)
for name in sorted(os.listdir(IMG)):
    if not name.lower().endswith((".jpg", ".jpeg")) or name.startswith("og-"):
        continue
    src = os.path.join(IMG, name); base = os.path.splitext(src)[0]
    if os.path.exists(base + ".webp") and os.path.getmtime(base + ".webp") >= os.path.getmtime(src):
        continue
    with Image.open(src) as im:
        im = im.convert("RGB")
        for w in SIZES:
            if im.width > w:
                im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(f"{base}-{w}.webp", "WEBP", quality=80, method=6)
        im.save(base + ".webp", "WEBP", quality=82, method=6)
    print("webp", name)
