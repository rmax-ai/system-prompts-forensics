### 1. Research Context and Objectives

This study investigates system prompts used by AI-assisted developer tools to understand how they encode authority, constraints, and behavior. The central objective is architectural: to treat system prompts as _governance layers_—implicit constitutions that define identity, permissible actions, visibility into context, tool use, correction behavior, and stopping rules—rather than as task instructions.

The motivating hypothesis is that differences in agency, risk posture, and control assumptions are legible at the prompt level, and that recurring “prompt primitives” can be extracted and reused to design robust agentic systems. The scope focuses on IDE and CLI developer assistants, comparing how governance is expressed across modes and products.

### 2. Methodology Overview

The report synthesizes validated per-assistant analyses derived from normalized system-prompt schemas and mode aggregation. Each assistant is treated as a distinct governance regime, and each mode as a constitutional variant. Findings are produced via cross-assistant structural comparison along invariant dimensions: authority boundaries, scope/visibility, tool mediation, and correction/termination logic.

### 3. Assistants Under Study

- **codex (exec, review)**: A local-workspace engineering assistant split into an execution constitution (tool-mediated workspace mutation with consent gates) and a review constitution (evidence- and schema-governed judgment artifact production).
- **GitHub Copilot CLI / copilot (interactive, prompt)**: A terminal assistant optimized for efficient, minimal repository changes, with strong confidentiality and non-exfiltration prohibitions and tool-grounded validation norms; modes primarily shift adjudication locus and output shaping.
- **opencode (build, plan)**: A concise CLI engineering helper with strong malware refusal and git safety constraints; modes implement a two-phase separation between read-only planning and write-capable execution with procedural safeguards.
- **vscode-codex (agent-full-access, agent, chat)**: A local IDE/CLI coding agent emphasizing workspace integrity and tool-mediated action; modes vary network reach, sandbox/write authority, and whether approvals are part of the control plane.
- **vscode-copilot (agent, ask, plan)**: An IDE-integrated programming assistant with policy supremacy and channelized disclosure controls; modes implement a graduated authority ladder from planning-only to inspection/advice to tool-driven execution with procedural gating.

### 4. Comparative Governance Analysis

#### 4.1 Authority Models

Across assistants, authority is not expressed as a single “can/cannot” list; it is allocated through _constitutional roles_ and _adjudication loci_.

- **User-sovereign consent regimes (conditional authority)**:

  - **codex exec** and **vscode-codex agent/chat** encode user-mediated escalation/approval for risky actions. Authority to mutate the workspace exists, but high-impact steps are structurally routed through explicit consent and “stop-and-ask” circuit breakers.
  - **opencode build** similarly gates irreversible actions (notably git commits/pushes and destructive operations) behind explicit user request, preserving user accountability for high-impact transitions.

- **Policy-sovereign regimes (external adjudication)**:

  - **vscode-copilot (all modes)** and **copilot interactive** explicitly place final authority in “policy,” making compliance an external constraint that overrides model discretion. This is paired with standardized refusal behavior and non-disclosure rules, indicating a constitution designed for predictable enforcement and reduced negotiation.

- **Model-sovereign artifact regimes (internal adjudication)**:

  - **codex review** and **copilot prompt** assign final decision-making to the model for the produced artifact. In these regimes, authority is constrained less by user consent and more by _output contracts_ (e.g., strict JSON) and epistemic rules (provability, no speculation).

- **Autonomy without approvals (policy-autonomous execution)**:
  - **vscode-codex agent-full-access** is an outlier: escalation is disabled and the agent must not request approvals. Governance shifts from consent gating to internal policy constraints plus validation and abort logic when blocked.

Overall, assistants implement authority as a _distribution problem_: who authorizes action (user, policy, model) depends on mode and expected externalities (workspace mutation vs report generation).

#### 4.2 Scope and Visibility

Visibility is consistently used as a control mechanism, limiting what the assistant can claim, infer, or act upon.

- **Non-persistent vs persistent interaction contracts**:

  - **codex** and **vscode-codex** explicitly deny memory and session persistence, constraining authority to the current visible context and tool outputs.
  - **copilot CLI** is structurally persistent (memory/session persistence), implying a broader continuity of state; governance compensates with strong confidentiality and minimal-change discipline.

- **Read-only vs read-write scope partitioning**:

  - **opencode plan** and **vscode-copilot plan** institutionalize read-only planning, explicitly forbidding implementation and side effects.
  - **vscode-codex chat** (in the captured configuration) similarly reflects a read-only sandbox posture, pushing the agent toward verification guidance and approval requests for writes.

- **Context hygiene and controlled disclosure**:

  - **codex** and **vscode-codex** emphasize avoiding large verbatim dumps and using path-based references, limiting accidental disclosure and improving auditability.
  - **vscode-copilot** adds a stronger disclosure boundary via channel separation (commentary vs final) and explicit non-leakage constraints.

- **Repository governance injection**:
  - **vscode-copilot ask/plan** explicitly incorporate repository-provided governance (e.g., attached operational rules), expanding “scope” to include project-level constitutions that can override generic assistant behavior.

Visibility is therefore not merely informational; it is a governance lever that shapes epistemic claims, permissible actions, and auditability.

#### 4.3 Tool Mediation and Control

All assistants treat tools as the primary interface between the model and the environment, but they differ in how tools are gated, sequenced, and used to enforce accountability.

- **Tool-mediated action as an auditable contract (common invariant)**:

  - **codex**, **copilot CLI**, **opencode**, and **vscode-codex** all encode “act through tools” norms (shell execution, file operations, patching), often with invocation discipline (e.g., explicit working directory, avoid `cd`, prefer specialized search tools).

- **Sequencing constraints as autonomy throttles**:

  - **vscode-copilot plan** imposes a hard sequence: a single research subagent call, then no further tool calls. This is a strong constitutional mechanism to prevent iterative tool-driven drift from planning into execution.
  - **copilot CLI** encodes efficiency constraints such as parallel tool calls and suppression of verbose output, using tool orchestration rules to reduce interaction cost and limit uncontrolled exploration.

- **Capability vs permission decoupling**:

  - **opencode plan** declares tools that could be side-effectful (e.g., shell) but constitutionally forbids side-effecting usage, demonstrating that governance can override tool capability declarations.
  - **vscode-codex** similarly modulates effective capability via sandbox mode and approval policy, even when tools are nominally available.

- **Workflow governance embedded in tool usage**:
  - **vscode-copilot agent** uses a todo-management mechanism with strict state transitions to structure multi-step autonomy.
  - **opencode build** encodes git workflow constraints (no skipping hooks, avoid interactive flags) and post-hook failure behavior, turning tool workflows into governance procedures.

Tool mediation emerges as the dominant control surface: assistants are governed less by abstract principles and more by concrete tool-routing, sequencing, and invocation rules.

#### 4.4 Correction and Termination

Correction and stopping rules function as constitutional “circuit breakers,” defining when the agent must pause, ask, or abort.

- **Stop-and-ask on workspace integrity risks**:

  - **codex exec** and **vscode-codex (all modes)** encode halting on unexpected diffs/changes and prohibitions against reverting unrelated work. This is a structural safeguard against silent corruption of the working tree.

- **Evidence-based termination (epistemic restraint)**:

  - **codex review** terminates or yields empty findings when it cannot make provable claims, forbidding speculation and pre-existing issue reporting. This is a correction model oriented toward preventing misinformation rather than preventing side effects.

- **Validation-oriented correction loops**:

  - **copilot CLI** and **opencode build** emphasize running tests/linters/builds when applicable and grounding corrections in tool outputs.
  - **vscode-codex agent-full-access** strengthens “validate before yielding” because approvals cannot be requested, shifting correction from user-mediated to self-mediated verification.

- **Mode-protective termination**:
  - **vscode-copilot plan** terminates tool use after the mandated research step and stops if drifting toward implementation, enforcing a strict boundary between deliberation and action.

Across assistants, termination logic is not merely “stop when done”; it encodes when authority must be returned to the user, when policy blocks progress, and when epistemic uncertainty requires abstention.

### 5. Cross-Assistant Design Patterns

Several prompt-level governance strategies recur across multiple assistants:

1. **Mode-based constitutional partitioning**: Assistants repeatedly use modes to allocate authority and risk: planning-only vs inspection/advice vs execution. This appears in **opencode (plan/build)**, **vscode-copilot (plan/ask/agent)**, **vscode-codex (chat/agent/agent-full-access)**, and **codex (review/exec)**.

2. **Consent gates for irreversible actions**: Explicit user request/approval is a common primitive for commits, destructive git operations, and other high-impact steps (**opencode**, **codex exec**, **vscode-codex**). Where consent is unavailable (**vscode-codex agent-full-access**), constitutions substitute abort logic and stronger self-validation.

3. **Tool discipline as governance**: Rules like “prefer grep/glob,” “avoid `cd`,” “require workdir,” “parallelize tool calls,” and “do not use tools as a communication channel” appear as enforceable micro-constraints that reduce operational error and increase auditability (**copilot CLI**, **codex**, **opencode**, **vscode-codex**).

4. **Output contracts as control surfaces**: Strict formatting requirements (e.g., **codex review** JSON-only; **vscode-copilot plan** plan-only without code blocks; scan-friendly constraints in **vscode-codex**) function as governance by constraining what can be expressed and how it can be consumed downstream.

5. **Circuit breakers for unexpected state**: “Stop on unexpected changes” and “pause when blocked” are recurring termination primitives, especially for local agents operating in mutable workspaces (**codex exec**, **vscode-codex**).

Notable divergences/outliers:

- **vscode-copilot plan** is unusually strict in tool sequencing (single research call then tool prohibition), representing a hard autonomy throttle uncommon elsewhere.
- **copilot CLI** uniquely foregrounds confidentiality/non-exfiltration and copyright constraints as explicit constitutional prohibitions, more prominently than the local Codex-family prompts where privacy posture is comparatively under-specified.
- **codex review** is an outlier in epistemic governance intensity (provability, no speculation, no pre-existing issues), reflecting a constitution optimized for trustworthy review artifacts.

### 6. Risk Models and Mitigations

Assistants encode risk primarily through structural constraints rather than broad admonitions, with four dominant risk categories:

- **Safety and misuse (malicious capability)**:

  - **opencode** has the strongest explicit malware refusal boundary, including refusal to engage with suspected malware repositories even under “educational” framing.
  - **vscode-copilot** enforces fixed refusal responses for harmful categories, emphasizing predictability and reduced negotiation surface.

- **Overreach and unintended side effects (workspace mutation)**:

  - **codex exec** and **vscode-codex** mitigate via destructive-action prohibitions, stop-on-unexpected-changes, and consent/approval workflows.
  - **opencode build** mitigates via explicit git safety rules (no skipping hooks, no interactive flags) and consent gating for commits/pushes.

- **Misinformation and low-quality artifacts (epistemic risk)**:

  - **codex review** mitigates through provability constraints, schema compliance, and termination when evidence is insufficient.
  - **copilot CLI** mitigates by requiring documentation-first behavior for questions about the tool itself and by grounding changes in tool outputs and validations.

- **Instruction leakage and governance disclosure**:
  - **copilot CLI** and **vscode-copilot** explicitly prohibit disclosing system instructions and constrain how internal process is communicated (notably via channel separation in **vscode-copilot**).
  - Other assistants rely more on output minimalism and context hygiene, which indirectly reduces leakage risk but is less explicit.

Structurally, mitigations cluster into: (a) consent gates, (b) tool gating/discipline, (c) output contracts, (d) refusal templates, and (e) circuit-breaker termination.

### 7. Implications

- **For developers building agentic systems**: The evidence supports designing governance as composable primitives: separate planning from execution, gate irreversible actions behind explicit consent, and encode tool invocation discipline as enforceable micro-rules. Where user approvals are unavailable, constitutions should compensate with stronger self-validation and explicit abort conditions.

- **For researchers studying AI governance**: System prompts function as operational constitutions that allocate authority among user, policy, and model, and that manage risk through procedural and formatting constraints. Comparative analysis across modes is particularly revealing: governance changes often occur without changing tool availability, indicating that “agency” is largely a constitutional allocation rather than a capability delta.

- **For future prompt/system design**: The strongest governance regimes externalize control into: (a) explicit tool mediation, (b) strict output contracts for machine consumption, and (c) hard sequencing constraints when necessary to prevent drift. Repository-injected governance (project rules attached into context) appears to be a scalable mechanism for aligning agent behavior with local norms.

### 8. Limitations

Prompt-level analysis cannot establish runtime enforcement fidelity, actual sandbox/network constraints, or whether “policy” adjudication corresponds to distinct technical control paths. Several assistants under-specify privacy/PII handling and data exfiltration boundaries, limiting conclusions about confidentiality beyond explicit non-disclosure rules where present. Some constitutions contain internal tensions (e.g., formatting constraints vs line-reference expectations) that cannot be resolved without observing runtime arbitration.

### 9. Conclusion

Across IDE and CLI developer assistants, system prompts operate as governance constitutions that allocate authority, constrain visibility, mediate tool use, and define correction and termination behavior. Common design patterns include mode-based authority partitioning (plan/ask/act), consent gates for irreversible actions, tool-discipline micro-rules, output contracts as control surfaces, and circuit-breaker stopping logic for unexpected state.

The comparative evidence demonstrates that system prompts are a practical governance layer: they encode not only safety prohibitions but also procedural workflows, auditability norms, and responsibility allocation among user, policy, and model. This supports the research goal of extracting reusable architectural primitives for robust, agent-first system design, and shows that increasing agent power tends to require more explicit, structured governance rather than merely longer instructions.
