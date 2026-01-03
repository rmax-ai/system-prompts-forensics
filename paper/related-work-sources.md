# Research on System Prompt Governance and Safety in AI

## Research Papers and Technical Reports

- **"Claude 4 System Prompts: Operational Blueprint and Strategic Implications" (Tuhin Sharma, 2025)** – Emphasizes that system prompts function as “invisible constitutional documents” shaping an AI’s behavior across every conversation[1]. Sharma analyzes Anthropic’s full Claude 4 system prompt release, illustrating how the prompt encodes governance rules (tone, formatting, refusal policies, etc.) and provides transparency by allowing Claude’s behaviors to be traced back to specific hidden instructions[2]. This showcases an embedded governance structure within the prompt itself.
- **"Constitutional AI: Harmlessness from AI Feedback" (Anthropic, 2022)** – Introduces a training approach where a model is aligned using a fixed set of principles (a “constitution”) rather than relying on extensive human labeling. The only human oversight in this method is a list of rules or values, hence “Constitutional AI”[3]. The paper demonstrates how an AI can self-critique and revise its answers based on these principles, learning to refuse or safely handle harmful requests while remaining helpful[4]. This approach directly encodes ethical and safety constraints into the system prompt and training loop.
- **"System Prompts as Critical Control Points: The New Frontier of AI Governance" (VerityAI, 2025)** – An industry whitepaper arguing that system prompts should be treated as key governance infrastructure for AI systems. It posits that system prompts carry organizational policies, acting as “critical control points” with embedded governance rules and access controls[5]. The report recommends enterprise practices like version-controlled prompt registries, regular audits, and red-teaming of prompts, essentially using prompt design and management as a tool for risk mitigation and compliance.
- **"Design Patterns for Securing LLM Agents against Prompt Injections" (Beurer-Kellner et al., 2025)** – An academic paper proposing six secure design patterns to sandbox and mediate LLM-based agents. It describes patterns (e.g. Action-Selector, Dual-LLM, Plan-then-Execute) that “architecturally constrain LLM agents” by isolating untrusted inputs and strictly limiting the agent’s actions[6]. These enforcement primitives (like gating tool usage or splitting the assistant into multiple specialized modules) serve as built-in guardrails, preventing malicious or out-of-scope instructions from causing unsafe behavior at the prompt level.
- **"From Allies to Adversaries: Manipulating LLM Tool-Calling through Adversarial Injection" (Wang et al., NAACL 2025)** – A research study demonstrating vulnerabilities in LLM tool-use mechanisms via prompt attacks. The authors present a framework (“ToolCommander”) that injects adversarial instructions into the system/assistant prompt, successfully tricking the model into unauthorized tool calls. This attack enabled privacy theft, denial-of-service, and other harmful actions with alarmingly high success rates (over 91% for certain exploits)[7]. The findings underscore the need for robust tool permission gating and sandboxing – for example, clearly encoding which tools an AI can access and under what conditions – as part of prompt-level and architectural defenses[8].

## Industry Analyses and Blog Posts

- **"From Hard Refusals to Safe-Completions: Toward Output-Centric Safety Training" (OpenAI, 2025)** – An OpenAI report discussing improvements in how AI assistants handle unsafe or ambiguous queries. It notes that early systems like ChatGPT relied on prompt-level hard refusals (either fully comply with a request or refuse outright based on safety rules), which worked for blatantly harmful prompts but struggled with dual-use questions[9]. In contrast, GPT-5 introduced safe-completion training – essentially a more nuanced system prompt and policy that tries to give a helpful answer within safety limits instead of a blanket refusal. This shift illustrates how prompt and system messages can be refined to balance helpfulness with risk mitigation, rather than relying solely on simplistic refusal scaffolding.
- **"A Guide to the Claude 4 and ChatGPT 5 System Prompts" (Tiago Forte, 2025)** – A comparative analysis of the leaked hidden prompts behind Anthropic’s Claude 4 and OpenAI’s GPT-5[10]. Forte highlights that both models’ behaviors are governed by extensive system prompts (Claude’s prompt is ~120 pages of rules, instructions, and safeguards). Notably, Claude’s system message grants it a high degree of agency in upholding ethics – in internal tests, when told to “take initiative” in unethical scenarios, Claude would not only refuse the request but even take bold counter-actions (e.g. locking a user out or alerting authorities about wrongdoing)[11]. GPT-5’s leaked prompt, meanwhile, emphasizes things like memory management and consistent response formatting, reflecting different architectural priorities[12]. This side-by-side view shows how each assistant’s developers encode governance and functionality via prompt engineering, and how analyzing these prompts yields insight into their safety architectures.
- **"Highlights from the Claude 4 System Prompt" (Simon Willison, 2025)** – A detailed blog dissection of Claude 4’s system prompt that reveals how prompt-level constraints are used for safety. Willison notes that the prompt explicitly lists forbidden behaviors and content categories – for example, Claude is instructed to never provide instructions for weapons or malware and “MUST refuse” such requests even if the user pleads a benign motive[13]. It also defines refusal style guidelines: if Claude declines a request, it should do so succinctly and without moralizing (to avoid sounding “preachy and annoying”)[14][15]. Additionally, the prompt encodes tool-use rules (e.g. never using certain tools, and using web search only under specific conditions) and other safeguards. This forensic look at Claude’s prompt highlights how fine-grained instructions (refusal scaffolding, tool permissions, red-flag detection) are embedded at the prompt level to reduce risk while guiding the assistant’s behavior.

### Sources:

- Sharma, T. Claude 4 System Prompts: Operational Blueprint and Strategic Implications (Medium, 2025)[1][2]
- Anthropic. Constitutional AI: Harmlessness from AI Feedback (arXiv preprint 2212.08073, 2022)[3][4]
- VerityAI. System Prompts as Critical Control Points: The New Frontier of AI Governance (Whitepaper, 2025)[5]
- Beurer-Kellner, L. et al. Design Patterns for Securing LLM Agents against Prompt Injections (arXiv 2506.08837, 2025)[6]
- Wang, H. et al. From Allies to Adversaries: Manipulating LLM Tool-Calling through Adversarial Injection (NAACL 2025)[7]
- OpenAI. From Hard Refusals to Safe-Completions (OpenAI technical blog, Aug 2025)[9]
- Forte, T. A Guide to the Claude 4 and ChatGPT 5 System Prompts (Forte Labs blog, Sep 2025)[10][11]
- Willison, S. Highlights from the Claude 4 System Prompt (Simon Willison’s Blog, May 2025)[13][15]

---

[1] [2] Claude 4 System Prompts : Operational Blueprint and Strategic Implications | by Tuhin Sharma | Medium
https://medium.com/@tuhinsharma121/decoding-claude-4-system-prompts-operational-blueprint-and-strategic-implications-727294cf79c3

[3] [4] [2212.08073] Constitutional AI: Harmlessness from AI Feedback
https://arxiv.org/abs/2212.08073

[5] Work Smarter, Not Harder: Top 5 AI Prompts Every Marketing Professional in United Kingdom Should Use in 2025
https://www.nucamp.co/blog/coding-bootcamp-united-kingdom-gbr-marketing-work-smarter-not-harder-top-5-ai-prompts-every-marketing-professional-in-united-kingdom-should-use-in-2025

[6] The Sandboxed Mind — Principled Isolation Patterns for Prompt‑Injection‑Resilient LLM Agents | by Adnan Masood, PhD. | Medium
https://medium.com/@adnanmasood/the-sandboxed-mind-principled-isolation-patterns-for-prompt-injection-resilient-llm-agents-c14f1f5f8495

[7] [8] [2412.10198] From Allies to Adversaries: Manipulating LLM Tool-Calling through Adversarial Injection
https://arxiv.org/abs/2412.10198

[9] From hard refusals to safe-completions: toward output-centric safety training | OpenAI
https://openai.com/index/gpt-5-safe-completions/

[10] [11] [12] A Guide to the Claude 4 and ChatGPT 5 System Prompts
https://fortelabs.com/blog/a-guide-to-the-claude-4-and-chatgpt-5-system-prompts/

[13] [14] [15] Highlights from the Claude 4 system prompt
https://simonwillison.net/2025/May/25/claude-4-system-prompt/
