# Analytics Events Implementation Plan (v1)

> Owner: Max Espinoza (rmax.ai)    Last updated: 2026-01-10

Summary
- Implement the instrumentation described in `.agent/docs/analytics-events.md` across the docs site.

Progress
- Branch `instrument/analytics-events` created.
- Analytics helper `docs/assets/js/analytics.js` added and included across canonical pages.
- Data attributes added to header nav and index CTA cards (`data-simple-nav-item`, `data-simple-event`, `data-cta-id`, `data-host`).
- Playwright test skeleton added under `tests/` to assert basic events in debug mode.

Next: finish unit tests if needed, expand Playwright tests for downloads and mailto, and add QA checklist.
- Deliver a small, well-tested analytics helper that captures the events, sanitizes metadata for privacy, and reliably forwards events to Simple Analytics (or a test proxy) for verification.

Goals (from spec)
- Measure which site surfaces drive reader → collaborator intent.
- Capture outbound interest and artifact downloads without exploding taxonomy.
- Guard taxonomy drift with a single source of truth and a lightweight deprecation workflow.

Scope
- Instrument the following events: `click_contact_email`, `click_nav`, `click_cta`, `click_outbound`, `download_asset`.
- Add markup (data attributes) to canonical docs pages and a site-wide JS helper that:
  - uses delegated click handling,
  - extracts and normalizes metadata per spec,
  - sends events to the analytics endpoint (Simple Analytics) or to a test proxy during CI/E2E.

Out of scope (for this plan)
- Complex server-side instrumentation or analytics schema changes outside of the events listed above.
- Building an internal analytics dashboard beyond verifying data in Simple Analytics and a short-lived debug view.

Deliverables
1. analytics helper JS (docs/assets/js/analytics.js or similar) included across docs pages
2. Markup updates to site pages: header nav, index CTA cards, high-signal outbound links, annotated downloads
3. Unit tests for helper utilities (extract host, extract file, parse mailto, normalize enums)
4. Playwright E2E tests that intercept analytics requests and assert payloads
5. A short QA checklist and a lightweight debug viewer (dev-only) that shows captured events
6. This plan file and a PR checklist to ensure the spec is updated for any future changes

Work breakdown (tasks)

0) Pre-work
- Create a tracking issue: "Implement analytics events (based on .agent/docs/analytics-events.md)" and reference this plan.
- Create branch `instrument/analytics-events`.

1) Add data attributes to content (low-risk, content changes)
- Files to change (examples):
  - docs/index.html (CTA cards)
  - docs/paper.html, docs/report.html, docs/appendix.html, docs/briefs.html (header nav and page-level anchors)
- Tasks per element type:
  - Header nav & TOC anchors: add `data-simple-nav-item` with one of: `summary`, `paper`, `report`, `appendix`, `briefs`.
  - CTA cards on index: add `data-simple-event="click_cta"` + `data-cta-id` (`paper_card`, `report_card`, `appendix_card`, `executive_brief_card`, `repo_card`).
  - High-signal outbound links: add explicit `data-simple-event="click_outbound"` + `data-host` where helpful (e.g., GitHub repo links).
  - Downloads: annotate non-standard artifacts with `data-simple-event="download_asset"` + `data-file` + `data-type`.
- Acceptance check: HTML changes are present in the branch and pass HTML linting (if available).

2) Implement analytics helper (core work)
- Create `docs/assets/js/analytics.js` (or vendor folder):
  - Single delegated `document.addEventListener('click', handler, true)` or similar to capture interactions.
  - Handler behavior:
    - Find nearest element with `data-simple-event` OR for nav/mailto/downloads, use heuristic fallbacks (mailto detection, extension-based download detection, host-based outbound detection).
    - Normalize metadata keys per spec:
      - `click_contact_email`: `email` (string, optional) – consider default redaction of local-part for privacy (capture domain only by default; configurable).
      - `click_nav`: `item` (enum: summary|paper|report|appendix|briefs) – read from `data-simple-nav-item`.
      - `click_cta`: `cta_id` – read from `data-cta-id`.
      - `click_outbound`: `host` (lowercased, strip leading www.), `path` (optional) – prefer `data-host` if present; otherwise parse `href`.
      - `download_asset`: `file` (pathname + search), `type` (enum derived from extension or `data-type`).
    - Send events to analytics transport:
      - In production: use Simple Analytics (via their recommended send method) or use `navigator.sendBeacon`/`fetch` to a proxy endpoint that forwards to SA.
      - In dev/test: write to console and (optionally) to a local stub endpoint for Playwright to assert against.
    - Keep implementation resilient (no uncaught exceptions when parsing malformed URLs or non-anchor elements).
    - Expose a debug mode: `window.__SIMPLENALYTICS_DEBUG__ = true` to log events and show them in a short-lived in-page debug viewer.
- Example helper (simplified):

```js
// extract helper examples
function normalizeHost(h) {
  return h.replace(/^www\./i, '').toLowerCase();
}

function fileTypeFromPath(path) {
  return path.split('.').pop().toLowerCase();
}

function sendEvent(name, payload) {
  // In production: send to Simple Analytics
  // For tests: send to /__analytics_mock (Playwright will intercept)
  if (window.__SIMPLENALYTICS_DEBUG__) console.debug('event', name, payload);
  try {
    const body = JSON.stringify({ name, payload, url: location.pathname });
    navigator.sendBeacon('/__analytics_collect', body) || fetch('/__analytics_collect', { method: 'POST', body, headers: { 'Content-Type': 'application/json' } });
  } catch (err) {
    console.warn('analytics send failed', err);
  }
}

// delegated click handler (sketch)
document.addEventListener('click', (ev) => {
  const el = ev.target.closest('a,button,[data-simple-event]');
  if (!el) return;
  // derive event name/metadata and call sendEvent(name, payload)
});
```

- Acceptance check: Helper is bundled or included across pages and does not break site behavior; helper code is covered by unit tests for parsing and normalization.

3) Tests
- Unit tests (Jest/Vitest): test small pure functions:
  - parseMailtoHref -> returns sanitized email/domain
  - extractHost -> lowercasing and www stripping
  - determineFileType -> handles query strings and unknown extensions
- Playwright E2E tests (tests/analytics.spec.ts):
  - Start site in dev.
  - Intercept calls to `/__analytics_collect` (or SA endpoint) and assert events for:
    - nav click events (header nav)
    - index CTA clicks with cta_id
    - outbound link click with host/path
    - download click resolves `file` and `type`
    - mailto click emits `click_contact_email` and payload follows privacy policy (domain-only unless config enabled)
- Acceptance check: Tests pass in CI / locally. The Playwright test asserts exact event names and presence of required fields.

4) QA & staging verification
- Add a staging smoke test: click several high-signal elements, verify events appear in Simple Analytics Events Explorer with expected keys.
- Provide a short QA guide in the PR description for reviewers to reproduce locally (enable debug mode, open debug viewer and click elements).
- Monitor for a few days post-release and watch for unexpected event names or attribute distributions.

5) Release & rollout
- Merge to main once unit and E2E tests pass and a reviewer verifies the HTML and helper.
- Deploy to staging, verify SA events in events explorer.
- Deploy to production.
- Observe for a week (or defined monitoring window) and ensure no event drift.

6) Versioning & deprecation workflow (enforced by the spec)
- Any new event name or metadata key requires updating `.agent/docs/analytics-events.md` before merge.
- Keep prior event names/attributes emitted for at least two weeks after announcing a change; add a migration note to the spec (e.g., "click_cta_v2 introduced on YYYY-MM-DD, old event retired on YYYY-MM-DD").

Acceptance criteria
- All five event types are emitted with the expected metadata when interacting with instrumented elements.
- Unit and E2E tests exist and pass in CI.
- Events are visible in Simple Analytics with the expected keys.
- The repository contains the code, tests, and a short QA guide; PR updates `.agent/docs/analytics-events.md` if any change to the taxonomy occurred.

Estimates (rough)
- HTML markup changes: 1–2 hours
- Analytics helper implementation + unit tests: 4–8 hours
- Playwright E2E tests and CI integration: 4–6 hours
- QA + staging verification + deploy: 2–4 hours
- Total: 1–2 developer days (depending on SA access and CI setup)

PR checklist (for reviewers)
- [ ] Does the change include a spec update if event names/keys changed?
- [ ] Are data attributes added consistent with `.agent/docs/analytics-events.md`?
- [ ] Is the analytics helper resilient and privacy-conscious (no PII by default)?
- [ ] Do unit tests cover parsing/normalization logic?
- [ ] Do Playwright tests exercise the real send path (stubbed in tests) and assert expected payloads?
- [ ] Does the deploy plan include verification steps for SA?

Risks & mitigations
- Missing events due to content not annotated: mitigate by fallback heuristics (e.g., outbound host detection and extension-based download detection) and add a debug viewer to spot gaps.
- Accidental PII capture: default to redacting local-parts of email addresses and require explicit approval to capture full emails.
- Event schema drift: strictly require spec updates and owner sign-off (Max Espinoza) in PRs.

Follow-ups / Nice-to-haves
- Short-lived debug page that shows recent events (dev mode) to speed QA.
- A small backing endpoint (in a developer-only namespace) to store and search recent events for debugging beyond SA's UI.
- Regular (monthly) audit to confirm that events in SA still match the spec.

-----

Notes: This plan is intentionally tactical and minimal: prefer data attributes + a single site helper + reliable tests. If you want I can:
- open the tracking issue and create the feature branch,
- or generate the initial analytics helper file and a Playwright test skeleton.


(End of plan)
