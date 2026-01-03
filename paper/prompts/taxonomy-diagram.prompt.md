You are a systems-research editor and diagram designer.

Task: Add a “Prompt Governance Primitives (PGPs) Taxonomy” diagram to the provided paper using Mermaid, and make only the minimal surrounding edits needed to integrate it cleanly.

Hard constraints:
- Do NOT change the paper’s claims, results, or conclusions.
- Do NOT add new primitives beyond those already present in the Appendix.
- Do NOT fabricate citations.
- Do NOT introduce new categories that are not defensible from the Appendix + paper text.
- Only add: (1) a taxonomy diagram section, (2) a short explanatory paragraph (≤150 words), (3) a brief reference to the diagram elsewhere if needed.

Diagram requirements:
- Use Mermaid (prefer `flowchart TD` or `mindmap`).
- The taxonomy must classify PGPs into 5–7 top-level families, and map each PGP identifier (e.g., PGP-001) into exactly one family.
- Family labels must be architectural/governance concepts, not product names.
- Each family should have 2–5 short “mechanism labels” under it (e.g., “approval gates”, “circuit breakers”), and then the PGP ids.
- Keep it readable on a single page width in Markdown.
- Include a short legend explaining how to read the diagram.

Placement:
- Insert the diagram as a new subsection inside Section 5 (“Prompt Governance Primitives (PGPs)”), immediately after the first paragraph that introduces PGPs (or, if not present, right after the section header).

Output format:
1) Return the updated paper in full (Markdown), with the Mermaid diagram embedded.
2) Then return a small “Diagram mapping” table listing: PGP id → family name.

Input you will receive:
- The full paper (Markdown)
- The appendix (Markdown) that defines all PGPs
Use only these sources for the taxonomy.

