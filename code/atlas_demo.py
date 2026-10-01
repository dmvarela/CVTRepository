"""Command-line demo for the Atlas micro-library."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from code.atlas_librarian import (
    ALLOWED_LAYER_TYPES,
    AtlasLibrary,
    AtlasLibrarian,
)


def _default_data_dir() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "research"
        / "atlas"
        / "data"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Atlas micro-library demo")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=_default_data_dir(),
        help="Directory containing Atlas concept JSON records.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    find = sub.add_parser("find", help="Find concept records by simple token overlap.")
    find.add_argument("query")

    trace = sub.add_parser("trace", help="Show provenance, lineage, and cliffs.")
    trace.add_argument("concept_id")

    reconstruct = sub.add_parser(
        "reconstruct",
        help="Reconstruct a source concept with assumptions visible.",
    )
    reconstruct.add_argument("concept_id")

    layers = sub.add_parser(
        "layers",
        help="Show typed source/interpretive layers without collapsing them.",
    )
    layers.add_argument("concept_id")
    layers.add_argument(
        "--type",
        dest="layer_type",
        choices=sorted(ALLOWED_LAYER_TYPES),
        default=None,
    )

    translate = sub.add_parser(
        "translate",
        help="Prepare a bounded translation packet for a target context.",
    )
    translate.add_argument("concept_id")
    translate.add_argument("target_context")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    library = AtlasLibrary.from_directory(args.data_dir)
    librarian = AtlasLibrarian(library)

    if args.command == "find":
        result = librarian.find(args.query)
    elif args.command == "trace":
        result = librarian.trace(args.concept_id)
    elif args.command == "reconstruct":
        result = librarian.reconstruct(args.concept_id)
    elif args.command == "layers":
        result = librarian.layered_view(
            args.concept_id,
            layer_type=args.layer_type,
        )
    elif args.command == "translate":
        result = librarian.prepare_translation(args.concept_id, args.target_context)
    else:  # pragma: no cover - argparse enforces the command set.
        raise RuntimeError(f"Unhandled command: {args.command}")

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
