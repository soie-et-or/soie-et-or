"""Soie et Or photo grade: muted colour, warm highlights, matte blacks, fine grain.

Usage: python3 tools/grade.py input.jpg output.jpg [--bw] [--crop 4:5]
"""
import sys
import numpy as np
from PIL import Image

def grade(im, bw=False, strength=1.0, seed=7):
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    if bw:
        a = np.repeat(lum[..., None], 3, axis=2)
    else:
        a = lum[..., None] + (a - lum[..., None]) * (1 - 0.48 * strength)   # mute saturation
    # gentle S-curve for depth
    a = a + 0.10 * strength * (a - 0.5) * (1 - np.abs(2 * a - 1))
    # split tone: warm, silky highlights; slightly cool, neutral shadows
    l = lum[..., None]
    warm = np.array([1.0, 0.94, 0.84])
    cool = np.array([0.94, 0.96, 1.0])
    a = a * (1 + 0.9 * strength * l * (warm - 1)) * (1 + 0.6 * strength * (1 - l) * (cool - 1))
    # matte: lift blacks, soften whites
    a = 0.045 * strength + a * (1 - 0.045 * strength - 0.02 * strength)
    # fine grain
    rng = np.random.default_rng(seed)
    a = a + rng.normal(0, 0.012 * strength, a.shape[:2])[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def crop_ratio(im, ratio, focus_y=0.5):
    w, h = im.size
    rw, rh = ratio
    if w / h > rw / rh:
        nw = int(h * rw / rh); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w * rh / rw); y = int((h - nh) * focus_y)
    return im.crop((0, y, w, y + nh))

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    im = Image.open(src)
    if "--crop" in sys.argv:
        r = sys.argv[sys.argv.index("--crop") + 1].split(":")
        im = crop_ratio(im, (int(r[0]), int(r[1])))
    out = grade(im, bw="--bw" in sys.argv)
    out.save(dst, "JPEG", quality=82, optimize=True, progressive=True)
