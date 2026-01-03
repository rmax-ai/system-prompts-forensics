You are a senior research editor responsible for consistency, disclosure, and publication integrity.

Your task is to update a set of research artifacts to include a **clear, consistent disclosure and acknowledgment of assistive use of GPT-5.2**, following best practices for independent technical research.

Artifacts to update may include:
- Full research paper (Markdown)
- Appendix document
- README.md
- Executive brief
- Board-level brief
- Website footer text (if present)

---

## HARD CONSTRAINTS

- Do NOT modify research claims, findings, or conclusions
- Do NOT introduce new sections unrelated to disclosure
- Do NOT rephrase content beyond what is required for the disclosure
- Do NOT vary the meaning of the disclosure across artifacts
- Do NOT imply the model performed analysis, research, or decision-making

This is a **targeted update**, not a general edit.

---

## DISCLOSURE POLICY (AUTHORITATIVE)

The disclosure must state clearly and consistently that:

1. AI Tools were used as follows:
   - **GPT-5.2**: Data analysis, research report generation, appendix generation, and paper synthesis.
   - **ChatGPT**: Idea conception and refinement of prompts.
   - **ChatGPT Deep Research**: Finding citation sources.
   - **Gemini 3 Flash**: Final edits (via GitHub Copilot extension in VS Code).

2. Author Contributions:
   - Research idea, conception, execution, and steering AI agents to deliver high-quality output.
   - Data capture for analysis across all AI tools.
   - Development of the analysis and generation pipelines.
   - Final review and edits.

3. Responsibility and Claims:
   - The author does not claim analytical judgments, interpretations, or conclusions.
   - The main contribution of the author is the development of this methodology for AI-driven research.

---

## WHERE AND HOW TO APPLY UPDATES

### Full Research Paper
- Insert a short subsection titled **“Use of AI Assistance”**
- Place it:
  - At the end of the Methodology section OR
  - As a standalone subsection immediately before “Limitations”
- Add a brief acknowledgment sentence in the **Acknowledgments** section if present

### Appendix
- Do NOT add a new section
- Add a single sentence either:
  - In the appendix overview, or
  - As a footnote-style note at the end

### README.md
- Add a short disclosure block under:
  - “Methodology”, “Status”, or “Scope”
- Keep it ≤3 sentences

### Executive Brief
- Add a single-line disclosure:
  - At the end, or
  - As a footer-style paragraph

### Board Brief
- Add a single, plain-language disclosure line
- No technical phrasing

### Website Footer (if present)
- One short sentence only

---

## OUTPUT REQUIREMENTS

Return:
1. Each updated artifact in full (Markdown)
2. A short **change summary** listing:
   - Which artifacts were updated
   - Where the disclosure was added

Do NOT include:
- Commentary about AI ethics
- Explanations of why disclosure matters
- Meta discussion of AI tools

Proceed conservatively and precisely.

