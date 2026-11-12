#!/usr/bin/env python3
"""
Cash4Tech static site generator.

Run:  python3 build.py
Output goes to ./docs, which GitHub Pages serves (Settings > Pages > main /docs).

Everything lives in this one file on purpose: shared header/footer, business facts,
and page content. Edit BUSINESS below to update the phone, address, hours, etc. once
Timothy confirms them, then rebuild.
"""
import json
import os
import shutil
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
SRC = os.path.join(ROOT, "src")

# ---------------------------------------------------------------------------
# Business facts. Anything set to None renders as a visible "needs confirmation" flag.
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Cash4Tech",
    "legal_name": "Cash4Tech, Inc.",
    "tagline": "Turn your tech into cash.",
    "phone": "(816) 579-4440",
    "phone_href": "tel:+18165794440",
    "domain": "https://getcash4tech.com",
    "city": "Gladstone",
    "region": "MO",
    "area": "Kansas City Northland",
    "street": None,          # e.g. "1234 NE Example Rd" — not yet provided
    "postal": None,
    "email": None,           # not yet provided
    "ebay_store": None,      # eBay store URL — not yet provided
    # Planned hours from the brief. HOURS_CONFIRMED stays False until Timothy confirms.
    "hours": [("Monday – Friday", "10 AM – 7 PM"), ("Saturday", "10 AM – 4 PM"), ("Sunday", "10 AM – 4 PM")],
    "hours_confirmed": False,
}

# Demo mode adds the yellow banner, shows ⚑ flags, and keeps search engines out.
DEMO = True
# Timothy's Shopify store. Set to its public URL (e.g. "https://cash4tech.myshopify.com")
# to turn on the "Shop online" buttons. The store is password-protected until he launches it.
SHOPIFY_STORE_URL = None
GTM_ID = None  # e.g. "GTM-XXXXXXX" — add when the tracking stack is confirmed

MAPS_QUERY = "Cash4Tech Gladstone MO"
DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=" + MAPS_QUERY.replace(" ", "+")


def todo(text):
    return f'<span class="todo">{text}</span>' if DEMO else ""


# ---------------------------------------------------------------------------
# Icons (inline SVG, stroke-based, inherit currentColor)
# ---------------------------------------------------------------------------
def icon(name):
    p = {
        "phone": '<rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/>',
        "android": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M6 6h12M6 18h12"/>',
        "tablet": '<rect x="4" y="2" width="16" height="20" rx="2.5"/><path d="M11 18.5h2"/>',
        "laptop": '<rect x="4" y="4" width="16" height="11" rx="1.5"/><path d="M2 19h20l-2-4H4z"/>',
        "desktop": '<rect x="2" y="3" width="20" height="13" rx="1.5"/><path d="M8 21h8M12 16v5"/>',
        "gamepad": '<path d="M6 8h12a4 4 0 0 1 4 4v1a4 4 0 0 1-7 2.6L14 15h-4l-1 .6A4 4 0 0 1 2 13v-1a4 4 0 0 1 4-4z"/><path d="M7 11v3M5.5 12.5h3M16 12h.01M18 13.5h.01"/>',
        "watch": '<rect x="6" y="6" width="12" height="12" rx="3"/><path d="M9 6l1-4h4l1 4M9 18l1 4h4l1-4M12 10v2l1.5 1"/>',
        "chip": '<rect x="6" y="6" width="12" height="12" rx="1.5"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><rect x="9.5" y="9.5" width="5" height="5"/>',
        "plug": '<path d="M9 2v6M15 2v6M6 8h12v3a6 6 0 0 1-12 0zM12 17v5"/>',
        "pin": '<path d="M12 22s7-6.3 7-12a7 7 0 0 0-14 0c0 5.7 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
        "call": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "store": '<path d="M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9h18M9 20v-6h6v6"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "hand": '<path d="M7 11V6a2 2 0 0 1 4 0v4M11 10V4a2 2 0 0 1 4 0v6M15 10V6a2 2 0 0 1 4 0v8a7 7 0 0 1-7 7h-1a7 7 0 0 1-5.6-2.8L3 15a2 2 0 0 1 3-2.6L7 14"/>',
        "check": '<path d="M5 12l5 5L19 7"/>',
        "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
        "people": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0M16 4.5a3.5 3.5 0 0 1 0 7M22 20a7 7 0 0 0-4-6.3"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l2.5 12h12L22 7H6"/>',
    }[name]
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')


HERO_ART = """
<svg viewBox="0 0 360 380" role="img" aria-label="Illustration of a phone, game controller and cash">
  <defs>
    <linearGradient id="scr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5b2a86"/><stop offset="1" stop-color="#1a0d29"/></linearGradient>
    <linearGradient id="cash" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6cc24a"/><stop offset="1" stop-color="#3b7a21"/></linearGradient>
  </defs>
  <g transform="rotate(-8 180 190)">
    <rect x="96" y="30" width="168" height="310" rx="30" fill="#17151f" stroke="#3a3746" stroke-width="3"/>
    <rect x="108" y="44" width="144" height="282" rx="20" fill="url(#scr)"/>
    <rect x="156" y="52" width="48" height="10" rx="5" fill="#0b0b0f"/>
    <text x="180" y="170" text-anchor="middle" font-family="Archivo, Arial Black, sans-serif" font-weight="900" font-size="30" fill="#fff">CA<tspan fill="#6cc24a">$</tspan>H</text>
    <text x="180" y="205" text-anchor="middle" font-family="Archivo, Arial Black, sans-serif" font-weight="900" font-size="30" fill="#fff"><tspan fill="#6cc24a">4</tspan><tspan fill="#c9a0ee">TECH</tspan></text>
    <rect x="132" y="250" width="96" height="30" rx="15" fill="#509e2f"/>
    <text x="180" y="270" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#fff">GET AN OFFER</text>
  </g>
  <g transform="translate(6 236) rotate(-14)">
    <rect width="120" height="64" rx="8" fill="url(#cash)"/>
    <rect x="6" y="6" width="108" height="52" rx="5" fill="none" stroke="#d6f2c8" stroke-width="1.5" opacity=".7"/>
    <circle cx="60" cy="32" r="16" fill="none" stroke="#e8f8df" stroke-width="2"/>
    <text x="60" y="39" text-anchor="middle" font-family="Archivo, Arial Black, sans-serif" font-weight="900" font-size="20" fill="#fff">$</text>
  </g>
  <g transform="translate(236 250) rotate(12)">
    <path d="M22 0h76a22 22 0 0 1 22 22v8a22 22 0 0 1-40 13l-6-7H46l-6 7A22 22 0 0 1 0 30v-8A22 22 0 0 1 22 0z" fill="#2a1240" stroke="#a874d6" stroke-width="2.5"/>
    <path d="M26 14v18M17 23h18" stroke="#6cc24a" stroke-width="4" stroke-linecap="round"/>
    <circle cx="88" cy="17" r="4.5" fill="#a874d6"/><circle cx="99" cy="27" r="4.5" fill="#6cc24a"/>
  </g>
</svg>
"""

LOGO = '<span aria-hidden="true">CA<span class="g">$</span>H<span class="g">4</span><span class="p">TECH</span></span><span class="skip">Cash4Tech home</span>'

# ---------------------------------------------------------------------------
# Categories (Sell Your Tech)
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        "slug": "iphone", "icon": "phone", "name": "iPhone", "plural": "iPhones",
        "card": "Upgrading? Bring in the iPhone you're replacing.",
        "title": "Sell Your iPhone in Gladstone & Kansas City",
        "desc": "Sell your used iPhone in person at Cash4Tech in Gladstone, MO. Bring it in, get an offer, and decide on the spot. No listings, no strangers, no shipping.",
        "intro": "Just upgraded, or have an older iPhone sitting in a drawer? Bring it to Cash4Tech in Gladstone. We'll look it over in person and make you an offer. You decide whether to take it.",
        "factors": ["Model and generation", "Storage capacity", "Carrier and lock status", "Battery health", "Screen and body condition", "Whether everything works: cameras, Face ID / Touch ID, buttons, charging"],
        "prep": ["Back up your photos and data to iCloud or a computer", "Turn off Find My iPhone and sign out of your Apple ID", "Know your passcode in case we need to check the device", "Remove your SIM card"],
    },
    {
        "slug": "samsung", "icon": "android", "name": "Samsung Phone", "plural": "Samsung phones",
        "card": "Galaxy S, Note, Z Fold and Flip, A series and more.",
        "title": "Sell Your Samsung Galaxy Phone in Kansas City",
        "desc": "Sell your Samsung Galaxy phone at Cash4Tech in Gladstone, MO. In-person evaluation and a straightforward offer you can accept or decline.",
        "intro": "Galaxy S, Galaxy Z Fold or Flip, Note, or A series, bring your Samsung to Cash4Tech for an in-person look and an offer. Other Android phones are welcome to ask about too.",
        "factors": ["Model and generation", "Storage capacity", "Carrier and lock status", "Screen condition, including burn-in", "Body and back-glass condition", "Whether cameras, charging and buttons all work"],
        "prep": ["Back up your data to your Samsung or Google account", "Remove your Google account and Samsung account from the phone", "Know your PIN or pattern in case we need to check the device", "Remove your SIM and any memory card"],
    },
    {
        "slug": "ipad", "icon": "tablet", "name": "iPad or Tablet", "plural": "iPads and tablets",
        "card": "iPad, iPad Air, iPad Pro, iPad mini and other tablets.",
        "title": "Sell Your iPad or Tablet in Gladstone, MO",
        "desc": "Sell your iPad or tablet locally at Cash4Tech in Gladstone. Bring it in for an in-person evaluation and an offer.",
        "intro": "iPads and tablets often get replaced long before they wear out. If yours isn't getting used, bring it to Cash4Tech for an offer.",
        "factors": ["Model and generation", "Storage capacity", "Wi-Fi only or cellular", "Screen and body condition", "Battery health", "Included accessories, such as a pencil or keyboard"],
        "prep": ["Back up anything you want to keep", "Turn off Find My iPad and sign out of your Apple ID (or remove your Google account)", "Know your passcode", "Bring accessories you'd like us to consider"],
    },
    {
        "slug": "laptop", "icon": "laptop", "name": "Laptop", "plural": "laptops",
        "card": "MacBooks, Windows laptops and Chromebooks.",
        "title": "Sell Your Laptop or MacBook in Kansas City",
        "desc": "Sell your used MacBook or Windows laptop at Cash4Tech in Gladstone, MO. In-person evaluation and an offer, no online listing required.",
        "intro": "Whether it's a MacBook, a Windows laptop or a Chromebook, bring it to Cash4Tech and we'll take a look. Specs and condition both matter, so bringing the charger helps us test it.",
        "factors": ["Brand, model and year", "Processor, memory (RAM) and storage", "Screen, keyboard and trackpad condition", "Battery health and cycle count", "Whether it powers on, charges and boots normally", "Whether the charger is included"],
        "prep": ["Back up your files", "Sign out of iCloud / Find My Mac, or your Microsoft account", "Bring the charger if you have it", "Know your login password in case we need to check the device"],
    },
    {
        "slug": "gaming-console", "icon": "gamepad", "name": "Gaming Console", "plural": "gaming consoles",
        "card": "PlayStation, Xbox, Nintendo Switch, controllers and accessories.",
        "title": "Sell Your PlayStation, Xbox or Nintendo Switch",
        "desc": "Sell your gaming console and accessories at Cash4Tech in Gladstone, MO. Bring in your PlayStation, Xbox or Nintendo Switch for an offer.",
        "intro": "Moved on to a new system? Bring your PlayStation, Xbox or Nintendo Switch to Cash4Tech. Controllers and accessories are worth bringing along too.",
        "factors": ["Console model and storage", "Whether it powers on and runs normally", "Controllers and cables included", "Cosmetic condition", "Disc drive or dock, where applicable"],
        "prep": ["Sign out of your PlayStation, Xbox or Nintendo account", "Deactivate it as your primary or home console", "Bring the power cable, HDMI cable and controllers", "Remove any game discs or cartridges you want to keep"],
    },
    {
        "slug": "smartwatch", "icon": "watch", "name": "Smartwatch", "plural": "smartwatches",
        "card": "Apple Watch, Galaxy Watch and other wearables.",
        "title": "Sell Your Apple Watch or Smartwatch in Kansas City",
        "desc": "Sell your Apple Watch, Galaxy Watch or other smartwatch at Cash4Tech in Gladstone, MO. In-person evaluation and an offer.",
        "intro": "Apple Watch, Galaxy Watch and other wearables can be worth bringing in. Stop by Cash4Tech and we'll take a look.",
        "factors": ["Model, size and series", "GPS only or cellular", "Case material", "Screen and case condition", "Battery health", "Whether the charger is included"],
        "prep": ["Unpair the watch from your phone. This also removes Activation Lock on Apple Watch", "Back up any health data you want to keep", "Bring the charger if you have it"],
    },
]

OTHER_CATS = [
    ("desktop", "Desktop Computers", "iMacs, Mac minis, towers and all-in-ones."),
    ("chip", "Computer Components", "Graphics cards, processors and other parts."),
    ("plug", "Other Electronics", "Not sure? Call ahead and ask about your item."),
]

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
NAV = [
    ("sell/", "Sell Your Tech"),
    ("how-it-works/", "How It Works"),
    ("shop/", "Shop"),
    ("about/", "About"),
    ("faq/", "FAQ"),
    ("visit/", "Visit Us"),
]


def page_shell(path, title, desc, body, active=None, noindex=False, schema=None):
    depth = path.count("/")
    base = "../" * depth if depth else "./"

    def u(p):
        return base + p

    nav_items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if active == href else ""
        extra = '<span class="soon">Soon</span>' if href == "shop/" else ""
        nav_items.append(f'<li><a href="{u(href)}"{cur}>{label}{extra}</a></li>')

    robots = '<meta name="robots" content="noindex, nofollow">' if (DEMO or noindex) else ""
    canonical = f'<link rel="canonical" href="{BUSINESS["domain"]}/{path}">'
    gtm_head = gtm_body = ""
    if GTM_ID:
        gtm_head = ("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
                    "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
                    "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
                    f"(window,document,'script','dataLayer','{GTM_ID}');</script>")
        gtm_body = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}" height="0" width="0" '
                    'style="display:none;visibility:hidden"></iframe></noscript>')
    else:
        gtm_head = "<!-- Google Tag Manager goes here once GTM_ID is set in build.py -->"

    schema_tag = ""
    if schema:
        schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'

    demo_bar = ""
    if DEMO:
        demo_bar = (f'<div class="demo-bar">Demo preview for Cash4Tech. Items marked <span class="todo">like this</span> '
                    f'need confirmation before launch. <a href="{u("roadmap/")}">See the roadmap</a></div>')

    b = BUSINESS
    addr_line = (f'{b["street"]}<br>{b["city"]}, {b["region"]} {b["postal"]}' if b["street"]
                 else f'{b["city"]}, {b["region"]} &middot; {b["area"]}<br>{todo("Street address")}')

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
{robots}
{canonical}
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b0b0f">
<link rel="icon" href="{u('assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{u('assets/css/site.css')}">
{gtm_head}
{schema_tag}
</head>
<body>
{gtm_body}
<a class="skip" href="#main">Skip to content</a>
{demo_bar}
<header class="site-header">
  <nav class="wrap nav" aria-label="Main">
    <a class="logo" href="{u('')}">{LOGO}</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav-links">Menu</button>
    <ul class="nav-links" id="nav-links">{''.join(nav_items)}</ul>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="{b['phone_href']}" data-track="click_to_call">{icon('call')}Call</a>
      <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">Directions</a>
    </div>
  </nav>
</header>
<main id="main">
{body.replace('{{base}}', base)}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="{u('')}">{LOGO}</a>
        <p class="mt-2">{b['tagline']}</p>
        <p>Independent, locally operated electronics buyer and reseller serving Gladstone and the Kansas City area.</p>
      </div>
      <div>
        <h4>Sell</h4>
        <ul>
          {''.join(f'<li><a href="{u("sell/" + c["slug"] + "/")}">{c["name"]}</a></li>' for c in CATEGORIES)}
          <li><a href="{u('sell/')}">Everything we buy</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{u('how-it-works/')}">How It Works</a></li>
          <li><a href="{u('about/')}">About Us</a></li>
          <li><a href="{u('faq/')}">FAQ</a></li>
          <li><a href="{u('shop/')}">Shop (coming soon)</a></li>
          <li><a href="{u('visit/')}">Visit &amp; Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit</h4>
        <p>{addr_line}</p>
        <p><a href="{b['phone_href']}" data-track="click_to_call">{b['phone']}</a></p>
        <p><a href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">Get directions &rarr;</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> {b['legal_name']} All rights reserved.</span>
      <span>Gladstone, Missouri &middot; Kansas City Northland</span>
    </div>
  </div>
</footer>
<div class="action-bar" aria-label="Quick actions">
  <a class="btn btn-purple" href="{b['phone_href']}" data-track="click_to_call">{icon('call')}Call</a>
  <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Directions</a>
</div>
<script src="{u('assets/js/site.js')}" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Reusable blocks
# ---------------------------------------------------------------------------
def cta_band(heading="Ready to turn your tech into cash?",
             text="Bring your device to our Gladstone store for an in-person offer."):
    return f"""
<section class="section tight">
  <div class="wrap">
    <div class="cta-band">
      <div>
        <h2>{heading}</h2>
        <p>{text}</p>
      </div>
      <div class="btn-row">
        <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Get Directions</a>
        <a class="btn btn-ghost" style="color:#fff" href="{BUSINESS['phone_href']}" data-track="click_to_call">{icon('call')}{BUSINESS['phone']}</a>
      </div>
    </div>
  </div>
</section>"""


def steps_block(dark=True):
    cls = "section dark" if dark else "section"
    return f"""
<section class="{cls}" id="how">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">How it works</span>
      <h2>Three simple steps. No listings, no strangers.</h2>
      <p class="lede">Skip the marketplace hassle. Bring your device in, get an offer, and you decide.</p>
    </div>
    <div class="grid grid-3 steps">
      <div class="step"><h3>Bring in your tech</h3><p>Stop by our Gladstone store with the electronics you want to sell.</p></div>
      <div class="step"><h3>Get an offer</h3><p>We look over the device's model, specs, condition and how well it works, then make you an offer.</p></div>
      <div class="step"><h3>Get paid</h3><p>Like the offer? Accept it and we complete the purchase. Not for you? You're free to decline.</p></div>
    </div>
  </div>
</section>"""


def category_cards(base_prefix="{{base}}"):
    cards = []
    for c in CATEGORIES:
        cards.append(f"""
      <a class="card cat-card" href="{base_prefix}sell/{c['slug']}/">
        <span class="icon">{icon(c['icon'])}</span>
        <h3>{c['name']}</h3>
        <p>{c['card']}</p>
        <span class="more">Learn more &rarr;</span>
      </a>""")
    for ic, name, text in OTHER_CATS:
        cards.append(f"""
      <div class="card cat-card">
        <span class="icon">{icon(ic)}</span>
        <h3>{name}</h3>
        <p>{text}</p>
      </div>""")
    return "".join(cards)


def hours_table():
    rows = "".join(f"<tr><td>{d}</td><td>{h}</td></tr>" for d, h in BUSINESS["hours"])
    note = "" if BUSINESS["hours_confirmed"] else f'<p class="mt-2 mb-0">{todo("Planned hours. Confirm hours and opening date before launch.")}</p>'
    return f'<table class="hours">{rows}</table>{note}'


def local_business_schema():
    b = BUSINESS
    addr = {"@type": "PostalAddress", "addressLocality": b["city"], "addressRegion": b["region"], "addressCountry": "US"}
    if b["street"]:
        addr["streetAddress"] = b["street"]
    if b["postal"]:
        addr["postalCode"] = b["postal"]
    data = {
        "@context": "https://schema.org",
        "@type": "ElectronicsStore",
        "name": b["name"],
        "legalName": b["legal_name"],
        "slogan": b["tagline"],
        "url": b["domain"],
        "telephone": "+1-816-579-4440",
        "address": addr,
        "areaServed": ["Gladstone, MO", "Kansas City Northland", "Kansas City metropolitan area"],
        "description": "Independent, locally operated business that buys used consumer electronics in person and resells them online.",
    }
    # Opening hours are added only after they're confirmed.
    if b["hours_confirmed"]:
        data["openingHours"] = ["Mo-Fr 10:00-19:00", "Sa 10:00-16:00", "Su 10:00-16:00"]
    return data


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Gladstone, MO &middot; Kansas City Northland</span>
      <h1>Turn your tech <span class="g">into cash.</span></h1>
      <p class="lede">Got electronics you no longer use? Bring them to Cash4Tech in Gladstone for an offer. Sell your phones, tablets, gaming consoles and more without the hassle of selling online.</p>
      <div class="btn-row">
        <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Get Directions</a>
        <a class="btn btn-ghost" href="{{{{base}}}}sell/">What We Buy</a>
        <a class="btn btn-ghost" href="{{{{base}}}}visit/#contact">Contact Us</a>
      </div>
      <div class="hero-meta">
        <span>{icon('store')}Real local store</span>
        <span>{icon('hand')}In-person offers</span>
        <span>{icon('check')}You decide</span>
      </div>
    </div>
    <div class="hero-art">{HERO_ART}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What we buy</span>
      <h2>Phones, tablets, laptops, consoles and more</h2>
      <p class="lede">Bring in the electronics you're not using. What we can accept and what we offer depend on the model, condition, specs and demand.</p>
    </div>
    <div class="grid grid-3">{category_cards()}</div>
  </div>
</section>

{steps_block()}

<section class="section">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Why Cash4Tech</span>
      <h2>Easier than selling it yourself</h2>
      <p class="lede">Selling online means photos, listings, haggling, no-shows, meetups with strangers and shipping. We handle all that for you.</p>
    </div>
    <div class="table-scroll">
      <table class="compare">
        <thead><tr><th></th><th>Cash4Tech</th><th>Selling it yourself online</th></tr></thead>
        <tbody>
          <tr><th>Listing</th><td>None. Just walk in</td><td>Photos, descriptions, pricing research</td></tr>
          <tr><th>Buyers</th><td>A local business</td><td>Strangers, lowball offers, no-shows</td></tr>
          <tr><th>Meetups</th><td>Our store, during business hours</td><td>Parking lots and driveways</td></tr>
          <tr><th>Shipping</th><td>None</td><td>Packing, labels, return risk</td></tr>
          <tr><th>Waiting</th><td>An offer while you're here</td><td>Days or weeks for a buyer</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Why people choose us</span>
      <h2>A local business you can talk to</h2>
    </div>
    <div class="grid grid-4">
      <div class="card"><span class="feat-icon">{icon('store')}</span><h3>Convenient</h3><p>A physical store in Gladstone, minutes from across the Northland.</p></div>
      <div class="card"><span class="feat-icon">{icon('spark')}</span><h3>Simple</h3><p>Bring it in, get an offer, decide. No accounts or listings.</p></div>
      <div class="card"><span class="feat-icon">{icon('people')}</span><h3>Personal</h3><p>Talk to real people at a local business, face to face.</p></div>
      <div class="card"><span class="feat-icon">{icon('shield')}</span><h3>Professional</h3><p>Devices are evaluated using an organized purchasing and testing process.</p></div>
    </div>
    <div class="todo-block mt-3"><strong>Reviews go here.</strong> Once real Google reviews come in, we can show them in this spot. We won't add any testimonials that aren't genuine.</div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Visit the store</span>
      <h2>Come see us in Gladstone</h2>
      <ul class="info-list">
        <li>{icon('pin')}<div><strong>Location</strong>Gladstone, MO, serving the Kansas City Northland and metro<br>{todo('Street address')}</div></li>
        <li>{icon('call')}<div><strong>Phone</strong><a href="{BUSINESS['phone_href']}" data-track="click_to_call">{BUSINESS['phone']}</a></div></li>
        <li>{icon('clock')}<div style="flex:1"><strong>Hours</strong>{hours_table()}</div></li>
      </ul>
      <div class="btn-row mt-2">
        <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Get Directions</a>
        <a class="btn btn-purple" href="{BUSINESS['phone_href']}" data-track="click_to_call">{icon('call')}Call the Store</a>
      </div>
    </div>
    <div class="map-box">
      <div>
        <p><strong>Map goes here</strong></p>
        <p class="muted">An embedded Google Map appears once the store address is confirmed.</p>
        {todo('Store address + photos of the storefront')}
      </div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Shopping for tech?</span>
      <h2>Tested, pre-owned electronics</h2>
      <p class="lede">The devices we buy are tested, graded and resold online. Shopping directly on this site is planned for the future.</p>
    </div>
    <div class="btn-row" style="align-self:center">
      <a class="btn btn-green" href="{{{{base}}}}shop/">{icon('cart')}Preview the Shop</a>
      {('<a class="btn btn-ghost" href="' + BUSINESS['ebay_store'] + '">Shop on eBay</a>') if BUSINESS['ebay_store'] else todo('eBay store link')}
    </div>
  </div>
</section>

{cta_band()}
"""
    return page_shell("", "Sell Your Phone, Tablet & Electronics for Cash | Cash4Tech Gladstone, MO",
                      "Sell used phones, iPads, laptops, gaming consoles and more at Cash4Tech in Gladstone, MO. Bring your tech in for an in-person offer. Serving the Kansas City Northland.",
                      body, schema=local_business_schema())


def page_hero(title, lede, crumbs=None, eyebrow=None):
    cr = ""
    if crumbs:
        cr = '<div class="crumbs">' + " / ".join(f'<a href="{h}">{t}</a>' if h else t for t, h in crumbs) + "</div>"
    eb = f'<span class="eyebrow">{eyebrow}</span>' if eyebrow else ""
    return f"""
<section class="hero page-hero">
  <div class="wrap">
    {cr}{eb}
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>"""


def sell_index():
    body = page_hero("What we buy",
                     "Phones, tablets, laptops, desktops, gaming consoles, smartwatches, components and more. Bring them in for an in-person offer.",
                     eyebrow="Sell your tech") + f"""
<section class="section">
  <div class="wrap">
    <div class="grid grid-3">{category_cards()}</div>
    <div class="card mt-3">
      <h3>What affects your offer</h3>
      <p>Every device is evaluated in person. Whether we can buy an item and what we offer depend on:</p>
      <div class="grid grid-3">
        <ul class="checklist"><li>Model and age</li><li>Specs and storage</li></ul>
        <ul class="checklist"><li>Physical condition</li><li>Whether everything works</li></ul>
        <ul class="checklist"><li>Current resale demand</li><li>Accessories included</li></ul>
      </div>
      <p class="muted mt-2 mb-0">We can't accept every device, and offers aren't set in advance. If you're unsure about an item, give us a call at <a href="{BUSINESS['phone_href']}" data-track="click_to_call">{BUSINESS['phone']}</a>.</p>
    </div>
  </div>
</section>
{steps_block()}
{cta_band()}
"""
    return page_shell("sell/", "What We Buy | Sell Used Electronics in Kansas City | Cash4Tech",
                      "Cash4Tech buys used phones, tablets, laptops, desktops, gaming consoles, smartwatches and more at our Gladstone, MO store.",
                      body, active="sell/")


def category_page(c):
    others = "".join(f'<li><a href="{{{{base}}}}sell/{o["slug"]}/">Sell your {o["name"]}</a></li>' for o in CATEGORIES if o is not c)
    factors = "".join(f"<li>{f}</li>" for f in c["factors"])
    prep = "".join(f"<li>{p}</li>" for p in c["prep"])
    body = page_hero(f"Sell your {c['name']}", c["intro"],
                     crumbs=[("Home", "{{base}}"), ("Sell Your Tech", "{{base}}sell/"), (c["name"], None)]) + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <h2>What we look at</h2>
      <p>Every {c['name'].lower()} is evaluated in person. Things that can affect your offer include:</p>
      <ul class="checklist">{factors}</ul>
      <p class="muted">Not every device can be accepted, and offers depend on condition and current demand. Call ahead if you'd like to ask about yours.</p>
    </div>
    <div class="card">
      <h2>Before you come in</h2>
      <p>A little prep makes the visit faster:</p>
      <ul class="checklist">{prep}</ul>
      <p class="muted mb-0">This is general guidance for getting a device ready. Ask us in store if you need a hand.</p>
    </div>
  </div>
</section>
<section class="section alt tight">
  <div class="wrap">
    <div class="grid grid-3">
      <div class="card"><h3>1. Bring it in</h3><p>Visit our Gladstone store with your {c['name'].lower()}.</p></div>
      <div class="card"><h3>2. Get an offer</h3><p>We check it over and make you an offer.</p></div>
      <div class="card"><h3>3. You decide</h3><p>Accept and get paid, or decline. It's your call.</p></div>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap">
    <h3>Selling something else?</h3>
    <ul>{others}<li><a href="{{{{base}}}}sell/">See everything we buy</a></li></ul>
  </div>
</section>
{cta_band(f"Bring your {c['name'].lower()} to Cash4Tech")}
"""
    return page_shell(f"sell/{c['slug']}/", c["title"] + " | Cash4Tech", c["desc"], body, active="sell/")


def how_it_works():
    body = page_hero("How selling works",
                     "No listings, no haggling with strangers, no shipping. Bring your device in, get an offer, and decide.",
                     eyebrow="How it works") + steps_block(dark=False) + f"""
<section class="section alt">
  <div class="wrap split">
    <div>
      <h2>What happens in the store</h2>
      <p>When you arrive, a team member takes a look at your device. We consider its specs, physical condition, how well it works and its resale value, then make you an offer.</p>
      <p>There's no obligation. If the offer works for you and the sale meets our purchasing requirements, we complete the purchase and pay you. If not, you take your device home.</p>
      <p>{todo('Payment methods, ID requirements and typical visit length. Confirm before listing them here.')}</p>
    </div>
    <div class="card">
      <h3>Why not just sell it online?</h3>
      <ul class="checklist">
        <li>No creating listings or taking photos</li>
        <li>No negotiating with strangers</li>
        <li>No arranging meetups</li>
        <li>No packing and shipping</li>
        <li>No waiting days or weeks for a buyer</li>
      </ul>
    </div>
  </div>
</section>
{cta_band()}
"""
    return page_shell("how-it-works/", "How It Works | Sell Your Electronics In Person | Cash4Tech",
                      "Selling your electronics at Cash4Tech is simple: bring your device to our Gladstone store, get an offer, and decide. No listings or shipping.",
                      body, active="how-it-works/")


def about():
    body = page_hero("About Cash4Tech",
                     "An independent, locally operated electronics buyer and reseller in Gladstone, Missouri, serving the Kansas City area.",
                     eyebrow="About us") + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <h2>Local and independent</h2>
      <p>Cash4Tech buys used consumer electronics directly from people in Gladstone, the Northland and across the Kansas City metro. Our store gives you a professional, comfortable place to sell your tech in person, without the hassle of selling online.</p>
      <p>The devices we buy are tested, graded and carefully inventoried, then resold to new owners through online marketplaces. That keeps good electronics in use and out of drawers.</p>
      <p>{todo('Founder story, team photo and when the store opened')}</p>
    </div>
    <div class="grid">
      <div class="card"><h3>We buy</h3><p>Used phones, tablets, laptops, desktops, gaming consoles, smartwatches and components, evaluated in person at our store.</p></div>
      <div class="card"><h3>We resell</h3><p>Tested, pre-owned electronics sold through online marketplaces, with our own online shop planned.</p></div>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><h2>What we stand for</h2></div>
    <div class="grid grid-4">
      <div class="card"><h3>Convenience</h3><p>A real store you can walk into.</p></div>
      <div class="card"><h3>Simplicity</h3><p>A process that's easy to understand.</p></div>
      <div class="card"><h3>Transparency</h3><p>We explain what goes into an offer.</p></div>
      <div class="card"><h3>Your choice</h3><p>Accept or decline. No pressure.</p></div>
    </div>
    <div class="todo-block mt-3"><strong>Store photos.</strong> The storefront and the purple-and-black interior would make great photos for this page and the home page.</div>
  </div>
</section>
{cta_band()}
"""
    return page_shell("about/", "About Cash4Tech | Local Electronics Buyer in Gladstone, MO",
                      "Cash4Tech is an independent, locally operated electronics purchasing and resale business in Gladstone, Missouri, serving the Kansas City area.",
                      body, active="about/")


def visit():
    b = BUSINESS
    body = page_hero("Visit &amp; contact",
                     "Stop by our Gladstone store or give us a call. We're happy to answer questions about your device before you come in.",
                     eyebrow="Visit us") + f"""
<section class="section">
  <div class="wrap split">
    <div>
      <ul class="info-list">
        <li>{icon('pin')}<div><strong>Address</strong>{b['street'] or todo('Street address')}<br>{b['city']}, {b['region']} {b['postal'] or ''}<br><a href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">Get driving directions &rarr;</a></div></li>
        <li>{icon('call')}<div><strong>Phone</strong><a href="{b['phone_href']}" data-track="click_to_call">{b['phone']}</a></div></li>
        <li>{icon('mail')}<div><strong>Email</strong>{('<a href="mailto:' + b['email'] + '">' + b['email'] + '</a>') if b['email'] else todo('Email address')}</div></li>
        <li>{icon('clock')}<div style="flex:1"><strong>Hours</strong>{hours_table()}</div></li>
      </ul>
    </div>
    <div class="map-box">
      <div>
        <p><strong>Map</strong></p>
        <p class="muted">A Google Map embed goes here once the address is confirmed and the Google Business Profile is live.</p>
        <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Open in Google Maps</a>
      </div>
    </div>
  </div>
</section>
<section class="section alt" id="contact">
  <div class="wrap split">
    <div>
      <span class="eyebrow">Contact us</span>
      <h2>Have a question?</h2>
      <p class="lede">Ask about a device before you come in, or anything else. For the fastest answer, call the store.</p>
      <p><a class="btn btn-purple" href="{b['phone_href']}" data-track="click_to_call">{icon('call')}{b['phone']}</a></p>
    </div>
    <form class="card form" id="contact-form" novalidate>
      <div><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></div>
      <div><label for="f-phone">Phone or email</label><input id="f-phone" name="contact" autocomplete="email" required></div>
      <div><label for="f-type">What's it about?</label>
        <select id="f-type" name="topic"><option>Selling a device</option><option>Buying a device</option><option>Something else</option></select></div>
      <div><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="4" placeholder="e.g. iPhone 14 Pro, 256 GB, cracked back glass"></textarea></div>
      <button class="btn btn-green" type="submit">Send message</button>
      <p class="form-note">Please don't include passwords, passcodes or account details.</p>
      <div class="todo-block form-status" id="form-status" role="status"><strong>Demo form.</strong> This isn't connected yet, so nothing was sent. Before launch it gets wired to an email inbox with spam protection.</div>
    </form>
  </div>
</section>
"""
    return page_shell("visit/", "Visit Cash4Tech | Store Location, Hours & Directions | Gladstone, MO",
                      "Find Cash4Tech in Gladstone, MO. Get directions, call (816) 579-4440, or send us a question about selling your electronics.",
                      body, active="visit/", schema=local_business_schema())


FAQS = [
    ("What electronics does Cash4Tech buy?",
     "We buy a range of used consumer electronics, including smartphones (iPhone and Android), tablets and iPads, laptops, desktop computers, gaming consoles and accessories, smartwatches, and computer components. "
     "We can't accept every device. Eligibility depends on the model, condition and demand. See <a href=\"{{base}}sell/\">what we buy</a> or call to ask about your item.", False),
    ("How are offers determined?",
     "Each device is evaluated in person. Offers are based on the model, specifications, physical condition, how well it works, its age and current resale demand. Prices aren't set in advance.", False),
    ("Can I decline an offer?",
     "Yes. You're always free to accept or decline. If you decline, you take your device home.", False),
    ("What should I do before selling my phone?",
     "Back up your data, sign out of your accounts (turn off Find My iPhone or remove your Google account), know your passcode, and remove your SIM card. Each <a href=\"{{base}}sell/\">device page</a> has specific tips.", False),
    ("How should I prepare my electronics for sale?",
     "Back up anything you want to keep, sign out of accounts tied to the device, and bring chargers, controllers or accessories you'd like us to consider.", False),
    ("Do I need identification to sell?", None, True),
    ("Do you buy damaged electronics?", None, True),
    ("Can I sell a carrier-locked or financed phone?", None, True),
    ("How will I be paid?", None, True),
    ("Can I get a quote online or by phone?", None, True),
]


def faq():
    items = []
    for q, a, pending in FAQS:
        if pending:
            a = todo("Answer depends on Cash4Tech policy. Timothy to confirm before launch.")
        items.append(f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>')
    # Only answered questions go into FAQ schema.
    schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("{{base}}", "/")}}
                       for q, a, pending in FAQS if not pending],
    }
    body = page_hero("Frequently asked questions",
                     "Answers about selling your electronics at Cash4Tech. Don't see your question? Give us a call.",
                     eyebrow="FAQ") + f"""
<section class="section">
  <div class="wrap narrow faq">
    {''.join(items)}
  </div>
</section>
{cta_band("Still have a question?", "Call us and we'll help you figure out whether your device is a fit.")}
"""
    return page_shell("faq/", "FAQ | Selling Electronics at Cash4Tech | Gladstone, MO",
                      "Common questions about selling your phone, tablet, laptop or game console at Cash4Tech in Gladstone, MO.",
                      body, active="faq/", schema=schema)


SAMPLE_PRODUCTS = [
    ("phone", "phones", "iPhone 13 — 128 GB", ["Unlocked", "Battery 89%", "Grade A"], "Sample", ["eBay", "Website"]),
    ("phone", "phones", "iPhone 13 — 128 GB", ["Verizon", "Battery 84%", "Grade B"], "Sample", ["eBay"]),
    ("android", "phones", "Galaxy S22 — 256 GB", ["Unlocked", "Battery 91%", "Grade A"], "Sample", ["eBay", "Website"]),
    ("laptop", "computers", "MacBook Air M1 — 8 GB / 256 GB", ["Cycle count 212", "Grade A-"], "Sample", ["eBay", "Website"]),
    ("gamepad", "gaming", "PlayStation 5 Disc Edition", ["1 controller", "Tested", "Grade B+"], "Sample", ["Website"]),
    ("tablet", "tablets", "iPad Air (5th gen) — 64 GB", ["Wi-Fi", "Battery 93%", "Grade A"], "Sample", ["eBay", "Website"]),
]


def shopify_button(label="Shop our online store"):
    if SHOPIFY_STORE_URL:
        return f'<a class="btn btn-green" href="{SHOPIFY_STORE_URL}" target="_blank" rel="noopener" data-track="shop_click">{icon("cart")}{label}</a>'
    return todo("Shopify store link (Todd to send)")


def shop():
    cards = []
    for ic, cat, name, specs, price, channels in SAMPLE_PRODUCTS:
        spec_html = "".join(f"<span>{s}</span>" for s in specs)
        cards.append(f"""
      <article class="card product" data-cat="{cat}">
        <div class="ph">{icon(ic)}<span class="badge badge-gray">Sample listing</span></div>
        <div class="body">
          <h3>{name}</h3>
          <div class="specs">{spec_html}</div>
          <div class="channels">Listed on: {', '.join(channels)}</div>
          <div class="price">$&nbsp;—</div>
        </div>
      </article>""")
    body = page_hero("Shop tested, pre-owned tech",
                     "Our online shop is on the way. Here's an early look at how it will work.",
                     eyebrow="Coming soon") + f"""
<section class="section">
  <div class="wrap">
    <div class="todo-block" style="margin-bottom:28px"><strong>Preview only.</strong> These are sample cards to show the layout. They aren't real inventory or prices. Online checkout runs through Cash4Tech's Shopify store, which is set up but hasn't launched yet.</div>
    <div class="filters" role="group" aria-label="Filter by category">
      <button data-filter="all" aria-pressed="true">All</button>
      <button data-filter="phones" aria-pressed="false">Phones</button>
      <button data-filter="tablets" aria-pressed="false">Tablets</button>
      <button data-filter="computers" aria-pressed="false">Computers</button>
      <button data-filter="gaming" aria-pressed="false">Gaming</button>
    </div>
    <div class="grid grid-3">{''.join(cards)}</div>
  </div>
</section>
<section class="section alt">
  <div class="wrap split">
    <div>
      <h2>Every device is one of a kind</h2>
      <p>Used electronics aren't identical. Two iPhone 13s can differ in storage, carrier, battery health and cosmetic condition. So each listing would show the actual device: its own photos, specs, test results and condition grade.</p>
      <p>Listings would come straight from Cash4Tech's Shopify inventory. When a device sells anywhere, on eBay, here or another marketplace, it's marked unavailable everywhere else so it's never sold twice.</p>
    </div>
    <div class="card">
      <h3>Planned shop features</h3>
      <ul class="checklist">
        <li>Search, categories and filters</li>
        <li>Real photos of each device</li>
        <li>Specs, condition and test results</li>
        <li>Secure checkout through a payment provider</li>
        <li>Shipping or local pickup in Gladstone</li>
        <li>Order confirmation and tracking</li>
      </ul>
    </div>
  </div>
</section>
<section class="section dark tight">
  <div class="wrap center">
    <h2>Shopping today?</h2>
    <p class="lede" style="margin:0 auto 20px">Cash4Tech currently sells tested electronics on eBay{', and has an online store on Shopify' if SHOPIFY_STORE_URL else ''}.</p>
    <div class="btn-row" style="justify-content:center">
    {shopify_button()}
    {('<a class="btn btn-ghost" href="' + BUSINESS['ebay_store'] + '">Shop our eBay store</a>') if BUSINESS['ebay_store'] else todo('eBay store link')}
    </div>
  </div>
</section>
"""
    return page_shell("shop/", "Shop Pre-Owned Electronics (Coming Soon) | Cash4Tech",
                      "Cash4Tech's online shop for tested, pre-owned electronics is coming soon.",
                      body, active="shop/")


ARCH_SVG = """
<svg class="arch" viewBox="0 0 900 430" role="img" aria-label="Architecture: Shopify inventory feeds a channel sync layer, which publishes to eBay, the Cash4Tech website and other marketplaces, and receives orders back">
  <defs>
    <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5d5d6b"/></marker>
  </defs>
  <style>
    .t{font:700 15px Inter,sans-serif;fill:#fff}
    .s{font:500 12px Inter,sans-serif;fill:#e7e2f0}
    .td{font:700 14px Inter,sans-serif;fill:#1b1b22}
    .sd{font:500 11.5px Inter,sans-serif;fill:#5d5d6b}
    .lbl{font:600 11px Inter,sans-serif;fill:#5d5d6b}
  </style>
  <!-- Store -->
  <rect x="20" y="40" width="190" height="110" rx="14" fill="#509e2f"/>
  <text x="115" y="84" text-anchor="middle" class="t">Gladstone store</text>
  <text x="115" y="106" text-anchor="middle" class="s">Buys devices in person</text>
  <text x="115" y="124" text-anchor="middle" class="s">Test · grade · photo</text>
  <!-- ERP -->
  <rect x="20" y="230" width="190" height="150" rx="14" fill="#2a1240"/>
  <text x="115" y="272" text-anchor="middle" class="t">Shopify (inventory)</text>
  <text x="115" y="296" text-anchor="middle" class="s">Source of truth for</text>
  <text x="115" y="314" text-anchor="middle" class="s">every device record:</text>
  <text x="115" y="334" text-anchor="middle" class="s">IMEI, specs, condition,</text>
  <text x="115" y="352" text-anchor="middle" class="s">cost, price, status</text>
  <path d="M115 152 V226" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)"/>
  <text x="124" y="194" class="lbl">new inventory record</text>
  <!-- Integration -->
  <rect x="320" y="150" width="230" height="150" rx="14" fill="#5b2a86"/>
  <text x="435" y="190" text-anchor="middle" class="t">Channel sync</text>
  <text x="435" y="214" text-anchor="middle" class="s">Publishes listings</text>
  <text x="435" y="232" text-anchor="middle" class="s">Imports orders</text>
  <text x="435" y="250" text-anchor="middle" class="s">Reserves &amp; syncs stock</text>
  <text x="435" y="268" text-anchor="middle" class="s">Retries &amp; reconciles</text>
  <path d="M212 300 C 260 300, 270 250, 316 240" fill="none" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)" marker-start="url(#ah)"/>
  <!-- Channels -->
  <rect x="660" y="30" width="220" height="70" rx="12" fill="#fff" stroke="#509e2f" stroke-width="2.5"/>
  <text x="770" y="60" text-anchor="middle" class="td">eBay</text>
  <text x="770" y="80" text-anchor="middle" class="sd">Live today</text>
  <rect x="660" y="120" width="220" height="70" rx="12" fill="#fff" stroke="#5b2a86" stroke-width="2.5" stroke-dasharray="6 5"/>
  <text x="770" y="150" text-anchor="middle" class="td">getcash4tech.com shop</text>
  <text x="770" y="170" text-anchor="middle" class="sd">Shopify Online Store · launching</text>
  <rect x="660" y="210" width="220" height="70" rx="12" fill="#fff" stroke="#9d99ad" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="770" y="240" text-anchor="middle" class="td">Amazon · Walmart</text>
  <text x="770" y="260" text-anchor="middle" class="sd">Under consideration</text>
  <rect x="660" y="300" width="220" height="70" rx="12" fill="#fff" stroke="#9d99ad" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="770" y="330" text-anchor="middle" class="td">Other marketplaces</text>
  <text x="770" y="350" text-anchor="middle" class="sd">As approved</text>
  <g stroke="#5d5d6b" stroke-width="2" fill="none">
    <path d="M552 200 C 600 200, 610 65, 656 65" marker-end="url(#ah)" marker-start="url(#ah)"/>
    <path d="M552 215 C 600 215, 610 155, 656 155" marker-end="url(#ah)" marker-start="url(#ah)"/>
    <path d="M552 240 C 600 240, 610 245, 656 245" marker-end="url(#ah)" marker-start="url(#ah)"/>
    <path d="M552 260 C 600 260, 610 335, 656 335" marker-end="url(#ah)" marker-start="url(#ah)"/>
  </g>
  <text x="330" y="136" class="lbl">listings, price, availability →</text>
  <text x="560" y="410" class="lbl">← orders, cancellations, returns, tracking</text>
</svg>
"""


def roadmap():
    body = page_hero("Where this site is headed",
                     "A one-page view of the plan from Timothy's brief: what this demo covers today, and how the site grows into online sales across every channel.",
                     eyebrow="Project roadmap · for Cash4Tech") + f"""
<section class="section">
  <div class="wrap">
    <div class="status-key">
      <span class="badge badge-green">In this demo</span>
      <span class="badge badge-purple">Planned</span>
      <span class="badge badge-gray">Needs a decision</span>
    </div>

    <div class="phase now">
      <h3>Phase 1 · Customer acquisition website <span class="badge badge-green">In this demo</span></h3>
      <p>Get local sellers through the door. This demo includes the home page, What We Buy plus six device pages, How It Works, About, Visit &amp; Contact, and FAQ. It also has click-to-call and directions buttons on every page, a sticky call/directions bar on phones, LocalBusiness and FAQ structured data, search-friendly URLs and page titles, and tracking hooks ready for Google Tag Manager.</p>
      <p class="mb-0"><strong>To launch:</strong> confirm address, hours and policies (every ⚑ on the site), add store photos, connect the contact form, set up Google Analytics 4 / Tag Manager, point getcash4tech.com here, and submit to Google Search Console and Google Business Profile.</p>
    </div>

    <div class="phase next">
      <h3>Phase 2 · Marketing optimization <span class="badge badge-purple">Planned</span></h3>
      <p class="mb-0">Ad landing pages for searches like "sell iPhone Kansas City" and "sell phone Gladstone MO", Google Ads conversion tracking for calls and directions, remarketing with a consent notice, real Google reviews on the site, and improvements based on actual visitor behavior.</p>
    </div>

    <div class="phase next">
      <h3>Phase 3 · E-commerce integration <span class="badge badge-purple">Planned</span> <span class="badge badge-gray">Store set up · not launched</span></h3>
      <p class="mb-0">The <a href="{{{{base}}}}shop/">Shop</a> section already has a place in the navigation and a layout preview. When it goes live, Shopify is the inventory source of truth: every device bought in store becomes a one-of-a-kind Shopify product with its own photos, condition and test results, and Shopify handles checkout and payments. The site's Shop buttons already link to the Shopify store.</p>
    </div>

    <div class="phase">
      <h3>Phase 4 · Multichannel optimization <span class="badge badge-purple">Planned</span></h3>
      <p class="mb-0">One inventory, many storefronts. A device listed on eBay, the website and other marketplaces sells once, and every other listing comes down automatically. This phase adds reservations, retries, reconciliation and alerts for failed syncs.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      <h2>How the pieces fit</h2>
      <p class="lede">Shopify is the single source of truth for inventory. Each device is listed once there and pushed out to every channel, so when it sells anywhere, it comes down everywhere else.</p>
    </div>
    <div class="arch-wrap">{ARCH_SVG}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>What we need from Timothy</h2><p class="lede">Only what blocks Phase 1 launch.</p></div>
    <div class="grid grid-2">
      <div class="card"><h3>Store details</h3><ul class="checklist"><li>Street address</li><li>Confirmed hours and opening date</li><li>Contact email</li><li>eBay store link</li></ul></div>
      <div class="card"><h3>Policies for the FAQ</h3><ul class="checklist"><li>ID requirements</li><li>Damaged and carrier-locked devices</li><li>How sellers are paid</li><li>Quotes by phone?</li></ul></div>
      <div class="card"><h3>Photos</h3><ul class="checklist"><li>Storefront and signage</li><li>Inside the store</li><li>Exact brand colors (hex codes, if the sign shop has them)</li></ul></div>
      <div class="card"><h3>Accounts</h3><ul class="checklist"><li>Access to the getcash4tech.com domain</li><li>Google Business Profile</li><li>Google Analytics / Tag Manager</li></ul></div>
    </div>
  </div>
</section>
"""
    return page_shell("roadmap/", "Cash4Tech Website Roadmap",
                      "Phased plan for getcash4tech.com: local customer acquisition first, then marketing, e-commerce and multichannel inventory sync.",
                      body, noindex=True)


def not_found():
    body = page_hero("Page not found", "Sorry, that page doesn't exist.") + """
<section class="section"><div class="wrap"><a class="btn btn-green" href="{{base}}">Back to home</a></div></section>"""
    return page_shell("404.html", "Page not found | Cash4Tech", "Page not found.", body, noindex=True)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def write(rel, html):
    path = os.path.join(OUT, rel)
    if rel.endswith("/") or rel == "":
        path = os.path.join(path, "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))

    pages = {
        "": home(),
        "sell/": sell_index(),
        "how-it-works/": how_it_works(),
        "about/": about(),
        "visit/": visit(),
        "faq/": faq(),
        "shop/": shop(),
        "roadmap/": roadmap(),
    }
    for c in CATEGORIES:
        pages[f"sell/{c['slug']}/"] = category_page(c)
    for rel, html in pages.items():
        write(rel, html)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        # 404 is served from any depth on GitHub Pages, so it uses absolute-from-site links via <base>.
        f.write(not_found())

    # robots + sitemap
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\nSitemap: {BUSINESS['domain']}/sitemap.xml\n")
    urls = [p for p in pages if p != "roadmap/"]
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in urls:
            f.write(f"  <url><loc>{BUSINESS['domain']}/{p}</loc></url>\n")
        f.write("</urlset>\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"Built {len(pages) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
