#!/usr/bin/env python3
"""Format D: product-layout pin. Mytheresa product images are placed side by side,
only resized, never cropped, cut out or recoloured.

Usage: python3 tools/make_lookpin.py spec.json
spec: {"file": "out/name", "img_dir": "dir with <PNUM>.jpg", "kicker": "...",
       "title": "...", "italic": "...", "sub": "...", "brands": "...", "cta": "...",
       "rows": [{"label": "The Camel Look", "items": [["P01217134", "Coat", "Max Mara"], ...]}]}
Missing images are drawn as labelled placeholders.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, 'fonts') + '/'
W, H = 1000, 1500
PAPER, INK, MUTED, GOLD, TILE = (255, 255, 255), (30, 26, 24), (120, 114, 108), (168, 138, 78), (240, 238, 235)

def font(name, size): return ImageFont.truetype(F + name, size)
BOD = font('bodoni-moda-latin-400-normal.woff', 64)
BODI = font('bodoni-moda-latin-400-italic.woff', 64)
BODI_S = font('bodoni-moda-latin-400-italic.woff', 30)
JOST = font('jost-latin-500-normal.woff', 19)
JOST_S = font('jost-latin-500-normal.woff', 16)
TEN = font('tenor-sans-latin-400-normal.woff', 24)

def tracked(d, cx, y, text, f, track, fill, left=None):
    ws = [d.textlength(c, font=f) for c in text]
    x = left if left is not None else cx - (sum(ws) + track * (len(text) - 1)) / 2
    for c, w in zip(text, ws):
        d.text((x, y), c, font=f, fill=fill); x += w + track

def ctext(d, y, t, f, fill):
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=fill)

TW, TH = 220, 249   # Mytheresa product images are 885x1000

def tile(img_dir, pnum, kind, brand, size=TW):
    p = os.path.join(img_dir or '', pnum + '.jpg')
    if img_dir and os.path.exists(p):
        im = Image.open(p).convert('RGB')
        return im.resize((TW, TH), Image.LANCZOS)          # resize only, same aspect
    t = Image.new('RGB', (TW, TH), TILE); d = ImageDraw.Draw(t)
    bf = BODI_S
    for sz in range(30, 14, -2):
        bf = font('bodoni-moda-latin-400-italic.woff', sz)
        if d.textlength(brand, font=bf) < size - 24: break
    for txt, f, y, col in ((kind.upper(), JOST_S, TH / 2 - 24, MUTED), (brand, bf, TH / 2 + 2, INK)):
        d.text(((size - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col)
    return t

def render(s, n_visible=None):
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    tracked(d, W / 2, 64, 'SOIE ET OR', TEN, 9, INK)
    d.line((W / 2 - 22, 108, W / 2 + 22, 108), fill=GOLD, width=2)
    tracked(d, W / 2, 140, s['kicker'].upper(), JOST, 5, MUTED)
    ctext(d, 172, s['title'], BOD, INK)
    ctext(d, 246, s['italic'], BODI, INK)
    ctext(d, 340, s['sub'], JOST, MUTED)
    size, gap = TW, 14; x0 = (W - (4 * size + 3 * gap)) // 2
    y = 410; k = 0
    for row in s['rows']:
        tracked(d, 0, y, row['label'].upper(), JOST, 4, GOLD, left=x0)
        if row.get('desc'):
            df = font('bodoni-moda-latin-400-italic.woff', 25)
            d.text((W - x0 - d.textlength(row['desc'], font=df), y - 6), row['desc'], font=df, fill=MUTED)
        y += 34
        for i, (pnum, kind, brand) in enumerate(row['items'][:4]):
            if n_visible is None or k < n_visible:
                im.paste(tile(s.get('img_dir'), pnum, kind, brand, size), (x0 + i * (size + gap), y))
            k += 1
        y += TH + 26
    ctext(d, H - 128, s['brands'], BODI_S, MUTED)
    tracked(d, W / 2, H - 70, s['cta'].upper(), JOST_S, 4, INK)
    return im

if __name__ == '__main__':
    s = json.load(open(sys.argv[1]))
    out = s['file']
    render(s).save(out + '.png')
    if s.get('video'):
        import subprocess, tempfile
        tmp = tempfile.mkdtemp(); n = sum(len(r['items'][:4]) for r in s['rows'])
        fps, per, hold = 30, 12, 90   # one product every 0.4 s, then hold 3 s
        frames = [render(s, i) for i in range(n + 1)]
        idx = 0
        for i in range(n + 1):
            for _ in range(per if i < n else hold):
                frames[i].save(f'{tmp}/{idx:05d}.png'); idx += 1
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/%05d.png',
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out + '.mp4'], check=True)
    print('wrote', out)
