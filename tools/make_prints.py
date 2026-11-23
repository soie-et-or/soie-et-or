"""Make Soie et Or "print" pins: a real photo turned into an illustrated print, with a season
effect (snow, autumn leaves, gold sparkle, string lights, sun), a slow zoom and the caption panel.
Writes an 8-second MP4 (video pin, 1000x1500) and a PNG cover per pin, next to the JSON file.

Usage: python3 tools/make_prints.py pins/2026-12-01/prints.json
Needs: pip install --break-system-packages opencv-python-headless numpy pillow ; ffmpeg on PATH.

prints.json is a list of objects:
  {"file": "gift-edit", "photo": "images/silk-gold-gloves-card.jpg" (path from the repo root),
   "mode": "colour" | "sepia" (drawn print) | "photo" (real photo, soft film look),  "focus": 0.0-1.0 (vertical crop),
   "effects": ["diamonds", "snow", "sparkle", "leaves", "lights", "sun"], "theme": "white" | "ink",
   "kicker": "The Jewelry Gift Edit", "title": "Gold she'll", "italic": "keep forever",
   "brands": "In the edit: Bvlgari · Pomellato" (optional; only for pins that link to a board),
   "cta": "DISCOVER THE EDIT · SOIE-ET-OR.COM" (or DISCOVER THE STORY for articles without an edit)}
Only use photos we have the rights to (own, Pexels, Unsplash). Never write that the person in a stock
photo wears or recommends a brand; brands only as "In the edit: ...".
"""
import cv2, numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
def soft_print(path, W=1000, k=12, light=0.18, lines=0.7):
    img=cv2.imread(path); h,w=img.shape[:2]; img=cv2.resize(img,(W,int(h*W/w)),interpolation=cv2.INTER_AREA)
    sty=cv2.stylization(img, sigma_s=40, sigma_r=0.3)
    Z=sty.reshape(-1,3).astype(np.float32)
    _,lab,cen=cv2.kmeans(Z,k,None,(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,20,1.0),3,cv2.KMEANS_PP_CENTERS)
    post=cen.astype(np.uint8)[lab.flatten()].reshape(sty.shape)
    post=cv2.addWeighted(post,.6,sty,.4,0)
    paper=np.full_like(post,(247,247,247))  # neutral light paper
    post=cv2.addWeighted(post,1-light,paper,light,0)
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY); g=cv2.medianBlur(g,5)
    edges=cv2.adaptiveThreshold(g,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,13,7)
    m=(255-edges)[...,None]/255.0*lines
    res=(post*(1-m)+np.array((38,40,48))*m).astype(np.uint8)
    # paper grain
    noise=np.random.default_rng(1).normal(0,6,res.shape[:2])[...,None]
    res=np.clip(res+noise,0,255).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(res,cv2.COLOR_BGR2RGB)).convert("RGBA")
def glow_dot(layer,x,y,r,col):
    g=Image.new("RGBA",layer.size,(0,0,0,0)); d=ImageDraw.Draw(g)
    d.ellipse([x-r*3,y-r*3,x+r*3,y+r*3],fill=col+(70,)); g=g.filter(ImageFilter.GaussianBlur(r*1.6))
    layer.alpha_composite(g); ImageDraw.Draw(layer).ellipse([x-r,y-r,x+r,y+r],fill=col+(255,))
def snow(im,n=220,seed=3):
    rnd=random.Random(seed); lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    for i in range(n):
        x=rnd.uniform(0,im.width); y=rnd.uniform(0,im.height); r=rnd.uniform(1.5,5)
        d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,rnd.randint(170,240)))
    big=Image.new("RGBA",im.size,(0,0,0,0)); db=ImageDraw.Draw(big)
    for i in range(14):
        x=rnd.uniform(0,im.width); y=rnd.uniform(0,im.height); r=rnd.uniform(10,18)
        for a in range(6):
            t=a*math.pi/3; db.line([x,y,x+r*math.cos(t),y+r*math.sin(t)],fill=(255,255,255,230),width=2)
            for s in (.55,):
                bx,by=x+r*s*math.cos(t),y+r*s*math.sin(t)
                for o in (-0.6,0.6): db.line([bx,by,bx+r*.35*math.cos(t+o),by+r*.35*math.sin(t+o)],fill=(255,255,255,230),width=2)
    im.alpha_composite(lay); im.alpha_composite(big)
def leaves(im,n=40,seed=5):
    rnd=random.Random(seed)
    for i in range(n):
        lay=Image.new("RGBA",(60,60),(0,0,0,0)); d=ImageDraw.Draw(lay)
        col=rnd.choice([(201,129,62),(168,69,47),(216,169,74),(184,92,58),(150,110,60)])
        d.polygon([(30,6),(44,22),(40,44),(30,54),(20,44),(16,22)],fill=col+(235,)); d.line([30,6,30,58],fill=(60,40,30,255),width=2)
        lay=lay.rotate(rnd.uniform(0,360),expand=True,resample=Image.BICUBIC); s=rnd.uniform(.5,1.1)
        lay=lay.resize((int(lay.width*s),int(lay.height*s)))
        im.alpha_composite(lay,(int(rnd.uniform(0,im.width-40)),int(rnd.uniform(0,im.height-40))))
def string_lights(im,y0=40,seed=2):
    lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay); W=im.width
    pts=[]
    for x in range(-20,W+40,6): pts.append((x, y0+35*math.sin(x/W*math.pi*2)+30))
    d.line(pts,fill=(40,36,34,255),width=2); im.alpha_composite(lay)
    for i,(x,y) in enumerate(pts[::9]): glow_dot(im,x,y+8,5,(255,214,140))
def sun(im,x,y,r):
    lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.ellipse([x-r*2,y-r*2,x+r*2,y+r*2],fill=(255,214,140,90)); lay=lay.filter(ImageFilter.GaussianBlur(r*.8)); im.alpha_composite(lay)
    lay=Image.new("RGBA",im.size,(0,0,0,0)); d=ImageDraw.Draw(lay); d.ellipse([x-r,y-r,x+r,y+r],fill=(250,200,110,170)); im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(4)))

import math, random, os, subprocess, shutil, json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
F=os.path.join(HERE,'fonts')+'/'
BOD=ImageFont.truetype(F+'bodoni-moda-latin-400-normal.woff',66); BODI=ImageFont.truetype(F+'bodoni-moda-latin-400-italic.woff',66)
BODI_S=ImageFont.truetype(F+'bodoni-moda-latin-400-italic.woff',38)
JOST=ImageFont.truetype(F+'jost-latin-500-normal.woff',24); JOST_S=ImageFont.truetype(F+'jost-latin-500-normal.woff',21)
TEN=ImageFont.truetype(F+'tenor-sans-latin-400-normal.woff',28)
W,H,PH=1000,1500,1080
INK=(30,26,24); PAPER=(255,255,255); GOLD=(194,154,82); MUTED=(107,102,96)
IMG=''
def tracked(d,cx,y,text,font,track,fill):
    ws=[d.textlength(c,font=font) for c in text]; x=cx-(sum(ws)+track*(len(text)-1))/2
    for c,w in zip(text,ws): d.text((x,y),c,font=font,fill=fill); x+=w+track
def ctext(d,y,t,f,fill): w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
def make_base(src,mode,light=.14):
    if mode=='photo':   # the real photo, with a soft film look (no drawing)
        from PIL import ImageEnhance
        im=Image.open(IMG+src).convert('RGB'); im=im.resize((1300,int(im.height*1300/im.width)),Image.LANCZOS)
        im=ImageEnhance.Color(im).enhance(.85); im=ImageEnhance.Contrast(im).enhance(1.06)
        grain=np.random.default_rng(3).normal(0,5,(im.height,im.width,1))
        return Image.fromarray(np.clip(np.asarray(im).astype(float)+grain,0,255).astype('uint8'))
    b=soft_print(IMG+src,W=1300,light=light,lines=.7)
    if mode=='sepia':
        g=b.convert('L'); lut=[tuple(int(INK[c]+((250,250,249)[c]-INK[c])*(i/255)**0.9) for c in range(3)) for i in range(256)]
        return Image.merge('RGB',[g.point([l[c] for l in lut]) for c in range(3)])
    return b.convert('RGB')
class Snow:
    def __init__(s,n=230,seed=4): r=random.Random(seed); s.f=[[r.uniform(0,W),r.uniform(0,PH),r.uniform(1.5,5),r.uniform(2,6),r.uniform(0,6.3)] for _ in range(n)]
    def draw(s,lay,t):
        d=ImageDraw.Draw(lay)
        for x0,y0,r,v,ph in s.f:
            x=x0+math.sin(t*1.3+ph)*12; y=(y0+t*v*40)%(PH+20)-10; d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,215))
class Leaves:
    def __init__(s,n=34,seed=6):
        r=random.Random(seed); s.l=[]
        for _ in range(n):
            col=r.choice([(201,129,62),(168,69,47),(216,169,74),(184,92,58),(150,110,60)])
            sp=Image.new('RGBA',(60,60),(0,0,0,0)); d=ImageDraw.Draw(sp)
            d.polygon([(30,6),(44,22),(40,44),(30,54),(20,44),(16,22)],fill=col+(240,)); d.line([30,6,30,58],fill=(60,40,30,255),width=2)
            s.l.append([sp,r.uniform(-50,W),r.uniform(0,PH),r.uniform(.5,1.0),r.uniform(30,70),r.uniform(25,60),r.uniform(0,360),r.uniform(-90,90),r.uniform(0,6.3)])
    def draw(s,lay,t):
        for sp,x0,y0,sc,vy,vx,rot,vr,ph in s.l:
            x=(x0+t*vx+math.sin(t*1.6+ph)*30)%(W+80)-40; y=(y0+t*vy)%(PH+60)-30
            im=sp.rotate(rot+t*vr,expand=True,resample=Image.BICUBIC); im=im.resize((int(im.width*sc),int(im.height*sc)))
            lay.alpha_composite(im,(int(x),int(y)))
class Sparkle:
    def __init__(s,n=40,seed=8,area=(0,0,W,PH)):
        r=random.Random(seed); x0,y0,x1,y1=area; s.p=[(r.uniform(x0,x1),r.uniform(y0,y1),r.uniform(2,4),r.uniform(0,6.3),r.uniform(1.5,3)) for _ in range(n)]
    def draw(s,lay,t):
        g=Image.new('RGBA',lay.size,(0,0,0,0)); d=ImageDraw.Draw(g); d2=ImageDraw.Draw(lay)
        for x,y,r,ph,sp in s.p:
            a=(math.sin(t*sp+ph)+1)/2
            if a<.15: continue
            d.ellipse([x-r*4,y-r*4,x+r*4,y+r*4],fill=(255,214,140,int(90*a)))
            L=r*3.2*a; d2.line([x-L,y,x+L,y],fill=(255,240,200,int(255*a)),width=2); d2.line([x,y-L,x,y+L],fill=(255,240,200,int(255*a)),width=2)
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(5)))
class Diamonds:
    """Small glittering diamonds that drift down slowly and catch the light."""
    def __init__(s,n=46,seed=12):
        r=random.Random(seed); s.d=[]
        for _ in range(n):
            size=r.uniform(5,15); sp=Image.new('RGBA',(int(size*2)+4,int(size*2.6)+4),(0,0,0,0)); dd=ImageDraw.Draw(sp)
            cx,cy=sp.width/2,sp.height/2; w,h=size,size*1.3
            dd.polygon([(cx,cy-h),(cx+w,cy-h*.25),(cx,cy+h),(cx-w,cy-h*.25)],fill=(255,255,255,190))
            dd.polygon([(cx,cy-h),(cx+w,cy-h*.25),(cx,cy-h*.1)],fill=(225,235,255,230))
            dd.polygon([(cx,cy-h*.1),(cx-w,cy-h*.25),(cx,cy+h)],fill=(205,215,235,170))
            s.d.append([sp,r.uniform(0,W),r.uniform(0,PH),r.uniform(18,45),r.uniform(0,6.3),r.uniform(1.5,3.5),r.uniform(-25,25)])
    def draw(s,lay,t):
        g=Image.new('RGBA',lay.size,(0,0,0,0)); dg=ImageDraw.Draw(g); dl=ImageDraw.Draw(lay)
        for sp,x0,y0,v,ph,tw,rot in s.d:
            x=x0+math.sin(t*.9+ph)*14; y=(y0+t*v)%(PH+40)-20
            a=.55+.45*math.sin(t*tw+ph)
            im=sp.rotate(rot+math.sin(t+ph)*15,expand=True,resample=Image.BICUBIC)
            im.putalpha(im.getchannel('A').point(lambda v:int(v*a)))
            lay.alpha_composite(im,(int(x-im.width/2),int(y-im.height/2)))
            if a>.9:   # a brief flash of light
                L=sp.width*1.1*(a-.9)*10
                dl.line([x-L,y,x+L,y],fill=(255,255,255,220),width=2); dl.line([x,y-L,x,y+L],fill=(255,255,255,220),width=2)
                dg.ellipse([x-L,y-L,x+L,y+L],fill=(255,245,220,110))
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(4)))
class Lights:
    def __init__(s,y0=30): 
        s.pts=[(x, y0+32*math.sin(x/W*math.pi*2)+28) for x in range(-20,W+40,6)]; s.bulbs=s.pts[::9]
    def draw(s,lay,t):
        d=ImageDraw.Draw(lay); d.line(s.pts,fill=(40,36,34,255),width=2)
        g=Image.new('RGBA',lay.size,(0,0,0,0)); dg=ImageDraw.Draw(g)
        for i,(x,y) in enumerate(s.bulbs):
            a=.65+.35*math.sin(t*3+i*1.7); dg.ellipse([x-16,y-8,x+16,y+24],fill=(255,214,140,int(110*a)))
            d.ellipse([x-5,y+3,x+5,y+13],fill=(255,226,160,255))
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(6)))
class Sun:
    def __init__(s,x,y,r): s.x,s.y,s.r=x,y,r
    def draw(s,lay,t):
        r=s.r*(1+.04*math.sin(t*1.2)); g=Image.new('RGBA',lay.size,(0,0,0,0)); d=ImageDraw.Draw(g)
        d.ellipse([s.x-r*2.2,s.y-r*2.2,s.x+r*2.2,s.y+r*2.2],fill=(255,214,140,80)); d.ellipse([s.x-r,s.y-r,s.x+r,s.y+r],fill=(250,200,110,170))
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(r*.35)))
class Sheen:
    """A soft band of light that glides diagonally across the photo, like light moving over silk."""
    def __init__(s,period=4.0,width=230,strength=70):
        s.p,s.w,s.k=period,width,strength
        L=int((W+PH)*1.6); band=Image.new('L',(L,s.w*3),0); d=ImageDraw.Draw(band)
        for i in range(s.w*3):
            v=math.exp(-((i-s.w*1.5)/(s.w*.45))**2); d.line([(0,i),(L,i)],fill=int(255*v))
        s.band=band.rotate(-32,expand=True,resample=Image.BICUBIC)
    def draw(s,lay,t):
        # dim the photo slightly everywhere and let a band of light travel across it
        f=(t%s.p)/s.p; x=int(-s.band.width*.75+f*(W+s.band.width*.6)); y=int((PH-s.band.height)/2)
        band=Image.new('L',lay.size,0); band.paste(s.band,(x,y))
        dark=band.point(lambda v:int(s.k*(1-v/255)))
        sh=Image.new('RGBA',lay.size,(20,16,12,0)); sh.putalpha(dark); lay.alpha_composite(sh)
        hi=Image.new('RGBA',lay.size,(255,250,240,0)); hi.putalpha(band.point(lambda v:int(v*.22))); lay.alpha_composite(hi)
class Bokeh:
    """Soft, warm out-of-focus lights drifting slowly upwards."""
    def __init__(s,n=26,seed=21):
        r=random.Random(seed); s.b=[(r.uniform(0,W),r.uniform(0,PH),r.uniform(10,34),r.uniform(6,16),r.uniform(0,6.3),r.uniform(.6,1.4)) for _ in range(n)]
    def draw(s,lay,t):
        g=Image.new('RGBA',lay.size,(0,0,0,0)); d=ImageDraw.Draw(g)
        for x0,y0,rad,v,ph,tw in s.b:
            x=x0+math.sin(t*.5+ph)*10; y=(y0-t*v)%(PH+80)-40
            a=.45+.35*math.sin(t*tw+ph)
            d.ellipse([x-rad,y-rad,x+rad,y+rad],fill=(255,236,205,int(120*a)),outline=(255,248,235,int(150*a)),width=2)
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)))
def render(name,src,mode,effects,kicker,title,italic,brands=None,cta="DISCOVER THE EDIT · SOIE-ET-OR.COM",focus=.5,zoom=.08,secs=8,light=.14,out_dir='.',theme='white'):
    BG,TX,MU,GD=((14,14,14),(255,255,255),(190,184,176),(212,176,108)) if theme=='ink' else (PAPER,INK,MUTED,GOLD)
    base=make_base(src,mode,light)
    fr=os.path.join(out_dir,f'.fr_{name}'); shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
    FPS=30; n=int(secs*FPS)
    for i in range(n):
        t=i/FPS; z=1+zoom*t/secs
        bw=int(W*z*1.0); bh=int(base.height*bw/base.width)
        if bh<PH: bh=PH; bw=int(base.width*PH/base.height)
        im=base.resize((bw,bh),Image.LANCZOS); ox=(bw-W)//2; oy=int((bh-PH)*focus)
        top=im.crop((ox,oy,ox+W,oy+PH)).convert('RGBA')
        for e in effects: e.draw(top,t)
        frame=Image.new('RGB',(W,H),BG); frame.paste(top.convert('RGB'),(0,0))
        d=ImageDraw.Draw(frame); d.line([0,PH,W,PH],fill=GD,width=2)
        tracked(d,W/2,PH-58,"SOIE ET OR",TEN,9,(255,255,255))
        a1=min(1,t/0.6); a2=max(0,min(1,(t-secs*.45)/0.6))
        L=Image.new('RGBA',(W,H-PH),(0,0,0,0)); ld=ImageDraw.Draw(L)
        tracked(ld,W/2,44,kicker.upper(),JOST,7,TX+(int(255*a1),))
        ctext(ld,86,title,BOD,TX+(int(255*a1),)); ctext(ld,166,italic,BODI,TX+(int(255*a1),))
        ld.line([W/2-45,268,W/2+45,268],fill=GD+(int(255*a1),),width=2)
        if brands: ctext(ld,284,brands,BODI_S,MU+(int(255*a2),))
        tracked(ld,W/2,352 if brands else 296,cta,JOST_S,5,TX+(int(255*a2),))
        frame.paste(L,(0,PH),L)
        frame.save(f'{fr}/f{i:04d}.png')
        if i==n-1: frame.save(os.path.join(out_dir,f'{name}.png'))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{fr}/f%04d.png','-c:v','libx264','-pix_fmt','yuv420p','-crf','21','-movflags','+faststart',os.path.join(out_dir,f'{name}.mp4')],check=True)
    shutil.rmtree(fr)


EFFECTS={'sheen':lambda: Sheen(),'bokeh':lambda: Bokeh(),'snow':lambda: Snow(200,4),'sparkle':lambda: Sparkle(24,3),'leaves':lambda: Leaves(34,6),
         'lights':lambda: Lights(18),'diamonds':lambda: Diamonds(46,12),'sun':lambda: Sun(790,230,70)}

def main(spec):
    out_dir=os.path.dirname(os.path.abspath(spec))
    for p in json.load(open(spec,encoding='utf-8')):
        render(p['file'],os.path.join(ROOT,p['photo']),p.get('mode','colour'),[EFFECTS[e]() for e in p.get('effects',[])],
               p['kicker'],p['title'],p['italic'],p.get('brands'),p.get('cta',"DISCOVER THE EDIT · SOIE-ET-OR.COM"),
               focus=float(p.get('focus',.5)),out_dir=out_dir,theme=p.get('theme','white'))
        print('made',p['file'])

if __name__=='__main__':
    main(sys.argv[1])
