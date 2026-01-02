#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["openai"]
# ///
"""
governance-primitives-reduce.py

Second-order reducer that derives Prompt Governance Primitives
from verbatim governance extraction artifacts.

Usage:
  uv run --locked governance-primitives-reduce.py \
    --prompt prompts/governance-primitives-reducer.prompt.md \
    --inputs governance/*.json \
    --model gpt-5.2 \
    --output primitives.registry.json
"""

import argparse
import hashlib
import json
import logging
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import openai
from openai.types.chat import ChatCompletionMessageParam


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        logging.exception(f"Failed to read {path}")
        sys.exit(1)


def clean_output(text: str) -> str:
    """
    Remove markdown fences if the model emits them accidentally.
    """
    pattern = r"```(?:json)?\s*\n(.*?)\n\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        logging.debug("Stripped markdown code fences from output")
        return match.group(1).strip()
    return text.strip()


def load_artifacts(paths: list[Path]) -> list[dict]:
    artifacts = []
    for path in paths:
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError:
            logging.exception(f"Invalid JSON in {path}")
            sys.exit(1)
        artifacts.append(
            {
                "file": path.name,
                "hash": hashlib.sha256(
                    json.dumps(data, sort_keys=True).encode("utf-8")
                ).hexdigest(),
                "data": data,
            }
        )
    return artifacts


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt governance primitives reducer")
    parser.add_argument(
        "--prompt",
        required=True,
        help="Second-order reducer prompt (Markdown)",
    )
    parser.add_argument(
        "--inputs",
        required=True,
        nargs="+",
        help="Governance extraction JSON files (glob supported by shell)",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Model name (e.g. gpt-5.2)",
    )
    parser.add_argument(
        "--seed", type=int, help="Seed for deterministic inference (optional)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output primitives registry JSON file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print request payload and exit without calling API",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    # Logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    prompt_path = Path(args.prompt)
    input_paths = [Path(p) for p in args.inputs]
    output_path = Path(args.output)

    reducer_prompt = read_text(prompt_path)
    artifacts = load_artifacts(input_paths)

    logging.info(f"Loaded {len(artifacts)} governance artifacts")

    # Capture metadata
    combined_hash = hashlib.sha256(
        "".join(a["hash"] for a in artifacts).encode("utf-8")
    ).hexdigest()

    capture_metadata = {
        "generated_at": datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "artifact_count": len(artifacts),
        "combined_hash": combined_hash,
        "environment": {
            "os": platform.system(),
            "arch": platform.machine(),
            "runtime": f"Python {platform.python_version()}",
        },
    }

    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": reducer_prompt,
        },
        {
            "role": "user",
            "content": f"""## Reduction Metadata

{json.dumps(capture_metadata, indent=2)}

""",
        },
        {
            "role": "user",
            "content": f"""## Governance Artifacts

{json.dumps(artifacts, indent=2, ensure_ascii=False)}

""",
        },
    ]

    if args.dry_run:
        print("Dry run mode enabled. Request payload:\n")
        print(f"Model: {args.model}")
        if args.seed is not None:
            print(f"Seed: {args.seed}")
        print(json.dumps(messages, indent=2, ensure_ascii=False))
        return

    client = openai.OpenAI()

    logging.info(f"Calling model {args.model}...")
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

    content = response.choices[0].message.content
    if not content:
        sys.exit("Model returned empty output")

    content = clean_output(content)

    # Validate JSON strictly
    try:
        registry = json.loads(content)
    except json.JSONDecodeError:
        logging.exception("Model output is not valid JSON")
        sys.exit(1)

    # Write output
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"Primitive registry written to {output_path}")
    except Exception:
        logging.exception("Failed to write output")
        sys.exit(1)


if __name__ == "__main__":
    main()
