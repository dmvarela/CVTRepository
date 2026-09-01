import sys
from pathlib import Path

GENOME_DIR = Path(__file__).parent / "genomes"


def load_genome(name: str) -> str:
    path = GENOME_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Genome '{name}' not found at {path}")
    return path.read_text(encoding="utf-8")


def list_genomes() -> None:
    print("\nAVAILABLE MVCG CANDIDATES")
    print("=" * 32)
    for path in sorted(GENOME_DIR.glob("*.md")):
        print(f"- {path.stem}")
    print()


def show_genome(name: str) -> None:
    genome = load_genome(name)
    print()
    print(f"MVCG: {name}")
    print("=" * 32)
    print(genome)


def main() -> None:
    if len(sys.argv) < 2:
        print("Commands:")
        print("  python app.py genomes")
        print("  python app.py genome ftlta_full")
        return

    command = sys.argv[1].lower()

    if command == "genomes":
        list_genomes()
    elif command == "genome":
        if len(sys.argv) < 3:
            print("Please specify a genome.")
            return
        show_genome(sys.argv[2])
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
