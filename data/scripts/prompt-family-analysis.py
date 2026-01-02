#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
prompt-family-analysis.py

Run a combined analysis over similarities.csv and band-report.csv to extract
prompt families as a CSV artifact.

Usage:
  uv run --locked prompt-family-analysis.py \
    --prompt prompt-family-analysis.md \
    --similarities similarities.csv \
    --bands band-report.csv \
    --model gpt-5.2 \
    --output prompt-families.csv
"""

import argparse
import csv
import logging
import re
import sys
from pathlib import Path

import openai

EXPECTED_HEADER = [
    "family_id",
    "band_range",
    "threshold_used",
    "family_label",
    "confidence",
    "family_size",
    "avg_weighted_similarity",
    "members",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def extract_csv_block(text: str) -> str:
    """
    Extract the first CSV-looking block from the model output.
    Allows optional Markdown fences.
    """
    fence = re.search(r"```(?:csv)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        return fence.group(1).strip()
    return text.strip()


def validate_csv(csv_text: str) -> None:
    reader = csv.reader(csv_text.splitlines())
    try:
        header = next(reader)
    except StopIteration:
        logging.exception("Model output is empty or not CSV")
        sys.exit(1)

    if header != EXPECTED_HEADER:
        sys.exit(
            "CSV header does not match expected format.\n"
            f"Expected: {EXPECTED_HEADER}\n"
            f"Got: {header}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract prompt families from similarity and band reports"
    )
    parser.add_argument("--prompt", required=True, help="Analysis prompt (Markdown)")
    parser.add_argument("--similarities", required=True, help="similarities.csv")
    parser.add_argument("--bands", required=True, help="band-report.csv")
    parser.add_argument("--model", required=True, help="Model name (e.g. gpt-5.2)")
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output",
        help="Output CSV file (prints to stdout if omitted)",
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
    sim_path = Path(args.similarities)
    band_path = Path(args.bands)

    prompt_text = read_text(prompt_path)
    sim_csv = read_text(sim_path)
    band_csv = read_text(band_path)

    messages = [
        {
            "role": "system",
            "content": prompt_text,
        },
        {
            "role": "user",
            "content": f"""## similarities.csv

```csv
{sim_csv}
```""",
        },
        {
            "role": "user",
            "content": f"""## band-report.csv

```csv
{band_csv}
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

    logging.info(f"Calling model {args.model} for family analysis...")
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            temperature=0,
            seed=args.seed,
        )
    except Exception:
        logging.exception("API call failed")
        sys.exit(1)

    output = response.choices[0].message.content
    if not output:
        sys.exit("Model returned empty output")

    csv_text = extract_csv_block(output)
    validate_csv(csv_text)

    if args.output:
        out = Path(args.output)
        try:
            out.write_text(csv_text, encoding="utf-8")
            logging.info(f"Prompt families written to {out}")
        except Exception:
            logging.exception("Failed to write output CSV")
            sys.exit(1)
    else:
        print(csv_text)


if __name__ == "__main__":
    main()
