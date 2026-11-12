# Cash4Tech website (demo)

Demo of getcash4tech.com for Cash4Tech, Inc. in Gladstone, MO. The focus is getting local sellers through the door (Phase 1), with room to grow into online sales through Shopify.

**Live preview:** https://jobs127.github.io/cash4tech-site/
**Roadmap page:** https://jobs127.github.io/cash4tech-site/roadmap/

## How it's built
- Plain static HTML/CSS/JS with no framework, so it loads fast and hosts anywhere.
- `build.py` generates every page into `docs/`, which GitHub Pages serves.
- Business facts (address, hours, email, eBay and Shopify links) live at the top of `build.py`. Anything left as `None` shows as a yellow ⚑ flag on the site.

```
python3 build.py        # rebuild docs/
```

## Before launch
- Fill in the ⚑ items (address, hours, policies, links) and set `DEMO = False`. That removes the banner and flags and lets search engines index the site.
- Set `SHOPIFY_STORE_URL` and `GTM_ID`.
- Connect the contact form to a form service.
- Point getcash4tech.com at the site.
