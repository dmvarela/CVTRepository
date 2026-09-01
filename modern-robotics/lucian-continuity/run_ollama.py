import argparse
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from run_probes import build_packet, load_probes

ROOT = Path(__file__).parent
RESULTS_DIR = ROOT / "results"


def call_ollama(host: str, model: str, prompt: str, temperature: float) -> dict:
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "options": {
            "temperature": temperature,
        },
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {url}. Is Ollama running? Original error: {exc}"
        ) from exc


def select_probes(probe_id: str | None) -> list[dict]:
    probes = load_probes()
    if probe_id is None:
        return probes

    selected = [probe for probe in probes if probe["id"] == probe_id]
    if not selected:
        raise ValueError(f"Unknown probe: {probe_id}")
    return selected


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run blind MVCG behavioral probes against a local Ollama model."
    )
    parser.add_argument("--model", required=True, help="Installed Ollama model name.")
    parser.add_argument("--genome", default="ftlta_full")
    parser.add_argument("--probe", help="Optional single probe ID.")
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--out",
        help="Optional JSONL result path. Default: results/<timestamp>_<model>_<genome>.jsonl",
    )
    args = parser.parse_args()

    probes = select_probes(args.probe)
    RESULTS_DIR.mkdir(exist_ok=True)

    if args.out:
        output_path = Path(args.out)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        safe_model = args.model.replace("/", "_").replace(":", "_")
        output_path = RESULTS_DIR / f"{stamp}_{safe_model}_{args.genome}.jsonl"

    rows = []
    for probe in probes:
        packet = build_packet(args.genome, probe)
        raw = call_ollama(args.host, args.model, packet, args.temperature)
        response_text = raw.get("message", {}).get("content", "")

        row = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "host": "ollama",
            "model": args.model,
            "genome_condition": args.genome,
            "probe_id": probe["id"],
            "temperature": args.temperature,
            "response": response_text,
            "done_reason": raw.get("done_reason"),
            "eval_count": raw.get("eval_count"),
            "prompt_eval_count": raw.get("prompt_eval_count"),
        }
        rows.append(row)
        print(f"[{args.genome}] {probe['id']}: {response_text}\n")

    with output_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Saved {len(rows)} result(s) to {output_path}")


if __name__ == "__main__":
    main()
