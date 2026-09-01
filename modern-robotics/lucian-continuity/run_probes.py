import argparse
import json
from pathlib import Path

ROOT = Path(__file__).parent
GENOME_DIR = ROOT / "genomes"
PROBE_FILE = ROOT / "probes" / "behavioral_probes.json"


def load_genome(name: str) -> str:
    if name == "control":
        return ""

    path = GENOME_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Genome '{name}' not found at {path}")
    return path.read_text(encoding="utf-8")


def load_probes() -> list[dict]:
    return json.loads(PROBE_FILE.read_text(encoding="utf-8"))


def build_packet(genome_name: str, probe: dict) -> str:
    genome = load_genome(genome_name)

    parts = [
        f"GENOME CONDITION: {genome_name}",
        "",
        "SYSTEM ORIENTATION:",
        genome if genome else "[No MVCG orientation supplied.]",
        "",
        f"PROBE ID: {probe['id']}",
        "",
        "USER TASK:",
        probe["prompt"],
        "",
        "INSTRUCTION:",
        "Respond naturally to the user task. Do not discuss the experimental condition or scoring rubric.",
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate blind MVCG behavioral probe packets.")
    parser.add_argument(
        "--genome",
        default="ftlta_full",
        help="Genome condition, e.g. control, ftlta_full, ablate_f, ablate_t, ablate_l, ablate_tau, ablate_a",
    )
    parser.add_argument("--probe", help="Optional probe ID. If omitted, all probes are emitted.")
    parser.add_argument("--out", help="Optional output file. Otherwise print to stdout.")
    args = parser.parse_args()

    probes = load_probes()
    if args.probe:
        probes = [p for p in probes if p["id"] == args.probe]
        if not probes:
            raise ValueError(f"Unknown probe: {args.probe}")

    packets = []
    for probe in probes:
        packets.append(build_packet(args.genome, probe))

    output = ("\n\n" + "=" * 72 + "\n\n").join(packets)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"Wrote {len(packets)} probe packet(s) to {args.out}")
    else:
        print(output)


if __name__ == "__main__":
    main()
