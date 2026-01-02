## 1. Introduction

This report compares how modern AI-assisted developer tools encode governance—authority, constraints, and interaction contracts—through their system-level constitutions. The scope covers CLI and IDE developer assistants spanning execution-oriented agents, review-only regimes, interactive terminal assistants, and planning-only modes.

System constitutions are analyzed as governance artifacts because they define durable institutional properties: who holds decision authority, what actions are permitted or prohibited, what context is visible, how tools mediate side effects, and how the interaction terminates. These properties shape the permissible behavior space more than any single user request.

Across the dataset, the tools fall into several stable governance regimes (“prompt families”): a tight Copilot CLI interactive/prompt pair, a tight OpenCode build/plan pair, two stable VS Code platform umbrellas (Codex-oriented and Copilot-oriented), and a persistent outlier review constitution.

## 2. Methodological Summary

The analysis proceeds in four steps:

1. **Normalization**: Each captured constitution is decomposed into a shared schema (identity, authority, scope, tools, constraints, reasoning, correction, termination), reducing stylistic noise while preserving governance semantics.
2. **Similarity measurement**: Pairwise similarity is computed using structural overlap and token-level similarity, combined into a weighted score; forbidden-action overlap is tracked separately.
3. **Band analysis**: Similarity thresholds are swept to observe when components merge or fragment, revealing stability bands that correspond to different governance scales.
4. **Family extraction**: Stable connected components at selected thresholds are treated as governance regimes (families), rather than mere clusters.

This method enables comparison without relying on proprietary internals: it uses only captured constitutions, normalized into a common representation, and justifies closeness/distance via explicit similarity scores and stability behavior.

## 3. The Prompt Family Landscape

**Family count and distribution.** The extraction yields 33 families across bands, but the landscape is dominated by a small number of stable regimes plus many threshold-induced singletons. Only a few families have size >1: key pairs (size 2), platform umbrellas (size 3–4), and cross-product umbrellas at lower thresholds (size 3–4). Confidence is correspondingly bimodal: high for stable multi-member regimes, low for repeated singletons that appear due to thresholding rather than durable separation.

**What similarity bands reveal about governance scale.**

- **High band (~0.74–0.71): mode-level near-identity.** Only one pair remains connected at these thresholds: the Copilot CLI interactive/prompt pair (weighted ≈0.742). This indicates near-identical interaction contracts with minor interface wrapper differences.
- **Mid band (~0.70–0.65): operational constitutions separate.** Most artifacts become singletons; only the OpenCode build/plan pair remains cohesive (weighted ≈0.634). This band distinguishes operational governance (tool discipline, phase separation, refusal posture) rather than surface structure.
- **Lower bands (~0.64–0.58): product/lineage umbrellas emerge.** Two IDE platform umbrellas become stable (Codex-in-VS Code; Copilot-in-VS Code), while non-IDE prompts merge into broader “developer workflow” umbrellas. This suggests that at these thresholds, shared platform embedding and shared workflow framing dominate over exact authority boundaries.

Band stability supports a three-level interpretation: **mode-level** similarity at the top band, **operational governance** in the mid band, and **product/lineage-level** governance at lower bands.

## 4. Comparative Analysis of Governance Regimes

### Family F1 (copilot-interactive-prompt-pair)

**Governance characteristics.** This regime encodes a terminal-assistant constitution with strong interaction discipline: concise responses, tool-first behavior, and explicit confidentiality constraints (non-disclosure of internal instructions). Authority is mediated through a rich tool surface (persistent bash sessions, file view/edit/create, GitHub MCP tools, web search) and a policy-final decision maker. It also encodes procedural constraints on tool usage (parallel tool calls, intent reporting rules, absolute-path requirements, and process-kill restrictions).

**Interaction contract.** A high-tempo, tool-mediated terminal workflow: minimal explanation, rapid tool execution, and strict refusal boundaries around sensitive data, harmful content, and instruction disclosure.

**Neighbor comparison (vs F2).** Both F1 and F2 are CLI-centered and tool-mediated, but F1 emphasizes _interaction protocol and confidentiality_ (e.g., instruction non-disclosure, documentation-first capability answers) while F2 emphasizes _workflow phase governance_ (plan vs build) and internal process controls (e.g., read-before-edit requirements, subagent delegation). The difference matters because it shifts governance from “how to converse and act safely in a terminal” (F1) to “how to structure multi-step engineering work across phases” (F2).

### Family F2 (opencode-build-plan-pair)

**Governance characteristics.** This regime encodes a workflow constitution with explicit phase separation: a plan/read-only mode that prohibits modifications and a build/execution mode that permits edits and command execution. It includes strong prohibitions around malicious code assistance and malware-adjacent work, restrictions on URL generation, and explicit git safety constraints (no commits/pushes unless requested; avoid destructive/interactive git operations). Tool mediation is explicit and specialized (read/glob/grep/edit/write/task/webfetch/todo/skill), with procedural rules such as “read before edit/write” and constraints on when subagents or todo tools may be used.

**Interaction contract.** A process-governed engineering assistant: minimal verbosity, explicit tool discipline, and a constitution that can switch authority envelopes by mode (read-only planning vs write-capable building).

**Neighbor comparison (vs F1).** Compared to F1’s emphasis on confidentiality and terminal interaction cadence, F2’s distinctive feature is _phase-locked authority_: plan mode hard-disables side effects, while build mode permits them under git and safety protocols. This difference matters because it externalizes governance into explicit operational phases rather than relying primarily on per-action prohibitions.

### Family F3 (singleton-codex-exec)

**Governance characteristics.** This execution-oriented constitution centers on local tool use (shell commands, patch editing, MCP resource access) with a sandbox/approval model and explicit prohibitions against destructive git/file actions unless requested or approved. It also encodes “stop-and-ask” behavior on unexpected workspace changes and a strong output contract (scan-friendly, path-referential, limited formatting).

**Interaction contract.** A local executor with user-consent gating: proceed via tools, avoid destructive actions, and halt on unexpected diffs.

**Neighbor comparison (vs F11/F19 umbrella).** Although F3 is a singleton at stricter thresholds, it later joins the Codex-in-VS Code umbrella at lower thresholds, indicating shared platform governance. The key difference at strict bands is likely the _mode-specific execution framing_ (exec) versus the broader IDE agent/chat constitutions; this matters because it suggests that “exec” is a specialized operational posture within a shared platform regime.

### Family F4 (singleton-codex-review)

**Governance characteristics.** This review constitution is structurally distinct: it enforces a strict output schema (valid JSON only), forbids speculative claims, forbids flagging pre-existing issues, and constrains comment bodies and code snippet length. It is evaluation-centric rather than action-centric, even though tool execution may be available.

**Interaction contract.** A constrained auditor: produce provable, schema-compliant findings with minimal, tightly scoped evidence.

**Neighbor comparison (vs F3).** Both are Codex-oriented and tool-capable, but F4’s authority is bounded by _epistemic and schema constraints_ (provability, JSON-only output, no PR fix generation), whereas F3 is bounded by _side-effect and consent constraints_ (destructive actions, approvals, unexpected changes). This difference matters because it encodes governance primarily as “what can be asserted and how it must be serialized,” not “what can be done.”

### Family F5 (singleton-vscode-codex-agent-full-access)

**Governance characteristics.** This regime resembles the Codex agent constitution but with an expanded permission envelope (full access, network enabled, approval_policy=never). It explicitly forbids requesting approvals and expects autonomous completion within the enlarged authority scope, while retaining prohibitions on destructive git actions and stop-on-unexpected-changes behavior.

**Interaction contract.** An autonomous local agent operating under a “no-interactive-approval” rule: proceed without consent prompts, but remain constrained against destructive actions and unexpected diffs.

**Neighbor comparison (vs F6/F7).** Relative to the standard agent/chat variants, the distinctive governance feature is the _approval-policy inversion_: the constitution removes the approval dialogue as a control surface, shifting governance toward internal restraint and validation before yielding. This matters because it changes where control is exercised—from user-mediated approvals to constitutional prohibitions and self-checks.

### Family F6 (singleton-vscode-codex-agent)

**Governance characteristics.** A tool-mediated IDE agent with sandbox/approval escalation rules, explicit destructive-action prohibitions, and stop-and-ask behavior on unexpected changes. It includes planning tool governance (when to plan, how to update plans) and strict output formatting conventions.

**Interaction contract.** A cooperative IDE agent: act via tools within sandbox constraints, escalate only under defined conditions, and keep outputs scan-friendly and path-referential.

**Neighbor comparison (vs F7).** Compared to chat mode, the agent constitution more explicitly encodes _operational loops_ (planning updates, escalation workflows) and side-effect management. This matters because it formalizes autonomy as a governed process rather than a conversational helper posture.

### Family F7 (singleton-vscode-codex-chat)

**Governance characteristics.** A conversational variant within the Codex-in-VS Code lineage, still tool-capable but framed around chat interaction. It retains the same core authority boundaries (no destructive actions without request/approval; stop on unexpected changes; sandbox/approval mediation) and the same output discipline.

**Interaction contract.** A chat-first interface to the same governed tool surface: conversational guidance with the option to act via tools under the same constraints.

**Neighbor comparison (vs F6).** The difference is primarily _interaction framing_ rather than authority: chat emphasizes explanation and dialogue, while agent emphasizes procedural execution governance. This matters because it suggests that within this lineage, “chat vs agent” is a mode-level contract layered atop a shared platform constitution.

### Family F8 (singleton-vscode-copilot-agent)

**Governance characteristics.** This IDE agent constitution encodes strong policy primacy (fixed refusal strings for disallowed content categories, explicit copyright avoidance), strict preamble/channel rules, and a broad tool surface including terminal execution, file operations, notebook tools, and subagents. It also encodes planning governance via a todo-list tool with strict state rules.

**Interaction contract.** A policy-governed IDE agent with explicit UI protocol: milestone preambles, tool-use opacity (do not announce tool choice), and structured planning when tasks are non-trivial.

**Neighbor comparison (vs F9/F10).** Compared to ask/plan variants, the agent mode has the broadest action surface (terminal, edits, subagents) and the most elaborate UI protocol. This matters because it concentrates governance in _policy compliance and interaction choreography_ rather than in sandbox/approval mechanics.

### Family F9 (singleton-vscode-copilot-ask)

**Governance characteristics.** A non-agentic assistance constitution emphasizing short, impersonal answers, policy compliance, and limited tool access (read/search/diff/symbol tools; no explicit edit/terminal tool in this capture). It includes operational prohibitions around commits and destructive actions, but the tool surface suggests a primarily advisory posture.

**Interaction contract.** A read-oriented IDE assistant: inspect and explain, with strong policy/refusal constraints and limited side-effect capability.

**Neighbor comparison (vs F12 pair).** Ask aligns closely with plan at lower thresholds (F12), indicating shared non-agentic governance. The difference matters because it separates “answering” from “planning” while keeping both within a read-oriented, policy-first authority envelope.

### Family F10 (singleton-vscode-copilot-plan)

**Governance characteristics.** A planning-only constitution with hard prohibitions on implementation and editing, plus a mandated research step via a subagent tool and a rule forbidding further tool calls after that step. It retains the same policy primacy (fixed refusal strings, copyright avoidance) and the same preamble/channel governance.

**Interaction contract.** A deliberation-only regime: produce a plan under strict workflow sequencing and without side effects.

**Neighbor comparison (vs F2 plan mode).** Both encode planning constraints, but this regime’s distinctive feature is _tool-call choreography_ (mandatory subagent-first, then no more tools) and _UI protocol_ (commentary preambles), whereas F2’s plan mode is primarily a _permission envelope_ (read-only) within a broader CLI workflow constitution. This matters because it shows two different ways to govern planning: sequencing constraints vs permission constraints.

### Family F11 (vscode-codex-agent-chat-cluster)

**Governance characteristics.** This stable platform regime unifies Codex execution/agent/chat/full-access variants at lower thresholds (avg weighted similarity ≈0.636–0.639 across repeated appearances). Shared constitutional features include: sandbox/approval mediation (even when disabled by policy), destructive-action prohibitions, stop-on-unexpected-changes behavior, MCP resource preference, and strict output formatting (scan-friendly, path references, minimal formatting).

**Interaction contract.** A platform constitution for local code work: tool-mediated action with consent/permission logic, and a strong “do no harm to the workspace” posture.

**Neighbor comparison (vs F18).** Both are IDE platform umbrellas, but this regime’s governance centers on _sandbox/approval and workspace integrity_ (unexpected changes, destructive commands), while the Copilot VS Code regime centers on _policy primacy, refusal strings, and UI protocol_ (preambles, tool opacity, todo governance). This difference matters because it locates control in different institutions: environment permissions vs policy-and-protocol constraints.

### Family F12 (vscode-copilot-ask-plan-pair)

**Governance characteristics.** A non-agentic Copilot VS Code regime where both modes share policy primacy, short/impersonal style, and limited side effects. Plan adds explicit planning templates and tool-call sequencing constraints; ask remains Q&A oriented.

**Interaction contract.** Advisory and deliberative assistance without autonomous execution.

**Neighbor comparison (vs F8).** The key difference is _authority surface_: F8 includes execution and editing tools plus todo governance for multi-step work, while F12 is closer to read/plan assistance. This matters because it separates “assistant as planner/advisor” from “assistant as acting agent” within the same platform lineage.

### Families F13–F33 (repeated singletons and lower-threshold umbrellas)

Across F13–F33, the repeated singleton families largely reflect threshold artifacts rather than stable distinct regimes, with two exceptions supported by stability behavior:

- **Codex review remains isolated across all bands** (F4/F13/F20/F28/F33), indicating a genuinely distinct governance posture centered on evaluation and schema compliance rather than action.
- **Non-IDE prompts merge into broader umbrellas at low thresholds** (F25, F30), indicating shared developer-work framing but weaker alignment on authority boundaries and tool mediation.

## 5. Cross-Tool and Cross-Vendor Comparison

**Codex-oriented vs Copilot-oriented families.**

- **Codex-oriented regimes (CLI exec; VS Code Codex umbrella)** emphasize _environment-mediated authority_: sandbox modes, approval policies, escalation parameters, and workspace integrity rules (not reverting unrelated changes; stop on unexpected diffs; destructive git prohibitions).
- **Copilot-oriented regimes (Copilot CLI pair; VS Code Copilot umbrella)** emphasize _policy-mediated authority and interaction protocol_: fixed refusal strings, confidentiality of internal instructions, UI preamble rules, tool opacity (“do not announce tool choice”), and structured planning via todo or plan templates.

**Convergence patterns (shared governance primitives).**

1. **Tool mediation as constitutional structure**: all regimes define explicit tool surfaces and invocation constraints, treating tools as the legitimate channel for side effects.
2. **Side-effect risk controls**: destructive-action prohibitions and cautious file/command handling recur across tools, though implemented via different mechanisms (approvals vs confirmations vs prohibitions).
3. **Mode separation**: multiple tools encode distinct constitutions for plan vs act vs ask/review, indicating a common governance pattern of authority envelopes by mode.

**Divergence patterns (distinct authority or safety models).**

- **Consent and permissions** diverge: Codex regimes encode explicit approval/escalation mechanics; Copilot VS Code regimes encode policy primacy and confirmation rules rather than a sandbox escalation protocol in the captured constitutions.
- **Refusal formalism** diverges: Copilot VS Code constitutions include fixed-string refusal requirements for certain categories; Codex and OpenCode emphasize procedural safety constraints and do not show the same fixed-phrase mechanism in the captured artifacts.
- **Interaction protocol** diverges: Copilot VS Code encodes commentary-channel preambles and tool opacity as governance; Codex regimes encode output scanability and file reference formats but not the same UI cadence rules.

**Mode-driven vs product-driven vs lineage-driven differences.**

- **Mode-driven**: plan vs agent vs chat/ask differences are visible within each platform umbrella (e.g., planning-only prohibitions; chat vs agent interaction framing).
- **Product-driven**: IDE embedding produces stable umbrellas (Codex-in-VS Code; Copilot-in-VS Code) that persist across thresholds, indicating platform-level governance contracts.
- **Lineage-driven**: non-IDE Copilot and OpenCode merge only at lower thresholds, suggesting shared developer-work framing but distinct operational governance.

## 6. Key Findings

1. **IDE embedding produces stable platform constitutions**: both VS Code umbrellas remain cohesive across multiple lower thresholds, indicating durable platform-level governance regimes rather than mode-specific templates.
2. **High-band similarity isolates near-identical interaction wrappers**: only the Copilot CLI interactive/prompt pair clusters at ~0.72 (weighted ≈0.742), consistent with a single constitution expressed through two entrypoints.
3. **Operational governance separates sharply at mid bands**: at ~0.68, most artifacts become singletons except the OpenCode build/plan pair, indicating that operational authority/tool contracts diverge even when structural schemas align.
4. **Review governance is constitutionally distinct**: the review regime remains isolated across all bands, reflecting a different authority model centered on provability and strict output schemas rather than tool-mediated action.
5. **Governance shifts from permission control to protocol control across lineages**: Codex-oriented regimes emphasize sandbox/approval mechanics; Copilot-oriented regimes emphasize policy primacy, refusal formalism, and UI/tool-use protocol.

## 7. Implications

**For tool designers.** The dataset suggests two dominant governance strategies: (a) permission- and approval-mediated authority (sandbox/escalation), and (b) protocol- and policy-mediated authority (fixed refusals, UI cadence, tool opacity). Designers can treat these as composable constitutional modules rather than monolithic prompts, selecting control surfaces appropriate to the environment (local CLI vs IDE) and mode (plan vs act vs review).

**For researchers studying agentic systems.** Band stability indicates that governance regimes can be meaningfully separated by scale: mode-level wrappers, operational constitutions, and platform-level umbrellas. This supports comparative work that focuses on authority boundaries and tool mediation rather than stylistic differences.

**For future prompt-governance evolution.** The presence of explicit phase separation (plan vs build) and explicit UI protocol (preambles, tool opacity) suggests a trend toward externalizing governance into structured workflows and interaction contracts, not merely expanding instruction length.

## 8. Limitations and Future Work

This analysis cannot conclude actual runtime enforcement, true permission boundaries, or data handling practices beyond what is encoded in the constitutions. It also cannot attribute intent beyond the explicit governance text and tool schemas captured.

Future work that would strengthen comparisons includes: (1) temporal/versioned captures to test regime stability over time, (2) additional tools and domains beyond developer workflows, (3) richer environment captures that clarify active sandbox/network settings, and (4) systematic feature audits that quantify specific authority primitives (approval gates, refusal formalism, tool opacity, schema enforcement) across regimes.

## 9. Conclusion

Modern developer tools converge on treating system constitutions as governance layers that define authority, tool mediation, and termination behavior. They diverge primarily in where control is institutionalized: environment permissions and approvals versus policy formalism and interaction protocol. Similarity bands and stability behavior show that governance operates at multiple scales—mode, operational workflow, and platform lineage—making constitutional analysis a defensible lens for comparing agent architectures without relying on proprietary internals.
