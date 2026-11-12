// Light / dark toggle. Default follows the system; a click saves the visitor's choice.
(function () {
  var btn = document.querySelector('.theme-btn');
  if (!btn) return;
  var root = document.documentElement;
  btn.addEventListener('click', function () {
    var cur = root.getAttribute('data-theme') ||
      (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem('c4t-theme', next); } catch (e) {}
  });
})();

// Cash4Tech — small, dependency-free site script.

// Mobile menu
(function () {
  var btn = document.querySelector('.menu-btn');
  var links = document.getElementById('nav-links');
  if (!btn || !links) return;
  btn.addEventListener('click', function () {
    var open = links.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Conversion tracking hooks.
// Every call, directions, and contact action carries data-track="...".
// Events go to window.dataLayer, ready for Google Tag Manager / GA4 / Google Ads
// once a container ID is added in build.py (GTM_ID).
(function () {
  window.dataLayer = window.dataLayer || [];
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-track]');
    if (!el) return;
    window.dataLayer.push({
      event: el.getAttribute('data-track'),
      link_text: (el.textContent || '').trim().slice(0, 80),
      page_path: location.pathname
    });
  });
})();

// Contact form (demo only: not connected to a backend yet).
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    window.dataLayer.push({ event: 'contact_form_submit_demo' });
    var status = document.getElementById('form-status');
    if (status) status.classList.add('show');
    form.querySelector('button[type="submit"]').disabled = true;
  });
})();

// Shop preview filters.
(function () {
  var bar = document.querySelector('.filters');
  if (!bar) return;
  var items = document.querySelectorAll('[data-cat]');
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    bar.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
    b.setAttribute('aria-pressed', 'true');
    var f = b.getAttribute('data-filter');
    items.forEach(function (it) {
      it.hidden = !(f === 'all' || it.getAttribute('data-cat') === f);
    });
  });
})();

// Footer year
(function () {
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();
