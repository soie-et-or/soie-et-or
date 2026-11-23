#!/usr/bin/env python3
"""A chaptered video pin: several photo pages (made with make_prints.render) joined into one MP4.

Usage: python3 tools/make_story.py spec.json
spec: {"file": "out/path/name", "secs": 3, "theme": "ink", "effects": ["diamonds"],
       "pages": [{"photo": "images/x.jpg", "kicker": "...", "title": "...", "italic": "...",
                  "brands": "... (optional)", "cta": "... (optional)", "focus": 0.5}, ...]}
The first page is also saved as <file>.png (the cover). Add "loop": true to end on the cover again.
Uses only our own photos, so it can go live without product-image permission.
"""
import json, os, subprocess, sys, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import make_prints as mp

def main(path):
    s = json.load(open(path)); out = s['file']; tmp = tempfile.mkdtemp()
    pages = s['pages'] + ([s['pages'][0]] if s.get('loop') else [])
    parts = []
    for i, p in enumerate(pages):
        name = f'p{i:02d}'
        mp.render(name, os.path.join(ROOT, p['photo']), p.get('mode', 'photo'),
                  [mp.EFFECTS[e]() for e in p.get('effects', s.get('effects', ['diamonds']))],
                  p['kicker'], p['title'], p['italic'], p.get('brands'),
                  p.get('cta', s.get('cta', 'SEE THE EDIT · SOIE-ET-OR.COM')),
                  focus=p.get('focus', .5), zoom=.05, secs=p.get('secs', s.get('secs', 3)),
                  out_dir=tmp, theme=p.get('theme', s.get('theme', 'ink')))
        parts.append(os.path.join(tmp, name + '.mp4'))
        if i == 0: shutil.copy(os.path.join(tmp, name + '.png'), out + '.png')
    lst = os.path.join(tmp, 'list.txt'); open(lst, 'w').write(''.join(f"file '{q}'\n" for q in parts))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', out + '.mp4'], check=True)
    shutil.rmtree(tmp, ignore_errors=True); print('wrote', out)

if __name__ == '__main__':
    main(sys.argv[1])
