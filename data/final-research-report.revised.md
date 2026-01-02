### 1. Research Context and Objectives

This study investigates system prompts in AI-assisted developer tools to understand how they encode authority, constraints, and behavior. We treat system prompts as _governance layers_—implicit constitutions defining identity, permissible actions, visibility, tool use, and termination rules—rather than mere task instructions.

The motivating hypothesis is that differences in agency, risk posture, and control assumptions are legible at the prompt level, and that recurring “prompt primitives” can be extracted to design robust agentic systems. The scope covers IDE and CLI assistants, comparing governance across modes and products.

### 2. Methodology Overview

The report synthesizes per-assistant analyses derived from normalized schemas. Each assistant is treated as a distinct governance regime, and each mode as a constitutional variant. Findings result from cross-assistant comparison of authority boundaries, scope/visibility, tool mediation, and correction/termination logic.

### 3. Assistants Under Study

- **codex (exec, review)**: A local assistant split into an execution constitution (tool-mediated workspace mutation with consent gates) and a review constitution (evidence-governed judgment artifact production).
- **GitHub Copilot CLI / copilot (interactive, prompt)**: A terminal assistant optimized for minimal repository changes, with strong non-exfiltration prohibitions and tool-grounded validation.
- **opencode (build, plan)**: A CLI helper with malware refusal and git safety constraints; modes separate read-only planning from write-capable execution with procedural safeguards.
- **vscode-codex (agent-full-access, agent, chat)**: A local agent emphasizing workspace integrity; modes vary network reach, sandbox authority, and approval requirements.
- **vscode-copilot (agent, ask, plan)**: An IDE assistant with policy supremacy and channelized disclosure; modes implement a graduated authority ladder from planning to tool-driven execution.

### 4. Comparative Governance Analysis

#### 4.1 Authority Models

Authority is allocated through _constitutional roles_ and _adjudication loci_ rather than simple permission lists. **“Policy-sovereign” refers to external adjudication mechanisms overriding model or user discretion, not generic safety policy.**

- **User-sovereign consent regimes (conditional authority)**: **codex exec**, **vscode-codex agent/chat**, and **opencode build** encode user-mediated escalation for risky actions. Authority to mutate the workspace exists, but high-impact steps are routed through explicit consent and “stop-and-ask” circuit breakers.

- **Policy-sovereign regimes (external adjudication)**: **vscode-copilot** and **copilot interactive** place final authority in “policy,” making compliance an external constraint overriding model discretion. This ensures predictable enforcement through standardized refusal behavior and non-disclosure rules.

- **Model-sovereign artifact regimes (internal adjudication)**: **codex review** and **copilot prompt** assign final decision-making to the model. Authority is constrained by output contracts (e.g., strict JSON) and epistemic rules (provability, no speculation).

- **Autonomy without approvals (policy-autonomous execution)**: **vscode-codex agent-full-access** disables escalation; governance shifts from consent gating to internal policy constraints and validation logic.

#### 4.2 Scope and Visibility

Visibility is a control mechanism shaping epistemic claims and permissible actions.

- **Interaction contracts**: **codex** and **vscode-codex** deny session persistence, constraining authority to the current context. **copilot CLI** is structurally persistent, requiring stronger confidentiality and minimal-change discipline.
- **Scope partitioning**: **opencode plan** and **vscode-copilot plan** institutionalize read-only planning, forbidding side effects. **vscode-codex chat** similarly maintains a read-only sandbox posture.
- **Context hygiene**: Assistants emphasize path-based references and avoid verbatim dumps to limit disclosure. **vscode-copilot** adds channel separation (commentary vs final) to prevent leakage.
- **Repository governance**: **vscode-copilot ask/plan** incorporate project-level rules, allowing local constitutions to override generic behavior.

#### 4.3 Tool Mediation and Control

Tools are the primary interface between the model and environment, serving as control surfaces where sequencing and workflow rules enforce procedural governance.

- **Auditable contracts**: Assistants encode “act through tools” norms with strict invocation discipline (e.g., explicit working directories, avoiding `cd`).
- **Autonomy throttles**: Sequencing constraints, such as **vscode-copilot plan**’s single research call, prevent iterative drift. **copilot CLI** uses efficiency rules to limit uncontrolled exploration.
- **Capability decoupling**: Governance often overrides tool capabilities; **opencode plan** declares side-effectful tools but constitutionally forbids their use.
- **Workflow procedures**: **vscode-copilot agent** uses todo-management for structured autonomy, while **opencode build** embeds git workflow constraints as governance procedures.

#### 4.4 Correction and Termination

Correction and stopping rules function as constitutional “circuit breakers.”

- **Integrity safeguards**: **codex exec** and **vscode-codex** halt on unexpected diffs to prevent workspace corruption.
- **Epistemic restraint**: **codex review** yields empty findings when claims aren't provable, preventing speculation.
- **Validation loops**: **copilot CLI** and **opencode build** ground corrections in tool outputs. **vscode-codex agent-full-access** relies on self-mediated verification since approvals are disabled.
- **Mode protection**: **vscode-copilot plan** terminates tool use after mandated steps to enforce the boundary between deliberation and action.

### 5. Cross-Assistant Design Patterns

Recurring governance strategies include:

1. **Mode-based partitioning**: Allocating authority across planning, advice, and execution modes.
2. **Consent gates**: Requiring explicit approval for irreversible actions (commits, destructive operations).
3. **Tool discipline**: Enforceable micro-rules (e.g., “prefer grep,” “require workdir”) that increase auditability.
4. **Output contracts**: Constraining expression through strict formatting (JSON-only, plan-only) to control downstream consumption.
5. **Circuit breakers**: Termination primitives for unexpected state or blocked progress.

Notable outliers include **vscode-copilot plan**’s strict sequencing and **codex review**’s intense epistemic governance.

### 6. Risk Models and Mitigations

Assistants encode risk through structural constraints:

- **Safety**: **opencode** uses explicit malware refusal; **vscode-copilot** employs fixed refusal templates.
- **Overreach**: Mitigated via destructive-action prohibitions, consent workflows, and git safety rules.
- **Epistemic risk**: Managed through provability constraints and grounding changes in tool outputs.
- **Leakage**: Addressed via explicit non-disclosure rules and channel separation.

### 7. Implications

Governance should be designed as composable primitives: separate planning from execution, gate irreversible actions, and encode tool discipline as micro-rules. System prompts function as operational constitutions allocating authority among user, policy, and model. Increasing agent power requires more structured governance—explicit tool mediation, strict output contracts, and hard sequencing—rather than merely longer instructions.

### 8. Limitations

Prompt analysis cannot establish runtime enforcement fidelity or actual sandbox constraints. Privacy handling is often under-specified, and internal tensions between formatting and reference rules may exist.

### 9. Conclusion

This study investigated the hypothesis that differences in agency, risk posture, and control assumptions are legible at the prompt level, and that recurring “prompt primitives” can be extracted to design robust agentic systems. The hypothesis is confirmed: structural analysis of system prompts reveals consistent governance layers and reusable architectural primitives across diverse assistants.

System prompts operate as governance constitutions that allocate authority, constrain visibility, and mediate tool use. Common patterns—mode-based partitioning, consent gates, and tool-discipline micro-rules—demonstrate that prompts are a practical layer for encoding procedural workflows and responsibility allocation. This confirms that "agency" is largely a constitutional allocation, and that robust agent-first design relies on structured governance.
