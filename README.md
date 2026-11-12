# Cash4Tech website (demo)

Demo of getcash4tech.com for Cash4Tech, Inc. in Gladstone, MO.

- **Sell Your Tech** (`/sell/...`): landing pages that bring local sellers into the store (cash offers, in person).
- **Buy Electronics** (`/buy/...`): reads the live Shopify catalog. The ERP already creates one Shopify product per physical device, and this site only reads it.

**Live preview:** https://jobs127.github.io/cash4tech-site/ · **Roadmap:** https://jobs127.github.io/cash4tech-site/roadmap/

## Editing
Everything editable lives in **`content.py`**:
- `BUSINESS`: address, hours, email and links. `None` shows as a yellow ⚑ flag.
- `SHOPIFY`: store domain plus a Storefront API **public** token (read-only). Never put an Admin API token here.
- `TAXONOMY`: category → brand → model. Each entry creates a Sell page and a Buy page. Add a model in a few lines, then rebuild. `query` is the Shopify product search for that Buy page.
- `SELL_FAQS` / `BUY_FAQS`.

```
python3 build.py     # regenerates docs/ (served by GitHub Pages: main /docs)
```

## Ground rules (from Cash4Tech)
- Don't activate Shopify Payments or any live payment processing. `checkout_enabled` stays `False` until the owner turns payments on.
- Don't modify the ERP or its Shopify sync. The site never writes inventory.
- No online quotes, mail-in or online payment to sellers. Sellers are paid in cash, in store.
- DNS lives in Cloudflare. Keep the Gmail MX, SPF, DKIM and DMARC records untouched.

## Before launch
Fill in the ⚑ items, add the Shopify token, match each `query` to the ERP's product types, vendors and tags, add the logo, set `GTM_ID`, set `DEMO = False`, and then point the domain.
