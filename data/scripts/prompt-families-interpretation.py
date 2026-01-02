#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
prompt-families-interpretation.py

Generate a human-readable interpretation report from prompt-families.csv
using a structured interpretation prompt.

Usage:
  uv run --locked prompt-families-interpretation.py \
    --prompt prompt-families.prompt.md \
    --families prompt-families.csv \
    --model gpt-5.2 \
    --output prompt-families-report.md
"""

import argparse
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interpret prompt families CSV into a structured analysis report"
    )
    parser.add_argument(
        "--prompt", required=True, help="Interpretation prompt (Markdown)"
    )
    parser.add_argument("--families", required=True, help="prompt-families.csv")
    parser.add_argument(
        "--model",
        default="gpt-5.2",
        help="Model name (default: gpt-5.2)",
    )
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output",
        help="Output report file (prints to stdout if omitted)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print request payload and exit without calling the API",
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

    prompt_path = Path(args.prompt)
    families_path = Path(args.families)

    prompt_text = read_text(prompt_path)
    families_csv = read_text(families_path)

    messages = [
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": f"""## prompt-families.csv

```csv
{families_csv}
```""",
        },
    ]

    if args.dry_run:
        print("Dry run — request payload:")
        print(f"Model: {args.model}")
        if args.seed is not None:
            print(f"Seed: {args.seed}")
        print("Messages:")
        for m in messages:
            print(f"\n[{m['role']}]\n{m['content']}")
        return

    client = openai.OpenAI()

    logging.info(f"Calling model {args.model} for family interpretation...")
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

    if args.output:
        out = Path(args.output)
        try:
            out.write_text(output.strip(), encoding="utf-8")
            logging.info(f"Interpretation report written to {out}")
        except Exception:
            logging.exception("Failed to write output file")
            sys.exit(1)
    else:
        print(output.strip())


if __name__ == "__main__":
    main()
