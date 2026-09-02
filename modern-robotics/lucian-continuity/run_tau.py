import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from run_ollama import call_ollama
from run_probes import load_genome

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"
TAU_SPEC = ROOT / "probes" / "tau_trace_conditions.json"
PROTOCOL_VERSION = "tau-0.01-trace-transversal"


def load_tau_spec() -> dict:
    with TAU_SPEC.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the transversal tau continuity trace experiment against local Ollama."
    )
    parser.add_argument("--model", required=True, help="Installed Ollama model name.")
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--num-predict", type=int, default=256)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument(
        "--think",
        action="store_true",
        help="Enable model thinking when supported. Disabled by default.",
    )
    parser.add_argument(
        "--condition",
        choices=["trace_full", "trace_distilled", "trace_none"],
        help="Optional single trace condition. Default runs all three.",
    )
    parser.add_argument("--out", help="Optional JSONL output path.")
    args = parser.parse_args()

    spec = load_tau_spec()
    ftla_orientation = load_genome("ftla_core")

    condition_names = (
        [args.condition]
        if args.condition
        else ["trace_full", "trace_distilled", "trace_none"]
    )

    RESULTS_DIR.mkdir(exist_ok=True)
    if args.out:
        output_path = Path(args.out)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_model = args.model.replace("/", "_").replace(":", "_")
        output_path = RESULTS_DIR / f"{stamp}_{safe_model}_tau_trace.jsonl"

    rows = []
    for condition_name in condition_names:
        recovered_context = spec["conditions"][condition_name]
        orientation = ftla_orientation
        if recovered_context:
            orientation += "\n\n" + recovered_context

        raw = call_ollama(
            args.host,
            args.model,
            orientation,
            spec["user_prompt"],
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
            "trace_condition": condition_name,
            "probe_id": spec["probe_id"],
            "temperature": args.temperature,
            "think": args.think,
            "num_predict": args.num_predict,
            "num_ctx": args.num_ctx,
            "response": response_text,
            "done_reason": raw.get("done_reason"),
            "eval_count": raw.get("eval_count"),
            "prompt_eval_count": raw.get("prompt_eval_count"),
            "total_duration": raw.get("total_duration"),
            "load_duration": raw.get("load_duration"),
            "prompt_eval_duration": raw.get("prompt_eval_duration"),
            "eval_duration": raw.get("eval_duration"),
        }
        rows.append(row)
        print(f"[{condition_name}] {spec['probe_id']}: {response_text}\n")

    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Saved {len(rows)} result(s) to {output_path}")


if __name__ == "__main__":
    main()
