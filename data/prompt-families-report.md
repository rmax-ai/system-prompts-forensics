### 1. Overview

- **Number of families:** 15 total, of which **5 are multi-member regimes (F1–F5)** and **10 are singletons (F6–F15)**.
- **Overall similarity landscape:** The landscape is **bimodal**: a small set of **tight, stable families** (notably F1, F2, F4) and a long tail of **unstable/isolated singletons** that likely reflect either (a) prompts that do not robustly cohere with others at the chosen band, or (b) artifacts of the family construction procedure (see Limitations).
- **What the band ranges imply:** All families sit in **high similarity bands (~0.70–0.77)**, which corresponds to **mode-level to operational-level similarity** rather than mere lineage. Families in these bands should be interpreted as sharing a common **interaction contract** (role framing, authority posture, and workflow shape), not just topical overlap. The narrow band ranges suggest the clustering is sensitive to thresholding: small changes could merge/split families.

---

### 2. Family-by-family interpretation

#### Family F1: copilot-interactive-prompt-pair

- **Members** `copilot.interactive.analysis.yaml; copilot.prompt.analysis.yaml`

- **Band and stability** Band **0.74–0.77** with threshold **0.76** indicates **very high cohesion**: these two prompts likely differ only in surface framing (e.g., “interactive” wrapper vs base “prompt”) while preserving the same governance constitution. This is the tightest regime in the file.

- **Governance characteristics** The naming suggests a **Copilot-style assistant** with an **interactive contract**: iterative turn-taking, user-in-the-loop clarification, and a “helpful IDE companion” posture rather than autonomous execution. The pair structure implies a **base constitution** (“prompt”) plus an **interaction modality overlay** (“interactive”) that constrains how the assistant engages (e.g., ask/confirm before acting, incremental steps).

- **What differentiates this family** Relative to the VSCode-* agent/chat families, this regime is likely **less agentic** and more **conversationally scaffolded**: it emphasizes interaction management over tool authority. It is also more internally consistent than the Codex exec/review pair, suggesting fewer role bifurcations.

- **Confidence assessment** **High** is supported by the **highest similarity band** and the minimal membership (a clean pair) consistent with a stable “base + variant” constitution.

---

#### Family F2: vscode-codex-agent-chat-trio

- **Members** `vscode-codex.agent-full-access.analysis.yaml; vscode-codex.agent.analysis.yaml; vscode-codex.chat.analysis.yaml`

- **Band and stability** Band **0.70–0.72** at **0.71** indicates **strong operational similarity** across three variants. The presence of “agent”, “agent-full-access”, and “chat” within one family suggests a shared core constitution with **permissioning and interaction-mode toggles**.

- **Governance characteristics** This appears to be a **VSCode-integrated Codex governance regime** with a spectrum from **chat** (conversational assistance) to **agent** (more autonomous workflow) to **full-access agent** (expanded authority). The trio implies a single constitutional template that parameterizes:
  - **Authority scope** (standard vs full-access),
  - **Interaction contract** (chat vs agentic),
  - Likely a consistent environment framing (VSCode context, coding tasks).

- **What differentiates this family** Compared to the VSCode-Copilot trio (F5), this family is distinguished by the **Codex lineage** and explicit **full-access** variant, implying a more formalized permission gradient inside the same regime. Compared to Copilot interactive (F1), it is more **tool/authority-oriented** and less purely conversational.

- **Confidence assessment** **High** is justified by a coherent three-member set with clear internal role variants that still remain within a tight similarity band.

---

#### Family F3: codex-exec-review-pair

- **Members** `codex.exec.analysis.yaml; codex.review.analysis.yaml`

- **Band and stability** Band **0.70–0.72** at **0.71** suggests these two prompts are intended as a paired regime, but the **average similarity is notably lower** than other multi-member families, indicating **role separation** is substantial: “exec” and “review” are complementary but constitutionally distinct.

- **Governance characteristics** The pair encodes a **two-phase governance pipeline**:
  - **Execution constitution** (“exec”): oriented toward producing changes/solutions.
  - **Review constitution** (“review”): oriented toward critique, verification, and risk control.
  The existence of a stable pair implies a governance design that **splits authority**: one role acts, another audits. This is a structural separation of duties rather than a mere stylistic variant.

- **What differentiates this family** Unlike F2/F5 where variants are mode toggles within one assistant identity, F3 is differentiated by **functional bifurcation** (do vs evaluate). It is closer to a “workflow constitution” than a single assistant persona.

- **Confidence assessment** **Medium** aligns with the weaker cohesion signal: the pair is plausible as a designed regime, but the similarity suggests they may be only loosely aligned beyond shared Codex lineage.

---

#### Family F4: opencode-build-plan-pair

- **Members** `opencode.build.analysis.yaml; opencode.plan.analysis.yaml`

- **Band and stability** Band **0.70–0.72** at **0.71** with relatively high average similarity indicates a **stable two-part regime** where “plan” and “build” are tightly coupled—more so than the Codex exec/review split.

- **Governance characteristics** The naming implies a governance constitution that explicitly separates:
  - **Planning** (deliberation, decomposition, sequencing),
  - **Building** (implementation/execution).
  Compared to exec/review, plan/build is typically a **forward pipeline** (decide → implement) rather than an adversarial check. The tightness suggests the same authority model and interaction contract, with only the **task phase** changing.

- **What differentiates this family** This family differs from F3 by emphasizing **preparatory planning** rather than **post-hoc review**. It differs from VSCode-* families by being less tied to an IDE-branded assistant identity and more to a **process-oriented constitution** (“opencode” as a product/lineage marker).

- **Confidence assessment** **High** is supported by strong cohesion and a clear, interpretable two-phase structure that commonly shares a single constitutional template.

---

#### Family F5: vscode-copilot-agent-ask-plan-trio

- **Members** `vscode-copilot.agent.analysis.yaml; vscode-copilot.ask.analysis.yaml; vscode-copilot.plan.analysis.yaml`

- **Band and stability** Band **0.70–0.72** at **0.71** indicates operational similarity, but with **moderate cohesion**: “agent”, “ask”, and “plan” are more behaviorally distinct than simple naming variants, suggesting multiple interaction contracts under a shared VSCode-Copilot umbrella.

- **Governance characteristics** This looks like a **VSCode Copilot regime** with three constitutions or sub-constitutions:
  - **ask**: a constrained, question-answer/helpdesk mode (user-led).
  - **plan**: a deliberative mode emphasizing structured decomposition.
  - **agent**: a more autonomous mode emphasizing action sequencing.
  The trio suggests a governance design that **routes user intent** into different operational modes rather than a single uniform assistant.

- **What differentiates this family** Relative to F2 (VSCode Codex), this family’s differentiation is less about permission (“full-access”) and more about **interaction intent routing** (“ask/plan/agent”). Relative to F1, it is less purely interactive and more explicitly **workflow-mode segmented**.

- **Confidence assessment** **Medium** is consistent with the weaker cohesion: the three modes may share branding and environment framing but diverge constitutionally in authority and workflow.

---

#### Family F6: singleton-other

- **Members** `codex.exec.analysis.yaml`

- **Band and stability** As a singleton at the same band/threshold as multi-member families, this indicates **instability or duplication in family assignment** rather than a meaningful standalone regime. Given that `codex.exec` already appears in F3, this singleton likely reflects a boundary/assignment artifact.

- **Governance characteristics** Interpretable only as the **exec** constitution within Codex; as a singleton it provides no additional stable regime evidence beyond F3.

- **What differentiates this family** It does not differentiate meaningfully; it is best treated as a **boundary case** of F3 rather than an independent constitution.

- **Confidence assessment** **Low** is appropriate: singleton status plus apparent overlap with F3 undermines regime distinctness.

---

#### Family F7: singleton-other

- **Members** `codex.review.analysis.yaml`

- **Band and stability** Same singleton caveat as F6; also overlaps with F3 membership.

- **Governance characteristics** The **review** constitution; likely an auditing/checking posture.

- **What differentiates this family** Best interpreted as the other half of F3 rather than a separate regime.

- **Confidence assessment** **Low** due to singleton status and overlap.

---

#### Family F8: singleton-other

- **Members** `opencode.build.analysis.yaml`

- **Band and stability** Singleton despite being in F4 suggests assignment instability.

- **Governance characteristics** The **build** phase constitution within Opencode.

- **What differentiates this family** Not meaningfully distinct from F4; likely a boundary artifact.

- **Confidence assessment** **Low**.

---

#### Family F9: singleton-other

- **Members** `opencode.plan.analysis.yaml`

- **Band and stability** Same as F8; overlaps with F4.

- **Governance characteristics** The **plan** phase constitution within Opencode.

- **What differentiates this family** Not meaningfully distinct from F4; likely a boundary artifact.

- **Confidence assessment** **Low**.

---

#### Family F10: singleton-other

- **Members** `vscode-codex.agent-full-access.analysis.yaml`

- **Band and stability** Singleton despite inclusion in F2 suggests the “full-access” variant may sit near a threshold boundary or the family construction emitted both grouped and ungrouped representations.

- **Governance characteristics** A **high-authority agent** constitution (expanded permissions) within VSCode Codex.

- **What differentiates this family** Potentially the most authority-permissive constitution among VSCode Codex variants; however, the singleton status prevents treating it as independently stable.

- **Confidence assessment** **Low**.

---

#### Family F11: singleton-other

- **Members** `vscode-codex.agent.analysis.yaml`

- **Band and stability** Singleton artifact given membership in F2.

- **Governance characteristics** Standard **agent** constitution in VSCode Codex.

- **What differentiates this family** Not meaningfully distinct from F2 without additional evidence.

- **Confidence assessment** **Low**.

---

#### Family F12: singleton-other

- **Members** `vscode-codex.chat.analysis.yaml`

- **Band and stability** Singleton artifact given membership in F2.

- **Governance characteristics** **Chat** constitution in VSCode Codex (lower autonomy).

- **What differentiates this family** Not meaningfully distinct from F2 without additional evidence.

- **Confidence assessment** **Low**.

---

#### Family F13: singleton-other

- **Members** `vscode-copilot.agent.analysis.yaml`

- **Band and stability** Singleton artifact given membership in F5.

- **Governance characteristics** **Agent** constitution in VSCode Copilot.

- **What differentiates this family** Not meaningfully distinct from F5 without additional evidence.

- **Confidence assessment** **Low**.

---

#### Family F14: singleton-other

- **Members** `vscode-copilot.ask.analysis.yaml`

- **Band and stability** Singleton artifact given membership in F5.

- **Governance characteristics** **Ask/Q&A** constitution in VSCode Copilot.

- **What differentiates this family** Not meaningfully distinct from F5 without additional evidence.

- **Confidence assessment** **Low**.

---

#### Family F15: singleton-other

- **Members** `vscode-copilot.plan.analysis.yaml`

- **Band and stability** Singleton artifact given membership in F5.

- **Governance characteristics** **Planning** constitution in VSCode Copilot.

- **What differentiates this family** Not meaningfully distinct from F5 without additional evidence.

- **Confidence assessment** **Low**.

---

### 3. Cross-family structure

- **Layering by product lineage (outer layer):**
  - **Copilot (generic)**: F1 (Copilot interactive/base).
  - **VSCode Codex**: F2 (agent/chat with permission gradient).
  - **VSCode Copilot**: F5 (agent/ask/plan intent routing).
  - **Codex (non-VSCode)**: F3 (exec/review split).
  - **Opencode**: F4 (plan/build pipeline).

- **Layering by governance pattern (inner layer):**
  - **Mode toggles within one assistant identity:** F2 and F5 (chat/agent/full-access; ask/plan/agent).
  - **Pipeline constitutions (phase-separated):** F4 (plan→build) and F3 (exec↔review, with stronger separation-of-duties).
  - **Interaction-first constitution:** F1 (interactive wrapper tightly bound to base prompt).

- **Siblings vs distant families:**
  - F2 and F5 are **siblings** (both VSCode-integrated, multi-mode regimes) but differ by lineage (Codex vs Copilot) and by whether the primary axis is **permissioning** (F2) or **intent/workflow routing** (F5).
  - F3 and F4 are **siblings** as phase-separated workflows, but differ in whether the second phase is **implementation** (build) or **audit** (review).
  - F1 is adjacent to F5 (Copilot-branded) but structurally distinct: **interaction contract** vs **mode routing**.

- **Bridges or boundary cases:**
  - The singleton families (F6–F15) function as **boundary echoes** of the multi-member regimes rather than true bridges. Their overlap with F2–F5 suggests the family extraction process may be emitting both **composite families** and **residual singletons** at the same threshold, which should not be interpreted as additional constitutions without corroboration.

---

### 4. Practical implications for research

- **How many representative prompts are needed:**
  - For constitutional coverage, prioritize **one representative per stable multi-member family (F1–F5)**: 5 prompts minimum.
  - For families that encode internal mode gradients (F2, F5), include **at least two representatives** (e.g., chat vs agent; ask vs agent) if studying authority/interaction differences: 7–9 prompts total.

- **Which families should be compared directly (and why):**
  - **F2 vs F5:** isolates **lineage effects** (Codex vs Copilot) under similar VSCode integration and multi-mode design.
  - **F3 vs F4:** isolates **workflow governance** differences: separation-of-duties (exec/review) vs forward pipeline (plan/build).
  - **F1 vs F5:** isolates **interactive conversational contract** vs **explicit mode routing** within Copilot-branded regimes.

- **Which differences are likely superficial vs constitutional:**
  - Likely superficial within a family: naming-level variants like “interactive” vs “prompt” (F1) or “chat” vs “agent” when tightly clustered (F2), unless the study targets autonomy/permissions explicitly.
  - Likely constitutional across families: **authority scope** (full-access vs standard), **phase separation** (plan/build vs exec/review), and **interaction contract** (interactive vs agentic).

---

### 5. Limitations and next steps

- **What this analysis cannot tell us:**
  - It cannot confirm actual tool permissions, safety constraints, or instruction hierarchies inside the prompts; filenames only weakly indicate these.
  - It cannot resolve whether singletons (F6–F15) are genuine regimes or artifacts; the overlap of members across families indicates the output is not a clean partition.
  - It cannot establish temporal evolution (versions) or causality (which regime derived from which).

- **What additional data would sharpen boundaries:**
  - **De-duplicated family assignment** (a strict partition or explicit multi-membership rationale) to distinguish true boundary prompts from artifacts.
  - The **full prompt texts** (or extracted governance features: tool list, permission statements, refusal policy, planning requirements) to validate inferred authority and workflow axes.
  - **Temporal/version metadata** to separate lineage similarity from stable constitutional similarity.
  - **Tooling diffs** (e.g., “full-access” capabilities enumerated) to test whether F2’s internal gradient is constitutional or nominal.