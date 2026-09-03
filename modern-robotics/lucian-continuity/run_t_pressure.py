import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from run_ollama import call_ollama
from run_probes import load_genome

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
PROBE_FILE = ROOT / "probes" / "t_pressure_probes_v004.json"
PROTOCOL_VERSION = "t-pressure-0.04"

CONDITIONS = {
    "control": "control",
    "full_v003": "ftlta_mechanistic_v003",
    "minus_t_v003": "ablate_t_mechanistic_v003",
}


def load_probes() -> list[dict]:
    return json.loads(PROBE_FILE.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the v0.04 T pressure experiment against local Ollama."
    )
    parser.add_argument("--model", required=True, help="Installed Ollama model name.")
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--num-predict", type=int, default=256)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--think", action="store_true")
    parser.add_argument(
        "--condition",
        choices=list(CONDITIONS),
        help="Optional single condition. Default runs all conditions.",
    )
    parser.add_argument("--probe", help="Optional single probe ID.")
    parser.add_argument("--out", help="Optional JSONL output path.")
    args = parser.parse_args()

    probes = load_probes()
    if args.probe:
        probes = [p for p in probes if p["id"] == args.probe]
        if not probes:
            raise ValueError(f"Unknown probe: {args.probe}")

    condition_names = [args.condition] if args.condition else list(CONDITIONS)

    RESULTS_DIR.mkdir(exist_ok=True)
    if args.out:
        output_path = Path(args.out)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_model = args.model.replace("/", "_").replace(":", "_")
        output_path = RESULTS_DIR / f"{stamp}_{safe_model}_t_pressure_v004.jsonl"

    rows = []
    for probe in probes:
        for condition_name in condition_names:
            orientation = load_genome(CONDITIONS[condition_name])
            raw = call_ollama(
                args.host,
                args.model,
                orientation,
                probe["prompt"],
                args.temperature,
                args.timeout,
                args.num_predict,
                args.num_ctx,
                args.think,
            )
            response_text = raw.get("message", {}).get("content", "")
            row = {
                "protocol_version": PROTOCOL_VERSION,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "host": "ollama",
                "model": args.model,
                "condition": condition_name,
                "probe_id": probe["id"],
                "temperature": args.temperature,
                "think": args.think,
                "num_predict": args.num_predict,
                "num_ctx": args.num_ctx,
                "response": response_text,
                "done_reason": raw.get("done_reason"),
                "eval_count": raw.get("eval_count"),
                "prompt_eval_count": raw.get("prompt_eval_count"),
                "total_duration": raw.get("total_duration"),
            }
            rows.append(row)
            print(f"[{condition_name}] {probe['id']}: {response_text}\n")

    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Saved {len(rows)} result(s) to {output_path}")


if __name__ == "__main__":
    main()
