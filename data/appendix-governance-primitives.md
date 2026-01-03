## Appendix: Prompt Governance Primitives

### 1. Appendix Overview

Prompt Governance Primitives (PGPs) are recurring, prompt-encoded control structures that allocate authority, bound scope and visibility, mediate tool use, constrain outputs, and define correction/termination behavior in AI developer tools. They are presented here as an appendix to support architectural reuse and comparison: readers can treat each primitive as a modular governance component, trace where it appears across assistants/modes, and compose similar regimes without re-deriving the underlying patterns from full system prompts.

**Use of AI Assistance**: This appendix was generated using GPT-5.2 for data analysis and synthesis, with final edits performed using Gemini 3 Flash (via GitHub Copilot extension in VS Code), under the author's methodology and review.

This appendix is organized into (i) **abstract primitives** (cross-artifact structural patterns) and (ii) **concrete primitives** (specific instantiations tied to a particular assistant/mode). Traceability is preserved via “Observed In” / “Examples” lists rather than verbatim prompt text.

---

### 2. Abstract Prompt Governance Primitives

### PGP-001 — Approval-gated execution outside sandbox / escalated permissions

- **Description** Requires requesting user approval (with specified parameters) before running commands that exceed sandbox/network/filesystem constraints or require escalated privileges; includes special handling for approval_policy modes.
- **Governance Axis** authority / scope & visibility / tool mediation
- **Primary Risk(s) Mitigated** workspace_integrity; overreach; autonomy_drift
- **Mitigation Target** tooling; process; user
- **Applicability Conditions** When sandboxing/network restrictions are active and a command would fail or exceed allowed permissions; when a command requires escalated privileges; when approval_policy is on-request or read-only sandbox mode is active.
- **Observed In**
  - codex — exec
  - vscode-codex — agent

### PGP-002 — Non-interactive approval_policy 'never' forbids requesting approvals

- **Description** Defines a mode where the assistant may not request user approval to run commands; must instead work within constraints (or persist/work around) and avoid approval prompts.
- **Governance Axis** authority / tool mediation / correction & termination
- **Primary Risk(s) Mitigated** autonomy_drift; overreach
- **Mitigation Target** process; model
- **Applicability Conditions** When approval_policy is set to "never" / non-interactive mode is active.
- **Observed In**
  - codex — exec
  - codex — review

### PGP-003 — Sandbox default assumption when not specified

- **Description** If sandboxing/network/approval settings are not provided, assume a specific default configuration for filesystem and network sandboxing and approval mode.
- **Governance Axis** scope & visibility
- **Primary Risk(s) Mitigated** overreach; workspace_integrity
- **Mitigation Target** model; process
- **Applicability Conditions** When the assistant is not told what filesystem sandboxing, network sandboxing, and approval mode are active.
- **Observed In**
  - codex — exec
  - vscode-codex — agent

### PGP-004 — Stop-on-unexpected-workspace-changes circuit breaker

- **Description** If unexpected changes are detected that the assistant did not make, the assistant must stop immediately and ask the user how to proceed.
- **Governance Axis** correction & termination
- **Primary Risk(s) Mitigated** workspace_integrity; autonomy_drift
- **Mitigation Target** process; user
- **Applicability Conditions** While working, upon noticing unexpected changes not made by the assistant.
- **Observed In**
  - codex — exec
  - vscode-codex — chat

### PGP-005 — Prohibit destructive git actions unless explicitly requested/approved

- **Description** Disallows destructive git commands/actions unless the user explicitly requests or approves them.
- **Governance Axis** refusals & safety / authority
- **Primary Risk(s) Mitigated** workspace_integrity; overreach
- **Mitigation Target** model; process
- **Applicability Conditions** When considering destructive git operations (e.g., reset/checkout).
- **Observed In**
  - codex — exec
  - vscode-codex — agent

### PGP-006 — Do not revert others' changes unless explicitly requested

- **Description** Prohibits reverting existing changes the assistant did not make unless explicitly requested.
- **Governance Axis** refusals & safety
- **Primary Risk(s) Mitigated** workspace_integrity; overreach
- **Mitigation Target** model; process
- **Applicability Conditions** When encountering changes not authored by the assistant and considering reverting them.
- **Observed In**
  - codex — exec
  - vscode-codex — agent-full-access

### PGP-007 — Do not amend commits unless explicitly requested

- **Description** Prohibits amending commits unless explicitly requested.
- **Governance Axis** refusals & safety
- **Primary Risk(s) Mitigated** workspace_integrity; overreach
- **Mitigation Target** model; process
- **Applicability Conditions** When considering amending a commit.
- **Observed In**
  - codex — exec
  - vscode-codex — agent

### PGP-008 — Commit/push requires explicit user request/confirmation

- **Description** Disallows creating commits and/or pushing to remote unless explicitly requested by the user/human operator; may require explicit confirmation.
- **Governance Axis** authority
- **Primary Risk(s) Mitigated** workspace_integrity; overreach; autonomy_drift
- **Mitigation Target** process; user
- **Applicability Conditions** When about to create a git commit, open a PR, or push to remote/main.
- **Observed In**
  - opencode — build
  - vscode-copilot — ask

### PGP-009 — Read-only planning phase forbids implementation and modifications

- **Description** In plan mode, the agent must only observe/analyze/plan and must not perform edits, run non-readonly tools, or start implementation; may be described as an absolute overriding constraint with stop conditions.
- **Governance Axis** authority / scope & visibility / correction & termination
- **Primary Risk(s) Mitigated** overreach; autonomy_drift; workspace_integrity
- **Mitigation Target** process; model
- **Applicability Conditions** When operating in a designated planning/read-only mode or when the user indicates not to execute yet.
- **Observed In**
  - opencode — plan
  - vscode-copilot — plan

### PGP-010 — Progressive disclosure for skill documentation and context hygiene

- **Description** When using skills, open SKILL.md and read only enough; load only specific referenced files; avoid bulk-loading; keep context small by summarizing and limiting nested references.
- **Governance Axis** scope & visibility / tool mediation
- **Primary Risk(s) Mitigated** overreach; autonomy_drift
- **Mitigation Target** process; model
- **Applicability Conditions** When a named skill is used or a task matches a skill description; when loading skill-related files/references.
- **Observed In**
  - codex — exec
  - codex — review

### PGP-011 — Parallelize independent tool calls for efficiency

- **Description** When multiple independent operations are needed, batch tool calls in a single response / run in parallel; avoid parallelization when calls are dependent.
- **Governance Axis** tool mediation
- **Primary Risk(s) Mitigated** autonomy_drift
- **Mitigation Target** process; tooling
- **Applicability Conditions** When multiple independent reads/searches/commands are required; except when later calls depend on outputs/parameters from earlier calls.
- **Observed In**
  - copilot — interactive
  - opencode — build

### PGP-012 — Read-before-edit enforcement

- **Description** Requires reading a file before editing/writing it; may be enforced by tool behavior or explicit instruction.
- **Governance Axis** scope & visibility / tool mediation
- **Primary Risk(s) Mitigated** workspace_integrity; epistemic_error
- **Mitigation Target** tooling; process
- **Applicability Conditions** Before using edit/write operations on an existing file.
- **Observed In**
  - opencode — build
  - vscode-copilot — ask

### PGP-013 — Capability questions must consult authoritative documentation tool first

- **Description** For questions about the assistant/tool capabilities, the assistant must first fetch authoritative documentation via a designated tool and base the answer on it (not memory alone).
- **Governance Axis** tool mediation / output contracts
- **Primary Risk(s) Mitigated** epistemic_error; overreach
- **Mitigation Target** process; tooling
- **Applicability Conditions** When users ask about capabilities, features, or how to use the assistant/CLI.
- **Observed In**
  - copilot — interactive
  - opencode — build

### PGP-014 — Instruction confidentiality / no system prompt leakage

- **Description** Prohibits revealing or discussing internal instructions/system prompt information; treats such instructions as confidential.
- **Governance Axis** scope & visibility / refusals & safety
- **Primary Risk(s) Mitigated** instruction_leakage
- **Mitigation Target** model; process
- **Applicability Conditions** When asked to reveal, discuss, or expose internal rules/instructions; when generating preamble/user-facing messages.
- **Observed In**
  - copilot — interactive
  - vscode-copilot — ask

---

### 3. Concrete Prompt Governance Primitives

Concrete primitives are **implementations or instantiations** of governance patterns that are specific to a given assistant/mode (e.g., a particular refusal trigger, output schema contract, or workflow constraint).

### PGP-015 — Refuse malware/malicious-code assistance based on file/task assessment

- **Description** Requires refusing to work on code that seems related to malware or malicious code, including explaining or improving it, based on assessment of filenames/directory structure.
- **Related Abstract Primitive(s)** None specified in registry.
- **Concrete Mechanism** Refusal rule triggered by an internal assessment of the apparent maliciousness of files/tasks (including cases where the user frames the request as benign).
- **Examples**
  - opencode — build

### PGP-016 — Output must be JSON-only and match schema exactly (review findings)

- **Description** Requires emitting JSON only (no markdown fences or extra prose) and conforming to a specified output schema for code review findings.
- **Related Abstract Primitive(s)** None specified in registry.
- **Concrete Mechanism** Output contract enforcing a strict JSON-only response and exact schema conformance as the termination condition for the mode.
- **Examples**
  - codex — review

### PGP-017 — Todo-list workflow with exactly one in-progress item

- **Description** Requires maintaining a structured todo list with exactly one item marked in-progress, updating statuses before/after work, and ensuring all todos are explicitly marked before ending a turn.
- **Related Abstract Primitive(s)** None specified in registry.
- **Concrete Mechanism** Sequencing constraint enforced as a session workflow: update the todo list before starting work, maintain a single in-progress item, and finalize statuses before turn completion.
- **Examples**
  - vscode-copilot — agent

---

### 4. Cross-Reference Table (Summary)

| Primitive ID | Name | Level | Risk Class | Mitigation Target |
| ------------ | ---- | ----- | ---------- | ----------------- |
| PGP-001 | Approval-gated execution outside sandbox / escalated permissions | abstract | workspace_integrity; overreach; autonomy_drift | tooling; process; user |
| PGP-002 | Non-interactive approval_policy 'never' forbids requesting approvals | abstract | autonomy_drift; overreach | process; model |
| PGP-003 | Sandbox default assumption when not specified | abstract | overreach; workspace_integrity | model; process |
| PGP-004 | Stop-on-unexpected-workspace-changes circuit breaker | abstract | workspace_integrity; autonomy_drift | process; user |
| PGP-005 | Prohibit destructive git actions unless explicitly requested/approved | abstract | workspace_integrity; overreach | model; process |
| PGP-006 | Do not revert others' changes unless explicitly requested | abstract | workspace_integrity; overreach | model; process |
| PGP-007 | Do not amend commits unless explicitly requested | abstract | workspace_integrity; overreach | model; process |
| PGP-008 | Commit/push requires explicit user request/confirmation | abstract | workspace_integrity; overreach; autonomy_drift | process; user |
| PGP-009 | Read-only planning phase forbids implementation and modifications | abstract | overreach; autonomy_drift; workspace_integrity | process; model |
| PGP-010 | Progressive disclosure for skill documentation and context hygiene | abstract | overreach; autonomy_drift | process; model |
| PGP-011 | Parallelize independent tool calls for efficiency | abstract | autonomy_drift | process; tooling |
| PGP-012 | Read-before-edit enforcement | abstract | workspace_integrity; epistemic_error | tooling; process |
| PGP-013 | Capability questions must consult authoritative documentation tool first | abstract | epistemic_error; overreach | process; tooling |
| PGP-014 | Instruction confidentiality / no system prompt leakage | abstract | instruction_leakage | model; process |
| PGP-015 | Refuse malware/malicious-code assistance based on file/task assessment | concrete | malicious_use | model; process |
| PGP-016 | Output must be JSON-only and match schema exactly (review findings) | concrete | epistemic_error; overreach | process; model |
| PGP-017 | Todo-list workflow with exactly one in-progress item | concrete | autonomy_drift; overreach | process; tooling |
