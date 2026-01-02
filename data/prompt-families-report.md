### 1. Overview

- **Number of families:** 33 (with substantial repetition across thresholds; many are singletons that reappear as the threshold changes).
- **Overall similarity landscape:** Two regimes dominate:
  1. **Tight, stable tool/IDE constitutions** (notably the VSCode-\* clusters) that remain cohesive across multiple lower thresholds, indicating a strong shared governance contract.
  2. **Looser “product-lineage” aggregations** (Copilot/OpenCode mixes) that only cohere at lower thresholds, suggesting shared surface structure (format, role framing) rather than identical authority/tooling contracts.
- **What the band ranges imply:**
  - **High bands (~0.74–0.71):** near mode-level similarity; essentially variants of the same interaction contract.
  - **Mid bands (~0.70–0.65):** operational similarity begins to separate into singletons; governance regimes are distinct enough that only very close pairs cluster.
  - **Lower bands (~0.64 down to ~0.58):** product/lineage similarity dominates; families become “umbrella constitutions” that group related but not identical regimes (e.g., agent/chat variants under a VSCode umbrella; or Copilot + OpenCode build/plan under a broader “developer workflow” umbrella).

---

### 2. Family-by-family interpretation

#### Family F1: copilot-interactive-prompt-pair

- **Members** copilot.interactive.analysis.yaml; copilot.prompt.analysis.yaml
- **Band and stability** At a high threshold band (~0.72), this is a very cohesive pair: the clustering suggests near-identical governance framing with minor role/interface differences (interactive vs prompt).
- **Governance characteristics** A **conversational/interactive assistant constitution**: likely emphasizes user-driven iteration, response formatting norms, and a bounded assistance role rather than autonomous execution. The “interactive” vs “prompt” naming implies two entrypoints into the same contract (dialogue loop vs single-shot prompt wrapper).
- **What differentiates this family** Compared to OpenCode (build/plan) and VSCode agent families, this regime is less about tool-mediated action and more about **interaction protocol** and response discipline.
- **Confidence assessment** **High**: tight band and a clean two-member pairing indicates stable similarity at a high abstraction level.

#### Family F2: opencode-build-plan-pair

- **Members** opencode.build.analysis.yaml; opencode.plan.analysis.yaml
- **Band and stability** Clusters at a mid-high threshold (~0.68) as a tight pair, indicating a shared operational constitution spanning “plan” and “build.”
- **Governance characteristics** A **workflow constitution** with explicit separation between **planning** and **execution/build** phases. The shared “opencode” prefix suggests a consistent authority model and output contract across phases (e.g., plan artifacts vs build steps), with the phase label being the main variation.
- **What differentiates this family** More **process-structured** than Copilot interactive/prompt; less IDE/tool-embedded than VSCode families.
- **Confidence assessment** **High**: stable two-member cohesion at a relatively strict threshold.

#### Family F3: singleton-codex-exec

- **Members** codex.exec.analysis.yaml
- **Band and stability** Singleton at ~0.68 indicates it does not meet the similarity threshold with others at this band, implying a distinct operational constitution at that strictness.
- **Governance characteristics** An **execution-oriented** constitution (“exec”)—likely prioritizing action completion, command-like outputs, or direct task fulfillment rather than deliberative planning or review.
- **What differentiates this family** Distinct from “review” and from VSCode-\* variants at this threshold; suggests “codex.exec” has unique constraints or formatting/tool assumptions not shared strongly enough at 0.68.
- **Confidence assessment** **Low**: singleton status provides limited evidence of stable boundaries; it later merges into a broader VSCode-Codex umbrella at lower thresholds.

#### Family F4: singleton-codex-review

- **Members** codex.review.analysis.yaml
- **Band and stability** Singleton at ~0.68: “review” is constitutionally distinct at this strictness.
- **Governance characteristics** A **review/audit constitution**: likely emphasizes critique, risk identification, and non-executing guidance. The naming implies a different authority posture (advisory, evaluative) than “exec.”
- **What differentiates this family** Separates along the **intent axis** (evaluate vs execute). Notably, it remains a singleton across multiple lower thresholds too, suggesting persistent distinctness.
- **Confidence assessment** **Low**: singleton, but its repeated singleton reappearance across thresholds is a weak signal of genuine separateness.

#### Family F5: singleton-vscode-codex-agent-full-access

- **Members** vscode-codex.agent-full-access.analysis.yaml
- **Band and stability** Singleton at ~0.68: “full-access” likely introduces tool/permission assumptions that make it distinct at strict similarity.
- **Governance characteristics** An **agentic IDE-embedded constitution** with elevated authority (“full-access”), implying broader tool reach, fewer restrictions, or expanded action scope.
- **What differentiates this family** Differentiated primarily by **authority/permission envelope** relative to other VSCode-Codex agent/chat variants.
- **Confidence assessment** **Low**: singleton at this band; later consistently groups with other VSCode-Codex prompts at lower thresholds, implying it is a variant within a larger regime.

#### Family F6: singleton-vscode-codex-agent

- **Members** vscode-codex.agent.analysis.yaml
- **Band and stability** Singleton at ~0.68: distinct enough from other prompts at strict operational similarity.
- **Governance characteristics** A **standard agent constitution** in VSCode context: likely tool-mediated, task-oriented, with an action loop and constraints typical of IDE agents.
- **What differentiates this family** Sits between “chat” (more conversational) and “full-access” (more permissive) along the **agency/authority** axis.
- **Confidence assessment** **Low**: singleton at this band; later merges into a stable VSCode-Codex cluster.

#### Family F7: singleton-vscode-codex-chat

- **Members** vscode-codex.chat.analysis.yaml
- **Band and stability** Singleton at ~0.68: “chat” framing differs from agent/execution framing at strict similarity.
- **Governance characteristics** A **conversational IDE assistant constitution**: likely emphasizes dialogue, explanation, and user confirmation rather than autonomous action.
- **What differentiates this family** Differentiated by **interaction contract** (chat) rather than tool authority (agent/full-access).
- **Confidence assessment** **Low**: singleton at this band; later becomes part of the stable VSCode-Codex umbrella.

#### Family F8: singleton-vscode-copilot-agent

- **Members** vscode-copilot.agent.analysis.yaml
- **Band and stability** Singleton at ~0.68: distinct at strict similarity from ask/plan variants.
- **Governance characteristics** A **VSCode Copilot agent constitution**: agentic posture, likely tool-aware, with an execution loop distinct from “ask” and “plan.”
- **What differentiates this family** Differentiated within the Copilot VSCode line by **agency level** (agent vs ask/plan).
- **Confidence assessment** **Low**: singleton at this band; later forms a stable cluster with ask/plan at lower thresholds.

#### Family F9: singleton-vscode-copilot-ask

- **Members** vscode-copilot.ask.analysis.yaml
- **Band and stability** Singleton at ~0.68: “ask” is a distinct operational mode at strict similarity.
- **Governance characteristics** A **query/assist constitution**: likely non-agentic, user-driven Q&A, bounded scope, minimal autonomous action.
- **What differentiates this family** Contrasts with “agent” (autonomy) and “plan” (structured deliberation) along the **intent and autonomy** axes.
- **Confidence assessment** **Low**: singleton at this band; later clusters with agent/plan at lower thresholds.

#### Family F10: singleton-vscode-copilot-plan

- **Members** vscode-copilot.plan.analysis.yaml
- **Band and stability** Singleton at ~0.68: “plan” mode is distinct at strict similarity.
- **Governance characteristics** A **planning constitution**: emphasizes decomposition, step ordering, and possibly constraints/assumptions documentation.
- **What differentiates this family** Differentiated by **deliberation structure** (plan artifacts) rather than direct answering (“ask”) or acting (“agent”).
- **Confidence assessment** **Low**: singleton at this band; later clusters with agent/ask.

#### Family F11: vscode-codex-agent-chat-cluster

- **Members** codex.exec.analysis.yaml; vscode-codex.agent-full-access.analysis.yaml; vscode-codex.agent.analysis.yaml; vscode-codex.chat.analysis.yaml
- **Band and stability** At ~0.64, these four cohere into a stable umbrella. This indicates a shared **Codex-in-VSCode governance lineage** where differences (exec vs agent vs chat vs full-access) are sub-modes within a common constitution.
- **Governance characteristics** A **tool/IDE-embedded regime** with multiple interaction modes. The unifying trait is likely a shared environment contract (VSCode context, code-centric tasks, structured outputs), with internal variation in autonomy and permissions.
- **What differentiates this family** This is the clearest **platform constitution**: it groups multiple modes under a shared IDE/tooling contract, unlike Copilot/OpenCode families that group by workflow or interaction wrapper.
- **Confidence assessment** **High**: multi-member cluster with strong average similarity and repeated reappearance at nearby thresholds (see F19/F26/F31).

#### Family F12: vscode-copilot-ask-plan-pair

- **Members** vscode-copilot.ask.analysis.yaml; vscode-copilot.plan.analysis.yaml
- **Band and stability** At ~0.625, “ask” and “plan” cohere, suggesting these are closer to each other than to “agent” at this threshold—i.e., both are more deliberative/non-autonomous than agentic mode.
- **Governance characteristics** A **non-agentic assistance constitution** within VSCode Copilot: one mode answers questions, the other structures plans, but both likely avoid direct tool execution.
- **What differentiates this family** Differentiated from the broader Copilot VSCode cluster (F18) by excluding “agent,” implying **autonomy** is the key separating dimension.
- **Confidence assessment** **High**: clean pair at a specific threshold with coherent mode interpretation.

#### Family F13: singleton-codex-review

- **Members** codex.review.analysis.yaml
- **Band and stability** Singleton at ~0.625: review remains distinct even as thresholds relax.
- **Governance characteristics** Same review/audit constitution as F4; persistent separation suggests materially different instruction structure (e.g., safety/quality gates, critique format).
- **What differentiates this family** Continues to sit outside the “Codex-in-VSCode action/chat” umbrella, implying review is not just a mode variant but a different governance posture.
- **Confidence assessment** **Low**: still singleton, but persistence across thresholds modestly supports distinctness.

#### Family F14: singleton-copilot-interactive

- **Members** copilot.interactive.analysis.yaml
- **Band and stability** Singleton at ~0.625: despite pairing with copilot.prompt at higher threshold (F1), here it is treated as its own family due to thresholding/band effects in the pipeline.
- **Governance characteristics** Interactive wrapper of the Copilot conversational constitution.
- **What differentiates this family** Boundary case created by thresholding: structurally close to copilot.prompt, but not grouped at this specific band.
- **Confidence assessment** **Low**: singleton driven by banding rather than strong evidence of separateness.

#### Family F15: singleton-copilot-prompt

- **Members** copilot.prompt.analysis.yaml
- **Band and stability** Singleton at ~0.625: same threshold artifact as F14.
- **Governance characteristics** Prompt-wrapper variant of the Copilot conversational constitution.
- **What differentiates this family** Same as F14: separation appears procedural (threshold) rather than constitutional.
- **Confidence assessment** **Low**: singleton with known close neighbor (copilot.interactive).

#### Family F16: singleton-opencode-build

- **Members** opencode.build.analysis.yaml
- **Band and stability** Singleton at ~0.625: threshold artifact given F2 pairing at higher band and later broader clustering.
- **Governance characteristics** Build/execution phase of the OpenCode workflow constitution.
- **What differentiates this family** Separated from opencode.plan at this band; likely minor structural differences amplified by thresholding.
- **Confidence assessment** **Low**: singleton with known close neighbor.

#### Family F17: singleton-opencode-plan

- **Members** opencode.plan.analysis.yaml
- **Band and stability** Singleton at ~0.625: threshold artifact.
- **Governance characteristics** Planning phase of the OpenCode workflow constitution.
- **What differentiates this family** Separated from build at this band; likely not a fundamentally different regime.
- **Confidence assessment** **Low**: singleton with known close neighbor.

#### Family F18: vscode-copilot-agent-ask-plan-cluster

- **Members** vscode-copilot.agent.analysis.yaml; vscode-copilot.ask.analysis.yaml; vscode-copilot.plan.analysis.yaml
- **Band and stability** At ~0.61, all three VSCode Copilot modes cohere, indicating a shared platform constitution with internal mode specialization.
- **Governance characteristics** A **VSCode Copilot platform regime** spanning agentic and non-agentic modes. Unifier is likely the IDE context and shared response/tooling conventions; internal differences are autonomy (agent) and deliberation structure (plan) vs Q&A (ask).
- **What differentiates this family** Compared to F12, this is the **full Copilot VSCode umbrella** including agentic authority; compared to Codex VSCode clusters, it is a sibling platform lineage (Copilot vs Codex).
- **Confidence assessment** **High**: stable multi-member cluster; reappears at lower thresholds (F27/F32).

#### Family F19: vscode-codex-agent-chat-cluster

- **Members** codex.exec.analysis.yaml; vscode-codex.agent-full-access.analysis.yaml; vscode-codex.agent.analysis.yaml; vscode-codex.chat.analysis.yaml
- **Band and stability** Same membership and high cohesion at ~0.61, reinforcing that this is a stable platform constitution rather than a threshold accident.
- **Governance characteristics** Same as F11: Codex-in-VSCode umbrella with multiple sub-modes.
- **What differentiates this family** Serves as the **Codex VSCode anchor** against which Copilot VSCode (F18) and non-IDE workflows (OpenCode/Copilot prompt) differ.
- **Confidence assessment** **High**: repeated stable cluster across bands.

#### Family F20: singleton-codex-review

- **Members** codex.review.analysis.yaml
- **Band and stability** Singleton at ~0.61: persistent separation.
- **Governance characteristics** Review/audit constitution.
- **What differentiates this family** Remains outside both VSCode platform umbrellas, suggesting review is a distinct governance regime not primarily defined by IDE/tool context.
- **Confidence assessment** **Low**: singleton, but consistently isolated.

#### Family F21: singleton-copilot-interactive

- **Members** copilot.interactive.analysis.yaml
- **Band and stability** Singleton at ~0.61: again a threshold artifact given known pairing and later clustering.
- **Governance characteristics** Copilot conversational/interactive wrapper.
- **What differentiates this family** Boundary case; not constitutionally unique.
- **Confidence assessment** **Low**.

#### Family F22: singleton-copilot-prompt

- **Members** copilot.prompt.analysis.yaml
- **Band and stability** Singleton at ~0.61: threshold artifact.
- **Governance characteristics** Copilot prompt wrapper.
- **What differentiates this family** Boundary case; not constitutionally unique.
- **Confidence assessment** **Low**.

#### Family F23: singleton-opencode-build

- **Members** opencode.build.analysis.yaml
- **Band and stability** Singleton at ~0.61: threshold artifact.
- **Governance characteristics** OpenCode build phase.
- **What differentiates this family** Boundary case; not constitutionally unique.
- **Confidence assessment** **Low**.

#### Family F24: singleton-opencode-plan

- **Members** opencode.plan.analysis.yaml
- **Band and stability** Singleton at ~0.61: threshold artifact.
- **Governance characteristics** OpenCode plan phase.
- **What differentiates this family** Boundary case; not constitutionally unique.
- **Confidence assessment** **Low**.

#### Family F25: copilot-interactive-prompt-opencode-build-cluster

- **Members** copilot.interactive.analysis.yaml; copilot.prompt.analysis.yaml; opencode.build.analysis.yaml
- **Band and stability** At ~0.595, a cross-product cluster forms. This indicates shared structural conventions (developer-assistant framing, workflow language, formatting) sufficient for product-lineage similarity, but not necessarily identical authority/tool contracts.
- **Governance characteristics** A **developer assistance workflow constitution** that blends conversational Copilot wrappers with an execution/build-oriented OpenCode prompt. The commonality is likely “help produce code changes” framing rather than shared tool permissions.
- **What differentiates this family** Acts as a **bridge** between Copilot conversational constitutions and OpenCode workflow constitutions; it excludes opencode.plan, implying “build/execution” aligns more with Copilot’s assistance framing than explicit planning does at this band.
- **Confidence assessment** **Medium**: cross-lineage clustering at a lower threshold is inherently less stable/precise; cohesion is moderate.

#### Family F26: vscode-codex-agent-chat-cluster

- **Members** codex.exec.analysis.yaml; vscode-codex.agent-full-access.analysis.yaml; vscode-codex.agent.analysis.yaml; vscode-codex.chat.analysis.yaml
- **Band and stability** Repeats the stable Codex VSCode umbrella at ~0.595.
- **Governance characteristics** Same platform constitution as F11/F19.
- **What differentiates this family** Continues to define the Codex VSCode regime as distinct from Copilot VSCode and from non-IDE workflow prompts.
- **Confidence assessment** **High**: repeated stable membership.

#### Family F27: vscode-copilot-agent-ask-plan-cluster

- **Members** vscode-copilot.agent.analysis.yaml; vscode-copilot.ask.analysis.yaml; vscode-copilot.plan.analysis.yaml
- **Band and stability** Repeats the stable Copilot VSCode umbrella at ~0.595.
- **Governance characteristics** Same platform constitution as F18.
- **What differentiates this family** Sibling to the Codex VSCode umbrella; differs mainly by product lineage (Copilot vs Codex) rather than by mode.
- **Confidence assessment** **High**: repeated stable membership.

#### Family F28: singleton-codex-review

- **Members** codex.review.analysis.yaml
- **Band and stability** Singleton at ~0.595: persistent.
- **Governance characteristics** Review/audit constitution.
- **What differentiates this family** Remains isolated even when cross-product clusters form, implying strong distinctiveness in instruction structure.
- **Confidence assessment** **Low** (singleton), with consistent isolation as supporting evidence.

#### Family F29: singleton-opencode-plan

- **Members** opencode.plan.analysis.yaml
- **Band and stability** Singleton at ~0.595: notable because opencode.build has joined a cross-product cluster (F25) while plan remains separate.
- **Governance characteristics** Planning constitution with stronger deliberation/structure signals that do not align as readily with Copilot wrappers at this band.
- **What differentiates this family** Differentiated from opencode.build by **phase emphasis** (planning artifacts) that resists blending into conversational assistance clusters.
- **Confidence assessment** **Low**: singleton, but its separation relative to build is a meaningful pattern.

#### Family F30: copilot-opencode-build-plan-cluster

- **Members** copilot.interactive.analysis.yaml; copilot.prompt.analysis.yaml; opencode.build.analysis.yaml; opencode.plan.analysis.yaml
- **Band and stability** At ~0.58, the broadest non-IDE umbrella forms, merging Copilot wrappers with both OpenCode phases. This is a low-threshold lineage/product similarity cluster.
- **Governance characteristics** A **general developer workflow constitution**: shared high-level contract of assisting software work across planning and building, with less sensitivity to exact authority/tooling details.
- **What differentiates this family** This is the **lowest-common-denominator umbrella** for non-VSCode prompts; it is less constitutionally specific than F1 or F2 and should be treated as a coarse grouping.
- **Confidence assessment** **Medium**: low-threshold aggregation is expected to be less precise; still useful for identifying a shared “developer workflow” super-family.

#### Family F31: vscode-codex-agent-chat-cluster

- **Members** codex.exec.analysis.yaml; vscode-codex.agent-full-access.analysis.yaml; vscode-codex.agent.analysis.yaml; vscode-codex.chat.analysis.yaml
- **Band and stability** Repeats the stable Codex VSCode umbrella at ~0.58.
- **Governance characteristics** Same as prior Codex VSCode clusters.
- **What differentiates this family** Remains distinct even as non-IDE prompts merge broadly, reinforcing that IDE/tool embedding is a primary constitutional separator.
- **Confidence assessment** **High**.

#### Family F32: vscode-copilot-agent-ask-plan-cluster

- **Members** vscode-copilot.agent.analysis.yaml; vscode-copilot.ask.analysis.yaml; vscode-copilot.plan.analysis.yaml
- **Band and stability** Repeats the stable Copilot VSCode umbrella at ~0.58.
- **Governance characteristics** Same as prior Copilot VSCode clusters.
- **What differentiates this family** Same sibling relationship to Codex VSCode; remains separate from the non-IDE Copilot/OpenCode umbrella.
- **Confidence assessment** **High**.

#### Family F33: singleton-codex-review

- **Members** codex.review.analysis.yaml
- **Band and stability** Singleton at ~0.58: review remains isolated even at the loosest band shown.
- **Governance characteristics** Review/audit constitution with a distinct interaction contract (evaluate rather than act/plan).
- **What differentiates this family** This is the clearest “different constitution” in the dataset: it does not join either IDE umbrellas or the broad developer workflow umbrella.
- **Confidence assessment** **Low** (singleton), but the persistent isolation across all bands is strong qualitative support for distinctness.

---

### 3. Cross-family structure

- **Primary layering dimension: environment/tool embedding**
  - **VSCode platform constitutions** form two stable sibling umbrellas:
    - **Codex VSCode umbrella:** F11/F19/F26/F31 (exec/agent/chat/full-access variants).
    - **Copilot VSCode umbrella:** F18/F27/F32 (agent/ask/plan variants).
  - These umbrellas remain stable across multiple thresholds, indicating that **IDE context + tooling contract** is a dominant constitutional feature.
- **Secondary layering dimension: workflow phase vs interaction wrapper (non-IDE)**
  - **Copilot wrapper constitution:** F1 (interactive/prompt) is tight at high threshold.
  - **OpenCode workflow constitution:** F2 (build/plan) is tight at mid-high threshold.
  - At lower thresholds, these merge into broader umbrellas (F25, then F30), indicating shared developer-work framing but weaker shared authority/tooling assumptions.
- **Persistent outlier regime**
  - **codex.review** remains isolated (F4/F13/F20/F28/F33), suggesting a governance constitution centered on evaluation/review that does not align with action/planning/IDE regimes.
- **Bridges / boundary cases**
  - **opencode.build** is a bridge earlier than **opencode.plan** (F25 vs F29), implying execution/build language aligns more readily with Copilot’s assistance framing than explicit planning language does.
  - The repeated singleton appearances of Copilot/OpenCode members at intermediate thresholds (F14–F17, F21–F24) look like **threshold artifacts** rather than true constitutional isolation, given their known tight pairings/merges elsewhere.

---

### 4. Practical implications for research

- **Representative prompts needed**
  - For constitutional coverage, treat the stable umbrellas as the key regimes:
    1. One representative from **VSCode-Codex umbrella** (plus optionally one “full-access” variant if studying permission envelopes).
    2. One representative from **VSCode-Copilot umbrella** (plus optionally “agent” vs “ask/plan” if studying autonomy).
    3. One representative from **Copilot wrapper (non-IDE)**.
    4. One representative from **OpenCode workflow** (plan/build split if studying phase separation).
    5. One representative from **Codex review** (must be separate).
  - Minimum: **5 prompts** (one per constitution). For mode-sensitive studies: **7–9** (include agent vs chat vs full-access; ask vs plan vs agent; build vs plan).
- **Which families to compare directly (and why)**
  - **VSCode-Codex vs VSCode-Copilot**: isolates product lineage under a shared IDE embedding; good for studying how governance differs when the environment contract is similar.
  - **OpenCode plan vs build**: isolates phase governance (deliberation vs execution).
  - **Copilot interactive vs prompt**: isolates interface wrapper effects under near-identical constitution.
  - **Codex review vs any action/agent family**: isolates the evaluate-vs-act constitutional axis.
- **Likely superficial vs constitutional differences**
  - Likely superficial: “interactive” vs “prompt” wrappers; “ask” vs “plan” may be mode-level but within the same platform constitution at lower thresholds.
  - More constitutional: IDE-embedded vs non-IDE; agentic vs review; permission envelope (“full-access”) within an agent regime.

---

### 5. Limitations and next steps

- **What this analysis cannot tell us**
  - It cannot confirm actual tool permissions, safety constraints, or execution capabilities; it only indicates similarity-derived governance structure inferred from filenames and clustering behavior.
  - It cannot distinguish whether clusters reflect shared policy text, shared formatting templates, or shared system-role constraints without inspecting prompt contents.
  - Repeated families across thresholds indicate stability, but do not provide a full dendrogram; adjacency is inferred indirectly.
- **Next steps to sharpen boundaries**
  - Add **prompt text feature audits**: explicitly compare authority statements, tool invocation rules, refusal/constraint language, and output schemas across families.
  - Include **temporal/versioned prompts** (if available) to test whether umbrellas are stable over time or reflect a snapshot.
  - Add **tool-diff metadata** (what tools exist, permission scopes) to separate “agent” similarity due to shared tool lists vs shared governance language.
  - Run a **hierarchical clustering / dendrogram extraction** to formalize the layering suggested by repeated clusters (especially the VSCode umbrellas and the non-IDE merge at low thresholds).
