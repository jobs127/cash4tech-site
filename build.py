#!/usr/bin/env python3
"""
Cash4Tech static site generator.

    python3 build.py

Reads content.py and writes every page into ./docs, which GitHub Pages serves
(Settings > Pages > Branch: main, folder: /docs). Edit content.py, not the HTML.
"""
import json
import os
import shutil
from html import escape

from content import (BUSINESS, SHOPIFY, DEMO, GTM_ID, TAXONOMY, GENERIC_FACTORS, GENERIC_PREP,
                     SELL_FAQS, BUY_FAQS)

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
SRC = os.path.join(ROOT, "src")

MAPS_QUERY = "Cash4Tech Gladstone MO"
DIRECTIONS_URL = "https://www.google.com/maps/dir/?api=1&destination=" + MAPS_QUERY.replace(" ", "+")
SHOP_LIVE = bool(SHOPIFY["domain"] and SHOPIFY["storefront_token"])


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
    <text x="180" y="170" text-anchor="middle" font-family="Inter Tight, Arial, sans-serif" font-weight="900" font-size="30" fill="#fff">CA<tspan fill="#6cc24a">$</tspan>H</text>
    <text x="180" y="205" text-anchor="middle" font-family="Inter Tight, Arial, sans-serif" font-weight="900" font-size="30" fill="#fff"><tspan fill="#6cc24a">4</tspan><tspan fill="#c9a0ee">TECH</tspan></text>
    <rect x="132" y="250" width="96" height="30" rx="15" fill="#509e2f"/>
    <text x="180" y="270" text-anchor="middle" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#fff">GET AN OFFER</text>
  </g>
  <g transform="translate(6 236) rotate(-14)">
    <rect width="120" height="64" rx="8" fill="url(#cash)"/>
    <rect x="6" y="6" width="108" height="52" rx="5" fill="none" stroke="#d6f2c8" stroke-width="1.5" opacity=".7"/>
    <circle cx="60" cy="32" r="16" fill="none" stroke="#e8f8df" stroke-width="2"/>
    <text x="60" y="39" text-anchor="middle" font-family="Inter Tight, Arial, sans-serif" font-weight="900" font-size="20" fill="#fff">$</text>
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
NAV = [
    ("sell/", "Sell Your Tech"),
    ("buy/", "Buy Electronics"),
    ("how-it-works/", "How It Works"),
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
        extra = ""
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
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{u('assets/img/favicon.svg')}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
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
          {''.join(f'<li><a href="{u("sell/" + c["slug"] + "/")}">{c["plural"]}</a></li>' for c in TAXONOMY)}
          <li><a href="{u('sell/')}">Everything we buy</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="{u('how-it-works/')}">How It Works</a></li>
          <li><a href="{u('about/')}">About Us</a></li>
          <li><a href="{u('faq/')}">FAQ</a></li>
          <li><a href="{u('buy/')}">Buy Electronics</a></li>
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
        <a class="btn btn-ghost" href="{BUSINESS['phone_href']}" data-track="click_to_call">{icon('call')}{BUSINESS['phone']}</a>
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
      <div class="step"><h3>Get cash</h3><p>Like the offer? Accept it and we pay you in cash. Not for you? You're free to decline.</p></div>
    </div>
  </div>
</section>"""


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
      <p>Payment is in cash. There are no online quotes and no mail-in. Everything happens in person at the store. {todo('ID requirements and typical visit length to confirm')}</p>
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
      <div class="card"><h3>We resell</h3><p>Tested, pre-owned electronics sold on eBay and right here in our <a href="{{{{base}}}}buy/">online shop</a>.</p></div>
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




# ---------------------------------------------------------------------------
# Taxonomy → nodes
# ---------------------------------------------------------------------------
def flatten():
    """Every category, brand and model as a node with inherited fields and its URL segment."""
    nodes = []

    def inherit(node, parent, key, default=None):
        return node.get(key) or (parent.get(key) if parent else None) or default

    for cat in TAXONOMY:
        c = dict(cat, kind="category", seg=f"{cat['slug']}/", parent=None, cat=cat)
        c["factors"] = inherit(cat, None, "factors", GENERIC_FACTORS)
        c["prep"] = inherit(cat, None, "prep", GENERIC_PREP)
        c["buy_notes"] = cat.get("buy_notes", [])
        nodes.append(c)
        for br in cat.get("children", []):
            b = dict(br, kind="brand", seg=f"{cat['slug']}/{br['slug']}/", parent=c, cat=cat)
            b["factors"] = inherit(br, c, "factors")
            b["prep"] = inherit(br, c, "prep")
            b["buy_notes"] = br.get("buy_notes") or c["buy_notes"]
            b["icon"] = br.get("icon") or c["icon"]
            nodes.append(b)
            for md in br.get("models", []):
                m = dict(md, kind="model", seg=f"{cat['slug']}/{md['slug']}/", parent=b, cat=cat)
                m["factors"] = b["factors"]
                m["prep"] = b["prep"]
                m["buy_notes"] = b["buy_notes"]
                m["icon"] = b["icon"]
                m["blurb"] = md.get("blurb") or md["about"]
                m["sell_intro"] = md.get("sell_intro") or (
                    f"Bring your {md['name']} to Cash4Tech in Gladstone for an in-person look and a cash offer. No listings, no strangers, no shipping.")
                m["buy_intro"] = md.get("buy_intro") or (
                    f"Every {md['name']} we have in stock, each listed on its own with photos of that exact device.")
                nodes.append(m)
    return nodes


NODES = flatten()


def children_of(node):
    return [n for n in NODES if n["parent"] is node or (n["parent"] is not None and n["parent"].get("slug") == node.get("slug") and n["parent"]["kind"] == node["kind"] and n["cat"] is node["cat"])]


def kids(node):
    return [n for n in NODES if n["parent"] is not None and n["parent"]["seg"] == node["seg"]]


def crumbs_for(node, section):
    label = "Sell Your Tech" if section == "sell" else "Buy Electronics"
    trail = [("Home", "{{base}}"), (label, "{{base}}" + section + "/")]
    chain = []
    p = node["parent"]
    while p:
        chain.insert(0, p)
        p = p["parent"]
    for a in chain:
        trail.append((a["plural"] if (section == "buy" or a["kind"] == "category") else a["name"], "{{base}}" + section + "/" + a["seg"]))
    trail.append((node["plural"] if (section == "buy" or node["kind"] == "category") else node["name"], None))
    return trail


def tile(n, section, more="Learn more"):
    return f"""
      <a class="card cat-card" href="{{{{base}}}}{section}/{n['seg']}">
        <span class="icon">{icon(n['icon'])}</span>
        <h3>{n['plural'] if section == 'buy' else n['name']}</h3>
        <p>{n['blurb']}</p>
        <span class="more">{more} &rarr;</span>
      </a>"""


def category_tiles(section):
    more = "Sell yours" if section == "sell" else "Shop now"
    return "".join(tile(n, section, more) for n in NODES if n["kind"] == "category")


def chip_links(node, section):
    ks = kids(node)
    if not ks:
        return ""
    label = {"category": "By brand", "brand": "Popular models"}.get(node["kind"], "")
    links = "".join(f'<a class="chip" href="{{{{base}}}}{section}/{k["seg"]}">{k["plural"] if section == "buy" else k["name"]}</a>' for k in ks)
    return f'<div class="chips"><span class="chips-label">{label}</span>{links}</div>'


def faq_items(faqs):
    out = []
    for q, a, pending in faqs:
        if pending:
            a = todo("Policy to confirm with Timothy before launch.")
        out.append(f'<details><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Sell pages
# ---------------------------------------------------------------------------
def a_an(word):
    w = word.lower()
    if w.endswith("components"):
        return word
    return ("an " if w[0] in "aeiox" else "a ") + word


def lname(n):
    """Name as used in a sentence: 'phone', 'iPhone 15', 'computer components'."""
    if n["kind"] != "category":
        return n["name"]
    return n.get("sentence_name") or n["name"].lower()


def sell_title(n):
    word = n["name"]
    return f"Sell Your {word} for Cash in Kansas City | Cash4Tech Gladstone"


def sell_node(n):
    name_l = lname(n)
    about = f'<div class="card mb-2"><h3>About the {n["name"]}</h3><p class="mb-0">{n["about"]}</p></div>' if n["kind"] == "model" else ""
    factors = "".join(f"<li>{f}</li>" for f in n["factors"])
    prep = "".join(f"<li>{p}</li>" for p in n["prep"])
    body = page_hero(f"Sell your {name_l}", n["sell_intro"], crumbs=crumbs_for(n, "sell"),
                     eyebrow="Cash for your tech · Gladstone, MO") + f"""
<section class="section">
  <div class="wrap">
    {chip_links(n, 'sell')}
    <div class="split">
      <div>
        {about}
        <h2>What we look at</h2>
        <p>Every device is evaluated in person. Things that can affect your offer include:</p>
        <ul class="checklist">{factors}</ul>
        <p class="muted">We can't accept every device, and offers depend on condition and current demand. Not sure about yours? Call <a href="{BUSINESS['phone_href']}" data-track="click_to_call">{BUSINESS['phone']}</a>.</p>
      </div>
      <div class="card">
        <h2>Before you come in</h2>
        <ul class="checklist">{prep}</ul>
        <p class="muted mb-0">General guidance for getting a device ready. We can help in store if you get stuck.</p>
      </div>
    </div>
  </div>
</section>
{steps_block()}
<section class="section tight">
  <div class="wrap split">
    <div class="faq">
      <h2>Quick answers</h2>
      {faq_items([f for f in SELL_FAQS if f[0] in ("How will I be paid?", "Can I decline an offer?", "Can I get a quote online?")])}
      <p class="mt-2"><a href="{{{{base}}}}faq/">More questions &rarr;</a></p>
    </div>
    <div class="card">
      <h3>Shopping for {a_an(name_l)} instead?</h3>
      <p>We also sell tested, pre-owned {n['plural'].lower() if n['kind'] == 'category' else n['plural']}.</p>
      <a class="btn btn-purple" href="{{{{base}}}}buy/{n['seg']}">Shop used {n['plural'] if n['kind'] != 'category' else n['plural'].lower()}</a>
    </div>
  </div>
</section>
{cta_band(f"Bring your {name_l} to Cash4Tech", "Visit our Gladstone store for an in-person cash offer.")}
"""
    desc = f"Sell your {name_l} for cash at Cash4Tech in Gladstone, MO, serving the Kansas City Northland. Bring it in, get an in-person offer, and get paid in cash."
    return page_shell(f"sell/{n['seg']}", sell_title(n), desc, body, active="sell/")


def sell_index():
    body = page_hero("Sell your tech for cash",
                     "Phones, tablets, laptops, computers, gaming consoles, smartwatches and components. Bring them to our Gladstone store for an in-person cash offer.",
                     eyebrow="Sell your tech") + f"""
<section class="section">
  <div class="wrap">
    <div class="grid grid-4">{category_tiles('sell')}</div>
    <div class="card mt-3">
      <h3>Popular right now</h3>
      <div class="chips mb-0">{''.join(f'<a class="chip" href="{{{{base}}}}sell/{n["seg"]}">Sell your {n["name"]}</a>' for n in NODES if n["kind"] != "category")}</div>
    </div>
  </div>
</section>
{steps_block()}
{cta_band()}
"""
    return page_shell("sell/", "Sell Electronics for Cash in Kansas City | Cash4Tech Gladstone, MO",
                      "Sell your phone, iPad, laptop, game console or smartwatch for cash at Cash4Tech in Gladstone, MO. In-person offers, paid in cash.",
                      body, active="sell/")


# ---------------------------------------------------------------------------
# Buy pages (live Shopify catalog)
# ---------------------------------------------------------------------------
def shop_config_script():
    cfg = {"domain": SHOPIFY["domain"], "token": SHOPIFY["storefront_token"],
           "version": SHOPIFY["api_version"], "checkout": SHOPIFY["checkout_enabled"],
           "phone": BUSINESS["phone"], "phoneHref": BUSINESS["phone_href"]}
    return f'<script>window.C4T_SHOP = {json.dumps(cfg)};</script>'


def fallback_terms(n):
    """Looser keyword search used when the structured query finds nothing (e.g. product types differ)."""
    names = [n["name"]] + [k["name"] for k in kids(n)]
    for k in kids(n):
        names += [m["name"] for m in kids(k)]
    return " OR ".join(f'"{x}"' for x in dict.fromkeys(names))


def product_grid(query, sample_name, limit=24, fallback=""):
    note = "" if SHOP_LIVE else f'<div class="todo-block mb-2"><strong>Sample cards.</strong> Live products from the Shopify catalog appear here once the store\'s Storefront API token is added to content.py.</div>'
    return f"""
    {note}
    <div class="product-grid grid grid-3" data-query="{escape(query)}" data-fallback="{escape(fallback)}" data-limit="{limit}" data-sample="{escape(sample_name)}" aria-live="polite">
      <p class="muted">Loading products&hellip;</p>
    </div>"""


def returns_card():
    return f"""
      <div class="card">
        <h3>Good to know</h3>
        <ul class="checklist">
          <li>Every listing is one specific device, shown in its own photos</li>
          <li>30-day returns. Buyer pays return shipping</li>
          <li>No separate product warranty</li>
        </ul>
        <p class="mb-0">{todo('Shipping options and full return policy wording to confirm')}</p>
      </div>"""


def buy_node(n):
    notes = "".join(f"<li>{x}</li>" for x in n["buy_notes"])
    plural = n["plural"] if n["kind"] != "category" else n["plural"].lower()
    body = page_hero(f"Shop used {plural}", n["buy_intro"], crumbs=crumbs_for(n, "buy"),
                     eyebrow="Buy electronics") + f"""
<section class="section">
  <div class="wrap">
    {chip_links(n, 'buy')}
    {product_grid(n['query'], n['name'], fallback=fallback_terms(n))}
  </div>
</section>
<section class="section alt tight">
  <div class="wrap split">
    <div>
      <h2>Buying {a_an('used ' + lname(n))}</h2>
      <ul class="checklist">{notes or '<li>Read the condition notes and look through every photo</li>'}<li>Questions about a listing? Call us at <a href="{BUSINESS['phone_href']}" data-track="click_to_call">{BUSINESS['phone']}</a></li></ul>
    </div>
    {returns_card()}
  </div>
</section>
<section class="section tight">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Have {a_an(lname(n))} to sell?</h2><p>Bring it to our Gladstone store for an in-person cash offer.</p></div>
      <a class="btn btn-green" href="{{{{base}}}}sell/{n['seg']}">Sell your {lname(n)}</a>
    </div>
  </div>
</section>
{shop_config_script()}
<script src="{{{{base}}}}assets/js/shop.js" defer></script>
"""
    desc = f"Shop tested, pre-owned {plural} from Cash4Tech in Gladstone, MO. Every listing shows photos of the actual device."
    return page_shell(f"buy/{n['seg']}", f"Used {n['plural']} for Sale | Cash4Tech", desc, body, active="buy/")


def buy_index():
    body = page_hero("Buy pre-owned electronics",
                     "Phones, tablets, laptops, consoles and more, each listed individually with photos of the actual device.",
                     eyebrow="Buy electronics") + f"""
<section class="section">
  <div class="wrap">
    <form class="search-bar" action="{{{{base}}}}buy/search/" role="search">
      <label class="skip" for="q">Search products</label>
      <input id="q" name="q" type="search" placeholder="Search, e.g. iPhone 15 256GB">
      <button class="btn btn-green" type="submit">Search</button>
    </form>
    <div class="grid grid-4">{category_tiles('buy')}</div>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <div class="section-head"><h2>Just listed</h2></div>
    {product_grid('', 'Device', 9)}
  </div>
</section>
<section class="section tight"><div class="wrap">{returns_card()}</div></section>
{shop_config_script()}
<script src="{{{{base}}}}assets/js/shop.js" defer></script>
"""
    return page_shell("buy/", "Buy Used Electronics | Phones, Laptops, Consoles | Cash4Tech",
                      "Shop tested, pre-owned phones, tablets, laptops, gaming consoles and smartwatches from Cash4Tech in Gladstone, MO.",
                      body, active="buy/")


def buy_search():
    body = page_hero("Search", "Search every device we have listed.", eyebrow="Buy electronics") + f"""
<section class="section">
  <div class="wrap">
    <form class="search-bar" action="./" role="search">
      <label class="skip" for="q">Search products</label>
      <input id="q" name="q" type="search" placeholder="Search, e.g. MacBook Air M2">
      <button class="btn btn-green" type="submit">Search</button>
    </form>
    <div class="product-grid grid grid-3" data-search="1" data-limit="36" data-sample="Device" aria-live="polite"></div>
  </div>
</section>
{shop_config_script()}
<script src="{{{{base}}}}assets/js/shop.js" defer></script>
"""
    return page_shell("buy/search/", "Search | Cash4Tech", "Search Cash4Tech's pre-owned electronics.", body, active="buy/", noindex=True)


def buy_item():
    body = f"""
<section class="section">
  <div class="wrap">
    <div class="crumbs crumbs-light"><a href="{{{{base}}}}">Home</a> / <a href="{{{{base}}}}buy/">Buy Electronics</a></div>
    <div id="product" class="product-detail" aria-live="polite"><p class="muted">Loading&hellip;</p></div>
  </div>
</section>
<section class="section alt tight"><div class="wrap">{returns_card()}</div></section>
{shop_config_script()}
<script src="{{{{base}}}}assets/js/shop.js" defer></script>
"""
    return page_shell("buy/item/", "Product | Cash4Tech", "Pre-owned electronics from Cash4Tech.", body, active="buy/")


# ---------------------------------------------------------------------------
# Home, FAQ, roadmap
# ---------------------------------------------------------------------------
def home():
    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Gladstone, MO &middot; Kansas City Northland</span>
      <h1>Turn your tech <span class="g">into cash.</span></h1>
      <p class="lede">Got electronics you no longer use? Bring them to Cash4Tech in Gladstone for an in-person offer, paid in cash. Sell your phones, tablets, gaming consoles and more without the hassle of selling online.</p>
      <div class="btn-row">
        <a class="btn btn-green" href="{DIRECTIONS_URL}" target="_blank" rel="noopener" data-track="get_directions">{icon('pin')}Get Directions</a>
        <a class="btn btn-ghost" href="{{{{base}}}}visit/">Visit Our Store</a>
        <a class="btn btn-ghost" href="{BUSINESS['phone_href']}" data-track="click_to_call">{icon('call')}Call Us</a>
      </div>
      <div class="hero-meta">
        <span>{icon('store')}Real local store</span>
        <span>{icon('hand')}In-person offers</span>
        <span>{icon('check')}Paid in cash</span>
      </div>
    </div>
    <div class="hero-art">{HERO_ART}</div>
  </div>
</section>

<section class="section tight split-paths">
  <div class="wrap grid grid-2">
    <a class="path-card path-sell" href="{{{{base}}}}sell/">
      <span class="eyebrow">Sell your tech</span>
      <h2>Get cash for your old devices</h2>
      <p>Bring it in, get an offer, walk out with cash.</p>
      <span class="more">See what we buy &rarr;</span>
    </a>
    <a class="path-card path-buy" href="{{{{base}}}}buy/">
      <span class="eyebrow">Buy electronics</span>
      <h2>Shop tested, pre-owned tech</h2>
      <p>Every listing is one real device, with its own photos.</p>
      <span class="more">Browse the shop &rarr;</span>
    </a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">What we buy</span>
      <h2>Phones, tablets, laptops, consoles and more</h2>
      <p class="lede">What we can accept and what we offer depend on the model, condition, specs and demand.</p>
    </div>
    <div class="grid grid-4">{category_tiles('sell')}</div>
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
          <tr><th>Meetups</th><td>Our store</td><td>Parking lots and driveways</td></tr>
          <tr><th>Shipping</th><td>None</td><td>Packing, labels, return risk</td></tr>
          <tr><th>Getting paid</th><td>Cash, at the counter</td><td>Days or weeks waiting for a buyer</td></tr>
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
    <div class="todo-block mt-3"><strong>Reviews go here.</strong> Real Google reviews can appear here once they come in. We won't add testimonials that aren't genuine.</div>
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
        <a class="btn btn-purple" href="{BUSINESS['phone_href']}" data-track="click_to_call">{icon('call')}Call Us</a>
      </div>
    </div>
    <div class="map-box">
      <div>
        <p><strong>Map goes here</strong></p>
        <p class="muted">An embedded Google Map appears once the store address is confirmed.</p>
        {todo('Store address + storefront photos')}
      </div>
    </div>
  </div>
</section>

<section class="section dark">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">Buy electronics</span>
      <h2>Shop tested, pre-owned tech</h2>
      <p class="lede">The devices we buy are tested, photographed and listed individually, so you see exactly what you're getting.</p>
    </div>
    <div class="grid grid-4 dark-tiles">{category_tiles('buy')}</div>
  </div>
</section>

{cta_band()}
"""
    return page_shell("", "Sell Your Phone & Electronics for Cash | Cash4Tech Gladstone, MO",
                      "Sell used phones, iPads, laptops, gaming consoles and more for cash at Cash4Tech in Gladstone, MO, or shop tested pre-owned electronics. Serving the Kansas City Northland.",
                      body, schema=local_business_schema())


def faq():
    answered = [(q, a) for q, a, p in SELL_FAQS + BUY_FAQS if not p]
    schema = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a.replace("{{base}}", "/")}} for q, a in answered]}
    body = page_hero("Frequently asked questions",
                     "Answers about selling your electronics to Cash4Tech and buying from us. Don't see your question? Give us a call.",
                     eyebrow="FAQ") + f"""
<section class="section">
  <div class="wrap narrow faq">
    <h2>Selling to Cash4Tech</h2>
    {faq_items(SELL_FAQS)}
    <h2 class="mt-3">Buying from Cash4Tech</h2>
    {faq_items(BUY_FAQS)}
  </div>
</section>
{cta_band("Still have a question?", "Call us and we'll help you out.")}
"""
    return page_shell("faq/", "FAQ | Selling & Buying Electronics | Cash4Tech Gladstone, MO",
                      "Common questions about selling your phone, tablet, laptop or game console to Cash4Tech for cash, and buying pre-owned electronics.",
                      body, active="faq/", schema=schema)


ARCH_SVG = """
<svg class="arch" viewBox="0 0 900 400" role="img" aria-label="Devices bought in store go into the Cash4Tech ERP, which publishes each one to Shopify and eBay. The website reads products from Shopify.">
  <defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5d5d6b"/></marker></defs>
  <style>.t{font:700 15px Inter,sans-serif;fill:#fff}.s{font:500 12px Inter,sans-serif;fill:#e7e2f0}.td{font:700 14px Inter,sans-serif;fill:#1b1b22}.sd{font:500 11.5px Inter,sans-serif;fill:#5d5d6b}.lbl{font:600 11px Inter,sans-serif;fill:#5d5d6b}</style>
  <rect x="20" y="30" width="190" height="100" rx="14" fill="#509e2f"/>
  <text x="115" y="70" text-anchor="middle" class="t">Gladstone store</text>
  <text x="115" y="92" text-anchor="middle" class="s">Buys devices for cash</text>
  <text x="115" y="110" text-anchor="middle" class="s">Test · grade · photograph</text>
  <path d="M115 132 V196" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)"/>
  <rect x="20" y="200" width="190" height="150" rx="14" fill="#2a1240"/>
  <text x="115" y="240" text-anchor="middle" class="t">Cash4Tech ERP</text>
  <text x="115" y="264" text-anchor="middle" class="s">Inventory authority</text>
  <text x="115" y="284" text-anchor="middle" class="s">One record per device</text>
  <text x="115" y="304" text-anchor="middle" class="s">Controls availability</text>
  <text x="115" y="324" text-anchor="middle" class="s">across every channel</text>
  <text x="128" y="170" class="lbl">already built</text>
  <rect x="340" y="60" width="210" height="120" rx="14" fill="#5b2a86"/>
  <text x="445" y="100" text-anchor="middle" class="t">Shopify</text>
  <text x="445" y="124" text-anchor="middle" class="s">One product per device</text>
  <text x="445" y="142" text-anchor="middle" class="s">Real photos · specs · price</text>
  <text x="445" y="160" text-anchor="middle" class="s">Cart &amp; checkout</text>
  <path d="M212 250 C 280 250, 280 120, 336 120" fill="none" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)"/>
  <text x="236" y="190" class="lbl">ERP sync (exists)</text>
  <rect x="340" y="250" width="210" height="90" rx="14" fill="#fff" stroke="#509e2f" stroke-width="2.5"/>
  <text x="445" y="288" text-anchor="middle" class="td">eBay</text>
  <text x="445" y="308" text-anchor="middle" class="sd">Live today</text>
  <path d="M212 300 C 270 300, 290 295, 336 295" fill="none" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)"/>
  <rect x="660" y="30" width="220" height="110" rx="12" fill="#fff" stroke="#5b2a86" stroke-width="2.5"/>
  <text x="770" y="66" text-anchor="middle" class="td">getcash4tech.com</text>
  <text x="770" y="88" text-anchor="middle" class="sd">Sell Your Tech pages</text>
  <text x="770" y="106" text-anchor="middle" class="sd">Buy Electronics pages</text>
  <text x="770" y="124" text-anchor="middle" class="sd">(this site)</text>
  <path d="M552 105 C 600 105, 610 85, 656 85" fill="none" stroke="#5d5d6b" stroke-width="2" marker-end="url(#ah)"/>
  <text x="560" y="78" class="lbl">read-only API</text>
  <rect x="660" y="250" width="220" height="90" rx="12" fill="#fff" stroke="#9d99ad" stroke-width="2" stroke-dasharray="6 5"/>
  <text x="770" y="288" text-anchor="middle" class="td">Amazon · Walmart</text>
  <text x="770" y="308" text-anchor="middle" class="sd">Under consideration</text>
  <path d="M552 300 C 600 300, 610 295, 656 295" fill="none" stroke="#9d99ad" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#ah)"/>
  <text x="340" y="385" class="lbl">The website never writes inventory. Sales flow back through Shopify → ERP, which pulls the device from every other channel.</text>
</svg>
"""


def roadmap():
    n_sell = sum(1 for _ in NODES) + 1
    body = page_hero("Where this site is headed",
                     "What this demo covers today, and how it grows into the full Sell + Buy site from Timothy's requirements.",
                     eyebrow="Project roadmap · for Cash4Tech") + f"""
<section class="section">
  <div class="wrap">
    <div class="status-key">
      <span class="badge badge-green">In this demo</span>
      <span class="badge badge-purple">Next</span>
      <span class="badge badge-gray">Owner only</span>
    </div>

    <div class="phase now">
      <h3>Sell Your Tech <span class="badge badge-green">In this demo</span></h3>
      <p class="mb-0">{n_sell} landing pages built from one template: category, then brand, then popular model (for example /sell/phones/, /sell/phones/iphone/, /sell/phones/iphone-15/). Each page has its own content: what affects the offer, how to prep that device, and model facts. Calls to action are Get Directions, Visit Our Store and Call Us, plus a sticky call/directions bar on phones. Copy says paid in cash, with no online quotes or mail-in. Adding a page means adding a few lines to content.py.</p>
    </div>

    <div class="phase now">
      <h3>Buy Electronics <span class="badge badge-green">In this demo</span></h3>
      <p class="mb-0">A matching page tree under /buy/ that reads products straight from Shopify through the read-only Storefront API. Each model page shows every in-stock unit of that model (three iPhone 15s are three cards, each with its own photos). There's search, a product page with the device's real photos, and the 30-day return terms. Until the Storefront token is added, the pages show labeled sample cards.</p>
    </div>

    <div class="phase next">
      <h3>Before launch <span class="badge badge-purple">Next</span></h3>
      <p class="mb-0">Connect the Storefront token and match each page's product search to the ERP's actual product types, vendors and tags. Fill in every ⚑ (address, hours, policies, shipping), swap in the real logo, set up GA4, Tag Manager and Search Console with call and directions tracking, then point getcash4tech.com here in Cloudflare without touching the Gmail MX, SPF, DKIM or DMARC records.</p>
    </div>

    <div class="phase">
      <h3>Online checkout <span class="badge badge-gray">Owner only</span></h3>
      <p class="mb-0">The product page already has a switch for an Add to cart button that hands off to Shopify's own checkout. It stays off until Timothy activates payments and approves shipping and tax settings. Nothing on this site turns on payment processing.</p>
    </div>

    <div class="phase">
      <h3>Growth <span class="badge badge-purple">Later</span></h3>
      <p class="mb-0">Hundreds more model pages, ad landing pages for searches like "sell iPhone Kansas City", real Google reviews, and more marketplaces through the ERP.</p>
    </div>
  </div>
</section>

<section class="section alt">
  <div class="wrap">
    <div class="section-head">
      <h2>How the pieces fit</h2>
      <p class="lede">The ERP stays in charge of inventory and already publishes to Shopify. The website only reads from Shopify. It never changes inventory or touches the ERP.</p>
    </div>
    <div class="arch-wrap">{ARCH_SVG}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Still needed</h2><p class="lede">Only what blocks launch.</p></div>
    <div class="grid grid-2">
      <div class="card"><h3>From Todd</h3><ul class="checklist"><li>Shopify store domain (.myshopify.com)</li><li>Storefront API token (Headless channel)</li><li>Accept the Cloudflare invite and audit the DNS records</li></ul></div>
      <div class="card"><h3>From Timothy</h3><ul class="checklist"><li>Street address and confirmed hours</li><li>Logo file</li><li>ID, damaged-device and locked-phone policies</li><li>Return policy wording and shipping rates</li><li>Storefront photos and eBay store link</li></ul></div>
    </div>
  </div>
</section>
"""
    return page_shell("roadmap/", "Cash4Tech Website Roadmap",
                      "Plan for getcash4tech.com: Sell Your Tech landing pages, a Shopify-backed Buy section, and launch steps.",
                      body, noindex=True)


def not_found():
    body = page_hero("Page not found", "Sorry, that page doesn't exist.") + """
<section class="section"><div class="wrap"><a class="btn btn-green" href="/">Back to home</a></div></section>"""
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
        "buy/": buy_index(),
        "buy/search/": buy_search(),
        "buy/item/": buy_item(),
        "how-it-works/": how_it_works(),
        "about/": about(),
        "visit/": visit(),
        "faq/": faq(),
        "roadmap/": roadmap(),
    }
    for n in NODES:
        pages["sell/" + n["seg"]] = sell_node(n)
        pages["buy/" + n["seg"]] = buy_node(n)
    for rel, html in pages.items():
        write(rel, html)
    write("404.html", not_found())

    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nDisallow: /\n" if DEMO else f"User-agent: *\nAllow: /\nSitemap: {BUSINESS['domain']}/sitemap.xml\n")
    skip = {"roadmap/", "buy/search/", "buy/item/"}
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in pages:
            if p not in skip:
                f.write(f"  <url><loc>{BUSINESS['domain']}/{p}</loc></url>\n")
        f.write("</urlset>\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    print(f"Built {len(pages) + 1} pages into {OUT}")


if __name__ == "__main__":
    main()
