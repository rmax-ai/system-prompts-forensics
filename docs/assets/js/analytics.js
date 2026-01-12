// Lightweight analytics helper for the docs site
(function () {
  if (window.__SIMPLE_ANALYTICS_LOADED__) return; // idempotent
  window.__SIMPLE_ANALYTICS_LOADED__ = true;

  // Debug and config flags (can be set before the script loads)
  const DEBUG = Boolean(window.__SIMPLENALYTICS_DEBUG__);
  const CAPTURE_EMAIL_FULL = Boolean(window.__SIMPLENALYTICS_CAPTURE_EMAIL__);
  const COLLECT_PATH = window.__SIMPLENALYTICS_COLLECT_PATH__ || '/__analytics_collect';

  // Helpers
  function normalizeHost(host) {
    try {
      return (host || '').replace(/^www\./i, '').toLowerCase();
    } catch (err) { return host; }
  }

  function fileTypeFromPath(path) {
    if (!path) return undefined;
    try {
      const p = path.split('?')[0];
      const parts = p.split('.');
      if (parts.length < 2) return undefined;
      const ext = parts.pop().toLowerCase();
      // Only treat certain known extensions as downloads to avoid flagging .html pages
      const ALLOWED = new Set(['pdf','zip','gz','tar','csv','tsv','xlsx','xls','pptx','ppt','docx','doc','png','jpg','jpeg','svg','cff','md','txt']);
      return ALLOWED.has(ext) ? ext : undefined;
    } catch (err) { return undefined; }
  }

  function sanitizeEmail(href) {
    // href example: mailto:hello@rmax.ai
    try {
      const m = href.replace(/^mailto:/i, '').split('?')[0];
      if (!m) return undefined;
      if (CAPTURE_EMAIL_FULL) return m;
      const domain = m.split('@').pop();
      return `@${domain}`; // redacted local-part
    } catch (err) { return undefined; }
  }

  function sendEvent(name, payload) {
    const event = { name, payload: payload || {}, url: location.pathname + location.search };
    if (DEBUG) {
      window.__SIMPLENEVENTS__ = window.__SIMPLENEVENTS__ || [];
      window.__SIMPLENEVENTS__.push(event);
      // show in debug UI
      renderDebugEvent(event);
      console.debug('[analytics] event:', event);
      return;
    }

    try {
      const body = JSON.stringify(event);
      if (navigator.sendBeacon) {
        try { navigator.sendBeacon(COLLECT_PATH, body); return; } catch (e) { /* fallthrough */ }
      }
      fetch(COLLECT_PATH, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body }).catch(() => {});
    } catch (err) {
      console.warn('analytics send failed', err);
    }
  }

  // Debug UI
  function renderDebugShell() {
    if (!DEBUG) return;
    if (document.getElementById('__analytics_debug')) return;
    const root = document.createElement('div');
    root.id = '__analytics_debug';
    Object.assign(root.style, {
      position: 'fixed', right: '12px', bottom: '12px', width: '360px', maxHeight: '60vh', overflow: 'auto', zIndex: 99999,
      background: 'rgba(17,24,39,0.95)', color: '#fff', fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto, sans-serif', fontSize: '13px', borderRadius: '8px', padding: '8px', boxShadow: '0 8px 30px rgba(2,6,23,0.4)'
    });
    const header = document.createElement('div');
    header.textContent = 'Analytics Debug (dev only)';
    header.style.fontWeight = '600'; header.style.marginBottom = '6px';
    root.appendChild(header);
    const list = document.createElement('div'); list.id = '__analytics_debug_list'; root.appendChild(list);
    document.body.appendChild(root);
  }

  function renderDebugEvent(evt) {
    if (!DEBUG) return;
    const list = document.getElementById('__analytics_debug_list');
    if (!list) return;
    const el = document.createElement('div');
    el.style.borderTop = '1px solid rgba(255,255,255,0.06)';
    el.style.paddingTop = '8px'; el.style.marginTop = '8px';
    el.innerHTML = `<div style="font-weight:600">${evt.name}</div><div style="opacity:.85;font-size:12px;white-space:pre-wrap;">${JSON.stringify(evt.payload, null, 2)}</div>`;
    list.prepend(el);
  }

  // Event detection
  function findInstrumentedEl(el) {
    if (!el) return null;
    return el.closest('[data-simple-event], [data-simple-nav-item], a[href^="mailto:"], a[href]');
  }

  function handleClick(ev) {
    try {
      const el = findInstrumentedEl(ev.target);
      if (!el) return;
      // preferred explicit event
      const explicit = el.getAttribute && el.getAttribute('data-simple-event');
      if (explicit === 'click_cta') {
        const cta = el.getAttribute('data-cta-id') || el.dataset.ctaId || undefined;
        sendEvent('click_cta', { cta_id: cta });
        return;
      }
      if (explicit === 'click_outbound') {
        const host = normalizeHost(el.getAttribute('data-host') || getHostFromHref(el.getAttribute('href')));
        const path = getPathFromHref(el.getAttribute('href'));
        sendEvent('click_outbound', { host, path });
        return;
      }
      if (explicit === 'download_asset') {
        const file = el.getAttribute('data-file') || getPathFromHref(el.getAttribute('href'));
        const type = el.getAttribute('data-type') || fileTypeFromPath(file);
        sendEvent('download_asset', { file, type });
        return;
      }

      // mailto
      if ((el.tagName || '').toLowerCase() === 'a' && (el.getAttribute('href') || '').toLowerCase().startsWith('mailto:')) {
        const email = sanitizeEmail(el.getAttribute('href'));
        sendEvent('click_contact_email', { email });
        return;
      }

      // nav
      if (el.getAttribute && el.getAttribute('data-simple-nav-item')) {
        const item = el.getAttribute('data-simple-nav-item');
        sendEvent('click_nav', { item });
        return;
      }

      // heuristic: outbound if hostname differs
      if ((el.tagName || '').toLowerCase() === 'a' && el.hostname && normalizeHost(el.hostname) !== normalizeHost(location.hostname)) {
        const host = normalizeHost(el.hostname);
        const path = getPathFromHref(el.getAttribute('href'));
        sendEvent('click_outbound', { host, path });
        return;
      }

      // heuristic: downloads by extension
      if ((el.tagName || '').toLowerCase() === 'a') {
        const href = el.getAttribute('href') || '';
        const ext = fileTypeFromPath(href);
        if (ext) {
          sendEvent('download_asset', { file: getPathFromHref(href), type: ext });
        }
      }
    } catch (err) {
      if (DEBUG) console.error('analytics handler error', err);
    }
  }

  function getHostFromHref(href) {
    try {
      if (!href) return undefined;
      const u = new URL(href, location.href);
      return u.hostname;
    } catch (err) { return undefined; }
  }
  function getPathFromHref(href) {
    try {
      if (!href) return undefined;
      const u = new URL(href, location.href);
      return u.pathname + (u.search || '');
    } catch (err) { return href; }
  }

  // Initialization
  document.addEventListener('click', handleClick, true);
  if (DEBUG) {
    window.__SIMPLENEVENTS__ = window.__SIMPLENEVENTS__ || [];
    renderDebugShell();
  }

  // Expose helpers for tests
  window.AnalyticsHelpers = { normalizeHost, fileTypeFromPath, sanitizeEmail, sendEvent };
})();
