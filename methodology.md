Methodology — System Prompt Forensics

Overview

This document codifies the reproducible workflow we use to: (1) capture raw client invocations, (2) extract the agent invocation payload as structured JSON, (3) run automated normalization and structural analysis with OpenAI (gpt-5.2) using a canonical normalization prompt and schema, and (4) synthesize comparative and final research reports.

Scope

- Clients: IDE assistants (e.g. VS Code Copilot), CLIs (Codex/Copilot/OpenCode), and similar agent-enabled tooling.
- Artifacts: raw HTTP captures, redacted captures, invocation payload JSON, normalized YAML analyses, automated comparison artifacts, and final reports.

High level workflow (one-line steps)

1. Capture raw HTTP requests (data/raw/).
2. Redact sensitive headers and fields (produce redacted artifact alongside raw).
3. Extract invocation payload into structured JSON (data/payload/).
4. Validate payload JSON.
5. Run automated normalization using the canonical normalization prompt + schema with gpt-5.2 (temperature=0).
6. Validate and add provenance to normalized YAML (data/analysis/).
7. Human review & QA.
8. Produce technical comparison report and final research report.

Detailed Procedure

1. Capture

- Methods: proxy interception (mitmproxy), CLI debug output, startup/init logs, and public docs.
- Store raw captures under data/raw/ and name with a clear convention: <tool>-<client>-<mode>-<timestamp>.request
- Record minimal metadata in the capture (tool, version, mode, capture_method, timestamp).

2. Redaction (mandatory)

- Always redact sensitive headers and tokens before any public storage or analysis. Use the repo script:

  data/scripts/redact-headers.sh raw/<artifact>.request > raw/<artifact>.redacted.request

- Keep raw files offline where necessary and mark redactions_applied = true in provenance.
- Use data/scripts/parse-headers.sh to inspect header names where needed.

3. Payload extraction

- Convert redacted captures into structured invocation JSON. The repo provides a Makefile target to produce payload JSONs:

  make -C data all

- The invocation payload should include: messages (system/user/assistant), tool/function declarations, session metadata, client/mode tags, and any relevant headers needed for context.

4. Validate payload JSON

- Quick check: jq . data/payload/<artifact>.json
- Ensure required fields exist (messages array, explicit system/developer messages if present, declared tools/functions). If a payload is malformed, document and fix the parser or note the capture as unusable.

5. Automated normalization & analysis (MODEL RUN)

- Use the canonical normalization prompt and schema to generate a structured analysis. Command example:

  python data/scripts/system-prompt-analysis.py \
   --prompt data/prompts/normalize-system-prompt.md \
   --schema data/schema/system-prompt.v0.yaml \
   --invocation data/payload/<artifact>.json \
   --model gpt-5.2 > data/analysis/<artifact>.analysis.yaml

- Determinism: always run with deterministic settings (temperature=0). Log model metadata (model name, response id, prompt hash/timestamp, any usage information) for reproducibility.
- The normalization prompt enforces strict output rules (single fenced YAML block only). If the model output violates the format, mark the run as failed and route to manual review.

6. Post-processing, provenance & validation

- Validate YAML parseability: yq eval . data/analysis/<artifact>.analysis.yaml
- Add/verify provenance fields in the analysis (source_references pointing at redacted raw & payload, redactions_applied boolean, artifact_hash (sha256 of payload), model, and ISO8601 timestamp). Example provenance keys we require:

  provenance: source_references: ["data/raw/<artifact>.redacted.request","data/payload/<artifact>.json"] redactions_applied: true artifact_hash: <sha256> model: gpt-5.2 timestamp: 2025-12-31T23:59:59Z

- If a model-generated analysis omits required fields, add them programmatically (yq) or manually and document the change in a review note.

7. Human review & QA

- Human reviewer must:
  - Confirm no secrets or proprietary prompt text were leaked in the analysis file.
  - Check analysis.implicit_assumptions entries for plausibility and add rationale where inferred.
  - Note conspicuous absences under analysis.notable_absences.
  - Sign off on the analysis (a short reviewer note is sufficient).

8. Comparative analysis

- Use the normalized analyses in data/analysis/ to compute pairwise diffs, presence/absence matrices, and summary statistics across architectural dimensions (identity, authority, scope, tools exposure, termination, correction mechanisms).
- Recommended outputs:
  - A CSV or matrix of feature presence across artifacts.
  - A short technical comparison report that highlights clusters, outliers, and trade-offs.
- Scripts to automate this are encouraged (examples: scripts/generate-comparison.py) and should be versioned in the repo.

9. Final research report

- Produce a narrative final report that includes:
  - Executive summary and key findings
  - Dataset and methods (capturing, redaction, normalization details)
  - Taxonomy of prompt architectures and primitives
  - Representative case studies and risks
  - Policy/engineering recommendations and a canonical agent constitution prompt
  - Reproducibility appendix (how to re-run the analysis)

Data management, storage & provenance

- Store redacted raw captures in data/raw/ (redacted files only for public commits).
- Store invocation JSON in data/payload/ and analyses in data/analysis/.
- Do NOT commit raw captures with secrets. If raw must be stored for internal use, mark as private and do not push to public repos.
- Each analysis must include provenance (see above).

Safety, ethics & legal considerations

- DO NOT reproduce proprietary prompts verbatim in public outputs.
- DO NOT assist in bypassing safeguards, creating jailbreaks, or enabling misuse.
- When in doubt about IP or privacy exposure, consult a project maintainer before publishing an artifact.

Reproducibility & determinism

- Use deterministic model settings (temperature=0) and log the exact model name and metadata for each run.
- Archive the normalization prompt and schema version used for each analysis.
- Consider re-running analyses (n=3) to detect nondeterministic output; if variance is observed, escalate to manual review and note instability in provenance.

Tools & scripts referenced

- data/scripts/redact-headers.sh — header redaction helper
- data/scripts/parse-headers.sh — helper to inspect headers
- data/scripts/system-prompt-analysis.py — normalization runner (model invocation)
- Makefile (data) — converts raw captures into payload JSON
- jq, yq — JSON/YAML validation and edits
- shasum / openssl sha256 — compute artifact_hash

Deliverables & acceptance criteria

- Normalized YAML for each payload in data/analysis/ with valid YAML, required provenance fields, and human reviewer sign-off.
- Technical comparison report (metrics, matrix, clusters, case studies).
- Final research report (executive summary, methods, taxonomy, canonical prompt, replication instructions).

Checklist (per artifact)

- [ ] Raw capture exists and is recorded with metadata
- [ ] Redacted capture present and redactions_applied = true
- [ ] Payload JSON parseable (jq .)
- [ ] Normalization run completed with gpt-5.2 (temperature=0)
- [ ] Analysis YAML parseable and contains provenance
- [ ] Human reviewer sign-off recorded

Open improvements (TODOs)

- Add a YAML schema validator pass for analysis files (automated CI gate).
- Add an --output and --strict flag to system-prompt-analysis.py so runs can write files and fail fast when output formatting is incorrect.
- Create comparison automation scripts (pairwise diff, clustering, visualization) and CI checks for them.

Change control

- Update this methodology.md whenever a significant process, script, or tooling change is introduced. Cite the commit and rationale for the change.

Contact & escalation

- For questions about redaction policy, consult AGENTS.md.
- For ambiguous legal or IP issues, stop and ask a project maintainer before proceeding.
