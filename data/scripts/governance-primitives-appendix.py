#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
governance-primitives-appendix.py

Generate the Appendix: Prompt Governance Primitives from:
- a finalized research report
- a Prompt Governance Primitives Registry (JSON)
- an appendix-generation prompt (Markdown)

Output:
  appendix-governance-primitives.md

Usage:
  uv run --locked scripts/governance-primitives-appendix.py \
    --prompt prompts/governance-primitives-appendix.prompt.md \
    --report final-research-report.md \
    --registry primitives.registry.json \
    --model gpt-5.2

Options:
  --dry-run   Print the assembled request and exit without calling the API
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import openai


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logging.exception(f"Failed to read JSON {path}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Appendix: Prompt Governance Primitives"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Appendix generation prompt (Markdown)",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Final research report (Markdown)",
    )
    parser.add_argument(
        "--registry",
        required=True,
        help="Prompt Governance Primitives Registry (JSON)",
    )
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Seed for deterministic inference (optional)",
    )
    parser.add_argument(
        "--output",
        default="appendix-governance-primitives.md",
        help="Output path (default: appendix-governance-primitives.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling the API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    prompt_text = read_text(Path(args.prompt))
    report_text = read_text(Path(args.report))
    registry_json = read_json(Path(args.registry))

    messages = [
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": f"""## Final Research Report (Context Only)

{report_text}
""",
        },
        {
            "role": "user",
            "content": f"""## Prompt Governance Primitives Registry (Authoritative)

```json
{json.dumps(registry_json, indent=2, ensure_ascii=False)}
```

""",
        },
    ]

    if args.dry_run:
        print("=== DRY RUN MODE ===\n")
        print(f"Model: {args.model}\n")
        if args.seed is not None:
            print(f"Seed: {args.seed}\n")
        for msg in messages:
            print(f"[{msg['role']}]\n{msg['content']}\n")
        return

    client = openai.OpenAI()

    logging.info("Calling model to generate governance primitives appendix...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0.1,
            seed=args.seed,
        )
    except Exception:
        logging.exception("API call failed")
        sys.exit(1)

    output = response.choices[0].message.content
    if not output:
        sys.exit("Model returned empty output")

    out_path = Path(args.output)
    try:
        out_path.write_text(output.strip(), encoding="utf-8")
        logging.info(f"Wrote appendix to {out_path}")
    except Exception:
        logging.exception("Failed to write output file")
        sys.exit(1)


if __name__ == "__main__":
    main()
