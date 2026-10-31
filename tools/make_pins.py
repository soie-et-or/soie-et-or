"""Make Soie et Or Pinterest pins (1000 x 1500) in the house style.

Usage: python3 tools/make_pins.py pins/2026-11-02/pins.json
Writes one PNG per pin next to the JSON file, plus PINPLAN.md with titles,
descriptions, links, boards and tagged topics, ready to copy into Pinterest.

pins.json is a list of objects:
  {"file": "10-silk-blouse", "theme": "white|silk|ink",
   "word": "Soie",                      # big gold italic word at the top
   "kicker": "Parisian style",          # small caps line
   "title": "How to Style", "italic": "a Silk Blouse",   # title, second line in italic
   "sub": "One short line under the gold rule.",
   "pin_title": "...", "description": "...", "link": "https://www.soie-et-or.com/journal/...",
   "board": "Parisian Style Outfits", "topics": ["...", "..."], "when": "Mon 2 Nov, 20:00"}
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
TEN = os.path.join(FONTS, "tenor-sans-latin-400-normal.woff")
JOST = os.path.join(FONTS, "jost-latin-500-normal.woff")
BOD = os.path.join(FONTS, "bodoni-moda-latin-400-normal.woff")
BODI = os.path.join(FONTS, "bodoni-moda-latin-400-italic.woff")
GOLD, GOLD_ON_INK = "#a88a4e", "#d4b06c"
W, H = 1000, 1500
THEMES = {"white": ("#ffffff", "#0e0e0e", "#6b6660"),
          "silk": ("#f4f3f1", "#0e0e0e", "#6b6660"),
          "ink": ("#0e0e0e", "#ffffff", "#cfcac4")}

def tracked(d, x, y, text, font, track, fill):
    ws = [d.textlength(c, font=font) for c in text]
    x = x - (sum(ws) + track * (len(text) - 1)) / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=font, fill=fill); x += w + track

def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def centred(d, y, text, font, fill):
    b = d.textbbox((0, 0), text, font=font)
    d.text(((W - (b[2] - b[0])) / 2 - b[0], y), text, font=font, fill=fill)

def make_pin(p, out_dir):
    bg, ink, muted = THEMES[p.get("theme", "white")]
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    tracked(d, W / 2, 90, "SOIE ET OR", ImageFont.truetype(TEN, 30), 30 * 0.32, ink)
    d.rectangle([W / 2 - 40, 150, W / 2 + 40, 152], fill=GOLD)
    size = 270
    fw = ImageFont.truetype(BODI, size)
    while d.textlength(p["word"], font=fw) > 900 and size > 120:
        size -= 10; fw = ImageFont.truetype(BODI, size)
    wb = d.textbbox((0, 0), p["word"], font=fw)
    d.text(((W - (wb[2] - wb[0])) / 2 - wb[0], 270 - wb[1]), p["word"], font=fw,
           fill=GOLD_ON_INK if p.get("theme") == "ink" else GOLD)
    tracked(d, W / 2, 700, p["kicker"].upper(), ImageFont.truetype(JOST, 24), 24 * 0.3, muted)
    tf = ImageFont.truetype(BOD, 84); y = 760
    for ln in wrap(d, p["title"], tf, 820):
        centred(d, y, ln, tf, ink); y += 100
    if p.get("italic"):
        itf = ImageFont.truetype(BODI, 84)
        for ln in wrap(d, p["italic"], itf, 860):
            centred(d, y, ln, itf, ink); y += 100
    y += 62
    d.rectangle([W / 2 - 60, y, W / 2 + 60, y + 2], fill=GOLD); y += 50
    sf = ImageFont.truetype(JOST, 32)
    for ln in wrap(d, p.get("sub", ""), sf, 860):
        centred(d, y, ln, sf, muted); y += 46
    tracked(d, W / 2, H - 90, "SOIE-ET-OR.COM", ImageFont.truetype(JOST, 22), 22 * 0.3, muted)
    if y >= H - 130:
        raise SystemExit(f"{p['file']}: text too long, shorten title or sub")
    img.save(os.path.join(out_dir, p["file"] + ".png"))

def main(spec):
    out_dir = os.path.dirname(os.path.abspath(spec))
    pins = json.load(open(spec, encoding="utf-8"))
    md = ["# Pinplanning", "", "Upload each image in Pinterest, paste the fields and pick the board.", ""]
    for p in pins:
        make_pin(p, out_dir)
        md += [f"## {p['file']}", "", f"![{p['pin_title']}]({p['file']}.png)", "",
               f"- **When:** {p.get('when', '')}", f"- **Board:** {p['board']}",
               f"- **Title:** {p['pin_title']}", f"- **Link:** {p['link']}",
               f"- **Tagged topics:** {' · '.join(p.get('topics', []))}", "",
               "Description:", "", "```", p["description"], "```", ""]
    open(os.path.join(out_dir, "PINPLAN.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"made {len(pins)} pins in {out_dir}")

if __name__ == "__main__":
    main(sys.argv[1])
