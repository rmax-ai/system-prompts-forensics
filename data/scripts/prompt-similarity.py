#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["PyYAML", "scikit-learn"]
# ///
"""
prompt-similarity.py

Compute pairwise similarity between normalized system-prompt YAML files
using structural, lexical, and constraint-based metrics.

Human-readable output is always printed to stdout.
Optionally, a CSV summary can be emitted for downstream analysis.

Usage:
  python prompt-similarity.py normalized/*.yaml
  python prompt-similarity.py normalized/*.yaml --csv similarities.csv
"""

from __future__ import annotations

import argparse
import csv
import logging
import re
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = {
    "the",
    "and",
    "or",
    "to",
    "of",
    "in",
    "for",
    "with",
    "on",
    "by",
    "is",
    "are",
    "be",
    "as",
    "that",
    "this",
    "it",
    "must",
    "should",
    "may",
    "only",
    "not",
    "do",
}

# Weighting rationale:
# - structure: governance shape (strongest signal)
# - forbidden: prohibitions encode risk boundaries
# - token: wording similarity (weakest, most brittle)
WEIGHTS = {
    "structure": 0.5,
    "forbidden": 0.3,
    "token": 0.2,
}


# -------------------------
# YAML loading and traversal
# -------------------------


def load_yaml(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        logging.exception(f"Failed to load YAML file {path}")
        sys.exit(1)


def extract_paths(obj: Any, prefix: str = "") -> Set[str]:
    paths: Set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            paths.add(new_prefix)
            paths |= extract_paths(value, new_prefix)
    elif isinstance(obj, list):
        for item in obj:
            paths |= extract_paths(item, prefix)
    return paths


def extract_text(obj: Any) -> List[str]:
    texts: List[str] = []
    if isinstance(obj, str):
        texts.append(obj)
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_text(item))
    elif isinstance(obj, dict):
        for value in obj.values():
            texts.extend(extract_text(value))
    return texts


# -------------------------
# Normalization + metrics
# -------------------------


def normalize_text(texts: Iterable[str]) -> str:
    tokens: List[str] = []
    for text in texts:
        words = re.findall(r"[a-zA-Z0-9]+", text.lower())
        tokens.extend(w for w in words if w not in STOPWORDS)
    return " ".join(tokens)


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def get_nested_set(obj: Dict[str, Any], path: List[str]) -> Set[str]:
    try:
        for p in path:
            obj = obj[p]
        if isinstance(obj, list):
            return {str(x) for x in obj}
    except Exception:
        pass
    return set()


# -------------------------
# Main
# -------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compute similarity between normalized system-prompt YAML files"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Normalized YAML files to compare (at least two)",
    )
    parser.add_argument(
        "--csv",
        help="Optional CSV output path for similarity matrix",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    paths = [Path(p) for p in args.files]
    if len(paths) < 2:
        sys.exit("Provide at least two YAML files to compare")

    if args.dry_run:
        print(f"Dry run: Would process {len(paths)} files")
        if args.csv:
            print(f"Dry run: Would write output to {args.csv}")
        return

    docs = [load_yaml(p) for p in paths]

    logging.debug("Extracting structural paths")
    structures = [extract_paths(d) for d in docs]

    logging.debug("Extracting and normalizing text")
    texts = [normalize_text(extract_text(d)) for d in docs]

    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform(texts)

    csv_rows: list[dict[str, str | float]] = []

    logging.info("Computing pairwise similarities")

    for (i, path_a), (j, path_b) in combinations(enumerate(paths), 2):
        struct_sim = jaccard(structures[i], structures[j])
        token_sim = cosine_similarity(vectors[i], vectors[j])[0][0]

        forbid_a = get_nested_set(docs[i], ["layers", "authority", "forbidden_actions"])
        forbid_b = get_nested_set(docs[j], ["layers", "authority", "forbidden_actions"])
        forbid_sim = jaccard(forbid_a, forbid_b)

        weighted_score = (
            WEIGHTS["structure"] * struct_sim
            + WEIGHTS["forbidden"] * forbid_sim
            + WEIGHTS["token"] * token_sim
        )

        # Human-readable output (unchanged, plus score)
        print(
            f"{path_a.name} ↔ {path_b.name} | "
            f"struct={struct_sim:.2f} "
            f"token={token_sim:.2f} "
            f"forbidden={forbid_sim:.2f} "
            f"score={weighted_score:.2f}"
        )

        csv_rows.append(
            {
                "file_a": path_a.name,
                "file_b": path_b.name,
                "struct_similarity": round(struct_sim, 4),
                "token_similarity": round(token_sim, 4),
                "forbidden_similarity": round(forbid_sim, 4),
                "weighted_score": round(weighted_score, 4),
            }
        )

    if args.csv:
        csv_path = Path(args.csv)
        logging.info(f"Writing CSV output to {csv_path}")
        try:
            with csv_path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=csv_rows[0].keys(),
                )
                writer.writeheader()
                writer.writerows(csv_rows)
        except Exception:
            logging.exception("Failed to write CSV output")
            sys.exit(1)


if __name__ == "__main__":
    main()
