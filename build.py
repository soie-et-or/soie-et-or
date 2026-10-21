"""Builds the static site for soie-et-or.com into ./site. Run: python3 build.py"""
import os, re, shutil
from content import SITE, ARTICLES, ABOUT, CONTACT, DISCLOSURE, PRIVACY, TERMS, DISCLOSURE_SHORT

OUT = os.path.join(os.path.dirname(__file__), "site")
FMT = dict(SITE)

# Which nav section each article category belongs to
GROUPS = {
    "clothing": {"label": "Clothing", "title": "Clothing", "dek": "Parisian ready-to-wear and wardrobes built to last.",
                 "cats": ["Wardrobe", "Brands", "Style notes"]},
    "jewelry": {"label": "Jewelry", "title": "Jewelry", "dek": "Fine jewelry to wear every day.", "cats": ["Jewelry"]},
    "watches": {"label": "Watches", "title": "Watches", "dek": "Watches, new and pre-owned, and how to buy them well.", "cats": ["Watches"]},
}
def group_of(a):
    for k, g in GROUPS.items():
        if a["category"] in g["cats"]:
            return k
    return "clothing"

CSS = r"""
/* Soie et Or — white, ink, one gold line. Layout: centred logo between two nav groups; split hero; four-up edit row; one reading column for articles. */
:root{
  --white:#ffffff; --ink:#0e0e0e; --body-ink:#2b2826; --muted:#6b6660; --line:#e6e3df; --silk:#f4f3f1; --gold:#a88a4e;
  --logo:"Tenor Sans", "Jost", system-ui, sans-serif;
  --display:"Bodoni Moda", Didot, "Bodoni 72", Georgia, serif;
  --body:"Jost", "Futura", "Avenir Next", system-ui, sans-serif;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--white);color:var(--body-ink);font:400 17px/1.7 var(--body)}
a{color:var(--ink);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--muted)}
a:focus-visible{outline:2px solid var(--gold);outline-offset:3px}
img{max-width:100%;display:block}
.wrap{max-width:1280px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
.narrow{max-width:700px}
.label,.kicker{font:500 11px/1.3 var(--body);letter-spacing:.24em;text-transform:uppercase;color:var(--muted)}

/* header */
.top{border-bottom:1px solid var(--line);background:var(--white)}
.top .wrap{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:20px;padding-block:22px}
.logo{font:400 24px/1 var(--logo);letter-spacing:.3em;color:var(--ink);text-decoration:none;white-space:nowrap;padding-left:.3em}
.logo:hover{color:var(--ink)}
.nav{display:flex;gap:28px;flex-wrap:wrap}
.nav.right{justify-content:flex-end}
.nav a{font:500 11px/1 var(--body);letter-spacing:.22em;text-transform:uppercase;text-decoration:none;color:var(--ink);padding-block:6px}
.nav a[aria-current]{border-bottom:1px solid var(--gold)}
@media (max-width:820px){
  .top .wrap{grid-template-columns:1fr;justify-items:center;gap:14px}
  .top .logo{order:-1;font-size:20px}
  .nav,.nav.right{justify-content:center;gap:20px}
}

/* tiles stand in for photography until product images arrive from the affiliate feeds */
.tile{background:var(--silk);display:flex;align-items:flex-end;justify-content:space-between;padding:24px;position:relative;overflow:hidden}
.tile .word{font:italic 400 clamp(40px,6vw,88px)/1 var(--display);color:var(--ink);opacity:.92}
.tile .rule{position:absolute;left:24px;top:24px;width:56px;height:1px;background:var(--gold)}

/* hero */
.hero{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-bottom:1px solid var(--line)}
.hero .tile{min-height:520px;border-right:1px solid var(--line)}
.hero .copy{display:flex;flex-direction:column;justify-content:center;gap:22px;padding:56px clamp(24px,5vw,72px);min-width:0}
.hero h1{font:400 clamp(38px,4.6vw,62px)/1.04 var(--display);color:var(--ink);margin:0;text-wrap:balance}
.hero p{margin:0;font-size:17px;color:var(--muted);max-width:44ch}
.btn{align-self:flex-start;display:inline-block;border:1px solid var(--ink);padding:15px 30px;font:500 11px/1 var(--body);letter-spacing:.24em;text-transform:uppercase;text-decoration:none;color:var(--ink)}
.btn:hover{background:var(--ink);color:var(--white)}
@media (max-width:820px){.hero{grid-template-columns:1fr}.hero .tile{min-height:300px;border-right:0;border-bottom:1px solid var(--line)}}

/* edit row + grids */
.row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:1px solid var(--line)}
.row .card{border-right:1px solid var(--line);padding:22px 24px 28px}
.row .card:last-child{border-right:0}
@media (max-width:980px){.row{grid-template-columns:repeat(2,minmax(0,1fr))}.row .card:nth-child(2n){border-right:0}.row .card{border-bottom:1px solid var(--line)}}
@media (max-width:520px){.row{grid-template-columns:1fr}.row .card{border-right:0}}
.card{display:flex;flex-direction:column;gap:14px;text-decoration:none;color:var(--ink);min-width:0}
.card .tile{aspect-ratio:4/5;max-width:100%;padding:18px}
.card .tile .word{font-size:clamp(30px,3vw,42px)}
.card .tile .rule{left:18px;top:18px;width:40px}
.card h3{font:400 22px/1.25 var(--display);margin:0;text-wrap:balance}
.card p{margin:0;color:var(--muted);font-size:15px;line-height:1.6}
.card:hover h3{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:4px}
.sec{padding-block:56px}
.sec-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.sec-head h2{font:400 32px/1.15 var(--display);color:var(--ink);margin:0}
.sec-head a{font:500 11px/1 var(--body);letter-spacing:.22em;text-transform:uppercase}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:44px 28px}

/* pillars */
.pillars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.pillar{padding:36px clamp(20px,3vw,40px);border-right:1px solid var(--line);display:flex;flex-direction:column;gap:10px;text-decoration:none}
.pillar:last-child{border-right:0}
.pillar h3{font:400 28px/1.15 var(--display);color:var(--ink);margin:0}
.pillar p{margin:0;color:var(--muted);font-size:15.5px}
@media (max-width:820px){.pillars{grid-template-columns:1fr}.pillar{border-right:0;border-bottom:1px solid var(--line)}.pillar:last-child{border-bottom:0}}

/* article + pages */
.art-head{padding-block:64px 36px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:18px}
.art-head h1{font:400 clamp(36px,5.2vw,60px)/1.06 var(--display);color:var(--ink);margin:0;text-wrap:balance;max-width:20ch}
.dek{font-size:19px;color:var(--muted);margin:0;max-width:46ch}
.meta{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0}
.crumb{text-decoration:none}
.gold-rule{width:56px;height:1px;background:var(--gold);border:0;margin:0}
.hero-tile{aspect-ratio:16/7;max-width:100%;margin-bottom:44px}
.tile.photo{padding:0}
.tile.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero .tile.photo{min-height:640px}
@media (max-width:820px){.hero .tile.photo{min-height:420px}.hero-tile.photo{aspect-ratio:4/3}}
.disclose{font-size:14px;line-height:1.55;color:var(--muted);border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 0;margin:0 0 34px}
.prose{color:var(--body-ink)}
.prose h2{font:400 30px/1.2 var(--display);color:var(--ink);margin:46px 0 12px;text-wrap:balance}
.prose p{margin:0 0 18px}
.prose ul,.prose ol{margin:0 0 20px;padding-left:22px}
.prose li{margin-bottom:10px}
.prose ol.numbered li::marker{font-family:var(--display);color:var(--gold)}
.prose strong{font-weight:500;color:var(--ink)}
.page-body{padding-bottom:80px}

/* footer */
footer{background:var(--ink);color:#cfcac4}
footer .wrap{padding-block:48px;display:grid;gap:24px}
.foot-row{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap}
footer .logo{color:#ffffff;font-size:20px}
footer .nav a{color:#ffffff}
footer .nav a:hover{color:#cfcac4}
.foot-note{font-size:13px;color:#a8a29b;max-width:76ch;margin:0}
footer .gold-rule{width:40px}
@media (prefers-reduced-motion: reduce){*{transition:none!important}}
"""

def rel(depth): return "../" * depth

def fix_links(html, depth):
    return re.sub(r'href="/(?!/)', f'href="{rel(depth)}', html)

def shell(title, desc, body, depth, current="", canonical=""):
    p = rel(depth)
    verify = (f'<meta name="p:domain_verify" content="{SITE["pinterest_verify"]}">' if SITE["pinterest_verify"]
              else '<!-- Pinterest: set pinterest_verify in content.py to add the p:domain_verify tag -->')
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ""
        return f'<a href="{p}{href}"{cur}>{label}</a>'
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE['url']}/{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:site_name" content="{SITE['name']}">
{verify}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&family=Jost:wght@400;500&family=Tenor+Sans&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
<header class="top"><div class="wrap">
<nav class="nav" aria-label="Sections">{a('clothing.html','Clothing','clothing')}{a('jewelry.html','Jewelry','jewelry')}{a('watches.html','Watches','watches')}</nav>
<a class="logo" href="{p}index.html" aria-label="Soie et Or, home">SOIE ET OR</a>
<nav class="nav right" aria-label="More">{a('journal/index.html','Journal','journal')}{a('about.html','About','about')}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="foot-row"><a class="logo" href="{p}index.html">SOIE ET OR</a>
<nav class="nav" aria-label="Footer"><a href="{p}affiliate-disclosure.html">Affiliate disclosure</a><a href="{p}privacy.html">Privacy</a><a href="{p}terms.html">Terms</a><a href="{p}contact.html">Contact</a><a href="{SITE['pinterest']}" rel="noopener">Pinterest</a></nav></div>
<hr class="gold-rule">
<p class="foot-note">Soie et Or is an independent editorial site. Some links are affiliate links: we may earn a commission when you buy, at no extra cost to you. Brand names belong to their owners; we are not affiliated with or endorsed by the brands we write about.</p>
<p class="foot-note">&copy; 2026 Soie et Or &middot; {SITE['domain']}</p>
</div></footer>
</body>
</html>
"""
    return fix_links(html, depth)

def tile(word, cls="", img=None, depth=0):
    """A photo when one is set ({file, alt, pos}), otherwise the silk tile with an italic word."""
    if img:
        pos = img.get("pos", "center")
        return (f'<div class="tile photo {cls}"><img src="{rel(depth)}assets/img/{img["file"]}" alt="{img["alt"]}" '
                f'loading="lazy" style="object-position:{pos}"></div>')
    return f'<div class="tile {cls}" aria-hidden="true"><span class="rule"></span><span class="word">{word}</span></div>'

def card(a, depth):
    p = rel(depth)
    return f"""<a class="card" href="{p}journal/{a['slug']}.html">
{tile(a['category'], img=a.get('image'), depth=depth)}
<span class="label">{a['category']} &middot; {a['read']}</span>
<h3>{a['title']}</h3><p>{a['dek']}</p></a>"""

def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def head_block(kicker, title, dek="", meta="", kicker_href=""):
    k = f'<a class="label crumb" href="{kicker_href}">{kicker}</a>' if kicker_href else f'<span class="label">{kicker}</span>'
    d = f'<p class="dek">{dek}</p>' if dek else ""
    m = f'<p class="meta">{meta}</p>' if meta else ""
    return f'<div class="wrap art-head">{k}<h1>{title}</h1><hr class="gold-rule">{d}{m}</div>'

def simple_page(fname, title, kicker, body, key=""):
    b = head_block(kicker, title) + f'<div class="wrap narrow page-body prose">{body.format(**FMT)}</div>'
    write(fname, shell(f"{title} · {SITE['name']}", f"{title}. {SITE['name']}: {SITE['tagline']}", b, 0, key, fname))

def build():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    with open(os.path.join(OUT, "assets", "style.css"), "w") as f: f.write(CSS)
    imgsrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    if os.path.isdir(imgsrc):
        shutil.copytree(imgsrc, os.path.join(OUT, "assets", "img"))

    lead, rest = ARTICLES[0], ARTICLES[1:]
    row = "\n".join(card(a, 0) for a in rest[:4])
    home = f"""<section class="hero">
{tile('Soie', img=SITE.get('hero_image'))}
<div class="copy">
<span class="kicker">The edit &middot; {lead['category']}</span>
<h1>{lead['title']}</h1>
<p>{lead['dek']}</p>
<a class="btn" href="journal/{lead['slug']}.html">Read the edit</a>
</div>
</section>
<section class="row" aria-label="Latest articles">{row}</section>
<section class="wrap sec">
<div class="sec-head"><h2>Quiet Parisian style, in silk and gold</h2><a href="journal/index.html">All articles</a></div><p class="dek" style="margin:0">An edit of Parisian ready-to-wear, fine jewelry and watches worth keeping.</p>
</section>
<section class="pillars wrap" style="padding-left:0;padding-right:0">
<a class="pillar" href="clothing.html"><span class="label">Soie</span><h3>Clothing</h3><p>Parisian ready-to-wear from Sandro, IRO, Acne Studios, Marni and Miu Miu. Capsule wardrobes built to last.</p></a>
<a class="pillar" href="jewelry.html"><span class="label">Or</span><h3>Jewelry</h3><p>Fine jewelry to wear every day, from houses like Pomellato and Chopard.</p></a>
<a class="pillar" href="watches.html"><span class="label">Temps</span><h3>Watches</h3><p>Watches, new and pre-owned, with honest guidance on buying well.</p></a>
</section>
"""
    write("index.html", shell(f"{SITE['name']} · Quiet Parisian style, in silk and gold",
        "An edit of quiet Parisian luxury: ready-to-wear, fine jewelry and watches worth keeping.", home, 0, "", ""))

    for key, g in GROUPS.items():
        items = [a for a in ARTICLES if group_of(a) == key]
        cards = "\n".join(card(a, 0) for a in items)
        b = head_block("Section", g["title"], g["dek"]) + f'<section class="wrap sec" style="padding-top:0"><div class="grid">{cards}</div></section>'
        write(f"{key}.html", shell(f"{g['title']} · {SITE['name']}", g["dek"], b, 0, key, f"{key}.html"))

    jcards = "\n".join(card(a, 1) for a in ARTICLES)
    jbody = head_block("Journal", "The journal", "Wardrobe notes, jewelry guides and honest advice on buying luxury well.") + \
            f'<section class="wrap sec" style="padding-top:0"><div class="grid">{jcards}</div></section>'
    write("journal/index.html", shell(f"Journal · {SITE['name']}", "Wardrobe notes, jewelry guides and advice on buying luxury well.", jbody, 1, "journal", "journal/"))

    for a in ARTICLES:
        g = group_of(a)
        others = [o for o in ARTICLES if o["slug"] != a["slug"]][:3]
        more = "\n".join(card(o, 1) for o in others)
        body = f"""<article>
{head_block(a['category'], a['title'], a['dek'], f"{a['date']} &middot; {a['read']} read", f"/{g}.html")}
<div class="wrap">{tile(a['category'], 'hero-tile', img=a.get('image'), depth=1)}</div>
<div class="wrap narrow page-body prose">
<p class="disclose">{DISCLOSURE_SHORT}</p>
{a['body']}
</div></article>
<section class="wrap sec" style="border-top:1px solid var(--line)"><div class="sec-head"><h2>Keep reading</h2><a href="/journal/index.html">All articles</a></div><div class="grid">{more}</div></section>"""
        write(f"journal/{a['slug']}.html", shell(f"{a['title']} · {SITE['name']}", a["dek"], body, 1, g, f"journal/{a['slug']}.html"))

    simple_page("about.html", "About Soie et Or", "About", ABOUT, "about")
    simple_page("contact.html", "Contact", "Contact", CONTACT)
    simple_page("affiliate-disclosure.html", "Affiliate disclosure", "Transparency", DISCLOSURE)
    simple_page("privacy.html", "Privacy policy", "Legal", PRIVACY)
    simple_page("terms.html", "Terms of use", "Legal", TERMS)

    nf = head_block("404", "This page has slipped away", 'The link may be old or mistyped. <a href="/index.html">Back to the home page</a>.')
    write("404.html", shell(f"Page not found · {SITE['name']}", "Page not found", nf, 0, "", "404.html"))

    urls = ["", "clothing.html", "jewelry.html", "watches.html", "journal/", "about.html", "contact.html",
            "affiliate-disclosure.html", "privacy.html", "terms.html"] + [f"journal/{a['slug']}.html" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc></url>" for u in urls) + "\n</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    build()
