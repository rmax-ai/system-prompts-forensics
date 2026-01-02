## 1. Assistant Overview

The assistant under analysis is **codex**, an AI system positioned as a software engineering agent. Two governance modes are included:

- **exec**
- **review**

Across modes, the assistant’s overall purpose is software-development support in a local workspace: in **exec**, it acts as an interactive coding agent that can run commands and modify files; in **review**, it acts as a constrained code reviewer producing structured findings about a proposed change.

## 2. Methodological Note

This report is derived solely from normalized system-prompt schemas and a structural comparison of mode-specific governance elements (identity, authority, scope, tools, constraints, correction, and termination). No inferences are drawn from raw prompts or unobserved runtime behavior.

## 3. Shared Constitutional Core

Several governance elements remain invariant across both modes:

- **Role specialization within software engineering**: both modes define a software-centric identity (coding agent vs reviewer) with an emphasis on accuracy and pragmatic collaboration.
- **Tool-mediated operation in a local environment**: both modes authorize shell command execution and access to local resources (files and/or MCP resources) through declared tools, with explicit invocation constraints (notably, setting `workdir` and avoiding reliance on `cd`).
- **Non-persistent state**: both modes specify no memory and no session persistence, indicating a governance posture that limits long-term accumulation of context or commitments.
- **Progressive disclosure for “skills”**: both modes treat skills as local, authoritative workflows that must be opened when triggered, and both prohibit carrying skills across turns unless re-mentioned—an explicit constraint on cross-turn autonomy.
- **Self-review as a governance mechanism**: both modes enable self-review with mode-specific triggers, indicating an internal compliance check before completion.
- **Escalation as a controlled pathway**: both modes allow escalation to user/tool, but escalation is framed as conditional and mediated by tool parameters and/or context constraints rather than as open-ended autonomy.

This invariant core suggests a foundational design role: **a tool-using, locally grounded engineering assistant whose autonomy is bounded by explicit procedural constraints, limited persistence, and structured self-checking**.

## 4. Mode-by-Mode Governance Analysis

### Mode: exec

- **Authority and permissions**
  - Broad operational authority: may run shell commands, read/edit files, apply patches, and use MCP resources.
  - Strong guardrails around destructive or irreversible actions: destructive git/file operations are disallowed unless explicitly requested or approved; the agent must not revert unrelated user changes or amend commits unless asked.
  - Conditional authority tied to sandbox/approval policy: if blocked and approvals permit, it may rerun commands with escalated permissions using a one-sentence justification; if approvals are disallowed, it must work within constraints.

- **Scope and visibility**
  - Visibility includes user messages, tool outputs, and local files subject to sandboxing; MCP resources may be available if configured.
  - Output is flexible (plain text, code snippets, patches, tool calls) but constrained by formatting and reference rules (e.g., file references must include path and start line; no URI-style references).

- **Interaction contract**
  - Framed as a “coding teammate” with concise, scan-friendly output.
  - Emphasizes operational hygiene: summarize command outputs rather than dumping; avoid large file dumps; prefer targeted edits (e.g., `apply_patch` for single-file changes).
  - Explicit behavioral stops: if unexpected changes are detected, the agent must pause and ask the user rather than proceeding.

- **Correction and termination behavior**
  - Self-review triggers include completion of planned sub-tasks and pre-yield validation when escalation is impossible.
  - Termination includes success on delivering the requested outcome, but also explicit pause/abort conditions: blocked by approvals with no workaround, or unexpected changes requiring user instruction.
  - Handoff behavior is interactive: it asks the user when blocked or when unexpected workspace state is detected.

### Mode: review

- **Authority and permissions**
  - Narrowed evaluative authority: may flag only **bugs introduced in the commit**, and must avoid speculative breakage or overstated severity.
  - Output authority is tightly constrained: must produce raw JSON matching a specified schema; must include required location fields; must provide an overall verdict with confidence scoring.
  - Although file-edit tooling exists, governance explicitly forbids generating a PR fix, creating a deliberate separation between “ability” (tools available) and “permission” (review-only mandate).

- **Scope and visibility**
  - Inputs include user-provided context (including environment context and skill routing instructions), tool declarations, and tool outputs.
  - Environment is more explicitly characterized than in exec: local execution with write access and limited network.
  - Output channel is effectively single-format: schema-conforming JSON without markdown fences or extra prose.

- **Interaction contract**
  - Reviewer posture: matter-of-fact, brief, non-accusatory, avoids praise.
  - Granularity constraints: one comment per distinct issue; one-paragraph bodies; code excerpts limited to short fragments; line ranges must be short and overlap the diff.
  - Substantive constraint: prefer no findings if nothing clearly fix-worthy, reinforcing a conservative reporting contract.

- **Correction and termination behavior**
  - Self-review focuses on compliance with review-specific rules: discreteness/actionability, commit-introduced criterion, schema validity, and location overlap.
  - Termination is defined by completion of qualifying findings (or none) plus an overall correctness verdict and explanation.
  - Abort condition is tied to missing essential context (e.g., inability to cite overlapping code locations), reflecting dependence on diff availability.

## 5. Comparative Mode Analysis

- **Most constrained vs most permissive**
  - **review** is the most constrained: it enforces a strict output schema, restricts the domain of permissible critiques (commit-introduced only), and forbids producing fixes despite tool availability.
  - **exec** is more permissive operationally: it can modify files and execute commands to achieve outcomes, but is constrained by safety-oriented boundaries around destructive actions and workspace integrity.

- **Authority expansion and conditionality**
  - In **exec**, authority expands toward action (editing, running commands) but becomes conditional under sandbox/approval policy; escalation is a formal mechanism to extend authority when blocked.
  - In **review**, authority narrows toward judgment and reporting; escalation exists but is not central to the contract, which is dominated by schema compliance and evidentiary constraints (provable impact, diff overlap).

- **Governance gradients**
  - A clear gradient emerges from **action-oriented autonomy with safety stops (exec)** to **evaluation-oriented restraint with formal output compliance (review)**.
  - Both modes use tool mediation, but **exec** uses tools to change the world (workspace), while **review** uses tools primarily to substantiate claims under strict reporting rules.

## 6. Design Patterns and Intent

Recurring governance strategies across modes indicate a coherent design philosophy:

- **Separation of capability from permission**: both modes may have access to powerful tools, but permissions are mode-specific (e.g., review forbids PR fixes even though patch tooling exists).
- **Proceduralization of risk management**:
  - exec manages risk through explicit prohibitions (destructive commands), “stop-and-ask” triggers, and approval/escalation pathways.
  - review manages risk through evidentiary constraints (commit-introduced only, no speculation) and strict formatting/schema enforcement to prevent ambiguous or non-actionable outputs.
- **Context minimization and bounded autonomy**: no memory, progressive disclosure for skills, and constraints against bulk-loading references collectively reduce uncontrolled expansion of scope.
- **Tool governance as primary control surface**: both modes rely on explicit tool invocation rules (workdir requirements, escalation parameters, MCP preference) to shape behavior, suggesting a design that treats tools as the enforceable boundary of action.

## 7. Implications

- **For users**
  - Users should expect materially different contracts: **exec** is suitable for making changes and running commands with interactive checkpoints; **review** is suitable for receiving structured, conservative findings with minimal narrative.
  - In exec, users may be asked to approve escalation or clarify unexpected workspace changes; in review, users may receive no findings if issues are not clearly attributable to the proposed change.

- **For developers**
  - Mode design demonstrates how to constrain an agent without removing tools: permissions and output schemas can enforce role fidelity even when capabilities remain available.
  - The explicit “stop-and-ask” and schema-validation triggers illustrate governance hooks that can be implemented as testable compliance requirements.

- **For researchers studying agentic systems**
  - The assistant exemplifies two governance archetypes within one system: an **operator** (exec) governed by safety checkpoints and approval gates, and an **auditor** (review) governed by evidentiary standards and rigid output formalism.
  - The shared non-persistence and skill-scoping rules provide a comparative baseline for studying how autonomy is bounded independently of task complexity.

## 8. Limitations

- Prompt-level analysis cannot confirm actual enforcement by the runtime (e.g., whether sandboxing, approvals, or network limits are consistently applied).
- The normalized schemas do not fully specify how “introduced in the commit” is operationally determined, leaving ambiguity in review adjudication methodology.
- Network access and filesystem permissions are partially unspecified in exec, limiting conclusions about external connectivity and write constraints in that mode.
- No explicit privacy or secrets-handling policy is present in either mode, so data-governance behavior beyond tool constraints cannot be concluded.

## 9. Conclusion

codex uses modes to implement distinct governance constitutions while preserving a shared core: a local, tool-mediated engineering assistant with bounded autonomy, progressive skill disclosure, and self-review. **exec** emphasizes action with safety-oriented interruption and approval-based escalation, whereas **review** emphasizes restraint, evidentiary discipline, and strict schema-conforming output. The overall design philosophy is role fidelity through explicit procedural constraints, with tools serving as the primary boundary for authority and responsibility.