# Content for soie-et-or.com — edit text here, then run build.py
SITE = {
    "name": "Soie et Or",
    "domain": "soie-et-or.com",
    "url": "https://www.soie-et-or.com",
    "tagline": "Quiet Parisian style, in silk and gold.",
    "email": "hello@soie-et-or.com",
    "updated": "20 October 2026",
    # Change these once the Pinterest business account exists
    "pinterest": "https://www.pinterest.com/soieetor/",
    "pinterest_label": "pinterest.com/soieetor",
    # Paste the content value of Pinterest's claim meta tag here (Settings > Claimed accounts > Websites)
    # Homepage hero photo (file lives in images/)
    "hero_image": {"file": "portrait-black-blazer.jpg", "pos": "center 30%",
                   "alt": "Woman in a black tailored blazer, leather gloves, statement rings and a steel watch"},
    "pinterest_verify": "befd5a5bd7eca69fc2921fe79cef2cc9",
}

DISCLOSURE_SHORT = ('Some links are affiliate links; we may earn a small commission. '
                    '<a href="/affiliate-disclosure.html">How this works</a>')

# Links to these domains count as affiliate links. The build adds rel="sponsored"
# to them and shows DISCLOSURE_SHORT at the top of any article that contains one.
AFFILIATE_DOMAINS = [
    "awin1.com", "tidd.ly",                                   # Awin
    "prf.hn",                                                 # Partnerize (Farfetch)
    "click.linksynergy.com", "linksynergy.com",               # Rakuten (Net-a-Porter)
    "anrdoezrs.net", "jdoqocy.com", "tkqlhce.com", "dpbolvw.net", "kqzyfj.com",  # CJ (Mytheresa, Vestiaire)
    "go.skimresources.com", "go.redirectingat.com",           # Skimlinks
    "sovrn.co", "shareasale.com", "shopmy.us", "liketk.it", "rstyle.me", "daisycon",
]

# How to add products to an article (shown as a "Shop the edit" row under the text):
#   "products": [
#     {"name": "Wool blazer", "brand": "Sandro", "shop": "Farfetch", "price": "€450",
#      "url": "https://www.awin1.com/...", "image": "https://.../product.jpg"},
#   ],

ARTICLES = [
 {
  "slug": "parisian-autumn-capsule",
  "title": "The Parisian Autumn Capsule: Ten Pieces, Endless Outfits",
  "dek": "A small wardrobe that does a lot of work, built the way Parisian women actually dress.",
  "category": "Wardrobe",
  "date": "20 October 2026",
  "read": "6 min",
  "tone": "camel",
  "image": {"file": "cafe-le-progres.jpg", "pos": "center 75%",
            "alt": "Cream Haussmann building with a red-awninged corner café in Paris"},
  "body": """
<p>Parisian style has a reputation for looking effortless. The effort is real, but it goes into choosing, not into dressing. A Parisian wardrobe tends to be small, quiet in colour and very well edited. Almost everything works with almost everything else, so getting dressed takes two minutes.</p>
<p>This is the ten-piece capsule we would build for autumn. The palette stays narrow on purpose: navy, black, ecru, camel and one deep accent. That restraint is what lets ten pieces turn into dozens of outfits.</p>
<h2>The ten pieces</h2>
<ol class="numbered">
<li><strong>A camel coat with a clean shoulder.</strong> The single most useful thing you will own from October to March. Look for a long, straight cut that closes without strain over a knit.</li>
<li><strong>A slightly oversized wool blazer.</strong> Navy or black. It goes over jeans, over a slip dress, over a turtleneck. Sandro does this shape well, with sharp tailoring that never looks corporate.</li>
<li><strong>A cream cable or rib knit.</strong> Chunky enough to wear alone, fine enough to fit under the blazer.</li>
<li><strong>A fine black turtleneck.</strong> Merino or cashmere. The quiet base layer for everything else on this list.</li>
<li><strong>Straight dark jeans.</strong> Full length, no rips, no fading. Acne Studios is the reference for denim that looks expensive because it is plain.</li>
<li><strong>Wide, fluid trousers.</strong> In wool or a heavy crepe. They move when you walk, which is half of their charm.</li>
<li><strong>A silk or satin midi skirt.</strong> Worn with a chunky knit and flat boots, it is the most Parisian outfit on this list.</li>
<li><strong>A leather jacket with a little edge.</strong> IRO, founded in Paris in 2005 with roots in rock music, is known for exactly this kind of jacket: fitted, a bit worn-in in spirit, never costume.</li>
<li><strong>Loafers or flat ankle boots.</strong> Paris is a walking city. Heels are the exception, not the rule.</li>
<li><strong>One piece of everyday gold.</strong> A ring or a chain you never take off. More on that in <a href="/journal/everyday-gold-jewelry.html">our guide to everyday gold</a>.</li>
</ol>
<h2>How to wear it</h2>
<p>Three formulas cover most days. Jeans, turtleneck, blazer and loafers for the office. Silk skirt, cream knit and ankle boots for a long lunch. Wide trousers, leather jacket and a fine knit for the evening. Add the coat and you are done.</p>
<p>The rule that ties it together: one interesting thing per outfit. If the skirt shines, everything around it is matte. If the jacket has edge, the rest stays soft.</p>
<h2>What to leave out</h2>
<p>Logos, trend colours you will tire of by January, and anything that needs a specific shoe to work. A capsule only works if every piece earns its place.</p>
"""
 },
 {
  "slug": "everyday-gold-jewelry",
  "title": "Everyday Gold: How to Wear Fine Jewelry With Knitwear and Denim",
  "dek": "Fine jewelry is not only for evenings. The Parisian way is to wear a few good pieces every single day.",
  "category": "Jewelry",
  "date": "20 October 2026",
  "read": "5 min",
  "tone": "gold",
  "image": {"file": "silk-gold-gloves-wide.jpg", "card": "silk-gold-gloves-card.jpg", "pos": "center 20%",
            "card_pos": "center 30%",
            "alt": "Woman in a white blouse and gold satin gloves, seated in a striped armchair"},
  "body": """
<p>There is a particular kind of elegance in a woman wearing a cashmere sweater, old jeans and one serious gold ring. Nothing matches, nothing is trying, and yet the whole look reads as considered. That is everyday gold, and it is one of the easiest ways to make a simple wardrobe feel luxurious.</p>
<h2>Start with one signature piece</h2>
<p>Rather than collecting many small trinkets, choose one piece that you will wear daily and that feels like yours. A sculptural ring, a chain with some weight, or a watch you love. Over time it becomes part of how people recognise you.</p>
<p>Pomellato, founded in Milan in 1967, built its reputation on this idea: fine jewelry meant to be worn, not kept in a safe. Its Nudo ring, a coloured gemstone held in a clean gold setting, is a good example of a piece that works with a T-shirt as easily as with a dress.</p>
<h2>Gold and knitwear</h2>
<p>Gold looks warmest against texture. A chain over a fine turtleneck, rings against a chunky cream cable knit, a gold watch peeking out of a cashmere cuff. Keep the knit in a quiet colour so the metal does the talking: ecru, camel, grey, navy or black.</p>
<h2>Gold and denim</h2>
<p>Denim is the great equaliser. It makes fine jewelry look relaxed instead of formal. A white shirt, straight jeans, loafers and a few gold pieces is a complete outfit for almost any occasion.</p>
<h2>Something with movement</h2>
<p>Chopard's Happy Diamonds collection is built around diamonds that move freely between two sapphire crystals. It sounds playful, and it is, but worn with simple clothes it reads as quietly joyful rather than flashy. A pendant or a small watch from the collection is enough.</p>
<h2>Mixing metals and stacking</h2>
<ul>
<li>Stick mostly to one metal tone, then break the rule once on purpose.</li>
<li>Stack rings across two or three fingers, not all on one.</li>
<li>Layer chains in different lengths and weights so each one stays visible.</li>
<li>Leave one area bare. If your hands are busy, keep your neck simple.</li>
</ul>
<p>The goal is not to look decorated. It is to look like you have always worn these pieces and never thought twice about it.</p>
"""
 },
 {
  "slug": "pre-owned-cartier-watch-guide",
  "title": "Buying a Pre-Owned Cartier Watch: What to Check Before You Pay",
  "dek": "A pre-owned watch can be a smart way into fine watchmaking. Here is how to buy one with confidence.",
  "category": "Watches",
  "date": "20 October 2026",
  "read": "6 min",
  "tone": "ink",
  "image": {"file": "watch-pocket-bw-wide.jpg", "card": "watch-pocket-bw-card.jpg", "pos": "center",
            "alt": "Black and white close-up of an open skeleton pocket watch with Roman numerals and a chain"},
  "body": """
<p>Few watches suit the Parisian wardrobe better than a Cartier. The Tank, with its rectangular case, has been worn by the most stylish people of the last century and still looks modern with a white shirt. The Santos and the Panthère have their own followings. Buying pre-owned can bring these pieces within reach, but it pays to know what you are looking at.</p>
<h2>1. Buy from a platform that authenticates</h2>
<p>The most important decision is where you buy. Specialist marketplaces and resale platforms that check watches before they ship take most of the risk out of the purchase. Chrono24, the large watch marketplace, offers buyer protection with a secure payment service and the option to have a watch certified. Vestiaire Collective and similar platforms authenticate luxury items before delivery.</p>
<h2>2. Ask for box and papers</h2>
<p>Original box and papers do not make a watch genuine on their own, but they help with resale and with service history. A watch with its warranty card and purchase documents is usually easier to sell later and may hold its value better.</p>
<h2>3. Check the service history</h2>
<p>Mechanical watches need servicing. Ask when the watch was last serviced and by whom. A recent service by the brand or a qualified watchmaker is a plus. If there is no history, budget for a service after you buy.</p>
<h2>4. Look closely at condition</h2>
<ul>
<li>Scratches on the case and bracelet are normal. Heavy polishing that softens the edges is less desirable.</li>
<li>The dial should be clean, with crisp printing and no moisture marks.</li>
<li>Check that the bracelet fits your wrist, or that extra links are included.</li>
</ul>
<h2>5. Quartz or automatic?</h2>
<p>Many classic Cartier models were made with quartz movements. They are accurate, need little care and are often more affordable. Automatic movements appeal to people who love mechanical watchmaking. Both are valid; choose the one that fits how you live.</p>
<h2>6. Compare before you commit</h2>
<p>Look at several listings of the same model and reference. If one is far cheaper than the rest, there is usually a reason. Ask questions and request extra photos. A good seller will be happy to answer.</p>
<p>A pre-owned watch bought carefully is one of the most rewarding purchases you can make. It is also, quietly, one of the most sustainable.</p>
"""
 },
 {
  "slug": "sandro-vs-iro",
  "title": "Sandro or IRO? Two Takes on Parisian Chic",
  "dek": "Both are Parisian, both are loved, but they dress very different women. Here is how to tell which one is yours.",
  "category": "Brands",
  "date": "20 October 2026",
  "read": "5 min",
  "tone": "blush",
  "image": {"file": "cafe-vrai-paris.jpg", "pos": "center 35%",
            "alt": "Paris café terrace with a neon sign under a canopy of colourful flowers"},
  "body": """
<p>If you shop for Parisian ready-to-wear, two names come up again and again: Sandro and IRO. They sit at a similar level and are often found on the same rails, yet their mood is quite different. Knowing which one fits you saves a lot of returns.</p>
<h2>Sandro: polished and feminine</h2>
<p>Sandro dresses the Parisian woman on her way to work, to dinner, to a gallery opening. Think tailored blazers, tweed jackets, knitted cardigans with jewel buttons, pleated skirts and dresses that move well. The look is put together and a little romantic, with sharp tailoring underneath.</p>
<p><strong>Choose Sandro if</strong> you like structure, you want pieces that work for the office as well as the weekend, and you enjoy a feminine detail such as a bow, a scalloped edge or a bit of lace.</p>
<h2>IRO: relaxed with an edge</h2>
<p>IRO was founded in Paris in 2005 by brothers Laurent and Arik Bitton, who came from the music industry. You can still feel that rock influence: leather jackets, slim jeans, slouchy knits, short dresses worn with boots. The look is cool and a little undone, the Parisian off-duty uniform.</p>
<p><strong>Choose IRO if</strong> your wardrobe leans casual, you like leather and denim, and you want clothes that look better the more you wear them.</p>
<h2>Fit and sizing</h2>
<p>Both brands use French sizing. Check each product's size guide, and read the fit notes on the retailer's page. Fitted knits and jackets in particular can run small, so it is worth checking measurements rather than guessing.</p>
<h2>Why not both?</h2>
<p>The two mix well. A Sandro tweed jacket over IRO jeans and a white T-shirt is a very good outfit. Add loafers and one gold piece and you have the Parisian balance of polish and ease.</p>
"""
 },
 {
  "slug": "what-is-quiet-luxury",
  "title": "What Quiet Luxury Really Means (and What It Does Not)",
  "dek": "The term is everywhere. Underneath the trend is a simple, lasting idea about how to dress.",
  "category": "Style notes",
  "date": "20 October 2026",
  "read": "4 min",
  "tone": "stone",
  "image": {"file": "paris-eiffel-street-wide.jpg", "card": "paris-eiffel-street-card.jpg", "pos": "center 40%",
            "card_pos": "center",
            "alt": "Quiet Paris street in the 7th arrondissement at dusk, with the Eiffel Tower at the end"},
  "body": """
<p>Quiet luxury became a buzzword, which is a little ironic for something meant to be quiet. Strip away the headlines and it describes a way of dressing that Parisian women have practised for a long time: buy fewer things, buy better things, and let them speak softly.</p>
<h2>What it is</h2>
<ul>
<li><strong>Fabric first.</strong> Cashmere, silk, good wool, real leather. The quality shows in how a piece drapes and ages.</li>
<li><strong>Fit that is right.</strong> A simple trouser that fits perfectly looks more expensive than an elaborate one that does not.</li>
<li><strong>A narrow palette.</strong> Neutrals with an occasional deep colour. Everything combines.</li>
<li><strong>Recognition through design, not logos.</strong> A Cartier Tank or a Pomellato ring is recognised by people who know, and invisible to people who do not. That is the point.</li>
</ul>
<h2>What it is not</h2>
<ul>
<li>It is not beige for the sake of beige. Colour is welcome when it is chosen.</li>
<li>It is not about price alone. A well-made piece from a smaller label can be quieter and more luxurious than a famous logo.</li>
<li>It is not a uniform you buy in one go. It is a wardrobe that grows slowly.</li>
</ul>
<h2>Where to start</h2>
<p>Start with the pieces you wear most: a coat, a knit, a pair of trousers and one piece of jewelry you never take off. Upgrade those first. Our <a href="/journal/parisian-autumn-capsule.html">Parisian autumn capsule</a> is a good map.</p>
"""
 },
 {
  "slug": "cost-per-wear",
  "title": "Cost Per Wear: How to Think About Investment Pieces",
  "dek": "A simple calculation that changes how you shop, and why the expensive coat can be the economical choice.",
  "category": "Wardrobe",
  "date": "20 October 2026",
  "read": "4 min",
  "tone": "camel",
  "image": {"file": "leather-jacket-street-wide.jpg", "card": "leather-jacket-street-card.jpg", "pos": "center 30%",
            "card_pos": "center",
            "alt": "Black and white street photo of a woman in an oversized leather jacket and lace-trimmed skirt"},
  "body": """
<p>Cost per wear is the price of a piece divided by the number of times you wear it. It is a simple idea, and it is the clearest way to judge whether a luxury purchase is indulgent or sensible.</p>
<h2>An example</h2>
<p>A coat that costs 900 euros and is worn 60 days a year for five years has been worn 300 times. That is 3 euros per wear. A trend coat that costs 150 euros and is worn ten times before it feels dated costs 15 euros per wear. The cheaper coat was five times more expensive.</p>
<h2>What makes a good investment piece</h2>
<ul>
<li><strong>You will wear it often.</strong> Be honest about your real life, not the life in the picture.</li>
<li><strong>It works with what you own.</strong> If it needs new shoes and a new bag, add those to the price.</li>
<li><strong>It is built to last.</strong> Look at seams, lining, buttons and fabric weight.</li>
<li><strong>It will not date quickly.</strong> Classic shapes in classic colours.</li>
</ul>
<h2>Jewelry and watches</h2>
<p>Fine jewelry and watches can be the ultimate cost-per-wear pieces. A ring worn every day for twenty years becomes almost free per wear, and good pieces can often be resold. Buying <a href="/journal/pre-owned-cartier-watch-guide.html">pre-owned</a> lowers the entry price further.</p>
<h2>When not to use it</h2>
<p>Cost per wear is a tool, not a rule. Some pieces are worth it for one perfect evening. The idea is not to stop enjoying fashion, but to spend with intention.</p>
"""
 },
 {
  "slug": "chic-travel-packing",
  "title": "The Chic Carry-On: Packing for a Weekend in Paris",
  "dek": "One good bag, a handful of pieces that all work together, and the accessories that make travel look effortless.",
  "category": "Travel",
  "date": "21 October 2026",
  "read": "5 min",
  "tone": "camel",
  "image": {"file": "paris-hotel-breakfast-wide.jpg", "card": "paris-hotel-breakfast-card.jpg", "pos": "center 40%",
            "card_pos": "center",
            "alt": "Breakfast tray with coffee, juice and croissants on a white bed by a Paris balcony window"},
  "body": """
<p>The most elegant travellers are rarely the ones with the most luggage. They carry one good bag, a few pieces that all combine, and accessories that do the work of a whole outfit. Here is how to pack a weekend in Paris, or anywhere, the quiet way.</p>
<h2>The bags</h2>
<ul>
<li><strong>A structured weekender.</strong> Leather or heavy canvas, with a shape that holds when it is half full. It should fit in the overhead bin and look just as good on a hotel luggage rack.</li>
<li><strong>A soft tote for the day.</strong> Big enough for a scarf, sunglasses and a book. Leave the logo bags at home; a plain tote in black, tan or ecru goes with everything.</li>
<li><strong>A small crossbody for the evening.</strong> Keys, phone, lipstick. Nothing more.</li>
</ul>
<h2>The outfits</h2>
<p>Pack in one palette so everything mixes: navy, black, cream and camel, with one accent colour at most. Travel in your bulkiest pieces, the coat and the knit, so the bag stays light.</p>
<ul>
<li>A long coat that works over everything</li>
<li>Straight jeans and one pair of fluid trousers</li>
<li>A fine knit, a white shirt and a silk top</li>
<li>One dress that goes from lunch to dinner</li>
<li>Loafers for walking, and one slightly dressier pair</li>
</ul>
<h2>Sunglasses</h2>
<p>The fastest way to look put together after a flight. Choose a shape that suits your face and that you will wear every day rather than a trend frame. Miu Miu is known for sunglasses with a playful, feminine edge; a classic black or tortoiseshell frame is the quiet alternative.</p>
<h2>The cap</h2>
<p>A cap is the travel accessory people forget, and it solves a lot: bad hair after a night train, bright sun in the south, a rainy morning in the city. Keep it plain, in wool, cashmere or cotton, in a neutral that matches your coat. Acne Studios makes caps and beanies in exactly that understated spirit.</p>
<h2>The rule</h2>
<p>If a piece only works with one other piece, leave it at home. Everything in the bag should earn its place twice.</p>
"""
 },
 {
  "slug": "french-lingerie-guide",
  "title": "French Lingerie: The Quiet Art of Dressing Underneath",
  "dek": "Silk, fine lace and the right fit. Why French women treat lingerie as the first layer of a good outfit.",
  "category": "Lingerie",
  "date": "21 October 2026",
  "read": "5 min",
  "tone": "blush",
  "image": {"file": "silk-ivory-wide.jpg", "card": "silk-ivory-card.jpg", "pos": "center",
            "card_pos": "center",
            "alt": "Draped ivory silk satin"},
  "body": """
<p>In France, lingerie is not reserved for special occasions. It is simply the first layer of getting dressed, chosen with the same care as a coat or a pair of shoes. Nobody else needs to see it. That is exactly the point.</p>
<h2>Fit comes first</h2>
<p>Beautiful lingerie that does not fit is never beautiful. Get measured properly, and measure again every year or two, because sizes change. A good fit makes everything you wear over it sit better, from a silk blouse to a fine knit.</p>
<h2>Fabrics worth paying for</h2>
<ul>
<li><strong>Silk.</strong> Soft, breathable and quietly luxurious. A silk camisole works under a blazer as well as on its own.</li>
<li><strong>Fine lace.</strong> Look for lace that lies flat and does not show through clothes.</li>
<li><strong>Cotton and modal.</strong> For everyday comfort, in good quality, they are just as chic.</li>
</ul>
<h2>Colours that work under everything</h2>
<p>Build the basics in shades close to your skin tone, plus black and ivory. Then add one or two sets in a colour you love simply because it makes you feel good.</p>
<h2>Pieces that go beyond underwear</h2>
<p>A silk slip dress, a lace-trimmed camisole or a fine bodysuit can be worn as part of an outfit. Under an oversized blazer, or with a lace hem peeking out beneath a knit, they add softness to tailoring. It is a very Parisian contrast.</p>
<h2>Caring for it</h2>
<ul>
<li>Hand wash in cool water, or use a mesh bag on a delicate cycle.</li>
<li>Never tumble dry silk or lace.</li>
<li>Store bras flat or cup-in-cup so they keep their shape.</li>
</ul>
<p>Treated well, good lingerie lasts for years. In cost-per-wear terms it is one of the best investments in a wardrobe.</p>
"""
 },
 {
  "slug": "three-boots-parisian-wardrobe",
  "title": "The Three Boots Every Parisian Wardrobe Needs",
  "dek": "A flat ankle boot, a knee-high riding boot and one with a heel. Together they cover every autumn and winter day.",
  "category": "Boots",
  "date": "21 October 2026",
  "read": "5 min",
  "tone": "ink",
  "image": {"file": "boots-street-bw-wide.jpg", "card": "boots-street-bw-card.jpg", "pos": "center 60%",
            "card_pos": "center 70%",
            "alt": "Black and white photo of black leather knee-high boots and grey socks on a city pavement"},
  "body": """
<p>Paris is a walking city, and from October to March its women walk in boots. Not dozens of pairs, just three good ones that together cover every occasion.</p>
<h2>1. The flat ankle boot</h2>
<p>A Chelsea or a simple zip ankle boot in black leather or dark brown suede. It is the boot you wear four days a week: with straight jeans, wide trousers, a midi skirt. Choose a slim sole and a clean toe so it looks as good at a dinner as on the street.</p>
<h2>2. The knee-high riding boot</h2>
<p>Flat or with a low heel, in smooth leather that fits the calf well. Worn with a knee-length skirt or a sweater dress, it is the most elegant winter outfit there is. With tucked-in jeans it turns casual and very French.</p>
<h2>3. The boot with a heel</h2>
<p>An ankle boot with a block or slim heel for evenings, offices and anything slightly dressed up. A pointed or almond toe looks sharpest under trousers.</p>
<h2>And for something tougher</h2>
<p>A lace-up combat boot adds edge to a feminine outfit: a silk skirt, a soft knit, chunky boots. Miu Miu and Acne Studios both do versions that balance tough and refined.</p>
<h2>Making them last</h2>
<ul>
<li>Protect new leather and suede with a spray before the first rain.</li>
<li>Use boot shapers or rolled magazines in tall boots so the shaft keeps its shape.</li>
<li>Have a cobbler add protective rubber soles; it can add years.</li>
<li>Let them dry slowly, away from the radiator.</li>
</ul>
<p>Three pairs, looked after well, will see you through many winters. That is the Parisian way of buying shoes.</p>
"""
 }
]

ABOUT = """
<p>Soie et Or means silk and gold. It is the shortest way we know to describe a certain kind of Parisian elegance: soft fabrics, a few precious things, and nothing that shouts.</p>
<p>This site is an edit of quiet luxury. We write about Parisian ready-to-wear, French lingerie, boots, fine jewelry and watches, chic travel, and the art of building a small wardrobe that lasts. We cover labels such as Sandro, IRO, Acne Studios, Marni and Miu Miu, and fine jewelry and watches from houses like Pomellato, Cartier and Chopard, including pre-owned pieces.</p>
<h2>How we choose</h2>
<ul>
<li>We favour quality, fit and longevity over trends.</li>
<li>We recommend pieces we would wear ourselves, and we say so when something is a splurge.</li>
<li>We prefer pieces that work with what you already own.</li>
</ul>
<h2>How we are funded</h2>
<p>Some links on this site are affiliate links. When you buy through them, we may earn a commission from the retailer, at no extra cost to you. Retailers never pay to be featured and never see our articles before they are published. Read our full <a href="/affiliate-disclosure.html">affiliate disclosure</a>.</p>
<h2>Who is behind Soie et Or</h2>
<p>Soie et Or is curated by Philippine, based in Rotterdam, the Netherlands. Every article, edit and pin on this site is chosen and written by her.</p>
"""

CONTACT = """
<p>We are happy to hear from readers, brands and retailers.</p>
<p>Email: <a href="mailto:{email}">{email}</a></p>
<p>We read every message and aim to reply within a few working days. For collaborations, please include a short description of what you have in mind.</p>
<p>Follow Soie et Or on Pinterest: <a href="{pinterest}" rel="noopener">{pinterest_label}</a></p>
"""

DISCLOSURE = """
<p>Soie et Or is a reader-supported editorial site. Some of the links on this site are affiliate links.</p>
<h2>What that means</h2>
<p>When you click an affiliate link and make a purchase, the retailer may pay us a small commission. The price you pay is the same as if you had gone to the retailer directly.</p>
<h2>Who we work with</h2>
<p>We work with affiliate networks such as Awin, and through them with luxury retailers and marketplaces. The list of retailers may change over time.</p>
<h2>Our editorial independence</h2>
<ul>
<li>We choose what to write about and what to recommend.</li>
<li>Retailers do not pay to be featured and do not review our content before publication.</li>
<li>We clearly mark articles and Pinterest pins that contain affiliate links.</li>
<li>Brand names and trademarks belong to their owners. Soie et Or is an independent site and is not affiliated with or endorsed by the brands we write about.</li>
</ul>
<h2>Pinterest</h2>
<p>Pins from Soie et Or may link to retailers through affiliate links. These pins are marked in their description.</p>
<p>Questions? Email <a href="mailto:{email}">{email}</a>.</p>
"""

PRIVACY = """
<p class="meta">Last updated: {updated}</p>
<p>This privacy policy explains what personal data Soie et Or collects when you visit {domain}, why, and what your rights are under the EU General Data Protection Regulation (GDPR).</p>
<h2>Who is responsible</h2>
<p>The data controller is Philippine, publisher of Soie et Or, based in Rotterdam, the Netherlands. Contact: <a href="mailto:{email}">{email}</a>.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Server logs.</strong> Our hosting provider automatically processes technical data such as IP address, browser type and the pages you visit, to deliver the site and keep it secure. Legal basis: legitimate interest.</li>
<li><strong>Emails you send us.</strong> If you contact us, we use your email address and message only to reply. Legal basis: legitimate interest.</li>
<li><strong>Analytics.</strong> We currently do not use analytics or advertising cookies. If that changes, we will update this policy and ask for consent where required.</li>
</ul>
<h2>Affiliate links and cookies</h2>
<p>When you click an affiliate link, you leave our site. The affiliate network (such as Awin) and the retailer may set cookies to record that you came from Soie et Or, so that a commission can be attributed if you buy. Their processing is governed by their own privacy policies. We receive reports of sales and commissions, not your name or contact details.</p>
<h2>Retention</h2>
<p>Emails are kept for as long as needed to handle your message and are deleted after at most two years. Server logs are kept by the hosting provider for a limited period.</p>
<h2>Your rights</h2>
<p>You have the right to access, correct or delete your personal data, to object to processing, and to data portability. Email us to exercise these rights. You also have the right to lodge a complaint with the Dutch Data Protection Authority (Autoriteit Persoonsgegevens).</p>
<h2>Changes</h2>
<p>We may update this policy. The date at the top shows the latest version.</p>
"""

TERMS = """
<p class="meta">Last updated: {updated}</p>
<p>By using {domain} you agree to these terms.</p>
<h2>Content</h2>
<p>The articles on this site are for general information and inspiration. We do our best to keep them accurate, but prices, availability and product details are set by retailers and can change at any time. Always check the retailer's website before you buy.</p>
<h2>No advice</h2>
<p>Nothing on this site is financial or investment advice. Comments about value or resale are general observations.</p>
<h2>Third-party websites</h2>
<p>We link to retailers and other websites that we do not control. We are not responsible for their content, products, prices, delivery or returns. Purchases are made directly with the retailer under its own terms.</p>
<h2>Intellectual property</h2>
<p>The text and design of this site belong to Soie et Or. You may share links and short quotes with credit. Brand names, logos and product images belong to their respective owners.</p>
<h2>Liability</h2>
<p>To the extent permitted by law, Soie et Or is not liable for any loss arising from the use of this site or of linked websites.</p>
<h2>Law</h2>
<p>These terms are governed by Dutch law.</p>
<p>Questions? Email <a href="mailto:{email}">{email}</a>.</p>
"""
