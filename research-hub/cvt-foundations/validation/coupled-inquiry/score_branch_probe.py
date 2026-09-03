import argparse
import json
import random
import socket
import urllib.error
import urllib.request
from pathlib import Path


def call_ollama(host, model, prompt, temperature, timeout, num_predict, num_ctx):
    url = host.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "stream": False,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a blinded research-method judge. Evaluate only the text shown. "
                    "Do not infer hidden conditions or reward a particular theory."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "options": {
            "temperature": temperature,
            "num_predict": num_predict,
            "num_ctx": num_ctx,
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
        raise RuntimeError(f"Judge timed out at {url}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach judge Ollama at {url}: {exc}") from exc


def load_rows(path):
    rows = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_prompt(items):
    blocks = []
    for label, text in items:
        blocks.append(f"OUTPUT {label}\n{text.strip()}")
    return (
        "Below are continuations from the same research checkpoint. Their conditions are hidden.\n\n"
        + "\n\n---\n\n".join(blocks)
        + "\n\nEvaluate each output independently on these dimensions from 0 to 4:\n"
          "1. problem_reframing: changes what the explanatory object is, rather than merely elaborating the checkpoint;\n"
          "2. whole_pattern_orientation: seeks a process that explains ordinary and difficult cases together;\n"
          "3. residual_patch_orientation: primarily treats the problem as explaining or patching a leftover remainder;\n"
          "4. measurement_orientation: primarily relocates the mismatch to observation/measurement/state representation;\n"
          "5. mechanism_orientation: seeks a causal or generating process rather than a list of components;\n"
          "6. relational_orientation: makes relations/configuration central rather than merely mentioning them;\n"
          "7. discriminating_test_quality: proposes a test that could distinguish rival explanations;\n"
          "8. exploratory_inflation: opens multiple candidate structures without endorsing them as established.\n\n"
          "Then identify the two outputs with the most different search representations and explain the difference in at most 120 words. "
          "Return strict JSON with keys scores and most_different_pair. scores must map each output label to the eight integer scores."
    )


def main():
    parser = argparse.ArgumentParser(description="Blind-score coupled inquiry branch outputs with an Ollama judge.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--judge-model", required=True)
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--num-predict", type=int, default=900)
    parser.add_argument("--num-ctx", type=int, default=8192)
    parser.add_argument("--seed", type=int, default=9022026)
    parser.add_argument("--out")
    args = parser.parse_args()

    rows = load_rows(args.input)
    grouped = {}
    for row in rows:
        grouped.setdefault(row["replicate"], []).append(row)

    rng = random.Random(args.seed)
    scored = []
    for rep, rep_rows in sorted(grouped.items()):
        shuffled = list(rep_rows)
        rng.shuffle(shuffled)
        label_map = {}
        items = []
        for i, row in enumerate(shuffled):
            label = chr(ord("A") + i)
            label_map[label] = {
                "blind_id": row["blind_id"],
                "condition_type": row["condition_type"],
            }
            items.append((label, row["response"]))

        raw = call_ollama(
            args.host,
            args.judge_model,
            build_prompt(items),
            args.temperature,
            args.timeout,
            args.num_predict,
            args.num_ctx,
        )
        judge_text = raw.get("message", {}).get("content", "")
        scored.append({
            "replicate": rep,
            "label_map": label_map,
            "judge_model": args.judge_model,
            "judge_response": judge_text,
        })
        print(f"rep={rep}\n{judge_text}\n")

    out_path = Path(args.out) if args.out else Path(args.input).with_suffix(".scored.jsonl")
    with out_path.open("w", encoding="utf-8") as handle:
        for row in scored:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Saved {len(scored)} blinded judge rows to {out_path}")


if __name__ == "__main__":
    main()
