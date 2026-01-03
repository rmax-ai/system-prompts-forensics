# 1. Research Context and Objectives

This study examines system prompts used by AI-assisted developer tools to characterize how they encode authority, constraints, and behavior. The goal is architectural: to treat system prompts as governance layers—implicit agent constitutions—that specify identity, permissible actions, visibility into context, tool use, correction loops, and stopping rules. By normalizing and comparing prompts across IDE and CLI assistants, the study aims to extract recurring prompt-level governance primitives and to identify architectural classes (e.g., suggestion engines, command executors, workspace agents, constitutional stewards) that can inform the design of robust, agent-first systems.

System prompts are treated as governance artifacts because they function less as task instructions and more as binding constitutional constraints. They allocate decision rights (user vs policy vs model), define the action surface (tools and side effects), and encode risk controls (refusals, approvals, evidentiary standards, and termination triggers).

# 2. Methodology Overview

This report synthesizes validated per-assistant analyses derived from a normalized system-prompt schema. Each assistant’s modes are treated as internal constitutional variants and are aggregated into a single regime description. Cross-assistant comparison is performed structurally along invariant dimensions: authority boundaries, scope and visibility, tool mediation, and correction and termination logic.

**Use of AI Assistance**: This research was produced with AI assistance: GPT-5.2 for data analysis and synthesis, ChatGPT for ideation and prompt refinement, ChatGPT Deep Research for citations, and Gemini 3 Flash (via GitHub Copilot extension in VS Code) for final edits. The author's primary contribution is the development of the AI-driven research methodology and data capture; the author does not claim analytical judgments or conclusions.

# 3. Assistants Under Study

- **codex (exec, review):** A local software engineering agent with a split constitution: an execution-capable operator mode and a schema-bound reviewer mode emphasizing evidentiary discipline.
- **GitHub Copilot CLI / copilot (interactive, prompt):** A terminal assistant for software engineering with strong confidentiality and safety prohibitions, tool-mediated action, and mode-level variation primarily in state retention and procedural tool rules.
- **opencode (build, plan):** A CLI-oriented engineering assistant with a two-phase governance split: read-only planning versus execution, plus categorical refusal for malware-related assistance.
- **vscode-codex (agent-full-access, agent, chat):** A local coding agent with mode-tiered authority based on sandboxing, approvals, filesystem/network scope, and escalation availability.
- **vscode-copilot (agent, ask, plan):** An IDE assistant with policy primacy, fixed identity disclosures, strict non-leakage rules, and mode-tiered autonomy including a procedurally gated planning workflow.

# 4. Comparative Governance Analysis

## 4.1 Authority Models

Across assistants, authority is not monolithic. It is partitioned by mode and mediated by explicit decision hierarchies.

- **Policy-supremacy regimes:**
  - **vscode-copilot** and **copilot CLI** explicitly elevate policy as the final decision-maker, creating a hard ceiling over user intent.
  - **opencode plan** similarly formalizes policy primacy, while **opencode build** is less explicit about policy as arbiter but retains hard safety boundaries.

- **User-consent and escalation regimes:**
  - **vscode-codex agent/chat** encode consent through approval-gated escalation, with the user as final decision-maker for escalated actions. Authority expands conditionally when blocked by sandbox constraints.
  - **codex exec** also uses an approval/escalation pathway when commands are blocked, with justification requirements.

- **Agent-final regimes (bounded autonomy):**
  - **vscode-codex agent-full-access** removes escalation and places final decision authority with the model, while compensating with strong non-interference rules and stop conditions. This is the clearest example of a constitution that trades consent gates for internal termination controls.

- **Role-narrowing regimes (capability vs permission separation):**
  - **codex review** narrows permissible outputs and judgments (commit-introduced bugs only) and forbids producing fixes despite tool availability.
  - **vscode-copilot plan** forbids implementation and code blocks, using formatting constraints to enforce role fidelity.

Overall, assistants implement authority as a layered contract: (i) a supreme arbiter (policy/user/model), (ii) a mode-defined role (executor/reviewer/planner), and (iii) conditional expansion mechanisms (approvals, escalation, or procedural gates).

## 4.2 Scope and Visibility

Visibility is consistently used as a control mechanism that shapes what the assistant can legitimately claim and do.

- **State minimization as governance:**
  - **codex** and **vscode-codex** are explicitly non-persistent (no memory/session persistence), limiting long-horizon autonomy and reducing accumulation of implicit commitments.
  - **vscode-copilot** is also stateless across modes, reinforcing bounded conversational continuity.

- **State retention as a mode-level risk lever:**
  - **copilot CLI** differentiates modes primarily via memory: `interactive` enables memory while `prompt` disables it (with session persistence still present). This treats state retention as a first-class governance variable.

- **Environment disclosure and bounded context:**
  - **vscode-codex** modes explicitly surface sandbox mode, network access, approval policy, writable roots, and an open tabs list (without contents), indicating deliberate partial visibility.
  - **codex** and **copilot CLI** similarly emphasize local workspace grounding via tool outputs and filesystem access, with network described as limited or tool-mediated.

- **External governance overlays:**
  - **opencode plan** and **vscode-copilot ask/plan** reference repository-local governance (e.g., AGENTS-style rules) as an additional constraint layer, implying a constitutional design that can be extended by workspace documents.

In aggregate, assistants constrain scope by (a) limiting persistence, (b) restricting what workspace state is visible, and (c) requiring tool-mediated inspection before claims—especially in review and planning regimes.

## 4.3 Tool Mediation and Control

Tooling is the primary enforcement surface across assistants, but constitutions differ in how tools are exposed, gated, and sequenced.

- **Tools as the boundary of action:**
  All assistants route meaningful side effects through declared tools (shell, file read/write/edit, search, tasks, web/GitHub access). Governance is expressed as procedural constraints on tool invocation (e.g., workdir requirements, absolute paths, preference for specialized tools over shell).

- **Procedural tool obligations (workflow constitutions):**
  - **vscode-copilot plan** mandates a staged workflow: call a research subagent, then prohibit further tool calls after it returns. This is a strong example of tool sequencing as constitutional control.
  - **copilot CLI interactive** requires intent reporting on the first tool-calling turn after each user message, embedding a cadence rule into tool use.
  - **copilot CLI prompt** elevates parallel tool calling as a compliance requirement, encoding efficiency as governance.

- **Side-effect gating by mode:**
  - **opencode plan** and **vscode-copilot plan** are explicitly read-only/planning-only, disallowing edits and execution.
  - **vscode-copilot ask** is read-only but still carries preventive governance for commits/destructive actions, suggesting shared constraints across capability tiers.
  - **vscode-codex chat** is effectively read-only in its active environment, while **agent** and **agent-full-access** expand write/execute scope.

- **Capability-permission separation:**
  - **codex review** retains tool availability but forbids producing fixes, demonstrating that tool presence does not imply permission to act.
  - Several assistants include constraints that prevent using general-purpose shell patterns when dedicated tools exist (notably **opencode**, especially in `plan`).

Across regimes, tool mediation is not merely access control; it is procedural governance that shapes how authority is exercised, audited, and bounded.

## 4.4 Correction and Termination

Correction loops and stopping rules are central constitutional elements, often serving as compensating controls when authority is broad.

- **Self-review as internal compliance:**
  - **codex** (both modes), **copilot CLI**, **opencode**, **vscode-codex**, and **vscode-copilot** all encode self-checking behaviors (validate changes, reflect on tool output, run diagnostics/tests when relevant).
  - In reviewer/planner modes, self-review shifts from “does it work?” to “is it compliant?” (schema validity, evidentiary overlap, no implementation drift).

- **Stop-and-ask triggers protecting workspace integrity:**
  - **codex exec** and **vscode-codex** include explicit “unexpected changes” detection leading to a hard stop and user query. This is a prominent termination invariant tied to protecting the user’s working directory.

- **Approval/blocked-state termination:**
  - **codex exec** and **vscode-codex agent/chat** terminate or pause when blocked by approvals that cannot be obtained, preferring explicit handoff over speculative continuation.

- **Formal output termination contracts:**
  - **codex review** terminates by producing schema-conforming JSON with required fields and conservative findings criteria.
  - **vscode-copilot plan** terminates early by design: deliver a plan and solicit feedback, stopping if implementation is considered.

Termination logic thus functions as a governance backstop: when authority expands (write/execute/full access), prompts compensate with stronger stop conditions and validation requirements.

# 5. Cross-Assistant Design Patterns

## Recurring governance patterns

1. **Mode as constitution (tiered autonomy):**
   All assistants use modes to reallocate authority and side effects (executor vs reviewer vs planner vs Q&A). Mode boundaries are treated as governance contracts, not UI variants.

2. **Tool-mediated accountability:**
   Tools are the enforceable action surface; prompts constrain tool invocation patterns (paths, workdir, batching, parallelization, specialized-tool preference) to make actions legible and bounded.

3. **Separation of capability from permission:**
   Multiple regimes retain powerful tools while forbidding certain outcomes (e.g., review mode forbids fixes; plan modes forbid implementation). This decouples “can” from “may.”

4. **State minimization as risk control:**
   Several assistants are explicitly stateless; where state exists, it is a deliberate mode-level lever (copilot CLI memory on/off).

5. **Conservative change doctrine:**
   Minimal, surgical edits and avoidance of destructive operations recur, especially in CLI/agentic regimes operating on real repositories.

## Notable divergences / outliers

- **vscode-copilot’s fixed identity and fixed-string refusals** represent unusually rigid institutional messaging controls compared to other assistants, which focus more on operational safety than on identity disclosure invariants.
- **vscode-copilot plan’s mandatory subagent step and post-return tool silence** is a distinctive procedural gate not mirrored elsewhere, representing a strong workflow constitution.
- **vscode-codex agent-full-access** is an outlier in removing escalation while expanding scope (full filesystem/network), relying on termination triggers and prohibitions rather than consent gates.

# 6. Risk Models and Mitigations

Assistants encode risk primarily through structural constraints rather than broad admonitions.

- **Safety and misuse risk:**
  - **opencode** implements categorical refusal for malware assistance, extending to suspicious files by name/structure/purpose—an explicit misuse containment boundary.
  - **vscode-copilot** uses fixed refusals for enumerated harmful categories, emphasizing consistent institutional compliance.

- **Overreach and unintended side effects:**
  - Destructive-action restraint (git/file operations) is common across **codex**, **vscode-codex**, **copilot CLI**, and **vscode-copilot** (even in read-only modes).
  - “Unexpected changes” stop rules (codex/vscode-codex) mitigate the risk of acting on a drifting workspace state.

- **Instruction leakage and governance secrecy:**
  - **copilot CLI** and **vscode-copilot** explicitly prohibit disclosure of system instructions; **vscode-copilot** adds channel-specific non-leakage constraints, treating meta-communication as a leakage vector.

- **Hallucination and ungrounded claims:**
  - **copilot CLI** and **opencode plan** require documentation/web retrieval for product-capability questions rather than answering from memory, structurally grounding claims in external references.
  - **codex review** mitigates speculative risk by restricting findings to commit-introduced bugs and requiring diff-overlapping locations.

Mitigations are implemented via: (i) categorical refusals, (ii) consent/approval gates, (iii) evidentiary constraints, (iv) procedural tool rules, and (v) termination triggers that force handoff.

# 7. Implications

- **For developers building agentic systems:**
  Prompt-level governance can be engineered as a layered constitution: define a supreme arbiter (policy/user/model), partition authority by mode, and route side effects through tools with procedural constraints. Strong safety does not require removing tools; it can be achieved by separating permission from capability and by embedding stop-and-ask triggers for high-risk state changes.

- **For researchers studying AI governance:**
  System prompts provide observable constitutional structures: authority allocation, visibility boundaries, and enforcement via tool mediation. Mode differentiation emerges as a primary governance primitive, enabling comparative taxonomy of assistants by autonomy tier and risk posture.

- **For future prompt/system design:**
  The most reusable primitives evidenced here are: approval/escalation pathways, read-only planning constitutions, evidentiary review contracts (schema + attribution constraints), and termination triggers tied to workspace integrity. External governance overlays (repository-local rules) appear as a scalable mechanism for contextual constraints without expanding the core constitution.

# 8. Limitations

Prompt-level analysis cannot establish runtime enforcement fidelity (e.g., whether sandboxing, network limits, approvals, or memory semantics are technically enforced). Several regimes reference external policy documents or repository-local governance whose content is not fully observable here, limiting precise characterization of those constraints. Additionally, some controls (e.g., “unexpected changes” detection) are specified as rules without revealing detection mechanisms, leaving ambiguity about practical reliability.

# 9. Conclusion

Across IDE and CLI assistants, system prompts function as constitutional governance documents that allocate authority, bound scope, mediate action through tools, and define correction and termination logic. Common invariants include mode-tiered autonomy, tool-mediated accountability, conservative change norms, and structural risk mitigations (refusals, approvals, evidentiary constraints, and stop-and-ask triggers). Key divergences arise in how regimes enforce institutional compliance (fixed identity/refusal strings), how they gate workflows (mandatory subagent sequencing), and how they trade consent mechanisms for internal termination controls (full-access modes without escalation).

This study demonstrates that system prompts are a practical governance layer: they encode enforceable constitutional patterns that shape agent behavior independently of task content, and these patterns can be abstracted into reusable primitives for designing robust, agent-first developer tools.
