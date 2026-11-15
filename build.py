"""Builds the static site for soie-et-or.com into ./site. Run: python3 build.py"""
import html as html_lib, json, os, re, shutil
from content import SITE, ARTICLES, ABOUT, CONTACT, DISCLOSURE, PRIVACY, TERMS, DISCLOSURE_SHORT, AFFILIATE_DOMAINS

OUT = os.path.join(os.path.dirname(__file__), "site")
FMT = dict(SITE)

# Which nav section each article category belongs to
GROUPS = {
    "clothing": {"label": "Clothing", "title": "Clothing", "dek": "Parisian ready-to-wear and wardrobes built to last.",
                 "cats": ["Wardrobe", "Brands", "Style notes"]},
    "jewelry": {"label": "Jewelry", "title": "Jewelry", "dek": "Fine jewelry to wear every day.", "cats": ["Jewelry"]},
    "watches": {"label": "Watches", "title": "Watches", "dek": "Watches, new and pre-owned, and how to buy them well.", "cats": ["Watches"]},
    "lingerie": {"label": "Lingerie", "title": "Lingerie", "dek": "French lingerie: silk, fine lace and the right fit.", "cats": ["Lingerie"]},
    "boots": {"label": "Boots", "title": "Boots", "dek": "The boots a Parisian wardrobe needs, and how to make them last.", "cats": ["Boots"]},
    "travel": {"label": "Travel", "title": "Chic travel", "dek": "Bags, outfits, sunglasses and caps for travelling light and well.", "cats": ["Travel"]},
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
.nav-item{position:relative}
.dropdown{position:absolute;top:100%;left:-18px;z-index:20;min-width:280px;max-width:340px;background:var(--white);border:1px solid var(--line);box-shadow:0 12px 32px rgba(14,14,14,.08);padding:14px 18px 16px;opacity:0;visibility:hidden;transform:translateY(4px);transition:opacity .2s ease,transform .2s ease,visibility .2s}
.nav.right .dropdown{left:auto;right:-18px}
.nav-item:hover .dropdown,.nav-item:focus-within .dropdown{opacity:1;visibility:visible;transform:none}
.dropdown ul{list-style:none;margin:0;padding:0}
.dropdown li{border-bottom:1px solid var(--line)}
.dropdown li:last-child{border-bottom:0}
.nav .dropdown a{display:block;font:400 16px/1.3 var(--display);letter-spacing:0;text-transform:none;padding:11px 0;color:var(--ink);border:0}
.nav .dropdown a:hover{text-decoration:underline;text-underline-offset:3px}
.nav .dropdown a.dropdown-all{font:500 11px/1 var(--body);letter-spacing:.22em;text-transform:uppercase;padding:14px 0 2px;color:var(--muted)}
@media (prefers-reduced-motion:reduce){.dropdown{transition:none}}
@media (max-width:820px){
  .top .wrap{grid-template-columns:1fr;justify-items:center;gap:14px}
  .top .logo{order:-1;font-size:20px}
  .nav,.nav.right{justify-content:center;gap:20px}
  .dropdown{display:none}
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
.pillar:nth-child(3n){border-right:0}
.pillar:nth-child(-n+3){border-bottom:1px solid var(--line)}
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
.disclose{font-size:12.5px;line-height:1.5;color:var(--muted);text-align:center;margin:-18px auto 28px;max-width:60ch}
.disclose a{color:var(--muted)}
.shop{padding-block:8px 64px}
.shop-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:28px;margin-bottom:24px}
.shop-head h2{font:400 28px/1.2 var(--display);color:var(--ink);margin:0}
.products{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:32px 24px}
.product{display:flex;flex-direction:column;gap:6px;text-decoration:none;color:var(--ink);min-width:0}
.product-img{aspect-ratio:4/5;max-width:100%;background:var(--silk);position:relative;overflow:hidden;margin-bottom:8px;display:flex;align-items:flex-end;padding:14px}
.product-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.product-img .word{font:italic 400 28px/1 var(--display);color:var(--ink)}
.product-name{font:400 18px/1.3 var(--display)}
.product-shop{font-size:13px;color:var(--muted)}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
.edit-strip{display:flex;flex-direction:column;gap:12px;padding-block:6px 26px}
.strip-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.home-strip{padding-bottom:64px}
.home-strip .strip-row{grid-template-columns:repeat(3,minmax(0,240px))}
.strip-tile{display:flex;flex-direction:column;gap:8px;min-width:0}
.strip-title{text-decoration:none;color:var(--ink);font:400 16px/1.25 var(--display);padding-block:4px}
.strip-title:hover{text-decoration:underline;text-underline-offset:3px}
.collage{display:grid;aspect-ratio:1/1;gap:2px;background:var(--line);border:1px solid var(--line)}
.collage a{display:block;background:#fff;position:relative;overflow:hidden;min-height:0}
.collage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:6%;box-sizing:border-box;transition:transform .4s ease}
.collage a:hover img{transform:scale(1.05)}
.collage.c3{grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr}
.collage.c3 a:first-child{grid-row:1/3}
.collage.c2{grid-template-columns:1fr 1fr}
@media (prefers-reduced-motion:reduce){.collage img{transition:none}.collage a:hover img{transform:none}}
.board{background:var(--silk);margin-block:40px;scroll-margin-top:24px}
.board-in{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);grid-template-areas:"text rail" "story rail";grid-template-rows:auto 1fr;column-gap:48px;row-gap:18px;padding-block:44px;align-items:start}
.board-text{grid-area:text;display:flex;flex-direction:column;gap:8px}
.board-text .label{font-size:11px}
.board-text h2{font:400 32px/1.15 var(--display);margin:0;color:var(--ink)}
.board-more{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);text-underline-offset:4px;margin-top:6px;padding-block:8px}
.board-intro{margin:0;color:var(--body-ink);font-size:16px;line-height:1.6}
.board-story{grid-area:story;margin:0;color:var(--muted);font:italic 400 16px/1.6 var(--display)}
.board-rail{grid-area:rail;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:28px 20px}
.piece{display:flex;flex-direction:column;gap:5px;min-width:0}
@media (min-width:761px){
.board-rail.n3{grid-template-columns:repeat(3,minmax(0,1fr))}
.board-rail.n4{grid-template-columns:repeat(4,minmax(0,1fr))}
.board-rail.n5{grid-template-columns:repeat(6,minmax(0,1fr))}
.board-rail.n5 .piece{grid-column:span 2}
.board-rail.n5 .piece:nth-child(4){grid-column:2/4}
.board-rail.n5 .piece:nth-child(5){grid-column:4/6}
}
.piece-img{display:block;aspect-ratio:1/1;background:#fff;position:relative;overflow:hidden;margin-bottom:8px}
.piece-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:10px;box-sizing:border-box;transition:transform .4s ease}
.piece:hover .piece-img img{transform:scale(1.03)}
@media (prefers-reduced-motion:reduce){.piece-img img{transition:none}.piece:hover .piece-img img{transform:none}}
.piece-img .word{position:absolute;left:12px;bottom:10px;font:italic 400 20px/1 var(--display);color:var(--ink)}
.piece .label{font-size:11px}
.piece-name{font:400 17px/1.3 var(--display);color:var(--ink);text-decoration:none}
.piece-name:hover{text-decoration:underline;text-underline-offset:3px}
.piece-shop{font-size:13px;color:var(--muted)}
.piece-regions{font-size:12px;letter-spacing:.08em;color:var(--muted)}
.piece-regions a{color:var(--ink);text-decoration:underline;text-underline-offset:3px;text-decoration-color:#bdb7b0;display:inline-block;padding:10px 2px}
.piece-regions a:hover{text-decoration-color:var(--ink)}
@media (max-width:760px){
.board{margin-block:32px}
.board-in{grid-template-columns:1fr;grid-template-rows:auto;grid-template-areas:"text" "rail" "story";padding-block:32px;row-gap:20px}
.board-text h2{font-size:28px}
.board-rail{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;margin-inline:calc(-1 * max(20px,env(safe-area-inset-left,0px)));padding-inline:max(20px,env(safe-area-inset-left,0px));scroll-padding-inline:max(20px,env(safe-area-inset-left,0px));-webkit-overflow-scrolling:touch;scrollbar-width:none}
.board-rail::-webkit-scrollbar{display:none}
.piece{flex:0 0 68%;scroll-snap-align:start}
.strip-row{gap:10px}
.strip-title{font-size:14px}
}
.product:hover .product-name{text-decoration:underline;text-underline-offset:3px}
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

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def iso_date(d):
    day, month, year = d.split()
    return f"{year}-{MONTHS.index(month) + 1:02d}-{int(day):02d}"

def social_meta(title, desc, canonical, image=None, article=None):
    """Open Graph / Twitter tags (link previews in WhatsApp, iMessage, Facebook) and JSON-LD for Google."""
    url = f"{SITE['url']}/{canonical}"
    img_file = (image or {}).get("file") or "og-default.jpg"
    img_url = f"{SITE['url']}/assets/img/{img_file}"
    alt = html_lib.escape((image or {}).get("alt") or f"{SITE['name']}: {SITE['tagline']}", quote=True)
    tags = [
        f'<meta property="og:type" content="{"article" if article else "website"}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{img_url}">',
        f'<meta property="og:image:alt" content="{alt}">',
        '<meta property="og:locale" content="en_GB">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    if article:
        ld = {"@context": "https://schema.org", "@type": "Article",
              "headline": article["title"], "description": article["dek"],
              "image": [img_url], "datePublished": iso_date(article["date"]),
              "author": {"@type": "Person", "name": "Philippine", "url": f"{SITE['url']}/about.html"},
              "publisher": {"@type": "Organization", "name": SITE["name"], "url": SITE["url"]},
              "mainEntityOfPage": url, "articleSection": article["category"]}
        tags.append(f'<meta property="article:published_time" content="{iso_date(article["date"])}">')
    elif canonical == "":
        ld = {"@context": "https://schema.org", "@type": "WebSite", "name": SITE["name"],
              "url": SITE["url"] + "/", "description": SITE["tagline"]}
    else:
        ld = None
    if ld:
        tags.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    return "\n".join(tags)

def shell(title, desc, body, depth, current="", canonical="", image=None, article=None):
    p = rel(depth)
    verify = (f'<meta name="p:domain_verify" content="{SITE["pinterest_verify"]}">' if SITE["pinterest_verify"]
              else '<!-- Pinterest: set pinterest_verify in content.py to add the p:domain_verify tag -->')
    def a(href, label, key):
        """Section link with a dropdown of its articles (desktop: on hover or keyboard focus; hidden on phones)."""
        cur = ' aria-current="page"' if key == current else ""
        arts = [x for x in ARTICLES if group_of(x) == key]
        if not arts:
            return f'<a href="{p}{href}"{cur}>{label}</a>'
        links = "".join(f'<li><a href="{p}journal/{x["slug"]}.html">{x["title"]}</a></li>' for x in arts)
        return (f'<div class="nav-item"><a href="{p}{href}"{cur}>{label}</a>'
                f'<div class="dropdown"><ul>{links}</ul><a class="dropdown-all" href="{p}{href}">All {label.lower()}</a></div></div>')
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
{social_meta(title, desc, canonical, image, article)}
{verify}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&family=Jost:wght@400;500&family=Tenor+Sans&display=swap">
<link rel="stylesheet" href="{p}assets/style.css">
</head>
<body>
<header class="top"><div class="wrap">
<nav class="nav" aria-label="Sections">{a('clothing.html','Clothing','clothing')}{a('lingerie.html','Lingerie','lingerie')}{a('boots.html','Boots','boots')}</nav>
<a class="logo" href="{p}index.html" aria-label="Soie et Or, home">SOIE ET OR</a>
<nav class="nav right" aria-label="More sections">{a('jewelry.html','Jewelry','jewelry')}{a('watches.html','Watches','watches')}{a('travel.html','Travel','travel')}</nav>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="foot-row"><a class="logo" href="{p}index.html">SOIE ET OR</a>
<nav class="nav" aria-label="Footer"><a href="{p}the-edit.html">The Edit</a><a href="{p}journal/index.html">Journal</a><a href="{p}about.html">About</a><a href="{p}affiliate-disclosure.html">Affiliate disclosure</a><a href="{p}privacy.html">Privacy</a><a href="{p}terms.html">Terms</a><a href="{p}contact.html">Contact</a><a href="{SITE['pinterest']}" rel="noopener">Pinterest</a></nav></div>
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

def card_img(a):
    """Cards use the optional 'card' crop of an article's image when there is one."""
    img = a.get("image")
    if img and img.get("card"):
        return {**img, "file": img["card"], "pos": img.get("card_pos", "center")}
    return img

def is_affiliate(url):
    host = re.sub(r"^https?://", "", url).split("/")[0].lower()
    return any(d in host for d in AFFILIATE_DOMAINS)

def mark_affiliate_links(html):
    """Give every affiliate link rel="sponsored noopener" and open it in a new tab."""
    def fix(m):
        tag, url = m.group(0), m.group(1)
        if not is_affiliate(url) or "rel=" in tag:
            return tag
        return tag[:-1] + ' rel="sponsored noopener" target="_blank">'
    return re.sub(r'<a\s[^>]*href="([^"]+)"[^>]*>', fix, html)

def shop_block(products):
    if not products:
        return ""
    items = []
    for pr in products:
        img = (f'<img src="{pr["image"]}" alt="{pr["brand"]} {pr["name"]}" loading="lazy">' if pr.get("image")
               else '<span class="word">Shop</span>')
        price = f' &middot; {pr["price"]}' if pr.get("price") else ""
        items.append(f'''<a class="product" href="{pr["url"]}">
<div class="product-img">{img}</div>
<span class="label">{pr["brand"]}</span>
<span class="product-name">{pr["name"]}</span>
<span class="product-shop">at {pr["shop"]}{price}</span></a>''')
    return f'''<section class="shop wrap" aria-label="Shop the edit">
<div class="shop-head"><h2>Shop the edit</h2><span class="label">Affiliate links &middot; we may earn a small commission</span></div>
<div class="products">{"".join(items)}</div></section>'''

TYPE_WORD = {"necklace": "Collier", "ring": "Bague", "bracelet": "Bracelet"}

AFF_ATTRS = 'rel="sponsored nofollow noopener" target="_blank"'
DEFAULT_REGION = "eu"   # where a click on the photo or name goes: "eu" (EU/UK programme) or "us"

def edit_id(e):
    return "edit-" + re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-")

def edit_board(e, story_href=""):
    """One themed board, full width between the article's paragraphs: text on the left,
    the pieces on the right (desktop) or as a swipeable row (phone). No prices (they change);
    product images come unaltered from the retailer's catalogue."""
    cards = []
    for pr in e["products"]:
        alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
        img = (f'<img src="{pr["image"]}" alt="{alt}" loading="lazy">' if pr.get("image")
               else f'<span class="word">{TYPE_WORD.get(pr.get("type", ""), "Shop")}</span>')
        urls = {"eu": pr.get("url_eu"), "us": pr.get("url_us")}
        main = urls.get(DEFAULT_REGION) or urls["eu"] or urls["us"] or "#"
        regions = []
        if urls["eu"]: regions.append(f'<a href="{urls["eu"]}" {AFF_ATTRS} aria-label="Discover {alt} in Europe and the UK">EU / UK</a>')
        if urls["us"]: regions.append(f'<a href="{urls["us"]}" {AFF_ATTRS} aria-label="Discover {alt} in the US">US</a>')
        cards.append(f'''<div class="piece" role="listitem">
<a class="piece-img" href="{main}" {AFF_ATTRS} tabindex="-1" aria-hidden="true">{img}</a>
<span class="label">{pr["type"].capitalize()} &middot; {pr["brand"]}</span>
<a class="piece-name" href="{main}" {AFF_ATTRS}>{pr["name"]}</a>
<span class="piece-shop">at {pr.get("shop", "Mytheresa")}</span>
<span class="piece-regions">Discover &mdash; {" &middot; ".join(regions)}</span>
</div>''')
    story = f'<p class="board-story">{e["story"]}</p>' if e.get("story") else ""
    n = len(e["products"])
    return f'''<section class="board" id="{edit_id(e)}" aria-label="{html_lib.escape(e["title"], quote=True)}">
<div class="wrap board-in">
<div class="board-text"><span class="label">The Edit &middot; affiliate links</span><h2>{e["title"]}</h2><p class="board-intro">{e.get("intro", "")}</p>{f'<a class="board-more" href="{story_href}">Read the story &rarr;</a>' if story_href else ""}</div>
<div class="board-rail n{n}" role="list" aria-label="{n} pieces">{"".join(cards)}</div>
{story}
</div></section>'''

def edit_strip(edits, heading="The Edit in this story", base="", narrow=True):
    """Near the top: one tile per edit. Each tile is a small collage of the edit's own product photos,
    laid out side by side in HTML (the images themselves are not altered or merged). Each photo links
    to that piece at the retailer; the title jumps to the board."""
    if not edits:
        return ""
    items = []
    for e in edits:
        shots = [pr for pr in e["products"] if pr.get("image")][:3]
        cells = []
        for pr in shots:
            url = pr.get(f"url_{DEFAULT_REGION}") or pr.get("url_eu") or pr.get("url_us")
            alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
            cells.append(f'<a href="{url}" {AFF_ATTRS} title="{alt}"><img src="{pr["image"]}" alt="{alt}" loading="lazy"></a>')
        items.append(f'''<div class="strip-tile"><div class="collage c{len(cells)}">{"".join(cells)}</div>
<a class="strip-title" href="{base}#{edit_id(e)}">{e["title"]} <span aria-hidden="true">&darr;</span></a></div>''')
    return f'''<nav class="wrap{" narrow" if narrow else ""} edit-strip" aria-label="{heading}">
<span class="label">{heading}</span><div class="strip-row">{"".join(items)}</div></nav>'''

def body_with_edits(body, edits):
    """Place each board right after the section whose <h2> matches its "after" (else at the end)."""
    if not edits:
        return f'<div class="wrap narrow page-body prose">\n{body}\n</div>'
    heads = [(m.start(), re.sub("<[^>]+>", "", m.group(1)).strip()) for m in re.finditer(r"<h2>(.*?)</h2>", body)]
    cuts = {}
    for e in edits:
        pos = len(body)
        for k, (start, text) in enumerate(heads):
            if text.lower() == e.get("after", "").lower():
                pos = heads[k + 1][0] if k + 1 < len(heads) else len(body)
        cuts.setdefault(pos, []).append(edit_board(e))
    out, last = [], 0
    for pos in sorted(cuts):
        chunk = body[last:pos].strip()
        if chunk:
            out.append(f'<div class="wrap narrow page-body prose">\n{chunk}\n</div>')
        out.extend(cuts[pos])
        last = pos
    tail = body[last:].strip()
    if tail:
        out.append(f'<div class="wrap narrow page-body prose">\n{tail}\n</div>')
    return "\n".join(out)

def card(a, depth):
    p = rel(depth)
    return f"""<a class="card" href="{p}journal/{a['slug']}.html">
{tile(a['category'], img=card_img(a), depth=depth)}
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
    all_edits = [(a, e) for a in ARTICLES for e in (a.get("edits") or [])]
    home_edit = ""
    if all_edits:
        home_edit = (f'''<section class="wrap sec home-edit" style="padding-bottom:0"><div class="sec-head"><h2>The Edit</h2><a href="the-edit.html">See the edit</a></div>
<p class="dek" style="margin:0 0 10px">Pieces we would choose ourselves, gathered by theme.</p><p class="disclose" style="text-align:left;margin:0 0 22px">{DISCLOSURE_SHORT}</p></section>'''
                     + edit_strip([e for _, e in all_edits], heading="Browse by theme", base="the-edit.html", narrow=False).replace('class="wrap edit-strip"', 'class="wrap edit-strip home-strip"'))
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
<a class="pillar" href="lingerie.html"><span class="label">Dessous</span><h3>Lingerie</h3><p>French lingerie in silk and fine lace: the first layer of a good outfit.</p></a>
<a class="pillar" href="boots.html"><span class="label">Bottes</span><h3>Boots</h3><p>Ankle, riding and heeled boots that see you through every winter.</p></a>
<a class="pillar" href="travel.html"><span class="label">Voyage</span><h3>Chic travel</h3><p>One good bag, a few pieces that all combine, sunglasses and a cap.</p></a>
</section>
{home_edit}
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
        shop = shop_block(a.get("products"))
        has_aff = bool(shop) or bool(a.get("edits")) or any(is_affiliate(u) for u in re.findall(r'href="([^"]+)"', a["body"]))
        notice = f'<div class="wrap narrow"><p class="disclose">{DISCLOSURE_SHORT}</p></div>' if has_aff else ""
        body = f"""<article>
{head_block(a['category'], a['title'], a['dek'], f"{a['date']} &middot; {a['read']} read", f"/{g}.html")}
{notice}
{edit_strip(a.get("edits"))}
<div class="wrap">{tile(a['category'], 'hero-tile', img=a.get('image'), depth=1)}</div>
{body_with_edits(a['body'], a.get("edits"))}
{shop}</article>
<section class="wrap sec" style="border-top:1px solid var(--line)"><div class="sec-head"><h2>Keep reading</h2><a href="/journal/index.html">All articles</a></div><div class="grid">{more}</div></section>"""
        body = mark_affiliate_links(body)
        write(f"journal/{a['slug']}.html", shell(f"{a['title']} · {SITE['name']}", a["dek"], body, 1, g, f"journal/{a['slug']}.html", image=a.get("image"), article=a))

    if all_edits:
        boards = "\n".join(edit_board(e, f"journal/{a['slug']}.html") for a, e in all_edits)
        eb = (head_block("The Edit", "The Edit", "Pieces we would choose ourselves. Each edit belongs to a story; read it there, or browse them all here.")
              + f'<div class="wrap narrow"><p class="disclose">{DISCLOSURE_SHORT}</p></div>'
              + edit_strip([e for _, e in all_edits], heading="The edits") + boards)
        write("the-edit.html", shell(f"The Edit · {SITE['name']}", "Fine jewelry and pieces worth keeping, gathered by theme by the editor of Soie et Or.", mark_affiliate_links(eb), 0, "", "the-edit.html"))

    simple_page("about.html", "About Soie et Or", "About", ABOUT, "about")
    simple_page("contact.html", "Contact", "Contact", CONTACT)
    simple_page("affiliate-disclosure.html", "Affiliate disclosure", "Transparency", DISCLOSURE)
    simple_page("privacy.html", "Privacy policy", "Legal", PRIVACY)
    simple_page("terms.html", "Terms of use", "Legal", TERMS)

    nf = head_block("404", "This page has slipped away", 'The link may be old or mistyped. <a href="/index.html">Back to the home page</a>.')
    write("404.html", shell(f"Page not found · {SITE['name']}", "Page not found", nf, 0, "", "404.html"))

    urls = ["", "clothing.html", "lingerie.html", "boots.html", "jewelry.html", "watches.html", "travel.html", "journal/", "about.html", "contact.html",
            "affiliate-disclosure.html", "privacy.html", "terms.html", "the-edit.html"] + [f"journal/{a['slug']}.html" for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc></url>" for u in urls) + "\n</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    build()
