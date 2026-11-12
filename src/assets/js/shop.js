// Cash4Tech — Buy Electronics.
// Reads products from Shopify's Storefront API (read-only). Never writes inventory.
// Config comes from window.C4T_SHOP, generated from content.py.
(function () {
  var cfg = window.C4T_SHOP || {};
  var live = !!(cfg.domain && cfg.token);
  var base = (document.querySelector('link[rel="stylesheet"][href*="assets/css"]') || {}).getAttribute
    ? document.querySelector('link[rel="stylesheet"][href*="assets/css"]').getAttribute('href').replace('assets/css/site.css', '')
    : './';

  function gql(query, variables) {
    return fetch('https://' + cfg.domain + '/api/' + cfg.version + '/graphql.json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Shopify-Storefront-Access-Token': cfg.token },
      body: JSON.stringify({ query: query, variables: variables })
    }).then(function (r) { return r.json(); }).then(function (j) {
      if (j.errors) throw new Error(j.errors[0].message);
      return j.data;
    });
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function sized(u, w) { return esc(u) + (String(u).indexOf('?') > -1 ? '&amp;' : '?') + 'width=' + w; }

  function money(m) {
    if (!m) return '';
    var n = Number(m.amount);
    try { return new Intl.NumberFormat('en-US', { style: 'currency', currency: m.currencyCode }).format(n); }
    catch (e) { return '$' + n.toFixed(2); }
  }

  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="7" y="2" width="10" height="20" rx="2.5"/><path d="M11 18h2"/></svg>';

  function card(p) {
    var img = p.featuredImage
      ? '<img src="' + sized(p.featuredImage.url, 600) + '" alt="' + esc(p.featuredImage.altText || p.title) + '" loading="lazy">'
      : ICON;
    return '<a class="card product" href="' + base + 'buy/item/?h=' + encodeURIComponent(p.handle) + '">' +
      '<div class="ph">' + img + '</div>' +
      '<div class="body"><h3>' + esc(p.title) + '</h3>' +
      (p.productType ? '<div class="specs"><span>' + esc(p.productType) + '</span>' + (p.vendor ? '<span>' + esc(p.vendor) + '</span>' : '') + '</div>' : '') +
      '<div class="price">' + money(p.priceRange && p.priceRange.minVariantPrice) + '</div>' +
      (p.availableForSale ? '' : '<div class="sold">Sold</div>') +
      '</div></a>';
  }

  function sampleCards(name, n) {
    var grades = ['Excellent', 'Good', 'Fair'];
    var out = '';
    for (var i = 0; i < n; i++) {
      out += '<article class="card product"><div class="ph">' + ICON + '<span class="badge badge-gray">Sample</span></div>' +
        '<div class="body"><h3>' + esc(name) + ' (sample listing)</h3>' +
        '<div class="specs"><span>Unit #' + (1001 + i) + '</span><span>Condition: ' + grades[i % 3] + '</span></div>' +
        '<div class="channels">Real photos of this exact device appear here</div>' +
        '<div class="price">$&nbsp;—</div></div></article>';
    }
    return out;
  }

  var LIST_Q = 'query($q:String!,$n:Int!){products(first:$n,query:$q,sortKey:CREATED_AT,reverse:true){nodes{handle title productType vendor availableForSale featuredImage{url altText} priceRange{minVariantPrice{amount currencyCode}}}}}';

  function fetchList(q, n) {
    var query = (q ? '(' + q + ') AND ' : '') + 'available_for_sale:true';
    return gql(LIST_Q, { q: query, n: n }).then(function (d) { return d.products.nodes; });
  }

  function fill(grid, q) {
    var n = parseInt(grid.getAttribute('data-limit') || '24', 10);
    if (!live) { grid.innerHTML = sampleCards(grid.getAttribute('data-sample') || 'Device', 3); return; }
    var fb = grid.getAttribute('data-fallback');
    fetchList(q, n).then(function (items) {
      return (items.length || !fb) ? items : fetchList(fb, n);
    }).then(function (items) {
      grid.innerHTML = items.length ? items.map(card).join('')
        : '<p class="muted">Nothing in stock here right now. New devices come in all the time, so check back soon or call ' +
          '<a href="' + cfg.phoneHref + '">' + esc(cfg.phone) + '</a>.</p>';
    }).catch(function () {
      grid.innerHTML = '<p class="muted">Products couldn\'t be loaded right now. Please try again shortly.</p>';
    });
  }

  document.querySelectorAll('.product-grid').forEach(function (grid) {
    if (grid.hasAttribute('data-search')) {
      var term = new URLSearchParams(location.search).get('q') || '';
      var input = document.getElementById('q');
      if (input) input.value = term;
      if (!term) { grid.innerHTML = '<p class="muted">Type what you\'re looking for above.</p>'; return; }
      fill(grid, '"' + term.replace(/"/g, '') + '"');
    } else {
      fill(grid, grid.getAttribute('data-query') || '');
    }
  });

  // Product page
  var pd = document.getElementById('product');
  if (!pd) return;
  var handle = new URLSearchParams(location.search).get('h');
  if (!live || !handle) {
    pd.innerHTML = '<div><div class="gallery-main">' + ICON + '</div></div><div><span class="badge badge-gray">Sample</span>' +
      '<h1 style="font-size:2rem">Product page preview</h1><p class="pd-price">$&nbsp;—</p>' +
      '<p class="pd-desc">Once Shopify is connected, this page shows one specific device: all of its real photos, its storage, color, condition notes and price, straight from the Shopify listing the ERP created.</p>' +
      '<a class="btn btn-purple" href="' + cfg.phoneHref + '" data-track="click_to_call">Call about a device</a></div>';
    return;
  }
  var ITEM_Q = 'query($h:String!){product(handle:$h){title vendor productType descriptionHtml availableForSale images(first:12){nodes{url altText}} variants(first:1){nodes{id availableForSale price{amount currencyCode}}}}}';
  gql(ITEM_Q, { h: handle }).then(function (d) {
    var p = d.product;
    if (!p) { pd.innerHTML = '<p>This device is no longer listed. <a href="' + base + 'buy/">Browse what\'s in stock</a>.</p>'; return; }
    document.title = p.title + ' | Cash4Tech';
    var imgs = p.images.nodes;
    var v = p.variants.nodes[0];
    var main = imgs[0] ? '<img id="pd-main" src="' + sized(imgs[0].url, 1000) + '" alt="' + esc(imgs[0].altText || p.title) + '">' : ICON;
    var thumbs = imgs.length > 1 ? '<div class="thumbs">' + imgs.map(function (im, i) {
      return '<button type="button" data-src="' + sized(im.url, 1000) + '" aria-current="' + (i === 0) + '"><img src="' + sized(im.url, 150) + '" alt=""></button>';
    }).join('') + '</div>' : '';
    var buy;
    if (!p.availableForSale) buy = '<p class="sold">This device has sold.</p>';
    else if (cfg.checkout) buy = '<button class="btn btn-green" id="add-to-cart" data-variant="' + esc(v.id) + '">Add to cart</button>';
    else buy = '<p class="muted">Online checkout is coming soon. To ask about this device, call us.</p>' +
      '<a class="btn btn-purple" href="' + cfg.phoneHref + '" data-track="click_to_call">Call ' + esc(cfg.phone) + '</a>';
    pd.innerHTML = '<div><div class="gallery-main">' + main + '</div>' + thumbs + '</div>' +
      '<div><span class="eyebrow">' + esc([p.vendor, p.productType].filter(Boolean).join(' · ')) + '</span>' +
      '<h1 style="font-size:clamp(1.7rem,4vw,2.4rem)">' + esc(p.title) + '</h1>' +
      '<p class="pd-price">' + money(v && v.price) + '</p>' + buy +
      '<div class="pd-desc mt-3">' + (p.descriptionHtml || '') + '</div></div>';
    pd.addEventListener('click', function (e) {
      var b = e.target.closest('.thumbs button');
      if (!b) return;
      document.getElementById('pd-main').src = b.getAttribute('data-src');
      pd.querySelectorAll('.thumbs button').forEach(function (x) { x.setAttribute('aria-current', x === b); });
    });
    // Checkout handoff: only active when the owner has enabled payments (content.py checkout_enabled).
    var atc = document.getElementById('add-to-cart');
    if (atc) atc.addEventListener('click', function () {
      atc.disabled = true;
      gql('mutation($v:ID!){cartCreate(input:{lines:[{merchandiseId:$v,quantity:1}]}){cart{checkoutUrl}}}', { v: atc.getAttribute('data-variant') })
        .then(function (d) { location.href = d.cartCreate.cart.checkoutUrl; })
        .catch(function () { atc.disabled = false; });
    });
  }).catch(function () {
    pd.innerHTML = '<p class="muted">This product couldn\'t be loaded right now. Please try again shortly.</p>';
  });
})();
