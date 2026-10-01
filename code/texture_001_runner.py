"""TEXTURE_001 isolated execution harness.

This module prepares one provider-visible prompt per frozen case and records raw
provider outputs without adjudicating them.

IMPORTANT:
- It does not call any model/provider API.
- It does not read the adjudication key.
- It does not authorize execution.
- One provider context must be fresh/isolated per item.

The intended workflow is:
    PREPARE -> external isolated provider run -> RECORD -> FREEZE -> ADJUDICATE

Provider execution is deliberately kept outside this file so credentials,
provider-specific state, and accidental cross-item context cannot be hidden
inside the Atlas harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Iterable
import argparse
import json
import re


CASE_HEADER = re.compile(r"^## (T\d{2})$", re.MULTILINE)
REQUIRED_FIELDS = (
    "Current state",
    "Constraint",
    "Information available",
    "Question",
)
OUTPUT_PATTERN = re.compile(
    r"^TRAJECTORY: "
    r"(WARRANTED_THEN_SUPERSEDED|UNWARRANTED_THEN_CORRECTED|INSUFFICIENT)\n"
    r"REOPEN_WAKE: (YES|NO)\n"
    r"ANSWER: (.+)$"
)


@dataclass(frozen=True)
class TextureCase:
    case_id: str
    current_state: str
    constraint: str
    information_available: str
    question: str

    def provider_prompt(self) -> str:
        return (
            "Answer this case using exactly:\n\n"
            "TRAJECTORY: <WARRANTED_THEN_SUPERSEDED | "
            "UNWARRANTED_THEN_CORRECTED | INSUFFICIENT>\n"
            "REOPEN_WAKE: <YES | NO>\n"
            "ANSWER: <one sentence, maximum 30 words>\n\n"
            "Do not infer facts that are not supplied.\n\n"
            f"Current state: {self.current_state}\n\n"
            f"Constraint: {self.constraint}\n\n"
            f"Information available: {self.information_available}\n\n"
            f"Question: {self.question}"
        )


def _extract_field(block: str, label: str) -> str:
    pattern = re.compile(
        rf"\*\*{re.escape(label)}:\*\*\s*(.+?)(?=\n\n\*\*|\Z)",
        re.DOTALL,
    )
    match = pattern.search(block)
    if not match:
        raise ValueError(f"Missing field: {label}")
    return " ".join(match.group(1).split())


def parse_cases(markdown: str) -> list[TextureCase]:
    matches = list(CASE_HEADER.finditer(markdown))
    if not matches:
        raise ValueError("No TEXTURE_001 cases found.")

    cases: list[TextureCase] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        block = markdown[start:end]
        fields = {name: _extract_field(block, name) for name in REQUIRED_FIELDS}
        cases.append(
            TextureCase(
                case_id=match.group(1),
                current_state=fields["Current state"],
                constraint=fields["Constraint"],
                information_available=fields["Information available"],
                question=fields["Question"],
            )
        )

    ids = [case.case_id for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate case IDs found.")
    return cases


def load_cases(path: Path) -> list[TextureCase]:
    return parse_cases(path.read_text(encoding="utf-8"))


def prompt_hash(prompt: str) -> str:
    return sha256(prompt.encode("utf-8")).hexdigest()


def prepare_packets(cases: Iterable[TextureCase], out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=False)
    manifest_items = []

    for case in cases:
        prompt = case.provider_prompt()
        prompt_path = out_dir / f"{case.case_id}.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        manifest_items.append(
            {
                "case_id": case.case_id,
                "prompt_file": prompt_path.name,
                "prompt_sha256": prompt_hash(prompt),
            }
        )

    manifest = {
        "experiment": "TEXTURE_001",
        "design": "v2.1",
        "packet_type": "provider_prompts",
        "contains_adjudication_key": False,
        "one_fresh_context_per_item_required": True,
        "item_count": len(manifest_items),
        "items": manifest_items,
    }
    (out_dir / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


def validate_raw_output(text: str) -> dict[str, str]:
    normalized = text.strip().replace("\r\n", "\n")
    match = OUTPUT_PATTERN.fullmatch(normalized)
    if not match:
        raise ValueError(
            "Output does not match the frozen three-line TEXTURE_001 format."
        )

    answer = match.group(3).strip()
    if len(answer.split()) > 30:
        raise ValueError("ANSWER exceeds the 30-word maximum.")

    return {
        "trajectory": match.group(1),
        "reopen_wake": match.group(2),
        "answer": answer,
    }


def record_output(
    *,
    case_id: str,
    raw_output_path: Path,
    prompt_path: Path,
    results_dir: Path,
    provider: str,
    model: str,
    run_id: str,
) -> Path:
    if not re.fullmatch(r"T\d{2}", case_id):
        raise ValueError("case_id must have form T01, T02, ...")

    raw = raw_output_path.read_text(encoding="utf-8")
    parsed = validate_raw_output(raw)
    prompt = prompt_path.read_text(encoding="utf-8")

    results_dir.mkdir(parents=True, exist_ok=True)
    destination = results_dir / f"{case_id}.json"
    if destination.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing frozen result: {destination}"
        )

    record = {
        "experiment": "TEXTURE_001",
        "design": "v2.1",
        "case_id": case_id,
        "provider": provider,
        "model": model,
        "run_id": run_id,
        "fresh_context_attested": True,
        "prompt_sha256": prompt_hash(prompt),
        "raw_output_sha256": sha256(raw.encode("utf-8")).hexdigest(),
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_output": raw.strip(),
        "parsed": parsed,
        "adjudicated": False,
    }
    destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return destination


def freeze_results(results_dir: Path, out_file: Path) -> dict:
    result_files = sorted(results_dir.glob("T??.json"))
    if not result_files:
        raise ValueError("No recorded results to freeze.")

    items = []
    for path in result_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        items.append(
            {
                "case_id": data["case_id"],
                "result_file": path.name,
                "result_sha256": sha256(path.read_bytes()).hexdigest(),
                "prompt_sha256": data["prompt_sha256"],
                "raw_output_sha256": data["raw_output_sha256"],
                "provider": data["provider"],
                "model": data["model"],
                "run_id": data["run_id"],
            }
        )

    freeze = {
        "experiment": "TEXTURE_001",
        "design": "v2.1",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "adjudicated": False,
        "item_count": len(items),
        "items": items,
    }
    if out_file.exists():
        raise FileExistsError(f"Refusing to overwrite freeze manifest: {out_file}")
    out_file.write_text(json.dumps(freeze, indent=2) + "\n", encoding="utf-8")
    return freeze


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="TEXTURE_001 prompt preparation and raw-result freezing harness."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="Prepare one prompt file per frozen case.")
    prepare.add_argument("--cases", type=Path, required=True)
    prepare.add_argument("--out-dir", type=Path, required=True)

    validate = sub.add_parser("validate-output", help="Validate one provider output.")
    validate.add_argument("--input", type=Path, required=True)

    record = sub.add_parser("record", help="Record one isolated provider output.")
    record.add_argument("--case-id", required=True)
    record.add_argument("--raw-output", type=Path, required=True)
    record.add_argument("--prompt", type=Path, required=True)
    record.add_argument("--results-dir", type=Path, required=True)
    record.add_argument("--provider", required=True)
    record.add_argument("--model", required=True)
    record.add_argument("--run-id", required=True)

    freeze = sub.add_parser("freeze", help="Freeze recorded raw results before scoring.")
    freeze.add_argument("--results-dir", type=Path, required=True)
    freeze.add_argument("--out-file", type=Path, required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "prepare":
        manifest = prepare_packets(load_cases(args.cases), args.out_dir)
        print(json.dumps(manifest, indent=2))
    elif args.command == "validate-output":
        parsed = validate_raw_output(args.input.read_text(encoding="utf-8"))
        print(json.dumps(parsed, indent=2))
    elif args.command == "record":
        path = record_output(
            case_id=args.case_id,
            raw_output_path=args.raw_output,
            prompt_path=args.prompt,
            results_dir=args.results_dir,
            provider=args.provider,
            model=args.model,
            run_id=args.run_id,
        )
        print(path)
    elif args.command == "freeze":
        frozen = freeze_results(args.results_dir, args.out_file)
        print(json.dumps(frozen, indent=2))
    else:  # pragma: no cover
        raise RuntimeError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
