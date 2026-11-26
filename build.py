"""Builds the static site for soie-et-or.com into ./site. Run: python3 build.py"""
import html as html_lib, json, os, re, shutil
from content import SITE, ARTICLES, ABOUT, CONTACT, DISCLOSURE, PRIVACY, TERMS, DISCLOSURE_SHORT, AFFILIATE_DOMAINS
# Boards without products yet (work in progress) are left out of the site
for _a in ARTICLES:
    if _a.get("edits"):
        _a["edits"] = [_e for _e in _a["edits"] if _e.get("products")]

OUT = os.path.join(os.path.dirname(__file__), "site")
FMT = dict(SITE)

# Which nav section each article category belongs to
GROUPS = {
    "clothing": {"label": "Clothing", "title": "Clothing", "dek": "Parisian ready-to-wear and wardrobes built to last.",
                 "seo_title": 'Parisian Capsule Wardrobe & Outfit Advice', "seo_desc": 'Parisian styling advice for clothing: capsule wardrobes, quiet luxury outfits and ready-to-wear pieces built to last.',
                 "cats": ["Wardrobe", "Brands", "Style notes"], "also": ["Travel"]},   # travel looks are outfits too, so they show here as well
    "jewelry": {"label": "Jewelry", "title": "Jewelry", "dek": "Fine jewelry to wear every day.", "seo_title": 'Fine Gold Jewelry Guides & Gift Ideas', "seo_desc": 'How to choose and wear fine gold jewelry the Parisian way: everyday pieces, gift ideas and buying well when gold is expensive.',
                 "cats": ["Jewelry"]},
    "watches": {"label": "Watches", "title": "Watches", "dek": "Watches, new and pre-owned, and how to buy them well.", "seo_title": "Small Women's Watches & Pre-Owned Watch Guides", "seo_desc": "Small, elegant women's watches and how to buy them well, new or pre-owned, with honest advice on what to check.",
                 "cats": ["Watches"]},
    "lingerie": {"label": "Lingerie", "title": "Lingerie", "dek": "French lingerie: silk, fine lace and the right fit.", "seo_title": 'French Lingerie: Silk & Lace, the Parisian Way', "seo_desc": 'French lingerie the Parisian way: silk camisoles, fine lace, slip dresses and what to wear under a blazer or a knit.',
                 "cats": ["Lingerie"]},
    "boots": {"label": "Boots", "title": "Boots", "dek": "The boots a Parisian wardrobe needs, and how to make them last.", "seo_title": "Women's Winter Boots: Ankle, Riding & Heeled", "seo_desc": 'The boots a Parisian winter wardrobe needs: flat ankle boots, riding boots and heeled boots, and how to wear each one.',
                 "cats": ["Boots"]},
    "travel": {"label": "Travel", "title": "Chic travel", "dek": "Bags, outfits, sunglasses and caps for travelling light and well.", "seo_title": 'Paris Travel Outfits & Chic Packing', "seo_desc": 'Chic travel outfits for a weekend in Paris: the carry-on, the bag and what to wear on the train or plane.',
                 "cats": ["Travel"]},
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
.only-mob{display:none}
@media (max-width:760px){.only-mob{display:block}.only-desk{display:none}}
.hero{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));border-bottom:1px solid var(--line)}
.hero .tile{min-height:520px;border-right:1px solid var(--line)}
.hero .copy{display:flex;flex-direction:column;justify-content:center;gap:22px;padding:56px clamp(24px,5vw,72px);min-width:0}
.hero h1{font:400 clamp(38px,4.6vw,62px)/1.04 var(--display);color:var(--ink);margin:0;text-wrap:balance}
.hero p{margin:0;font-size:17px;color:var(--muted);max-width:44ch}
.btn{align-self:flex-start;display:inline-block;border:1px solid var(--ink);padding:15px 30px;font:500 11px/1 var(--body);letter-spacing:.24em;text-transform:uppercase;text-decoration:none;color:var(--ink)}
.btn:hover{background:var(--ink);color:var(--white)}
.btns{display:inline-grid;grid-template-columns:1fr 1fr;gap:12px;align-self:flex-start}.btns .btn{text-align:center;align-self:stretch}@media (max-width:520px){.btns{grid-template-columns:1fr}}.btn-solid{background:var(--ink);color:var(--white)}.btn-solid:hover{background:transparent;color:var(--ink)}
@media (max-width:820px){.hero{grid-template-columns:1fr}.hero .tile{min-height:0;height:56vw;max-height:300px;border-right:0;border-bottom:1px solid var(--line)}.hero .copy{padding:26px 18px 30px;gap:16px}}

/* edit row + grids */
.row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-bottom:1px solid var(--line)}
.row .card{border-right:1px solid var(--line);padding:22px 24px 28px}
.row .card:last-child{border-right:0}
@media (max-width:980px){.row{grid-template-columns:repeat(2,minmax(0,1fr))}.row .card:nth-child(2n){border-right:0}.row .card{border-bottom:1px solid var(--line)}}
@media (max-width:520px){.row{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}.row .card{flex:0 0 62%;scroll-snap-align:start;border-right:1px solid var(--line);border-bottom:0;padding:16px 16px 20px}.row .card p{display:none}.row .card h3{font-size:17px}}
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
.theme-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}.theme-chips a{border:1px solid var(--line);padding:8px 14px;font:500 11px/1 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--ink);text-decoration:none}.theme-chips a:hover{border-color:var(--ink)}
.theme-chips label{border:1px solid var(--line);padding:8px 14px;font:500 11px/1 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--ink)}.theme-chips label:hover{border-color:var(--ink)}
.home-edit{padding-top:32px;padding-bottom:0}.home-strip .label{display:none}.strip-sub{display:block;margin-top:3px;font:500 10px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.promise{text-align:center;font:italic 400 clamp(17px,2.2vw,21px)/1.4 var(--display);color:var(--muted);margin:0;padding:14px 16px;border-bottom:1px solid var(--line)}
.rules-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:22px clamp(14px,1.6vw,24px) 12px}.rules-head a{font:500 11px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--ink)}
.rules{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));border-top:1px solid var(--line);border-bottom:1px solid var(--line);counter-reset:r}
.rules li{counter-increment:r;border-right:1px solid var(--line)}.rules li:last-child{border-right:0}
.rules a{display:flex;flex-direction:column;gap:6px;padding:18px clamp(14px,1.6vw,24px);text-decoration:none;height:100%}
.rules-title{counter-increment:none!important;display:flex;flex-direction:column;justify-content:center;gap:10px;padding:18px clamp(14px,1.6vw,24px)}.rules-title a{display:inline;padding:0;font:500 11px/1 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--ink);text-decoration:underline}.rules .rules-title a::before{content:none}
.rules a::before{content:counter(r);font:400 15px var(--mark);color:var(--gold)}
.rules .rule{font:400 18px/1.25 var(--display);color:var(--ink)}.rules .rule i{display:block}
.rules a:hover .rule{text-decoration:underline;text-underline-offset:3px}
@media (max-width:820px){.rules{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}.rules li{flex:0 0 58%;scroll-snap-align:start;border-right:1px solid var(--line)}.rules li.rules-title{flex-basis:38%}}
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
/* hero slides: N photos + texts cross-fade on one clock (--n slides, 6s each); still first slide for reduced motion */
.hero .h1{font:400 clamp(38px,4.6vw,62px)/1.04 var(--display);color:var(--ink);margin:0;text-wrap:balance}
.hero .h1 i,.hero h1 i{display:block}
.slides{position:relative;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.copy.stack{display:grid;align-items:center}
.copy.stack>.slide{grid-area:1/1;display:flex;flex-direction:column;justify-content:center;gap:22px;min-width:0}
@media (max-width:820px){.copy.stack>.slide{gap:16px}}
.copy.stack .btns{grid-template-columns:15rem}@media (min-width:1100px){.copy.stack .btns{grid-template-columns:repeat(2,15rem)}}@media (max-width:820px){.copy.stack{align-items:stretch}.copy.stack>.slide{justify-content:flex-start}.copy.stack .btns{margin-top:auto}}
.slides img+img,.copy.stack>.slide+.slide{opacity:0;visibility:hidden}
@media (prefers-reduced-motion:no-preference){
.slides img,.copy.stack>.slide{animation:slide calc(var(--n)*6s) linear infinite;animation-delay:calc((var(--i)*6s) - var(--n)*6s)}
.slides img{animation-name:slideimg}
.hero:hover .slides img,.hero:hover .slide,.hero:focus-within .slides img,.hero:focus-within .slide{animation-play-state:paused}}
@keyframes slide{0%{opacity:1;visibility:visible}21%{opacity:1;visibility:visible}25%{opacity:0;visibility:hidden}96%{opacity:0;visibility:hidden}100%{opacity:1;visibility:visible}}
@keyframes slideimg{0%{opacity:1;visibility:visible;transform:scale(1.02)}21%{opacity:1;visibility:visible}25%{opacity:0;visibility:hidden;transform:scale(1.09)}96%{opacity:0;visibility:hidden;transform:scale(1.02)}100%{opacity:1;visibility:visible;transform:scale(1.02)}}
.hero-tile{aspect-ratio:16/7;max-width:100%;margin-bottom:44px}
.tile.photo{padding:0}
.tile.photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero .tile.photo{min-height:640px}
@media (max-width:820px){.hero .tile.photo{min-height:0;height:72vw;max-height:320px}.hero-tile.photo{aspect-ratio:4/3}}
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
.strip-row{display:flex;gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.strip-row .strip-tile{flex:0 0 230px;scroll-snap-align:start}
@media (min-width:761px){.edit-strip.narrow .strip-tile{flex-basis:calc((100% - 32px) / 3)}}
.marquee{display:contents}
@media (min-width:821px) and (prefers-reduced-motion:no-preference){.home-strip .strip-row{overflow-x:auto;scroll-snap-type:none}.home-strip .marquee{display:flex;gap:16px;width:max-content;animation:glide 140s linear infinite}.home-strip .strip-row:hover .marquee,.home-strip .strip-row:focus-within .marquee{animation-play-state:paused}}
@keyframes glide{to{transform:translateX(calc(-50% - 8px))}}
.home-strip{padding-bottom:64px}
.home-strip .strip-row .strip-tile{flex-basis:250px}
.strip-tile{display:flex;flex-direction:column;gap:8px;min-width:0}
.strip-title{text-decoration:none;color:var(--ink);font:400 16px/1.25 var(--display);padding-block:4px}
.strip-title:hover{text-decoration:underline;text-underline-offset:3px}
.strip-title .down{color:var(--gold);margin-left:6px;vertical-align:-1px;transition:transform .25s ease}
.strip-title:hover .down{transform:translateY(2px)}
@media (prefers-reduced-motion:reduce){.strip-title .down{transition:none}.strip-title:hover .down{transform:none}}
.collage{display:grid;aspect-ratio:1/1;gap:3px;background:#fff}
.collage a{display:block;background:#efefef;position:relative;overflow:hidden;min-height:0}
.collage img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:6%;box-sizing:border-box;transition:transform .4s ease}
.collage a:hover img{transform:scale(1.05)}
.collage.c3{grid-template-columns:2fr 1fr;grid-template-rows:1fr 1fr}
.collage.c3 a:first-child{grid-row:1/3}
.collage.c2{grid-template-columns:1fr 1fr}
@media (prefers-reduced-motion:reduce){.collage img{transition:none}.collage a:hover img{transform:none}}
.rail-sec{border-top:1px solid var(--line);padding-block:44px 52px;margin-top:40px}
.rail-sec .sec-head{margin-bottom:4px}
.rail-note{margin:0 0 22px;color:var(--muted);font-size:13px}
.rail{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding-inline:max(20px,calc((100vw - 1280px)/2 + 20px));scroll-padding-inline:max(20px,calc((100vw - 1280px)/2 + 20px));padding-bottom:12px;scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.rail .piece{flex:0 0 210px;scroll-snap-align:start}
.rail .piece-img{background:var(--silk)}
@media (max-width:760px){.rail{gap:14px}.rail .piece{flex-basis:62%}}
.board{background:var(--silk);margin-block:40px;scroll-margin-top:24px}
.board-in{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);grid-template-areas:"text rail" "story rail";grid-template-rows:auto 1fr;column-gap:48px;row-gap:18px;padding-block:44px;align-items:start}
.board-text{grid-area:text;display:flex;flex-direction:column;gap:8px}
.board-text .label{font-size:11px;white-space:nowrap}
.board-text h2{font:400 32px/1.15 var(--display);margin:0;color:var(--ink)}
.board-more{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);text-underline-offset:4px;margin-top:6px;padding-block:8px}
.board-intro{margin:0;color:var(--body-ink);font-size:16px;line-height:1.6}
.board-story{grid-area:story;margin:0;color:var(--muted);font:italic 400 16px/1.6 var(--display)}
.board-rail{grid-area:rail;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:28px 20px}
/* numbered list board (capsule): number, advice and the piece in one row */
.board.cap{background:var(--silk)}
.cap-in{padding-block:40px 48px}
.cap-label{font-size:11px;margin:0 0 22px}
.cap-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px}
.cap-row{display:grid;grid-template-columns:150px minmax(0,1fr);gap:22px;align-items:start;padding-block:22px;border-top:1px solid var(--line)}
.cap-img{display:block;aspect-ratio:1/1;background:#fff;position:relative;overflow:hidden}
.cap-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:8px;box-sizing:border-box}
.cap-img.empty{background:transparent;border:1px solid var(--line)}
.cap-img .word{position:absolute;left:12px;bottom:10px;font:italic 400 18px/1 var(--display);color:var(--muted)}
.cap-text{display:flex;flex-direction:column;gap:6px;min-width:0}
.cap-num{font:italic 400 30px/1 var(--display);color:var(--gold,#a88a4e)}
.cap-text h3{font:400 21px/1.25 var(--display);margin:0;color:var(--ink)}
.cap-text p{margin:0;font-size:15px;line-height:1.55;color:var(--body-ink)}
.cap-shop{display:flex;flex-direction:column;gap:3px;margin-top:6px;padding-top:10px;border-top:1px dotted var(--line)}
.cap-shop .label{font-size:10.5px}
.cap-shop .piece-name{font-size:16px}
@media (max-width:820px){.cap-list{grid-template-columns:1fr}.cap-row{grid-template-columns:112px minmax(0,1fr);gap:16px;padding-block:18px}.cap-num{font-size:24px}.cap-text h3{font-size:19px}.cap-text p{font-size:14.5px}}
/* our picks page */
.pick-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 30px}
.sub-chips{margin-top:-18px}.sub-chips label{font-size:10px;padding:7px 12px;border-style:dashed}
.pick-chips label{cursor:pointer;user-select:none}
.pf:focus-visible~.pick-chips{outline:2px solid var(--gold);outline-offset:4px}
.pick-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:36px 22px;padding-bottom:60px}
@media (max-width:1000px){.pick-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:640px){.pick-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:26px 14px}}
.pick-from{font-size:12px;letter-spacing:.06em;color:var(--ink);text-underline-offset:3px;margin-top:4px}
.pick .piece-img{background:#fff}
.piece{display:flex;flex-direction:column;gap:5px;min-width:0}
@media (min-width:761px){
.board-rail.n3{grid-template-columns:repeat(3,minmax(0,1fr))}
.board-rail.n4{grid-template-columns:repeat(4,minmax(0,1fr))}
.board-rail.n5{grid-template-columns:repeat(6,minmax(0,1fr))}
.board-rail.n6{grid-template-columns:repeat(3,minmax(0,1fr))}
.board-rail.n7,.board-rail.n8{grid-template-columns:repeat(4,minmax(0,1fr))}
.board-rail.n5 .piece{grid-column:span 2}
.board-rail.n5 .piece:nth-child(4){grid-column:2/4}
.board-rail.n5 .piece:nth-child(5){grid-column:4/6}
.board-rail.scroll{display:flex;gap:20px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px;scrollbar-width:thin;scrollbar-color:var(--line) transparent}
.board-rail.scroll .piece{flex:0 0 calc((100% - 60px) / 3.4);scroll-snap-align:start}
}
.piece-img{display:block;aspect-ratio:1/1;background:#fff;position:relative;overflow:hidden;margin-bottom:8px}
.piece-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;padding:10px;box-sizing:border-box;transition:transform .4s ease}
.piece:hover .piece-img img{transform:scale(1.03)}
@media (prefers-reduced-motion:reduce){.piece-img img{transition:none}.piece:hover .piece-img img{transform:none}}
.piece-img .word{position:absolute;left:12px;bottom:10px;font:italic 400 20px/1 var(--display);color:var(--ink)}
.piece .label{font-size:11px}
.piece-name{font:400 17px/1.3 var(--display);color:var(--ink);text-decoration:none}
.piece-name:hover{text-decoration:underline;text-underline-offset:3px}
.piece-why{display:block;margin-top:4px;font:italic 400 14px/1.35 var(--display);color:var(--muted)}
.piece-shop{font-size:13px;color:var(--muted)}
.gift-note{display:flex;flex-direction:column;gap:2px;margin:10px 0 2px;font-size:13.5px;line-height:1.45;border-top:1px solid var(--line);padding-top:10px}
.gift-note dt{margin-top:6px;font:500 10px/1.6 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
.gift-note dd{margin:0;color:var(--body-ink)}
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
.strip-row{gap:12px}
.strip-row .strip-tile{flex-basis:62%}
.strip-title{font-size:14px}
}
.product:hover .product-name{text-decoration:underline;text-underline-offset:3px}
.prose{color:var(--body-ink)}
.prose h2{font:400 30px/1.2 var(--display);color:var(--ink);margin:46px 0 12px;text-wrap:balance}
.prose p{margin:0 0 18px}
.prose .story-nav{font-size:13px;letter-spacing:.06em;line-height:2;color:var(--muted);border-block:1px solid var(--line);padding-block:10px;margin-bottom:26px}
.story-nav span{font-size:11px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;margin-right:8px}
.story-nav a{white-space:nowrap;color:var(--ink);text-underline-offset:3px;text-decoration-color:#bdb7b0}
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

def jpeg_size(path):
    """(width, height) of a JPEG without third-party libraries; None if unknown."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                return None
            marker = data[i + 1]
            length = int.from_bytes(data[i + 2:i + 4], "big")
            if marker in (0xC0, 0xC1, 0xC2):
                return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
            i += 2 + length
    except OSError:
        return None
    return None

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
        *([f'<meta property="og:image:width" content="{size[0]}">', f'<meta property="og:image:height" content="{size[1]}">']
          if (size := jpeg_size(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", img_file))) else []),
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
<title>{html_lib.escape(title, quote=False)}</title>
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="description" content="{html_lib.escape(desc, quote=True)}">
<link rel="canonical" href="{SITE['url']}/{canonical}">
<meta property="og:title" content="{html_lib.escape(title, quote=True)}">
<meta property="og:description" content="{html_lib.escape(desc, quote=True)}">
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

TYPE_WORD = {"necklace": "Collier", "ring": "Bague", "bracelet": "Bracelet", "earrings": "Boucles", "watch": "Montre", "boot": "Bottes",
             "camisole": "Caraco", "bra": "Soutien-gorge", "bralette": "Bralette", "bodysuit": "Body", "corset": "Corset", "top": "Haut",
             "slip dress": "Nuisette", "gown": "Robe", "dress": "Robe", "coat": "Manteau", "jacket": "Veste", "blazer": "Blazer", "cardigan": "Gilet", "knit jacket": "Gilet", "sweater": "Pull", "jeans": "Jean", "trousers": "Pantalon", "shirt": "Chemise", "bag": "Sac", "suitcase": "Valise", "sneakers": "Baskets", "loafers": "Mocassins", "sunglasses": "Lunettes", "cap": "Casquette", "hat": "Chapeau", "beret": "Béret", "gloves": "Gants", "mittens": "Moufles", "scarf": "Écharpe", "headphones": "Casque", "t-shirt": "T-shirt", "blouse": "Blouse",  "belt": "Ceinture", "tights": "Collant", "skirt": "Jupe", "shorts": "Short", "pyjama trousers": "Pyjama", "pyjama top": "Pyjama", "headband": "Bandeau"}

AFF_ATTRS = 'rel="sponsored nofollow noopener" target="_blank"'
DEFAULT_REGION = "eu"   # where a click on the photo or name goes: "eu" (EU/UK programme) or "us"

def edit_id(e):
    return "edit-" + re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-")

def gift_note(pr):
    g = pr.get("gift")
    if not g:
        return ""
    return (f'<dl class="gift-note"><dt>Why</dt><dd>{g["why"]}</dd><dt>What</dt><dd>{g["what"]}</dd>'
            f'<dt>Stands for</dt><dd>{g["means"]}</dd></dl>')

def board_key(e):
    """Short name of a board for tracking, e.g. 'The Heeled Knee-High Edit' -> 'heeled-knee-high'."""
    k = re.sub(r"[^a-z0-9]+", "-", e["title"].lower()).strip("-")
    return re.sub(r"^the-|-edit$", "", k)

def tag(url, label):
    """Add a Rakuten subID (u1) so reports show which board and which spot on the site a sale came from.
    Only the board and the spot go in, never anything about the reader."""
    if url and "linksynergy.com" in url and "u1=" not in url:
        return f"{url}&u1={label[:72]}"
    return url
sub_tag = tag   # alias: build() has a local variable called tag

def list_board(e, place="art"):
    """A numbered list where each item carries its own piece: number, the advice, then the product.
    Items without a product show the advice only. Used for articles built as a list (the capsule)."""
    byp = {pr["url_eu"].rsplit("-", 1)[-1].lower(): pr for pr in e["products"]}
    rows = []
    for it in e["items"]:
        pr = byp.get(it.get("p", "").lower())
        shop = ""
        if pr:
            alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
            label = f"{place}-{board_key(e)}"
            urls = {"eu": tag(pr.get("url_eu"), label), "us": tag(pr.get("url_us"), label)}
            main = urls.get(DEFAULT_REGION) or urls["eu"] or urls["us"]
            regions = []
            if urls["eu"]: regions.append(f'<a href="{urls["eu"]}" {AFF_ATTRS} aria-label="Discover {alt} in Europe and the UK">EU / UK</a>')
            if urls["us"]: regions.append(f'<a href="{urls["us"]}" {AFF_ATTRS} aria-label="Discover {alt} in the US">US</a>')
            img = f'<a class="cap-img" href="{main}" {AFF_ATTRS} tabindex="-1" aria-hidden="true"><img src="{pr["image"]}" alt="{alt}" loading="lazy"></a>'
            shop = (f'<div class="cap-shop"><span class="label">{pr["brand"]}</span><a class="piece-name" href="{main}" {AFF_ATTRS}>{pr["name"]}</a>'
                    f'<span class="piece-regions">Discover &mdash; {" &middot; ".join(regions)}</span></div>')
        else:
            img = f'<span class="cap-img empty" aria-hidden="true"><span class="word">{TYPE_WORD.get(it.get("type", ""), "")}</span></span>'
        rows.append(f'<li class="cap-row{"" if pr else " no-piece"}">{img}<div class="cap-text"><span class="cap-num">{it["n"]:02d}</span>'
                    f'<h3>{it["head"]}</h3><p>{it["text"]}</p>{shop}</div></li>')
    return f'''<section class="board cap" id="{edit_id(e)}" aria-label="{html_lib.escape(e["title"], quote=True)}">
<div class="wrap cap-in"><p class="label cap-label">The Edit &middot; Mytheresa &middot; affiliate links</p>
<ol class="cap-list">{"".join(rows)}</ol></div></section>'''

def edit_board(e, story_href="", place="art"):
    """One themed board, full width between the article's paragraphs: text on the left,
    the pieces on the right (desktop) or as a swipeable row (phone). No prices (they change);
    product images come unaltered from the retailer's catalogue."""
    shops = {pr.get("shop", "Mytheresa") for pr in e["products"]}
    one_shop = shops.pop() if len(shops) == 1 else ""   # name the shop once on the board, not on every card
    cards = []
    for pr in e["products"]:
        alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
        img = (f'<img src="{pr["image"]}" alt="{alt}" loading="lazy">' if pr.get("image")
               else f'<span class="word">{TYPE_WORD.get(pr.get("type", ""), "Shop")}</span>')
        label = f"{place}-{board_key(e)}"
        urls = {"eu": tag(pr.get("url_eu"), label), "us": tag(pr.get("url_us"), label)}
        main = urls.get(DEFAULT_REGION) or urls["eu"] or urls["us"] or "#"
        regions = []
        if urls["eu"]: regions.append(f'<a href="{urls["eu"]}" {AFF_ATTRS} aria-label="Discover {alt} in Europe and the UK">EU / UK</a>')
        if urls["us"]: regions.append(f'<a href="{urls["us"]}" {AFF_ATTRS} aria-label="Discover {alt} in the US">US</a>')
        cards.append(f'''<div class="piece" role="listitem">
<a class="piece-img" href="{main}" {AFF_ATTRS} tabindex="-1" aria-hidden="true">{img}</a>
<span class="label">{pr["type"].capitalize()} &middot; {pr["brand"]}</span>
<a class="piece-name" href="{main}" {AFF_ATTRS}>{pr["name"]}</a>
{f'<span class="piece-why">{pr["why"]}</span>' if pr.get("why") else ""}
{"" if one_shop else f'<span class="piece-shop">at {pr.get("shop", "Mytheresa")}</span>'}
{gift_note(pr)}<span class="piece-regions">Discover &mdash; {" &middot; ".join(regions)}</span>
</div>''')
    story = f'<p class="board-story">{e["story"]}</p>' if e.get("story") else ""
    n = len(e["products"])
    return f'''<section class="board" id="{edit_id(e)}" aria-label="{html_lib.escape(e["title"], quote=True)}">
<div class="wrap board-in">
<div class="board-text"><span class="label">The Edit{f" &middot; {one_shop}" if one_shop else ""} &middot; affiliate links</span><h2>{e["title"]}</h2><p class="board-intro">{e.get("intro", "")}</p>{f'<a class="board-more" href="{story_href}">Read the story &rarr;</a>' if story_href else ""}</div>
<div class="board-rail n{n}{" scroll" if e.get("scroll") else ""}" role="list" aria-label="{n} pieces">{"".join(cards)}</div>
{story}
</div></section>'''

def edit_strip(edits, heading="The Edit in this story", base="", narrow=True, place="strip", subs=None):
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
            url = tag(pr.get(f"url_{DEFAULT_REGION}") or pr.get("url_eu") or pr.get("url_us"), f"{place}-{board_key(e)}")
            alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
            cells.append(f'<a href="{url}" {AFF_ATTRS} title="{alt}"><img src="{pr["image"]}" alt="{alt}" loading="lazy"></a>')
        sub = f'<span class="strip-sub">{subs[e["title"]]}</span>' if subs and e["title"] in subs else ""
        items.append(f'''<div class="strip-tile"><div class="collage c{len(cells)}">{"".join(cells)}</div>
<a class="strip-title" href="{base}#{edit_id(e)}">{e["title"]}{"" if base else ' <svg class="down" width="9" height="14" viewBox="0 0 9 14" aria-hidden="true"><path d="M4.5 0.5v12.2M0.8 9l3.7 3.7L8.2 9" fill="none" stroke="currentColor" stroke-width="1"/></svg>'}</a>{sub}</div>''')
    return f'''<nav class="wrap{" narrow" if narrow else ""} edit-strip" aria-label="{heading}">
<span class="label">{heading}</span><div class="strip-row">{"".join(items)}</div></nav>'''

def marquee(strip_html):
    """Desktop: let the home strip glide slowly on its own (CSS only, no script). The tiles are repeated once,
    hidden from screen readers and keyboard, so the loop is seamless. Hover pauses it; phones keep swiping;
    people who prefer reduced motion get the normal row."""
    a = strip_html.index('<div class="strip-row">') + len('<div class="strip-row">')
    e = strip_html.rindex('</div></nav>')
    items = strip_html[a:e]
    dup = items.replace('<div class="strip-tile">', '<div class="strip-tile" aria-hidden="true">').replace('<a ', '<a tabindex="-1" ')
    return strip_html[:a] + f'<div class="marquee">{items}{dup}</div>' + strip_html[e:]

def edit_rail(current_slug, limit=10):
    """'From The Edit' at the foot of an article: a swipeable row of pieces from the edits of *other*
    articles, so every story ends with a few of the editor's picks."""
    picks = [(pr, e) for a in ARTICLES if a["slug"] != current_slug for e in (a.get("edits") or [])
             for pr in e["products"] if pr.get("image")][:limit]
    if not picks:
        return ""
    cards = []
    for pr, e in picks:
        alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
        url = tag(pr.get(f"url_{DEFAULT_REGION}") or pr.get("url_eu") or pr.get("url_us"), f"rail-{board_key(e)}")
        cards.append(f'''<div class="piece" role="listitem">
<a class="piece-img" href="{url}" {AFF_ATTRS} tabindex="-1" aria-hidden="true"><img src="{pr["image"]}" alt="{alt}" loading="lazy"></a>
<span class="label">{pr["brand"]}</span>
<a class="piece-name" href="{url}" {AFF_ATTRS}>{pr["name"]}</a>
</div>''')
    shops = {pr.get("shop", "Mytheresa") for pr, _ in picks}
    where = f" &middot; all at {shops.pop()}" if len(shops) == 1 else ""
    return f'''<section class="rail-sec" aria-label="From The Edit"><div class="wrap">
<div class="sec-head"><h2>From The Edit</h2><a href="/the-edit.html">See all</a></div>
<p class="rail-note">Other pieces we would choose ourselves &middot; affiliate links{where}</p></div>
<div class="rail" role="list">{"".join(cards)}</div></section>'''

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
        cuts.setdefault(pos, []).append(list_board(e) if e.get("items") else edit_board(e))
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
    iconsrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")   # tab and home-screen icons, served from the root
    if os.path.isdir(iconsrc):
        for name in os.listdir(iconsrc):
            shutil.copy(os.path.join(iconsrc, name), os.path.join(OUT, name))

    lead = next((a for a in ARTICLES if a["slug"] == SITE.get("lead")), ARTICLES[0])
    rest = [a for a in ARTICLES if a is not lead]
    row = "\n".join(card(a, 0) for a in rest[:4])
    all_edits = [(a, e) for a in ARTICLES for e in (a.get("edits") or [])]
    all_edits.sort(key=lambda ae: not ae[1].get("first"))
    home_edit = ""
    if all_edits:
        GL = {"clothing": "Looks", "jewelry": "Jewelry", "watches": "Watches", "lingerie": "Lingerie", "boots": "Boots", "travel": "Travel"}
        subs = {e["title"]: f'{GL.get(group_of(a), "")} &middot; {len(e["products"])} pieces' for a, e in all_edits}
        present = [k for k in GROUPS if any(group_of(a) == k for a, _ in all_edits)]
        chips = "".join(f'<a href="{k}.html">{GL[k]}</a>' for k in present)
        home_edit = (f'''<section class="wrap home-edit"><div class="sec-head"><h2>The Edit</h2><a href="the-edit.html">See the edit</a></div>
<nav class="theme-chips" aria-label="Shop by theme">{chips}</nav><p class="disclose" style="text-align:left;margin:0">{DISCLOSURE_SHORT}</p></section>'''
                     + marquee(edit_strip([e for _, e in all_edits], heading="Browse by theme", base="the-edit.html", narrow=False, place="home", subs=subs)).replace('class="wrap edit-strip"', 'class="wrap edit-strip home-strip"'))
    slides = SITE.get("hero_slides") or []
    if slides:
        n = len(slides)
        imgs = "".join(f'<img src="assets/img/{sl["img"]}" alt="{sl["alt"] if i == 0 else ""}"{" aria-hidden=\"true\"" if i else ""} '
                       f'{"" if i == 0 else "loading=\"lazy\" "}style="object-position:{sl.get("pos","center")};--i:{i}">' for i, sl in enumerate(slides))
        texts = ""
        for i, sl in enumerate(slides):
            tag = "h1" if i == 0 else "p"
            cls = "" if i == 0 else ' class="h1"'
            texts += (f'<div class="slide" style="--i:{i}"{" aria-hidden=\"true\"" if i else ""}><span class="kicker">{sl["kicker"]}</span>'
                      f'<{tag}{cls}>{sl["title"]} <i>{sl["italic"]}</i></{tag}><p>{sl["dek"]}</p>'
                      f'<div class="btns"><a class="btn" href="{sl["href"]}"{" tabindex=\"-1\"" if i else ""}>{sl["cta"]}</a>'
                      f'<a class="btn btn-solid" href="the-edit.html"{" tabindex=\"-1\"" if i else ""}>Shop the edits</a></div></div>')
        hero_html = (f'<section class="hero" style="--n:{n}"><div class="tile photo slides">{imgs}</div>'
                     f'<div class="copy stack">{texts}</div></section>')
    else:
        hero_html = f"""<section class="hero">
{tile('Soie', img=SITE.get('hero_image'))}
<div class="copy">
<span class="kicker">{SITE.get('lead_kicker', 'The edit &middot; ' + lead['category'])}</span>
<h1>{lead['title']}</h1>
<p>{lead['dek']}</p>
<div class="btns"><a class="btn" href="journal/{lead['slug']}.html">{SITE.get('lead_cta', 'Read the article')}</a><a class="btn btn-solid" href="the-edit.html">Shop the edits</a></div>
</div>
</section>"""
    home = f"""<p class="promise">Parisian styling advice, one look at a time.</p>
{hero_html}
{home_edit}
<ol class="rules"><li class="rules-title"><span class="rule">Five rules<i>for 2026</i></span><a href="journal/index.html">All articles</a></li><li><a href="journal/everyday-gold-jewelry.html"><span class="label">Fine jewelry</span><span class="rule">One good piece,<i>worn every day</i></span></a></li><li><a href="journal/what-is-quiet-luxury.html"><span class="label">Quiet luxury</span><span class="rule">Fabric over logos,<i>colour when chosen</i></span></a></li><li><a href="journal/three-boots-parisian-wardrobe.html"><span class="label">Boots</span><span class="rule">Three pairs<i>for every winter day</i></span></a></li><li><a href="journal/french-lingerie-guide.html"><span class="label">Lingerie</span><span class="rule">Silk underneath,<i>lace that lies flat</i></span></a></li><li><a href="journal/the-case-for-a-small-watch.html"><span class="label">Watches</span><span class="rule">A small watch<i>says enough</i></span></a></li></ol>
<section class="row" aria-label="Latest articles">{row}</section>
<section class="wrap sec" style="padding-bottom:0"><div class="sec-head"><h2>Quiet Parisian style, in silk and gold</h2></div></section>
<section class="pillars wrap" style="padding-left:0;padding-right:0">
<a class="pillar" href="clothing.html"><span class="label">Soie</span><h3>Clothing</h3><p>Parisian ready-to-wear from Sandro, IRO, Acne Studios, Marni and Miu Miu. Capsule wardrobes built to last.</p></a>
<a class="pillar" href="jewelry.html"><span class="label">Or</span><h3>Jewelry</h3><p>Fine jewelry to wear every day, from houses like Pomellato and Chopard.</p></a>
<a class="pillar" href="watches.html"><span class="label">Temps</span><h3>Watches</h3><p>Watches, new and pre-owned, with honest guidance on buying well.</p></a>
<a class="pillar" href="lingerie.html"><span class="label">Dessous</span><h3>Lingerie</h3><p>French lingerie in silk and fine lace: the first layer of a good outfit.</p></a>
<a class="pillar" href="boots.html"><span class="label">Bottes</span><h3>Boots</h3><p>Ankle, riding and heeled boots that see you through every winter.</p></a>
<a class="pillar" href="travel.html"><span class="label">Voyage</span><h3>Chic travel</h3><p>Three travel outfits for a weekend in Paris: the case, the bag and what to wear on the way.</p></a>
</section>
"""
    write("index.html", shell(f"{SITE['name']} · Parisian Styling Advice, Quiet Luxury & Fine Jewelry",
        "Parisian styling advice, one look at a time: complete outfits, capsule wardrobes, fine jewelry and watches worth keeping.", home, 0, "", ""))

    for key, g in GROUPS.items():
        items = [a for a in ARTICLES if group_of(a) == key or a["category"] in g.get("also", [])]
        cards = "\n".join(card(a, 0) for a in items)
        g_edits = [e for a in items for e in (a.get("edits") or [])]
        peek = (edit_strip(g_edits, heading=f"From the edit &middot; {g['title'].lower()}", base="the-edit.html", narrow=False, place="cat")
                .replace('class="wrap edit-strip"', 'class="wrap edit-strip home-strip"')
                + f'<p class="disclose wrap" style="text-align:left;max-width:none;margin:-14px auto 28px">{DISCLOSURE_SHORT}</p>') if g_edits else ""
        b = head_block("Section", g["title"], g["dek"]) + peek + f'<section class="wrap sec" style="padding-top:0"><div class="grid">{cards}</div></section>'
        write(f"{key}.html", shell(f"{g.get('seo_title', g['title'])} · {SITE['name']}", g.get("seo_desc", g["dek"]), b, 0, key, f"{key}.html"))

    jcards = "\n".join(card(a, 1) for a in ARTICLES)
    jbody = head_block("Journal", "The journal", "Wardrobe notes, jewelry guides and honest advice on buying luxury well.") + \
            f'<section class="wrap sec" style="padding-top:0"><div class="grid">{jcards}</div></section>'
    write("journal/index.html", shell(f"Journal: Parisian Style Advice & Buying Guides · {SITE['name']}", "Parisian styling advice, wardrobe notes, fine jewelry guides and honest advice on buying luxury well.", jbody, 1, "journal", "journal/"))

    for a in ARTICLES:
        g = group_of(a)
        others = [o for o in ARTICLES if o["slug"] != a["slug"]][:3]
        more = "\n".join(card(o, 1) for o in others)
        shop = shop_block(a.get("products"))
        rail = edit_rail(a["slug"])
        has_aff = bool(shop) or bool(rail) or bool(a.get("edits")) or any(is_affiliate(u) for u in re.findall(r'href="([^"]+)"', a["body"]))
        notice = f'<div class="wrap narrow"><p class="disclose">{DISCLOSURE_SHORT}</p></div>' if has_aff else ""
        body = f"""<article>
{head_block(a['category'], a['title'], a['dek'], f"{a['date']} &middot; {a['read']} read", f"/{g}.html")}
{notice}
{edit_strip(a.get("edits"))}
<div class="wrap">{tile(a['category'], 'hero-tile', img=a.get('image'), depth=1)}</div>
{body_with_edits(a['body'], a.get("edits"))}
{shop}{rail}</article>
<section class="wrap sec" style="border-top:1px solid var(--line)"><div class="sec-head"><h2>Keep reading</h2><a href="/journal/index.html">All articles</a></div><div class="grid">{more}</div></section>"""
        body = mark_affiliate_links(body)
        write(f"journal/{a['slug']}.html", shell(f"{a.get('seo_title', a['title'])} · {SITE['name']}", a.get("seo_desc", a["dek"]), body, 1, g, f"journal/{a['slug']}.html", image=a.get("image"), article=a))

    if all_edits:
        boards = "\n".join(edit_board(e, f"journal/{a['slug']}.html", place="page") for a, e in all_edits)
        eb = (head_block("The Edit", "The Edit", "Pieces we would choose ourselves. Each edit belongs to a story; read it there, or browse them all here.")
              + f'<div class="wrap narrow"><p class="disclose">{DISCLOSURE_SHORT}</p></div>'
              + edit_strip([e for _, e in all_edits], heading="The edits", place="pstrip") + boards)
        write("the-edit.html", shell(f"The Edit: Parisian Style Picks by Theme · {SITE['name']}", "Complete looks and pieces worth keeping, gathered by theme: quiet luxury outfits, boots, French lingerie, fine jewelry and travel.", mark_affiliate_links(eb), 0, "", "the-edit.html"))

    # Our picks: every piece once, filtered by kind (CSS only: radio buttons + :checked), each linking back to its look.
    PICK_CATS = [("coats", "Coats", {"coat"}),
                 ("jackets", "Jackets & blazers", {"jacket", "blazer"}),
                 ("knits", "Knitwear", {"sweater", "knit", "cardigan", "knit jacket"}),
                 ("shirts", "Shirts", {"shirt", "blouse"}),
                 ("tops", "Tops", {"top", "t-shirt"}),
                 ("dresses", "Dresses", {"dress", "gown", "slip dress"}),
                 ("skirts", "Skirts", {"skirt"}),
                 ("trousers", "Trousers & jeans", {"trousers", "jeans"}),
                 ("lingerie", "Lace tops & lingerie", {"shorts", "camisole", "bra", "bralette", "bodysuit", "corset", "pyjama trousers", "pyjama top"}),
                 ("boots", "Boots", {"boot"}),
                 ("shoes", "Sneakers", {"sneakers", "loafers", "pumps", "shoes"}),
                 ("bags", "Bags", {"bag"}),
                 ("cases", "Suitcases", {"suitcase"}),
                 ("jewelry", "Jewelry", {"necklace", "ring", "bracelet", "earrings"}),
                 ("watches", "Watches", {"watch"}),
                 ("extras", "Accessories", {"scarf", "sunglasses", "cap", "beret", "hat", "gloves", "mittens", "belt", "tights", "headband", "headphones"})]
    seen, picks = {}, []
    for a, e in all_edits:
        for pr in e["products"]:
            k = pr.get("image") or pr.get("url_eu")
            if k in seen:
                seen[k]["n"] += 1
                continue
            cat = next((c for c, _, ts in PICK_CATS if pr.get("type") in ts), "extras")
            if pr.get("type") == "coat" and "leather" in pr["name"].lower():
                cat = "jackets"   # leather coats sit with the jackets
            if pr.get("type") == "top" and "lace" in pr["name"].lower():
                cat = "lingerie"  # lace tops sit with the lingerie
            seen[k] = {"pr": pr, "a": a, "e": e, "cat": cat, "n": 1}
            picks.append(seen[k])
    order = {c: i for i, (c, _, _) in enumerate(PICK_CATS)}
    picks.sort(key=lambda p: order[p["cat"]])
    cards = []
    for p in picks:
        pr = p["pr"]; alt = html_lib.escape(f'{pr["brand"]} {pr["name"]}', quote=True)
        urls = {"eu": sub_tag(pr.get("url_eu"), "picks-" + p["cat"]), "us": sub_tag(pr.get("url_us"), "picks-" + p["cat"])}
        main = urls.get(DEFAULT_REGION) or urls["eu"] or urls["us"] or "#"
        regions = []
        if urls["eu"]: regions.append(f'<a href="{urls["eu"]}" {AFF_ATTRS} aria-label="Discover {alt} in Europe and the UK">EU / UK</a>')
        if urls["us"]: regions.append(f'<a href="{urls["us"]}" {AFF_ATTRS} aria-label="Discover {alt} in the US">US</a>')
        more = f' &middot; in {p["n"]} looks' if p["n"] > 1 else ""
        sub = ""
        if p["cat"] == "boots":
            nm = pr["name"].lower()
            sub = (" s-western" if any(w in nm for w in ("cowboy", "western", "biker")) else
                   " s-knee" if "knee" in nm else " s-ankle" if ("ankle" in nm or "chelsea" in nm) else "")
        elif p["cat"] == "extras":
            sub = {"sunglasses": " s-sunglasses", "cap": " s-hats", "beret": " s-hats", "hat": " s-hats", "headband": " s-hats",
                   "gloves": " s-gloves", "mittens": " s-gloves", "scarf": " s-scarves", "tights": " s-tights", "belt": " s-belts"}.get(pr.get("type"), "")
        elif p["cat"] == "jewelry":
            sub = {"necklace": " s-necklaces", "ring": " s-rings", "bracelet": " s-bracelets", "earrings": " s-earrings"}.get(pr.get("type"), "")
        cards.append(f'''<div class="piece pick c-{p["cat"]}{sub}" role="listitem">
<a class="piece-img" href="{main}" {AFF_ATTRS} tabindex="-1" aria-hidden="true"><img src="{pr["image"]}" alt="{alt}" loading="lazy"></a>
<span class="label">{pr["type"].capitalize()} &middot; {pr["brand"]}</span>
<a class="piece-name" href="{main}" {AFF_ATTRS}>{pr["name"]}</a>
{f'<span class="piece-why">{pr["why"]}</span>' if pr.get("why") else ""}
<a class="pick-from" href="journal/{p["a"]["slug"]}.html#{edit_id(p["e"])}">From: {p["e"]["title"]}{more} &rarr;</a>
<span class="piece-regions">Discover &mdash; {" &middot; ".join(regions)}</span>
</div>''')
    present = [c for c in PICK_CATS if any(p["cat"] == c[0] for p in picks)]
    radios = '<input type="radio" name="pf" id="pf-all" class="pf" checked>' + "".join(f'<input type="radio" name="pf" id="pf-{c}" class="pf">' for c, _, _ in present)
    chips = '<label for="pf-all">All</label>' + "".join(f'<label for="pf-{c}">{lab}</label>' for c, lab, _ in present)
    rules = "".join(f'#pf-{c}:checked~.pick-grid .pick:not(.c-{c}){{display:none}}#pf-{c}:checked~.pick-chips label[for=pf-{c}]{{background:var(--ink);color:var(--white)}}' for c, _, _ in present)
    SUBS = {"boots": ("All boots", [("ankle", "Ankle boots"), ("knee", "Knee-high boots"), ("western", "Western & biker")]),
            "jewelry": ("All jewelry", [("necklaces", "Necklaces"), ("rings", "Rings"), ("bracelets", "Bracelets"), ("earrings", "Earrings")]),
            "extras": ("All accessories", [("sunglasses", "Sunglasses"), ("hats", "Hats & caps"), ("gloves", "Gloves"), ("scarves", "Scarves"), ("tights", "Tights"), ("belts", "Belts")])}
    subchips = ""
    rules += ".sub-chips{display:none!important}"
    for c, (all_lab, opts) in SUBS.items():
        opts = [(k, lab) for k, lab in opts if any(f" s-{k}" in x for x in cards)]
        radios += f'<input type="radio" name="sf-{c}" id="sf-{c}-all" class="pf" checked>' + "".join(f'<input type="radio" name="sf-{c}" id="sf-{c}-{k}" class="pf">' for k, _ in opts)
        subchips += (f'<div class="pick-chips sub-chips sub-{c} theme-chips" role="group" aria-label="Filter {c} by type"><label for="sf-{c}-all">{all_lab}</label>'
                     + "".join(f'<label for="sf-{c}-{k}">{lab}</label>' for k, lab in opts) + '</div>')
        rules += (f'#pf-{c}:checked~.sub-{c}{{display:flex!important}}#sf-{c}-all:checked~.sub-{c} label[for=sf-{c}-all]{{background:var(--ink);color:var(--white)}}'
                  + "".join(f'#pf-{c}:checked~#sf-{c}-{k}:checked~.pick-grid .pick.c-{c}:not(.s-{k}){{display:none}}#sf-{c}-{k}:checked~.sub-{c} label[for=sf-{c}-{k}]{{background:var(--ink);color:var(--white)}}' for k, _ in opts))
    pb = (head_block("The Edit", "Our picks", "Every piece from our looks, in one place. Filter by what you are looking for; each piece shows the look it belongs to.")
          + f'''<section class="wrap picks"><style>.pf{{position:absolute;opacity:0;pointer-events:none}}#pf-all:checked~.pick-chips label[for=pf-all]{{background:var(--ink);color:var(--white)}}{rules}</style>
<p class="disclose" style="text-align:left;margin:0 0 18px">{DISCLOSURE_SHORT}</p>{radios}
<div class="pick-chips theme-chips" role="group" aria-label="Filter by kind">{chips}</div>
{subchips}
<div class="pick-grid" role="list">{"".join(cards)}</div></section>''')
    write("our-picks.html", shell(f"Our Picks: Parisian Wardrobe Pieces by Kind · {SITE['name']}", "Every piece from our Parisian looks in one place, filtered by kind: coats, knits, boots, bags, jewelry and watches.", mark_affiliate_links(pb), 0, "", "our-picks.html").replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))

    simple_page("about.html", "About Soie et Or", "About", ABOUT, "about")
    simple_page("contact.html", "Contact", "Contact", CONTACT)
    simple_page("affiliate-disclosure.html", "Affiliate disclosure", "Transparency", DISCLOSURE)
    simple_page("privacy.html", "Privacy policy", "Legal", PRIVACY)
    simple_page("terms.html", "Terms of use", "Legal", TERMS)

    nf = head_block("404", "This page has slipped away", 'The link may be old or mistyped. <a href="/index.html">Back to the home page</a>.')
    write("404.html", shell(f"Page not found · {SITE['name']}", "Page not found", nf, 0, "", "404.html").replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1))

    urls = ["", "clothing.html", "lingerie.html", "boots.html", "jewelry.html", "watches.html", "travel.html", "journal/", "about.html", "contact.html",
            "affiliate-disclosure.html", "privacy.html", "terms.html", "the-edit.html"] + [f"journal/{a['slug']}.html" for a in ARTICLES]
    lastmod = {f"journal/{a['slug']}.html": f"<lastmod>{iso_date(a.get('updated', a['date']))[:10]}</lastmod>" for a in ARTICLES}
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "\n".join(f"  <url><loc>{SITE['url']}/{u}</loc>{lastmod.get(u, '')}</url>" for u in urls) + "\n</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")

if __name__ == "__main__":
    build()
