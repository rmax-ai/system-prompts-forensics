# Analytics QA Checklist

✅ Steps to verify locally

1. Open `docs/index.html` in a browser (file:// or serve with a local static server).
2. Open the browser console and set `window.__SIMPLENALYTICS_DEBUG__ = true` (or leave unset; the pages set it for `file:`/localhost automatically).
3. Click header nav items (Summary, Paper, Report, Appendix, Briefs) and confirm a `click_nav` event appears in the debug viewer (bottom-right) and in `window.__SIMPLENEVENTS__`.
4. Click CTA cards on the index page and verify `click_cta` events with `cta_id` payloads appear.
5. Click the GitHub repo link and verify a `click_outbound` event with `host: "github.com"` appears.
6. If you add a `mailto:` link in a test page, click it and verify `click_contact_email` is emitted and the email is redacted to domain only unless `window.__SIMPLENALYTICS_CAPTURE_EMAIL__ = true`.

⚙️ Notes

- Debug mode saves events to `window.__SIMPLENEVENTS__` and shows them in a small floating panel. This avoids network requests in local testing and allows Playwright tests to assert events reliably.
- In production, the helper attempts to send events to `window.__SIMPLENALYTICS_COLLECT_PATH__` (defaults to `/__analytics_collect`) using `navigator.sendBeacon` or `fetch` as a fallback.

If anything fails, open an issue and attach a screenshot of the debug viewer and console logs.