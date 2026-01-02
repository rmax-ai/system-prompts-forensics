### 1. Introduction

This report compares how contemporary AI-assisted developer tools encode governance—authority, constraints, and interaction contracts—through their system-level constitutions. The scope covers CLI and IDE-integrated assistants spanning Codex-oriented and Copilot-oriented products, plus an agentic CLI tool (opencode). Rather than treating these constitutions as task instructions, the analysis treats them as governance artifacts: they define who may act, what may be observed, which tools mediate action, how conflicts are resolved, and when interaction must stop.

Across the dataset, five stable governance regimes (prompt families) emerge alongside a tail of unstable singletons. The stable regimes correspond to: (i) a tightly coupled Copilot CLI interactive/base pair, (ii) a VSCode-integrated Codex trio with permission gradients, (iii) a Codex exec/review split, (iv) an opencode plan/build split, and (v) a VSCode Copilot trio segmented by ask/plan/agent modes.

---

### 2. Methodological Summary

The workflow normalizes heterogeneous system constitutions into a shared structural schema (identity, authority, scope, tools, constraints, correction, termination), reducing stylistic variance while preserving governance semantics. Similarity is then measured pairwise using a weighted score combining structural overlap, token-level similarity, and forbidden-action similarity. Band analysis evaluates how connected components form as similarity thresholds change, revealing stability ranges where regimes cohere. Prompt families are extracted as stable governance regimes within high-similarity bands, enabling comparison without relying on proprietary internals or performance claims.

This method supports defensible cross-tool comparison because it operates on observable constitutional content (roles, tool surfaces, prohibitions, escalation rules, output contracts) rather than model behavior or hidden implementation details.

---

### 3. The Prompt Family Landscape

**Family structure.** The landscape contains **15 families**, of which **5 are multi-member stable regimes (F1–F5)** and **10 are singletons (F6–F15)**. The multi-member regimes range from **2 to 3 members** each, indicating that most stable regimes are either paired variants (base + mode overlay; phase split) or small mode suites (chat/agent/full-access; ask/plan/agent). Confidence is **high** for F1, F2, and F4; **medium** for F3 and F5; and **low** for the singleton tail, which overlaps with the multi-member regimes and is best interpreted as an artifact of assignment rather than distinct constitutions.

**Similarity bands and scale.** Band stability shows that at **0.77** all artifacts are isolated; at **0.76–0.74** only very tight pairs form; at **0.71–0.70** small operational suites (pairs/trios) appear; and at **0.57** everything collapses into a single component. Interpreted as governance scale:
- **~0.76** captures near-identical constitutions (variant overlays within the same regime).
- **~0.71** captures **operational governance regimes**: shared interaction contracts with meaningful mode/phase differentiation.
- **≤0.57** collapses into **product-level commonalities** (shared schema and generic agent scaffolding), too coarse to distinguish regimes.

---

### 4. Comparative Analysis of Governance Regimes

#### F1 (0.74–0.77): copilot-interactive-prompt-pair (high)

**Governance characteristics.**
- **Authority boundaries:** Policy is explicitly the final arbiter (final decision maker = policy). Prohibitions include confidentiality of system rules, restrictions on sensitive data sharing, secrets in code, harmful content, and copyright infringement. There are also operational prohibitions (e.g., avoid pkill/killall; minimize deletions).
- **Scope and visibility:** Persistent session behavior is present (session persistence true), and at least one variant indicates memory may be enabled; the constitution assumes an interactive terminal context with environment snapshots and tool outputs visible.
- **Tool mediation:** A broad tool surface is declared: persistent bash sessions (sync/async), filesystem view/edit/create with absolute-path constraints, search tools (grep/glob), UI intent reporting, documentation fetch for capability questions, GitHub MCP tools, and web search. Tool invocation rules emphasize parallelization, suppression of verbose output, and strict pairing rules for UI intent reporting.
- **Correction and termination:** Self-review is oriented toward regression avoidance (baseline and post-change checks) and minimal edits. Termination includes stopping when blocked by limitations or when user guidance is required.

**Interaction contract.** This regime encodes a **terminal assistant contract**: act through tools with minimal explanation, keep responses short, and treat policy/confidentiality as overriding user requests. It also encodes a “documentation-first” epistemic rule for capability questions, shifting authority from assistant memory to an internal documentation tool.

**Comparison to neighboring family (F5).** Both F1 and F5 are Copilot-oriented and policy-governed, but F1’s constitution is **interaction-first and tool-efficiency-first** (parallel tool calls, UI intent reporting, documentation fetch), whereas F5 is **mode-segmented** (ask/plan/agent) with stronger IDE-specific channel governance and identity constraints. The difference matters because F1 centralizes governance in tool mediation and operational efficiency, while F5 centralizes governance in mode routing and output-channel discipline.

---

#### F2 (0.70–0.72): vscode-codex-agent-chat-trio (high)

**Governance characteristics.**
- **Authority boundaries:** The core boundary is **consent and workspace integrity**: prohibitions against destructive git/file operations without explicit request/approval, prohibitions against reverting user changes, and mandatory stop-and-ask behavior on unexpected changes. Approval policy and sandbox mode parameterize authority; in standard variants, the user is the final decision maker for escalation, while the full-access variant disables escalation and shifts final decision making to the agent within the configured mode.
- **Scope and visibility:** The constitution assumes local execution with explicit environment context (sandbox_mode, network_access, approval_policy, writable_roots). Memory and persistence are off. Visibility includes tool outputs and limited IDE context (e.g., open tabs list).
- **Tool mediation:** Tools are tightly scoped to local action: shell command execution with workdir constraints, patch application, plan updates, image attachment, and MCP resource listing/reading. Invocation rules encode a procedural escalation mechanism (rerun with escalated permissions plus a one-sentence justification, without pre-messaging).
- **Correction and termination:** Correction is tied to plan updates and sandbox failures; termination includes pausing for user instruction when blocked by approvals or when unexpected changes are detected.

**Interaction contract.** This regime encodes a **sandboxed local coding agent contract**: the agent may act, but authority is mediated by explicit environment parameters and a consent workflow. The constitution treats the user’s workspace state (dirty worktree, unexpected changes) as a protected asset, requiring procedural halts rather than unilateral remediation.

**Comparison to neighboring family (F3).** Both are Codex-oriented and tool-mediated, but F2 is a **single-agent constitution with parameterized permissions**, whereas F3 is a **separation-of-duties regime** (execution vs review). The difference matters because F2’s governance is primarily about *how* to act safely in a shared environment, while F3’s governance is about *who* is authorized to judge correctness and what outputs are permitted.

---

#### F3 (0.70–0.72): codex-exec-review-pair (medium)

**Governance characteristics.**
- **Authority boundaries:** The exec constitution emphasizes safe execution (avoid destructive commands, stop on unexpected changes, do not amend commits unless asked) and tool-mediated escalation when permitted. The review constitution sharply constrains authority by **limiting what may be criticized** (only issues introduced in the commit), forbidding speculative claims, and forbidding generating a PR fix. It also imposes strict output constraints (schema-matching JSON only).
- **Scope and visibility:** Both assume local tool access and MCP resources, but the review constitution assumes access to diff context sufficient to cite precise code locations and overlap line ranges.
- **Tool mediation:** Both declare shell_command and MCP tools; review additionally allows apply_patch but constitutionally discourages using it for fixes. Tool choice is auto and parallel tool calls are disabled in the review capture, indicating a more serialized, controlled workflow.
- **Correction and termination:** Review includes explicit self-checks for schema compliance and commit-introduced-only findings; termination is defined by producing a complete set of qualifying findings (or none) and a verdict.

**Interaction contract.** This regime encodes a **two-role pipeline**: one constitution authorizes action in the workspace; the other authorizes judgment under strict evidentiary and formatting constraints. The review role is governance-heavy in output contract (machine-validated JSON) and epistemic restraint (provable impact, no speculation).

**Comparison to neighboring family (F4).** Both are phase-separated regimes, but F3’s second phase is **audit/verification** with constrained authority and strict output schema, whereas F4’s second phase is **implementation** with operational tool constraints. The difference matters because F3 externalizes risk control into a distinct constitutional role, while F4 internalizes risk control into phase-specific permissions (read-only vs write).

---

#### F4 (0.70–0.72): opencode-build-plan-pair (high)

**Governance characteristics.**
- **Authority boundaries:** The defining boundary is **plan-mode read-only governance**: in plan mode, file edits and system-changing commands are forbidden. Outside plan mode, authority expands to editing/writing with tool-enforced read-before-edit/write constraints. A prominent safety boundary is refusal of malware/malicious-code assistance, including refusal to explain or improve suspicious code.
- **Scope and visibility:** Local filesystem and terminal outputs are visible; web access exists via a dedicated fetch tool but is constrained by a “no URL guessing” rule. Session persistence is enabled, but memory is off.
- **Tool mediation:** The tool surface is broad and explicitly structured: dedicated read/glob/grep/edit/write tools, bash with a safety protocol (especially for git), a task tool for subagents, todo tools, and a skill loader. Invocation rules discourage using bash for file operations and enforce read-before-edit/write.
- **Correction and termination:** Correction includes post-task lint/typecheck when commands are discoverable, but plan mode forbids execution. Termination in plan mode is explicitly “stop after producing a plan / clarifying questions,” and after file work it stops without extra summary unless requested.

**Interaction contract.** This regime encodes a **process-oriented CLI agent contract**: governance is enforced through phase gating (plan vs build), tool separation (specialized file tools vs bash), and categorical refusals for malware-adjacent work. It also encodes a minimalism contract (very short responses unless requested) and explicit limits on proactive behavior (be proactive only within user-requested actions).

**Comparison to neighboring family (F2).** Both are local tool-using agents, but F4’s governance is **tool-architecture-driven** (specialized tools, read-before-write enforcement, subagent delegation) and includes a strong malicious-code refusal boundary, whereas F2’s governance is **sandbox/approval-driven** (escalation parameters, user consent as final authority). The difference matters because F4 relies on internal tool discipline to bound risk, while F2 relies on external permissioning and user approvals.

---

#### F5 (0.70–0.72): vscode-copilot-agent-ask-plan-trio (medium)

**Governance characteristics.**
- **Authority boundaries:** Policy is the final decision maker. Identity is partially fixed (mandated responses for name/model queries). Safety governance includes fixed-string refusal for specified harmful categories and copyright avoidance. Operational authority is segmented: ask mode is largely read/search; agent mode includes editing and terminal execution; plan mode forbids implementation and imposes a mandatory research subagent step.
- **Scope and visibility:** The constitution assumes an IDE environment with tool-mediated workspace access. Memory and persistence are off. A distinctive feature is **channel governance**: commentary-channel preambles are required before tool call batches, with strict non-leakage rules.
- **Tool mediation:** Tool surfaces are extensive and IDE-specific: workspace search/read tools, diff/error retrieval, terminal execution, notebook tooling with strict constraints, todo management, subagent invocation, and limited web fetch/repo search tools. Invocation rules encode workflow discipline (todo state machine, exact-match replacement constraints, notebook execution rules).
- **Correction and termination:** Correction is tied to diagnostics (errors/tests) and todo completion. Plan mode termination is explicit: stop after presenting a plan and request feedback; no tool calls after the research subagent returns.

**Interaction contract.** This regime encodes a **mode-routed IDE assistant contract**: user intent is routed into ask/plan/agent constitutions with distinct authority and tool surfaces. It also encodes a **presentation contract** (preambles, markdown formatting, sometimes emoji requirements) that governs how actions are narrated and how internal governance is kept confidential.

**Comparison to neighboring family (F1).** Both are Copilot-oriented and policy-governed with broad tool surfaces, but F5 is more **constitutionally segmented by mode** and more **presentation-governed** (channel separation, preamble cadence, fixed identity strings). F1 is more **terminal-operational** (parallel tool calls, documentation fetch, absolute-path file ops) and less focused on multi-channel narration. The difference matters because F5 treats interaction framing as a governance mechanism (what can be said, where, and how), while F1 treats tool discipline and minimal-change norms as the primary governance mechanism.

---

#### F6–F15: singleton-other (low)

These singletons overlap with the multi-member regimes (e.g., artifacts already present in F2–F5 also appear as singletons). Given the band analysis and the family interpretation memo, they are best treated as **boundary echoes** produced by the extraction procedure rather than independent governance regimes. They do not add stable constitutional patterns beyond what is captured in F1–F5.

---

### 5. Cross-Tool and Cross-Vendor Comparison

**Codex-oriented vs Copilot-oriented families.**
- Codex-oriented regimes (F2, F3) emphasize **workspace integrity and procedural consent**: prohibitions on destructive operations, stop-on-unexpected-changes, and explicit escalation workflows tied to sandbox/approval parameters. Governance is frequently expressed as *procedures for acting safely* in a local environment.
- Copilot-oriented regimes (F1, F5) emphasize **policy primacy and interaction-channel governance**: confidentiality of system rules, fixed refusal strings for certain categories, fixed identity/model disclosures, and structured narration (preambles) around tool use. Governance is frequently expressed as *constraints on what may be said and how actions are mediated through UI/tooling*.

**Convergence (shared governance patterns).**
1. **Tool-mediated authority** is universal: action is permitted primarily through declared tools with explicit invocation constraints (workdir requirements, absolute paths, exact-match edits, batching rules).
2. **Protected user state** appears across regimes: avoid destructive operations, avoid unintended file loss, and require explicit user intent for high-risk actions (commits, destructive commands).
3. **Mode/phase segmentation** is common: chat vs agent vs full-access; ask vs plan vs agent; plan vs build; exec vs review. Governance increasingly appears as a suite of constitutions rather than a single monolith.

**Divergence (distinct authority or safety models).**
- **Consent model divergence:** Codex regimes encode consent via sandbox approvals and escalation parameters with the user as final authority (in standard modes), while Copilot regimes encode consent via policy finality and fixed refusal/identity constraints.
- **Safety scope divergence:** opencode uniquely foregrounds malware/malicious-code refusal as a primary boundary; Copilot foregrounds content-policy categories and confidentiality; Codex foregrounds destructive-operation avoidance and workspace integrity.
- **Narration governance divergence:** VSCode Copilot encodes a strong two-channel contract (commentary preambles vs final answers) and prohibits leakage through preambles; Codex CLI regimes focus more on output scanability and file reference formatting than on channel separation.

**Mode-driven vs product-driven vs lineage-driven differences.**
- Many differences are **mode-driven** (plan-only vs build/agent; read-only vs full-access) as shown by tight within-family similarity (F1, F2, F4).
- Some differences are **product-driven** (IDE narration/preambles, notebook tool governance, todo state machines in VSCode Copilot).
- Lineage effects are visible but conservative: Codex families share a consent/sandbox framing; Copilot families share policy primacy and confidentiality constraints. Similarity scores indicate that cross-vendor structural similarity remains high (structural similarity often near 1.0), suggesting shared constitutional scaffolding even where authority models diverge.

---

### 6. Key Findings

1. **Governance converges on tool-mediated constitutions**: authority is primarily exercised through declared tools with explicit invocation constraints, rather than through free-form action.
2. **Governance diverges on the locus of final authority**: Codex regimes frequently place escalation decisions with the user via approval workflows, while Copilot regimes more often place final authority with policy, including fixed refusal and identity constraints.
3. **Operational safety is encoded as workspace-state protection across tools**, especially via prohibitions on destructive commands and mandatory stop-and-ask behavior when unexpected changes are detected.
4. **Mode/phase segmentation is a dominant governance pattern**: stable regimes are suites of constitutions (ask/plan/agent; chat/agent/full-access; plan/build; exec/review) rather than single constitutions.
5. **At similarity thresholds around ~0.71, regimes reflect operational interaction contracts**, while below ~0.57 the landscape collapses into product-level common scaffolding, indicating a governance “phase transition” from regime-specific to generic agent structure.

---

### 7. Implications

**For tool designers.** The evidence suggests that robust governance is increasingly achieved by **constitutional modularity**: separate modes/phases with distinct authority boundaries and tool surfaces. Designers can externalize risk control by (i) gating side effects via explicit approval parameters, (ii) enforcing tool-level preconditions (e.g., read-before-write), and (iii) using strict output contracts (schemas) where downstream automation depends on compliance.

**For researchers studying agentic systems.** Prompt families behave like **stable governance regimes**: they encode recurring constitutional primitives (escalation workflows, protected workspace invariants, tool invocation law, narration/channel separation). Comparative work should focus on these primitives rather than surface wording, and should treat similarity bands as evidence for regime boundaries.

**For future prompt-governance evolution.** The trajectory implied by the regimes is toward **multi-constitution systems**: governance is distributed across mode routers, phase gates, and tool contracts. This supports more granular authority allocation (e.g., planning without execution; review without fixing) without requiring a single constitution to cover all cases.

---

### 8. Limitations and Future Work

This analysis cannot conclude actual runtime enforcement, real permission boundaries, or the effectiveness of safeguards; it only characterizes what is encoded constitutionally. It also cannot resolve whether the singleton families represent genuine regimes, given their overlap with multi-member regimes and the sensitivity of family extraction to thresholding.

Future work would be strengthened by: (i) additional temporal versions to test regime stability over time, (ii) more tools and domains beyond developer tooling, (iii) a strict partitioning or explicit multi-membership rationale for family assignment, and (iv) richer environment captures that explicitly state active sandbox/network/approval settings for all artifacts.

---

### 9. Conclusion

Modern developer tools encode governance through constitutions that define authority boundaries, tool-mediated action, protected workspace invariants, and termination/correction rules. The comparative landscape shows both convergence—shared reliance on tool contracts and safety invariants—and divergence—different loci of final authority (user approval workflows vs policy primacy) and different governance mechanisms (phase gating, mode routing, narration/channel separation). Treating these constitutions as governance artifacts provides a practical lens for comparing agent architectures without relying on proprietary internals, and it highlights modular constitutional design as a central pattern in contemporary developer tooling.