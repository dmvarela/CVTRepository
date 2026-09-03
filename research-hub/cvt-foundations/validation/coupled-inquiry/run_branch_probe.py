import argparse
import json
import random
import socket
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent
DEFAULT_SPEC = ROOT / "checkpoint_001.json"
RESULTS_DIR = ROOT / "results"
PROTOCOL_VERSION = "0.1-local-branch-probe"


def call_ollama(host, model, prompt, temperature, timeout, num_predict, num_ctx, seed):
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Continue the research dialogue directly and naturally. "
                    "Do not discuss hidden conditions, experiments, branches, or scoring. "
                    "Do not assume the prior framing is correct merely because it was proposed."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "num_ctx": num_ctx,
            "seed": seed,
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (TimeoutError, socket.timeout) as exc:
        raise RuntimeError(f"Ollama timed out at {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach Ollama at {url}: {exc}") from exc


def build_prompt(spec, condition):
    return (
        "RESEARCH CHECKPOINT\n"
        + spec["base_context"].strip()
        + "\n\nINCOMING MOVE\n"
        + condition["incoming_move"].strip()
        + "\n\nNEXT TASK\n"
        + spec["task"].strip()
    )


def main():
    parser = argparse.ArgumentParser(description="Run isolated coupled-inquiry branch probes against local Ollama.")
    parser.add_argument("--model", required=True)
    parser.add_argument("--spec", default=str(DEFAULT_SPEC))
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--replicates", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--num-predict", type=int, default=600)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--seed-base", type=int, default=260902)
    parser.add_argument("--out")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    RESULTS_DIR.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_model = args.model.replace("/", "_").replace(":", "_")
    out_path = Path(args.out) if args.out else RESULTS_DIR / f"{stamp}_{safe_model}_{spec['id']}.jsonl"

    jobs = []
    for rep in range(args.replicates):
        for condition in spec["conditions"]:
            jobs.append((rep, condition))
    random.Random(args.seed_base).shuffle(jobs)

    rows = []
    for index, (rep, condition) in enumerate(jobs, start=1):
        seed = args.seed_base + rep
        prompt = build_prompt(spec, condition)
        raw = call_ollama(
            args.host,
            args.model,
            prompt,
            args.temperature,
            args.timeout,
            args.num_predict,
            args.num_ctx,
            seed,
        )
        response_text = raw.get("message", {}).get("content", "")
        row = {
            "protocol_version": PROTOCOL_VERSION,
            "checkpoint_id": spec["id"],
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "model": args.model,
            "blind_id": condition["blind_id"],
            "condition_type": condition["type"],
            "replicate": rep,
            "seed": seed,
            "temperature": args.temperature,
            "response": response_text,
            "done_reason": raw.get("done_reason"),
            "eval_count": raw.get("eval_count"),
            "prompt_eval_count": raw.get("prompt_eval_count"),
        }
        rows.append(row)
        print(f"[{index}/{len(jobs)}] {condition['blind_id']} rep={rep}\n{response_text}\n")

    with out_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Saved {len(rows)} isolated branch outputs to {out_path}")


if __name__ == "__main__":
    main()
