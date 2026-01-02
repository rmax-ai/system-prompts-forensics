AGENTS.md — System Prompt Forensics (agent knowledge base)

Purpose (TL;DR)

- This repository treats captured "system prompts" as governance constitutions and provides artifacts, schemas, and scripts to normalize, analyze, and compare them across tools (IDE assistants, CLIs, agent frameworks).
- Primary outputs: normalized YAML analyses (schema v0), a taxonomy of prompt architectures, annotated prompt analyses, composable prompt primitives, and a canonical agent constitution prompt.

Quick facts

- Scope: VS Code Copilot, Codex CLI, Copilot CLI, OpenCode CLI, and similar tools
- Artifacts: raw HTTP request captures (data/raw), JSON payloads (data/payload), schema & normalization prompt (data/schema, data/prompts), analysis scripts (data/scripts)
- Safety: Do NOT reproduce proprietary prompts verbatim. Redact sensitive headers before publishing. Refuse to assist with or analyze clearly malicious code.

Data & artifacts (where to look)

- data/raw/\*.request — raw mitmproxy HTTP captures (MUST be redacted before public sharing)
- data/payload/\*.json — JSON payloads produced from raw requests (see data/Makefile)
- data/prompts/normalize-system-prompt.md — normalization instructions used to drive model-based analysis
- data/schema/system-prompt.v0.yaml — canonical normalization schema (metadata, layers, analysis, provenance)
- data/scripts/system-prompt-analysis.py — helper that runs normalization using an LLM
- data/scripts/redact-headers.sh — required redaction of known sensitive headers
- data/scripts/parse-headers.sh — helper to inspect header names
- backup/ — archival copies of captures

Processing scripts & common commands

- Convert raw captures into payloads:
  - make -C data all
- Redact sensitive headers before processing or committing:
  - data/scripts/redact-headers.sh raw/example.request > raw/example.redacted.request
- Run a normalization analysis (example):
  - python data/scripts/system-prompt-analysis.py \
    --prompt data/prompts/normalize-system-prompt.md \
    --schema data/schema/system-prompt.v0.yaml \
    --invocation data/payload/<artifact>.json \
    --model gpt-5.2
- Quick checks:

  - jq . data/payload/<artifact>.json # validate JSON
  - yq eval . data/analysis/<artifact>.yaml # validate YAML (recommended) Normalization rules (agent-facing summary)

- Treat the system prompt as a governance constitution (who the agent is, authority, scope, tools, constraints, termination).
- Prefer structure over wording: map content into schema fields rather than quoting long prose.
- Prohibitions take precedence over permissions.
- Record implicit assumptions in analysis.implicit_assumptions and conspicuous missing items under analysis.notable_absences.
- Do NOT invent tools, privileges, or guarantees not supported by the payload.
- The normalization prompt enforces strict output rules: a single fenced YAML document only — remove fencing when saving to disk.

Output conventions & storage

- Normalized analyses must conform to data/schema/system-prompt.v0.yaml.
- Recommended storage path: data/analysis/<payload_basename>.analysis.yaml (create data/analysis/ if absent).
- Each analysis should include provenance fields: source_references (point to raw and payload files, but never include sensitive verbatim text), redactions_applied (boolean), artifact_hash, model (name/version), and timestamp.

Safety & governance (non-negotiable)

- DO NOT commit raw captures containing secrets or tokens. Always redact using data/scripts/redact-headers.sh before committing any real captures.
- DO NOT reproduce proprietary prompt text verbatim in public outputs. Use summarized or redacted excerpts and reference provenance only.
- REFUSE work on tasks involving clearly malicious code, or requests to bypass safeguards or jailbreak models.

Suggested research workflow (concise)

1. Capture: add raw/\*.request (or place raw capture in data/raw/). Treat as sensitive by default.
2. Redact: run data/scripts/redact-headers.sh and keep a redacted copy.
3. Convert: run make -C data to generate payload/\*.json.
4. Normalize: run system-prompt-analysis.py with the canonical prompt and schema (temperature=0 recommended for deterministic structure).
5. Validate: parse the output YAML, run schema/YAML checks, and add provenance metadata.
6. Store: save to data/analysis/ with consistent naming and commit only redacted artifacts and analyses.
7. Compare / synthesize: run pairwise diffs across normalized YAML to surface architectural trade-offs and update taxonomy/primitives.

Agent behavior guidelines (how an agent should act in this repo)

- Be surgical: make minimal edits and prefer adding small, well-documented analysis files over large rewrites.
- Be explicit: when you infer something, add it to analysis.implicit_assumptions with a brief rationale.
- Be conservative about exposure: never print or commit secrets; prefer hashes and redaction flags in provenance.
- Use repository tools (Makefile, scripts) rather than re-implementing parsing logic.
- If making changes that affect repository state (new analyses, scripts), ask for confirmation before committing or pushing.

Script development guidelines (robustness & debuggability)

- **Fail loudly**: Scripts must exit with a non-zero status code on error. Never catch exceptions without re-raising or logging a terminal error message.
- **Structured CLI**: Use `argparse` for all scripts. Include a `--verbose` or `--debug` flag to surface internal state and LLM raw responses.
- **Input validation**: Explicitly check for the existence of input files and validate formats (JSON/YAML) before processing.
- **Logging**: Use `logging` or print to `stderr` for status updates and errors. Keep `stdout` clean for primary data output (or use `--output` files).
- **Type safety**: Use Python type hints to improve maintainability and catch common bugs early.
- **No silent skips**: If a script is processing multiple files and one fails, it should either halt or clearly report the failure in the final summary/exit code.

Temperature guidelines

- **Record-producing scripts** → `temperature = 0` (mandatory): Use for extraction, normalization, reduction, validation, audits, registries, or any artifact that is versioned, diffed, hashed, or fed into automation. Determinism is an invariant.
- **Structured analysis scripts** → `temperature = 0.1–0.3` (optional): Use for summaries, reports, or explanations derived from fixed inputs where structure and facts must remain stable, but phrasing may vary slightly.
- **Exploratory or generative scripts** → `temperature ≥ 0.5` (intentional): Use for ideation, hypothesis generation, alternative designs, naming, or speculative synthesis where coverage and novelty matter more than reproducibility.

Makefile guidelines (automation & reproducibility)

- **Use `uv run`**: Always execute Python scripts via `uv run --locked` to ensure dependency consistency.
- **Configurable variables**: Use variables for models (`ANALYSIS_MODEL`) and flags (`DRY_RUN`) to allow easy overrides from the CLI.
- **Pattern rules**: Use pattern rules (e.g., `%.analysis.yaml: payload/%.json`) for scalable file transformations.
- **Directory management**: Use `@mkdir -p $(dir $@)` within rules to ensure output directories exist before writing.
- **Comprehensive `clean`**: The `clean` target must remove all generated artifacts to allow for a fresh state.
- **Dynamic file lists**: Use `$(wildcard ...)` and `$(patsubst ...)` to automatically pick up new payloads or analyses.

Quality checks & automation hints

- Add CI that validates: payload JSON parseability, analysis YAML parseability, and presence of provenance fields (recommended future step).
- Ensure system-prompt-analysis.py runs with deterministic settings (temperature=0) and log the model response and metadata for reproducibility.

Where to look for examples

- data/payload contains many sample payloads (copilot._, codex._, opencode.\*) that are good starting points for case studies.
- data/prompts/normalize-system-prompt.md shows strict normalization rules that the model must follow.
- data/schema/system-prompt.v0.yaml is the schema to map analyses to.

If you're stuck

- Check git history (git log) to find earlier analyses and who worked on them.
- Ask a human maintainer before committing sensitive data or performing irreversible operations.

Notes

- This repository focuses on architecture and governance, not on extracting or publishing proprietary content. Keep that distinction clear in analyses and outputs.

(End of AGENTS.md)
