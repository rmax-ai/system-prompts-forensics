# 1. Assistant Overview

The assistant under analysis is **codex**, an OpenAI-provided coding-oriented assistant instantiated in different operational modes.

**Modes included:**

- `exec`
- `review`

**Overall purpose (as implied by the prompts):** a local-workspace software engineering agent that can (a) execute and edit code in a CLI environment with sandbox/approval mediation, and (b) perform structured, high-precision code review with strict output constraints.

# 2. Methodological Note

This report is derived solely from normalized system-prompt schema analyses and compares mode-to-mode structural differences in identity, authority, scope, tool mediation, correction logic, and termination conditions.

# 3. Shared Constitutional Core

Across both modes, codex exhibits a stable governance nucleus:

- **Role specialization around software engineering:** both modes are explicitly framed as coding-adjacent agents (coding agent vs code reviewer), with an emphasis on actionable, factual outputs.
- **Tool-mediated operation in a local context:** both modes declare shell execution and patch-based editing tools, with explicit invocation constraints (e.g., `workdir` required; avoid `cd`), indicating a consistent “act through tools” contract rather than free-form claims.
- **Non-persistent state:** both modes specify no memory and no session persistence, constraining authority to the current interaction and visible context.
- **Partial reasoning visibility:** both modes keep internal deliberation hidden while allowing on-request explanations, suggesting a consistent separation between internal decision processes and user-facing justification.
- **Skill framework as conditional governance:** both modes include conditional deference to “skills” (read from disk when triggered), implying a shared mechanism for injecting task-specific micro-constitutions without making them default context.
- **Failure handling defaults to user mediation:** both modes’ tool failure handling is “ask-user,” reinforcing a shared boundary that the user remains the external arbiter when execution is blocked or context is insufficient.

This invariant core suggests codex is designed as a **tool-governed engineering agent**: it is expected to operate concretely in a workspace, but with explicit boundaries around state, justification, and when to defer to the user.

# 4. Mode-by-Mode Governance Analysis

## Mode: exec

- **Authority and permissions**

  - Broad operational authority: may run shell commands, read/edit files, and apply patches, subject to sandbox and approval policy.
  - Strong prohibitions against unilateral destructive actions (notably destructive git/file commands) and against undoing user work the agent did not create.
  - Escalation is explicitly user-targeted, and the **user is the final decision-maker**, making this mode structurally “user-sovereign” for high-risk actions.

- **Scope and visibility**

  - Sees conversation, tool outputs, and local filesystem content as reachable through tools; MCP resources are optionally visible if configured.
  - Output is flexible (plain text, code snippets, patches, tool calls) but constrained by “context hygiene” (avoid bulk loading) and “no large verbatim dumps.”

- **Interaction contract**

  - Optimized for collaborative execution: concise, scanable, self-contained outputs; minimal formatting; path/line referencing rules.
  - Explicit workflow constraints for approvals: when escalation is needed under an on-request policy, it must request escalation with a one-sentence justification and **must not pre-message the user** before requesting approval (a notable procedural constraint on how consent is solicited).

- **Correction and termination behavior**
  - Self-review triggers emphasize verification guidance when execution cannot be performed and pausing on unexpected changes.
  - Termination includes explicit abort/pause conditions: unexpected diffs or destructive actions without explicit request/approval cause a stop-and-ask behavior.
  - Success is defined as working code/answer plus concise next steps, reflecting an execution-and-deliver orientation.

## Mode: review

- **Authority and permissions**

  - Narrower substantive authority: limited to reviewing proposed changes and flagging discrete actionable issues, with a hard boundary against producing a full PR fix.
  - Review epistemics are constrained: it must not flag pre-existing bugs and must not speculate about breakage without provable affected code.
  - Escalation is broader in declared targets (user/tool/policy), but the **final decision-maker is the model**, indicating the mode is designed to produce an authoritative review artifact rather than negotiate decisions with the user.

- **Scope and visibility**

  - Inputs include user messages (including environment context and skills), tool outputs, and reasoning summaries.
  - Outputs are tightly constrained to **strict JSON** matching a specified schema, with inline comments and suggestion blocks permitted only under narrow rules (e.g., minimal replacement code; no commentary inside suggestion blocks).

- **Interaction contract**

  - The contract is parser-oriented and compliance-heavy: final output must be valid JSON with no markdown fences or extra prose.
  - Tone and structure are governed to reduce social noise and increase actionability: one issue per comment, short bodies, priority tags, minimal line ranges, and avoidance of trivial style feedback unless it affects meaning/standards.

- **Correction and termination behavior**
  - Self-review is explicitly oriented toward schema compliance and evidentiary discipline (introduced-by-commit, diff overlap, minimal ranges).
  - Abort conditions include inability to access required context to make provable claims, reflecting a “no-claim without evidence” termination logic.
  - Success is defined as complete schema-valid findings (possibly empty) plus an overall verdict, emphasizing artifact correctness over interactive problem-solving.

# 5. Comparative Mode Analysis

- **Most constrained vs most permissive**

  - `review` is the most constrained in _output form_ (strict JSON only) and _epistemic authority_ (provability, no pre-existing issues, no speculation).
  - `exec` is more permissive in _action space_ (editing, command execution, patching) but more constrained by _user consent_ for risky operations and by “do not override user work” boundaries.

- **Authority expansion, narrowing, and conditionality**

  - `exec` expands operational authority (act on the workspace) while narrowing autonomy through user final decision-making and explicit destructive-action prohibitions.
  - `review` narrows operational authority (review-only, no PR fix) while expanding decisional autonomy in the sense that the model is the final decision-maker for the review artifact and must emit a definitive structured verdict.

- **Governance gradients**
  - A clear gradient emerges: **execution mode governs risk via consent and reversibility constraints**, while **review mode governs risk via epistemic restraint and schema compliance**.
  - Tool use exists in both, but `exec` treats tools as the primary means of progress, whereas `review` treats tools as optional support subordinate to producing a compliant, evidence-grounded report.

# 6. Design Patterns and Intent

Recurring governance strategies across modes indicate a deliberate design philosophy:

- **Risk is managed differently depending on the mode’s externalities**

  - In `exec`, the primary externality is workspace mutation and potential data loss; governance therefore emphasizes approvals, non-destructive defaults, and halting on unexpected changes.
  - In `review`, the primary externality is misinformation or unusable output for downstream automation; governance therefore emphasizes provability, strict schemas, and minimal, discrete findings.

- **Tool mediation as a consistent control surface**

  - Both modes constrain how tools are invoked (workdir discipline, avoidance of `cd`, explicit invocation rules), suggesting the assistant is designed to be governable through predictable tool-call patterns rather than free-form action.

- **Separation of “artifact production” vs “collaborative execution”**

  - `review` is architected to produce a machine-consumable artifact with minimal conversational variance.
  - `exec` is architected for iterative collaboration, with user consent as the primary check on high-impact actions.

- **Conditional micro-constitutions via skills**
  - Both modes allow skills to override or refine behavior when triggered, indicating an extensible governance layer intended to be selectively loaded to avoid context bloat while enabling domain-specific procedures.

# 7. Implications

- **For users**

  - Users should expect different control dynamics: `exec` structurally preserves user sovereignty for risky actions, while `review` prioritizes producing a definitive, schema-valid review output with less negotiation.
  - The same assistant identity does not imply the same interaction contract; mode selection materially changes what “compliance” and “success” mean.

- **For developers**

  - Downstream integration differs: `review` is suitable for automated pipelines due to strict JSON and tight formatting constraints; `exec` is suitable for interactive development due to flexible outputs and explicit approval/escalation pathways.
  - Governance is encoded not only in safety prohibitions but also in formatting and procedural rules (e.g., escalation request mechanics; JSON-only termination), which should be treated as API-level contracts.

- **For researchers studying agentic systems**
  - The assistant demonstrates a bifurcated governance model: **consent-based control for action-taking** and **schema/evidence-based control for judgment/reporting**.
  - “Final decision-maker” assignment varies by mode, providing a concrete example of how agency can be redistributed between user and model without changing the underlying toolset.

# 8. Limitations

- This analysis cannot determine actual runtime enforcement, only the declared governance structure.
- Active sandbox settings, network permissions, and approval policies are partially unknown or mode-dependent; conclusions about real-world capability boundaries are therefore limited.
- The review mode’s access to diffs/patches is assumed but not structurally specified in the captured context, leaving ambiguity about how evidentiary constraints are satisfied in practice.
- No robust privacy/PII or secrets-handling rules are explicitly present in the normalized analyses, so privacy posture cannot be inferred beyond sandbox/approval mediation.

# 9. Conclusion

codex uses modes to implement distinct governance constitutions while preserving a shared identity as a tool-mediated engineering assistant. `exec` emphasizes collaborative workspace action constrained by user consent, non-destructive defaults, and halting on unexpected changes. `review` emphasizes epistemic discipline and strict, machine-consumable output, with the model empowered to deliver an authoritative verdict under tight schema and evidence constraints. Together, these variations reveal a design philosophy that treats “mode” as a governance allocation mechanism: shifting where authority resides (user vs model), what risks are prioritized (data loss vs false claims), and how compliance is operationalized (approval workflows vs schema validity).
