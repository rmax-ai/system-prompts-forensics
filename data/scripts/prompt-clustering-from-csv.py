#!/usr/bin/env python3
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""
prompt-clustering-from-csv.py

Cluster normalized system-prompt files using a precomputed similarities CSV.
Automatically selects a similarity threshold and builds clusters.

Expected CSV columns:
  - file_a
  - file_b
  - weighted_score

Usage:
  uv run --locked python prompt-clustering-from-csv.py similarities.csv
  uv run --locked python prompt-clustering-from-csv.py similarities.csv --csv clusters.csv
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import numpy as np

# -------------------------
# Threshold auto-tuning
# -------------------------


def auto_threshold(scores: List[float]) -> float:
    """
    Pick threshold via largest-gap (1D knee) heuristic.
    """
    if len(scores) < 2:
        return 1.0

    scores = sorted(scores, reverse=True)
    diffs = [scores[i] - scores[i + 1] for i in range(len(scores) - 1)]
    idx = int(np.argmax(diffs))
    return round(scores[idx + 1], 2)


# -------------------------
# Clustering
# -------------------------


def build_clusters(
    files: Set[str],
    edges: Dict[Tuple[str, str], float],
    threshold: float,
) -> Dict[int, Set[str]]:
    graph: Dict[str, Set[str]] = {f: set() for f in files}

    for (a, b), score in edges.items():
        if score >= threshold:
            graph[a].add(b)
            graph[b].add(a)

    visited: Set[str] = set()
    clusters: Dict[int, Set[str]] = {}
    cid = 0

    for node in graph:
        if node in visited:
            continue
        stack = [node]
        cluster = set()

        while stack:
            cur = stack.pop()
            if cur in visited:
                continue
            visited.add(cur)
            cluster.add(cur)
            stack.extend(graph[cur] - visited)

        clusters[cid] = cluster
        cid += 1

    return clusters


# -------------------------
# Main
# -------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Cluster prompts from a similarities CSV with auto-tuned threshold"
    )
    parser.add_argument("csv", help="similarities.csv input file")
    parser.add_argument(
        "--csv-out", help="Optional CSV output path for cluster assignments"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done and exit",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"CSV file not found: {csv_path}")

    if args.dry_run:
        print(f"Dry run: Would process {csv_path}")
        if args.csv_out:
            print(f"Dry run: Would write output to {args.csv_out}")
        return

    edges: Dict[Tuple[str, str], float] = {}
    files: Set[str] = set()
    scores: List[float] = []

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"file_a", "file_b", "weighted_score"}
        if not required.issubset(reader.fieldnames or []):
            sys.exit(f"CSV must contain columns: {', '.join(required)}")

        for row in reader:
            a = row["file_a"]
            b = row["file_b"]
            score = float(row["weighted_score"])
            files.update([a, b])
            edges[(a, b)] = score
            scores.append(score)

    threshold = auto_threshold(scores)
    logging.info(f"Auto-selected similarity threshold: {threshold}")

    clusters = build_clusters(files, edges, threshold)

    print(f"\nClusters (threshold ≥ {threshold}):\n")
    for cid, members in clusters.items():
        print(f"Cluster {cid} ({len(members)} files):")
        for m in sorted(members):
            print(f"  - {m}")
        print()

    if args.csv_out:
        out_path = Path(args.csv_out)
        rows = []
        for cid, members in clusters.items():
            for m in members:
                rows.append(
                    {
                        "file": m,
                        "cluster_id": cid,
                        "threshold": threshold,
                    }
                )

        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        logging.info(f"Cluster CSV written to {out_path}")


if __name__ == "__main__":
    main()
