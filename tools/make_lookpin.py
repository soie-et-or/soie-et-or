#!/usr/bin/env python3
"""Format D: product-layout pin. Video: overview page, then one page per look, back to overview.
 Mytheresa product images are placed side by side,
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
    nr = len(s['rows'])
    th = int(min(TH, (H - 180 - 410) / nr - 34 - 16)); size = int(th * 885 / 1000)
    gap = 14; x0 = (W - (4 * size + 3 * gap)) // 2
    y = 410; k = 0
    for row in s['rows']:
        tracked(d, 0, y, row['label'].upper(), JOST, 4, GOLD, left=x0)
        if row.get('desc'):
            df = font('bodoni-moda-latin-400-italic.woff', 25)
            d.text((W - x0 - d.textlength(row['desc'], font=df), y - 6), row['desc'], font=df, fill=MUTED)
        y += 34
        for i, (pnum, kind, brand) in enumerate(row['items'][:4]):
            if n_visible is None or k < n_visible:
                t_ = tile(s.get('img_dir'), pnum, kind, brand)
                if t_.size != (size, th): t_ = t_.resize((size, th), Image.LANCZOS)
                im.paste(t_, (x0 + i * (size + gap), y))
            k += 1
        y += th + 16
    ctext(d, H - 128, s['brands'], BODI_S, MUTED)
    tracked(d, W / 2, H - 70, s['cta'].upper(), JOST_S, 4, INK)
    return im

def render_look(s, row, n, total):
    """One look per page: 2x2 grid of large product images."""
    im = Image.new('RGB', (W, H), PAPER); d = ImageDraw.Draw(im)
    tracked(d, W / 2, 64, 'SOIE ET OR', TEN, 9, INK)
    d.line((W / 2 - 22, 108, W / 2 + 22, 108), fill=GOLD, width=2)
    tracked(d, W / 2, 140, f"{s.get('page_label', 'Look').upper()} {n} OF {total}", JOST, 5, GOLD)
    words = row['label'].rsplit(' ', 1)
    a, b = words[0] + ' ', (words[1] if len(words) > 1 else '')
    wa, wb = d.textlength(a, font=BOD), d.textlength(b, font=BODI)
    x = (W - wa - wb) / 2; d.text((x, 172), a, font=BOD, fill=INK); d.text((x + wa, 172), b, font=BODI, fill=INK)
    wear = row.get('wear') or row.get('desc') or ''
    WF = font('jost-latin-500-normal.woff', 21)
    lines, cur = [], ''
    for w_ in wear.split():
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=WF) > 820 and cur: lines.append(cur); cur = w_
        else: cur = t
    if cur: lines.append(cur)
    for i, ln in enumerate(lines[:3]): ctext(d, 262 + i * 31, ln, WF, MUTED)
    top_y = 262 + 31 * len(lines[:3]) + 22
    its = row['items']
    rows = row.get('outfit') or [its[i:i + 3] for i in range(0, len(its), 3)]   # default: grid of three per row
    gap, maxw, top, bottom = 10, 920, top_y, H - 150
    avail = bottom - top - gap * (len(rows) - 1)
    hs = []
    for r in rows:   # height per row so the widest row fits, capped so all rows fit
        n = len(r); tw = min((maxw - gap * (n - 1)) / n, 300 * 885 / 1000)
        hs.append(tw * 1000 / 885)
    scale = min(1, avail / sum(hs)); y = top + (avail - sum(hs) * scale) / 2
    allb = []
    for r, h in zip(rows, hs):
        th = int(h * scale); tw = int(th * 885 / 1000); n = len(r)
        x = (W - (n * tw + (n - 1) * gap)) // 2
        for pnum, kind, brand in r:
            allb.append(brand)
            p = os.path.join(s.get('img_dir') or '', pnum + '.jpg')
            if os.path.exists(p):
                t = Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS)   # resize only
            else:
                t = Image.new('RGB', (tw, th), TILE); td = ImageDraw.Draw(t)
                for txt, f, yy, col in ((kind.upper(), JOST_S, th / 2 - 22, MUTED), (brand, JOST_S, th / 2 + 4, INK)):
                    td.text(((tw - td.textlength(txt, font=f)) / 2, yy), txt, font=f, fill=col)
            im.paste(t, (x, int(y))); x += tw + gap
        y += th + gap
    brands = ' · '.join(dict.fromkeys(allb))
    bf = BODI_S
    for sz in range(30, 16, -1):
        bf = font('bodoni-moda-latin-400-italic.woff', sz)
        if d.textlength(brands, font=bf) < W - 60: break
    ctext(d, H - 128, brands, bf, MUTED)
    tracked(d, W / 2, H - 70, s['cta'].upper(), JOST_S, 4, INK)
    return im

def video(s, out, fps=30, hold=75, fade=12):
    import subprocess, tempfile
    pages = [render(s)] + [render_look(s, r, i + 1, len(s['rows'])) for i, r in enumerate(s['rows'])] + [render(s)]
    tmp = tempfile.mkdtemp(); idx = 0
    def save(fr):
        nonlocal idx; fr.save(f'{tmp}/{idx:05d}.png'); idx += 1
    for i, pg in enumerate(pages):
        for _ in range(hold if i < len(pages) - 1 else 45): save(pg)
        if i < len(pages) - 1:
            for f in range(1, fade + 1): save(Image.blend(pg, pages[i + 1], f / (fade + 1)))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', f'{tmp}/%05d.png',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out + '.mp4'], check=True)

if __name__ == '__main__':
    s = json.load(open(sys.argv[1]))
    out = s['file']
    render(s).save(out + '.png')
    for i, r in enumerate(s['rows']):
        render_look(s, r, i + 1, len(s['rows'])).save(f'{out}-look{i + 1}.png')
    if s.get('video'): video(s, out)
    print('wrote', out)
