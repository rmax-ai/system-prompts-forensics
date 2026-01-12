Title: Implement analytics events (based on .agent/docs/analytics-events.md)

Owner: @rmax

Description:
Implement the analytics instrumentation across the docs site according to the spec in `.agent/docs/analytics-events.md`.

Acceptance criteria:
- `docs/assets/js/analytics.js` exists and is included on canonical pages
- Header nav has `data-simple-nav-item` attributes
- Index CTA cards have `data-simple-event="click_cta"` and `data-cta-id`
- High-signal outbound links annotated with `data-simple-event="click_outbound"` and `data-host`
- Tests exist under `tests/` that assert the basic events in debug mode

Notes:
- Dev debug mode writes events to `window.__SIMPLENEVENTS__` for easy Playwright assertions.
- See `.agent/plans/analytics-events.plan.md` for implementation plan and QA checklist.
