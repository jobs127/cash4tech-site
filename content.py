"""
Cash4Tech site content.

This is the file to edit. build.py turns it into pages.

- BUSINESS: store facts. Anything set to None shows on the demo as a yellow ⚑ flag.
- SHOPIFY: connection for the Buy section. Use a Storefront API *public* access token only
  (read-only product access, safe in a browser). Never put an Admin API token here.
- TAXONOMY: category → brand → model. Each node produces a Sell page and a Buy page.
  Add a dict here and rebuild to add a page; the templates do the rest.
  `query` is the Shopify product search used on that node's Buy page. Adjust once the
  ERP's product attribute mapping (product type, vendor, tags) is final.
"""

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
    "street": None,          # not yet provided
    "postal": None,
    "email": None,           # not yet provided
    "ebay_store": None,      # eBay store URL, not yet provided
    # Planned hours from the brief. Shown with a flag until hours_confirmed is True.
    "hours": [("Monday – Friday", "10 AM – 7 PM"), ("Saturday", "10 AM – 4 PM"), ("Sunday", "10 AM – 4 PM")],
    "hours_confirmed": False,
}

SHOPIFY = {
    "domain": None,            # e.g. "cash4tech.myshopify.com"
    "storefront_token": None,  # Storefront API public access token (Headless channel)
    "api_version": "2025-07",
    # Stays False until the owner activates payments. While False, product pages show
    # "Call about this device" instead of a cart button.
    "checkout_enabled": False,
}

DEMO = True      # yellow banner + ⚑ flags + noindex
GTM_ID = None    # "GTM-XXXXXXX" once Google Tag Manager is set up

# ---------------------------------------------------------------------------
# Shared defaults (a node can override any of these)
# ---------------------------------------------------------------------------
GENERIC_FACTORS = ["Model and age", "Specs and storage", "Physical condition",
                   "Whether everything works", "Current resale demand", "Accessories included"]
GENERIC_PREP = ["Back up anything you want to keep", "Sign out of any accounts tied to the device",
                "Bring chargers or accessories you'd like us to consider"]

APPLE_PREP = ["Back up to iCloud or a computer",
              "Turn off Find My and sign out of your Apple ID. A device still locked to an Apple ID can't be resold",
              "Know your passcode in case we need to check the device", "Remove your SIM card"]
ANDROID_PREP = ["Back up to your Google or Samsung account",
                "Remove your Google account. Android's Factory Reset Protection locks the phone to it otherwise",
                "Remove your Samsung account", "Know your PIN or pattern", "Remove your SIM and any memory card"]

TAXONOMY = [
    {
        "slug": "phones", "name": "Phone", "plural": "Phones", "icon": "phone",
        "blurb": "iPhone, Samsung Galaxy and other smartphones.",
        "sell_intro": "Upgraded to a new phone? Bring the old one to Cash4Tech in Gladstone. We'll check it over in person and make you a cash offer, with no listing or meeting strangers.",
        "buy_intro": "Pre-owned smartphones, each listed individually with photos of the actual phone, its storage, condition and price.",
        "factors": ["Model and generation", "Storage capacity", "Carrier and lock status", "Battery health",
                    "Screen and body condition", "Whether cameras, Face ID / fingerprint, buttons and charging work"],
        "prep": ["Back up your photos and data", "Sign out of iCloud (Find My) or your Google account",
                 "Know your passcode", "Remove your SIM card"],
        "buy_notes": ["Check carrier compatibility. Each listing notes whether the phone is unlocked or tied to a carrier",
                      "Look at the battery and condition details in the description",
                      "Photos are of the actual phone you'll receive, not stock images"],
        "query": "product_type:Phones",
        "children": [
            {
                "slug": "iphone", "name": "iPhone", "plural": "iPhones", "brand": "Apple", "icon": "phone",
                "blurb": "Every generation, including Pro and Pro Max models.",
                "sell_intro": "Bring your iPhone to Cash4Tech for an in-person look and a cash offer. Newer models, higher storage and good battery health usually matter most. Every phone is evaluated individually.",
                "buy_intro": "Pre-owned iPhones, each one its own listing, so you can see the exact storage, color, condition and photos of the phone you're buying.",
                "prep": APPLE_PREP,
                "query": "product_type:Phones AND vendor:Apple",
                "models": [
                    {"slug": "iphone-16", "name": "iPhone 16", "plural": "iPhone 16s",
                     "about": "Released in 2024, the iPhone 16 family (16, 16 Plus, 16 Pro, 16 Pro Max) added the Camera Control button. Storage starts at 128 GB.",
                     "query": "product_type:Phones AND \"iPhone 16\""},
                    {"slug": "iphone-15", "name": "iPhone 15", "plural": "iPhone 15s",
                     "about": "Released in 2023, the iPhone 15 family was the first to switch from Lightning to USB-C. It came in 128 GB, 256 GB and 512 GB, with a 1 TB option on Pro models.",
                     "query": "product_type:Phones AND \"iPhone 15\""},
                    {"slug": "iphone-14", "name": "iPhone 14", "plural": "iPhone 14s",
                     "about": "Released in 2022. US iPhone 14 models are eSIM-only, with no physical SIM tray, so carrier and activation status are especially important.",
                     "query": "product_type:Phones AND \"iPhone 14\""},
                ],
            },
            {
                "slug": "samsung", "name": "Samsung Galaxy", "plural": "Samsung phones", "brand": "Samsung", "icon": "android",
                "blurb": "Galaxy S, Z Fold, Z Flip, Note and A series.",
                "sell_intro": "Bring your Samsung Galaxy to Cash4Tech: Galaxy S, Z Fold, Z Flip, Note or A series. On Samsung phones we look closely at screen condition, including burn-in.",
                "buy_intro": "Pre-owned Samsung Galaxy phones, listed one by one with real photos and condition details.",
                "factors": ["Model and generation", "Storage capacity", "Carrier and lock status",
                            "Screen condition, including burn-in", "Back-glass condition", "Whether cameras, charging and buttons work"],
                "prep": ANDROID_PREP,
                "query": "product_type:Phones AND vendor:Samsung",
                "models": [
                    {"slug": "galaxy-s24", "name": "Galaxy S24", "plural": "Galaxy S24s",
                     "about": "Released in 2024 as the S24, S24+ and S24 Ultra. The Ultra has a built-in S Pen, so bring it along if you have it.",
                     "query": "product_type:Phones AND \"Galaxy S24\""},
                    {"slug": "galaxy-s23", "name": "Galaxy S23", "plural": "Galaxy S23s",
                     "about": "Released in 2023 as the S23, S23+ and S23 Ultra.",
                     "query": "product_type:Phones AND \"Galaxy S23\""},
                ],
            },
        ],
    },
    {
        "slug": "tablets", "name": "Tablet", "plural": "Tablets", "icon": "tablet",
        "blurb": "iPad, iPad Air, iPad Pro, iPad mini and Android tablets.",
        "sell_intro": "Tablets often get replaced long before they wear out. If yours is sitting unused, bring it to Cash4Tech for a cash offer.",
        "buy_intro": "Pre-owned tablets with photos of the actual device and full condition details.",
        "factors": ["Model and generation", "Storage capacity", "Wi-Fi only or cellular", "Screen and body condition",
                    "Battery health", "Accessories such as a pencil or keyboard"],
        "buy_notes": ["Check whether it's Wi-Fi only or cellular", "Confirm the model supports the accessories you want to use"],
        "query": "product_type:Tablets",
        "children": [
            {
                "slug": "ipad", "name": "iPad", "plural": "iPads", "brand": "Apple", "icon": "tablet",
                "blurb": "iPad, iPad Air, iPad Pro and iPad mini.",
                "sell_intro": "Bring in your iPad, iPad Air, iPad Pro or iPad mini. An Apple Pencil or keyboard that goes with it is worth bringing along.",
                "buy_intro": "Pre-owned iPads, each listed individually with its exact storage, connectivity and condition.",
                "prep": APPLE_PREP[:3],
                "query": "product_type:Tablets AND vendor:Apple",
            },
        ],
    },
    {
        "slug": "laptops", "name": "Laptop", "plural": "Laptops", "icon": "laptop",
        "blurb": "MacBooks, Windows laptops and Chromebooks.",
        "sell_intro": "MacBook, Windows laptop or Chromebook, bring it in with its charger so we can test it, and we'll make you a cash offer.",
        "buy_intro": "Pre-owned laptops listed with their real specs (processor, memory and storage) plus photos and condition.",
        "factors": ["Brand, model and year", "Processor, memory and storage", "Screen, keyboard and trackpad condition",
                    "Battery health and cycle count", "Whether it boots and charges normally", "Whether the charger is included"],
        "prep": ["Back up your files", "Sign out of iCloud / Find My Mac, or your Microsoft account",
                 "Bring the charger", "Know your login password"],
        "buy_notes": ["Compare processor, memory and storage across listings", "Check battery details in the description"],
        "query": "product_type:Laptops",
        "children": [
            {
                "slug": "macbook", "name": "MacBook", "plural": "MacBooks", "brand": "Apple", "icon": "laptop",
                "blurb": "MacBook Air and MacBook Pro.",
                "sell_intro": "Bring in your MacBook Air or MacBook Pro. Apple silicon models (M1 and newer) and higher memory and storage configurations tend to matter most.",
                "buy_intro": "Pre-owned MacBook Air and MacBook Pro laptops, each with its exact chip, memory and storage listed.",
                "prep": ["Back up with Time Machine or iCloud", "Turn off Find My Mac and sign out of your Apple ID", "Bring the charger"],
                "query": "product_type:Laptops AND vendor:Apple",
            },
        ],
    },
    {
        "slug": "computers", "name": "Computer", "plural": "Computers", "icon": "desktop",
        "blurb": "iMacs, Mac minis, desktops and all-in-ones.",
        "sell_intro": "Desktop towers, iMacs, Mac minis and all-in-ones. Bring the computer and its power cable and we'll take a look.",
        "buy_intro": "Pre-owned desktop computers listed with their real specs and condition.",
        "factors": ["Brand and model", "Processor, memory, storage and graphics", "Whether it boots normally", "Physical condition"],
        "query": "product_type:Computers",
    },
    {
        "slug": "gaming", "name": "Gaming Console", "plural": "Gaming Consoles", "icon": "gamepad",
        "blurb": "PlayStation, Xbox, Nintendo Switch and accessories.",
        "sell_intro": "Moved on to a new system? Bring your console, controllers and cables to Cash4Tech for a cash offer.",
        "buy_intro": "Pre-owned consoles and accessories, tested and listed with photos of the actual unit.",
        "factors": ["Console model and storage", "Whether it powers on and runs normally", "Controllers and cables included",
                    "Disc drive or dock, where applicable", "Cosmetic condition"],
        "prep": ["Sign out of your PlayStation, Xbox or Nintendo account", "Deactivate it as your primary or home console",
                 "Bring the power cable, HDMI cable and controllers", "Take out any game discs or cartridges you want to keep"],
        "buy_notes": ["Check which controllers and cables are included", "Disc vs. digital editions are noted on each listing"],
        "query": "product_type:\"Video Game Consoles\"",
        "children": [
            {
                "slug": "playstation", "name": "PlayStation", "plural": "PlayStations", "brand": "Sony", "icon": "gamepad",
                "blurb": "PS5, PS5 Slim, PS5 Pro, PS4 and controllers.",
                "sell_intro": "Bring in your PlayStation console and DualSense or DualShock controllers. Disc and Digital editions are evaluated differently, so we'll check which one you have.",
                "buy_intro": "Pre-owned PlayStation consoles and controllers, listed individually.",
                "prep": ["Sign out of your PlayStation Network account", "Turn off 'Console Sharing and Offline Play' for your account on this console",
                         "Bring the power cable, HDMI cable and controllers"],
                "query": "\"PlayStation\"",
                "models": [
                    {"slug": "playstation-5", "name": "PlayStation 5", "plural": "PS5 consoles",
                     "about": "The PS5 launched in 2020 in Disc and Digital editions. The slimmer redesign arrived in 2023 and the PS5 Pro in 2024. Tell us which version you have, or we'll check.",
                     "query": "\"PlayStation 5\" OR \"PS5\""},
                ],
            },
            {
                "slug": "xbox", "name": "Xbox", "plural": "Xbox consoles", "brand": "Microsoft", "icon": "gamepad",
                "blurb": "Xbox Series X, Series S, Xbox One and controllers.",
                "sell_intro": "Bring in your Xbox Series X, Series S or Xbox One, with controllers and cables.",
                "buy_intro": "Pre-owned Xbox consoles and controllers, listed individually.",
                "prep": ["Sign out of your Microsoft account", "Remove it as your home Xbox", "Bring the power cable, HDMI cable and controllers"],
                "query": "\"Xbox\"",
                "models": [
                    {"slug": "xbox-series-x", "name": "Xbox Series X", "plural": "Xbox Series X consoles",
                     "about": "Launched in 2020. The Series X has a disc drive; the smaller Series S is digital-only.",
                     "query": "\"Xbox Series X\""},
                ],
            },
            {
                "slug": "nintendo-switch", "name": "Nintendo Switch", "plural": "Nintendo Switch consoles", "brand": "Nintendo", "icon": "gamepad",
                "blurb": "Switch, Switch OLED, Switch Lite and Switch 2.",
                "sell_intro": "Bring in your Nintendo Switch: original, OLED, Lite or Switch 2. The dock, Joy-Con and power adapter are worth bringing too.",
                "buy_intro": "Pre-owned Nintendo Switch consoles and accessories, listed individually.",
                "prep": ["Back up your saves with Nintendo Switch Online or transfer them", "Deregister it as your primary console in the eShop",
                         "Do a full system reset", "Bring the dock, Joy-Con and power adapter"],
                "query": "\"Nintendo Switch\"",
                "models": [
                    {"slug": "nintendo-switch-oled", "name": "Nintendo Switch OLED", "plural": "Switch OLED consoles",
                     "about": "Released in 2021 with a 7-inch OLED screen, 64 GB of storage and a dock with a wired LAN port. Screen condition matters most.",
                     "query": "\"Switch OLED\""},
                ],
            },
        ],
    },
    {
        "slug": "smartwatches", "name": "Smartwatch", "plural": "Smartwatches", "icon": "watch",
        "blurb": "Apple Watch, Galaxy Watch and other wearables.",
        "sell_intro": "Apple Watch, Galaxy Watch and other wearables can be worth bringing in. Stop by and we'll take a look.",
        "buy_intro": "Pre-owned smartwatches listed with case size, connectivity and condition.",
        "factors": ["Model, size and series", "GPS only or cellular", "Case material", "Screen and case condition",
                    "Battery health", "Whether the charger is included"],
        "prep": ["Unpair it from your phone", "Back up any health data you want to keep", "Bring the charger"],
        "buy_notes": ["Check case size and band compatibility", "Check whether it's GPS-only or cellular"],
        "query": "product_type:Smartwatches",
        "children": [
            {
                "slug": "apple-watch", "name": "Apple Watch", "plural": "Apple Watches", "brand": "Apple", "icon": "watch",
                "blurb": "Series, SE and Ultra models.",
                "sell_intro": "Bring in your Apple Watch: Series, SE or Ultra. Unpairing it from your iPhone first removes Activation Lock, which we need before we can buy it.",
                "buy_intro": "Pre-owned Apple Watches, each listed with its series, case size, material and condition.",
                "prep": ["Unpair it from your iPhone in the Watch app. This also removes Activation Lock",
                         "Back up any health data", "Bring the charger"],
                "query": "product_type:Smartwatches AND vendor:Apple",
            },
        ],
    },
    {
        "slug": "components", "name": "Computer Component", "sentence_name": "computer components", "plural": "Computer Components", "icon": "chip",
        "blurb": "Graphics cards, processors and other parts.",
        "sell_intro": "Upgraded your PC? Graphics cards, processors and other components can be worth bringing in. Call ahead to ask about specific parts.",
        "buy_intro": "Pre-owned PC components listed individually with photos of the actual part.",
        "factors": ["Exact part and model", "Whether it's been tested and works", "Physical condition", "Current demand"],
        "query": "product_type:\"Computer Components\"",
    },
]

# ---------------------------------------------------------------------------
# FAQ. pending=True shows a flag instead of an answer until Timothy confirms.
# ---------------------------------------------------------------------------
SELL_FAQS = [
    ("What electronics does Cash4Tech buy?",
     "Phones (iPhone and Android), tablets and iPads, laptops, desktop computers, gaming consoles and accessories, smartwatches and computer components. "
     "We can't accept every device. It depends on the model, condition and demand. See <a href=\"{{base}}sell/\">what we buy</a> or call to ask about yours.", False),
    ("How will I be paid?", "In cash, at the store, once you accept an offer.", False),
    ("How are offers determined?",
     "We evaluate each device in person, looking at the model, specs, physical condition, how well it works, its age and current resale demand. Prices aren't set in advance.", False),
    ("Can I decline an offer?", "Yes. You're always free to decline and take your device home.", False),
    ("Can I get a quote online?", "Not at this time. Offers are made in person at the store after we've looked at the device.", False),
    ("Can I mail my device in?", "No. We only buy devices in person at our Gladstone store.", False),
    ("What should I do before selling my phone?",
     "Back up your data, sign out of your accounts (turn off Find My iPhone, or remove your Google account), know your passcode, and remove your SIM card. Each <a href=\"{{base}}sell/phones/\">device page</a> has specific tips.", False),
    ("Do I need identification to sell?", None, True),
    ("Do you buy damaged or cracked devices?", None, True),
    ("Can I sell a carrier-locked or financed phone?", None, True),
]

BUY_FAQS = [
    ("Are the photos of the actual device?", "Yes. Every listing is one specific device, and the photos are of that device, not stock images.", False),
    ("Why are there several listings for the same model?",
     "Used devices differ: storage, color, battery health and cosmetic condition. Each physical device gets its own listing so you know exactly what you're getting.", False),
    ("What's your return policy?",
     "You can return an item within 30 days. The buyer pays return shipping. There's no separate product warranty.", False),
    ("Return policy details", None, True),
    ("How much is shipping?", None, True),
]
