# Analytics Events Spec (v1)

> Owner: Max Espinoza (rmax.ai)    Last updated: 2026-01-10  
> Version: 2026.01.10

## Goals
1. Measure which site surfaces drive reader → collaborator intent (Summary, Paper, Report, Appendix, Briefs → GitHub / contact).
2. Capture outbound interest (GitHub, rmax.ai, X, LinkedIn) and artifact downloads without exploding the taxonomy.
3. Guard taxonomy drift with a single source of truth and a lightweight deprecation workflow.

## Event reference

### `click_contact_email`
- **Trigger:** User activates any `mailto:` link for rmax.ai addresses (e.g., `hello@rmax.ai`, `contact@rmax.ai`). Automated click handler watches `mailto:` URIs and flags them once per interaction.
- **Metadata**
  - `email` (string, optional) – populated with the address in the clicked URI.
- **Notes:** The docs site currently does not expose mailto links; this event captures contact intent across the rmax.ai ecosystem when present.

### `click_nav`
- **Trigger:** Header nav or in-page anchor clicks that guide readers to the site’s primary pages (Summary, Paper, Report, Appendix, Briefs).
- **Metadata**
  - `item` (enum): `summary`, `paper`, `report`, `appendix`, `briefs`.
- **Notes:** Add `data-simple-nav-item` to header and TOC anchors so nav clicks map consistently to the taxonomy. Example:

```
<a href="paper.html" data-simple-nav-item="paper">Paper</a>
```

### `click_cta`
- **Trigger:** High-signal CTAs beyond baseline nav. On this site, these are the index "Key Artifacts" cards and other prominent action links (e.g., Research Paper card, Technical Report card, GitHub repository card).
- **Metadata**
  - `cta_id` (enum): `paper_card`, `report_card`, `appendix_card`, `executive_brief_card`, `board_brief_card`, `repo_card`.
- **Notes:** Only add a new `cta_id` when the CTA has measurable downstream outcomes; document the new value in this spec before deployment. Example:

```
<a href="paper.html" data-simple-event="click_cta" data-cta-id="paper_card">Research Paper</a>
```

### `click_outbound`
- **Trigger:** Clicks that resolve to a hostname external to the docs site (canonical docs host: `system-prompts-forensics.rmax.ai`). Outbound destinations include `github.com`, `rmax.ai`, `x.com`, `linkedin.com`, etc.
- **Metadata**
  - `host` (string, lowercased, without leading `www.`) – e.g., `github.com`.
  - `path` (string, optional) – useful for distinguishing a repo or file path (e.g., `/rmax-ai/system-prompts-forensics`).
- **Notes:** Annotate high-signal links when the host alone is ambiguous. Example:

```
<a href="https://github.com/rmax-ai/system-prompts-forensics" data-simple-event="click_outbound" data-host="github.com">GitHub Repository</a>
```

### `download_asset`
- **Trigger:** Clicks on links whose resolved path ends in a stable download extension (`.pdf`, `.zip`, `.png`, `.svg`, etc.). On this site, assets include images used in pages and high-value repository files (e.g., `CITATION.cff`).
- **Metadata**
  - `file` (string) – the pathname plus search string of the target asset.
  - `type` (enum): `pdf`, `zip`, `gz`, `tar`, `csv`, `tsv`, `xlsx`, `xls`, `pptx`, `ppt`, `docx`, `doc`, `png`, `jpg`, `jpeg`, `svg`, `cff`, `md`, `txt`.
- **Notes:** Use `data-simple-event="download_asset"` for non-standard extensions to ensure reliable typing. Example:

```
<a href="https://github.com/rmax-ai/system-prompts-forensics/blob/main/CITATION.cff" data-simple-event="download_asset" data-file="/rmax-ai/system-prompts-forensics/CITATION.cff" data-type="cff">View CITATION.cff</a>
```

## Implementation guidance for docs site
- Header nav: add `data-simple-nav-item` to these anchors: `index.html` (`summary`), `paper.html` (`paper`), `report.html` (`report`), `appendix.html` (`appendix`), `briefs.html` (`briefs`).

Implementation note: the analytics helper `docs/assets/js/analytics.js` has been added and included across canonical pages. The helper exposes a dev-only debug mode (`window.__SIMPLENALYTICS_DEBUG__`) which writes events to `window.__SIMPLENEVENTS__` and shows a short-lived in-page debug viewer to speed QA.
- CTA cards on index: add `data-simple-event="click_cta"` + `data-cta-id` with one of the enumerated values.
- Outbound links (header/footer/repo links): automated host detection is generally sufficient, but prefer explicit `data-simple-event="click_outbound"` + `data-host` for high-signal destinations.
- Downloads: annotate non-standard or high-value artifacts with `data-simple-event="download_asset"` and `data-file`/`data-type`.
- On-page anchors (e.g., briefs TOC `#executive`, `#board`): annotate with `data-simple-nav-item` if you want per-section counts; otherwise rely on page-level `click_nav`.

## Page → event mapping (quick reference)
- index.html (Summary): header nav clicks → `click_nav` / `summary`; cards → `click_cta` (`paper_card`, `report_card`, `appendix_card`, `executive_brief_card`, `repo_card`).
- paper.html: header nav → `click_nav` / `paper`; outbound links to GitHub → `click_outbound`.
- report.html: header nav → `click_nav` / `report`.
- appendix.html: header nav → `click_nav` / `appendix`; PGP anchors may be instrumented for per-primitive interest.
- briefs.html: header nav → `click_nav` / `briefs`; section anchors (`#executive`, `#board`) optionally instrumented.

## Versioning & deprecation
1. **Schema changes:** Any new event name or metadata key requires this document to be updated before merging; reference the revision in the PR description.
2. **Deprecation policy:** Keep prior event names and attributes in the DOM and event queue for at least two weeks after announcing changes; add a migration note to this spec (e.g., "`click_cta_v2` introduced on YYYY-MM-DD, old event retired on YYYY-MM-DD").
3. **Validation guardrails:** Use the simple analytics helper (`click` listener + `data-simple-event` attributes) to keep event names consistent. Before release verify that the new event surfaces in the Simple Analytics Events Explorer with the expected metadata keys.

## Operational notes
- **Event ownership:** Max Espinoza (rmax.ai) is the steward for analytics instrumentation. File an issue or PR if you encounter regressions or need new event types.
- **Drift protection:** This file is the canonical taxonomy; insist on updates during code review before introducing new `data-simple-event` values or automated handlers.
- **Privacy:** The site uses Simple Analytics (privacy-first). Avoid collecting PII as event metadata and prefer host/path/file identifiers over user information.

