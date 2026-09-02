from __future__ import annotations

import argparse
import ctypes
import json
import os
import platform
import shutil
import subprocess
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class HostReport:
    os: str
    os_release: str
    architecture: str
    python: str
    cpu: str
    logical_cpus: int | None
    ram_gb: float | None
    gpu: list[dict[str, Any]]
    ollama_cli: str | None
    ollama_version: str | None
    ollama_service: bool
    ollama_models: list[str]
    recommendation: str
    notes: list[str]


def bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 1)


def total_ram_gb() -> float | None:
    if os.name == "nt":
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return bytes_to_gb(status.ullTotalPhys)
        return None

    if hasattr(os, "sysconf"):
        try:
            page_size = os.sysconf("SC_PAGE_SIZE")
            pages = os.sysconf("SC_PHYS_PAGES")
            return bytes_to_gb(page_size * pages)
        except (ValueError, OSError, AttributeError):
            pass
    return None


def run_command(args: list[str], timeout: float = 4.0) -> str | None:
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.SubprocessError):
        return None

    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def nvidia_gpus() -> list[dict[str, Any]]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return []

    output = run_command(
        [
            nvidia_smi,
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if not output:
        return []

    devices = []
    for line in output.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 3:
            continue
        try:
            vram_mb = int(float(parts[1]))
        except ValueError:
            vram_mb = None
        devices.append(
            {
                "name": parts[0],
                "vram_gb": round(vram_mb / 1024, 1) if vram_mb is not None else None,
                "driver": parts[2],
                "source": "nvidia-smi",
            }
        )
    return devices


def powershell_path() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def windows_gpu_names() -> list[dict[str, Any]]:
    shell = powershell_path()
    if os.name != "nt" or not shell:
        return []

    script = (
        "Get-CimInstance Win32_VideoController | "
        "Select-Object Name,AdapterRAM,DriverVersion | ConvertTo-Json -Compress"
    )
    output = run_command([shell, "-NoProfile", "-Command", script], timeout=6.0)
    if not output:
        return []

    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return []

    if isinstance(payload, dict):
        payload = [payload]

    devices: list[dict[str, Any]] = []
    for item in payload:
        adapter_ram = item.get("AdapterRAM")
        vram = None
        if isinstance(adapter_ram, int) and adapter_ram > 0:
            vram = bytes_to_gb(adapter_ram)
        devices.append(
            {
                "name": item.get("Name") or "Unknown GPU",
                "vram_gb": vram,
                "driver": item.get("DriverVersion"),
                "source": "Windows CIM",
            }
        )
    return devices


def detect_gpus() -> list[dict[str, Any]]:
    devices = nvidia_gpus()
    if devices:
        return devices
    return windows_gpu_names()


def ollama_status() -> tuple[str | None, str | None, bool, list[str]]:
    cli = shutil.which("ollama")
    version = run_command([cli, "--version"]) if cli else None

    service = False
    models: list[str] = []
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=1.5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        service = True
        for item in payload.get("models", []):
            name = item.get("name") or item.get("model")
            if name:
                models.append(name)
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        pass

    return cli, version, service, models


def recommend(ram_gb: float | None, gpus: list[dict[str, Any]]) -> tuple[str, list[str]]:
    notes: list[str] = []
    known_vram = [
        gpu["vram_gb"]
        for gpu in gpus
        if isinstance(gpu.get("vram_gb"), (int, float))
    ]
    max_vram = max(known_vram) if known_vram else None

    if max_vram is not None:
        if max_vram >= 16:
            rec = "MEDIUM/HIGH local host: start with a 7–14B quantized model; larger models may be practical after a speed/memory check."
        elif max_vram >= 10:
            rec = "MEDIUM local host: start with a 7–9B quantized model."
        elif max_vram >= 6:
            rec = "SMALL/MEDIUM local host: start with a 3–8B quantized model."
        elif max_vram >= 4:
            rec = "SMALL local host: start with a 3–4B quantized model."
        else:
            rec = "LIGHT local host: start with a 1–3B quantized model."
    elif ram_gb is not None:
        if ram_gb >= 32:
            rec = "CPU/RAM-capable host: start with a 7–9B quantized model; expect slower inference without usable GPU acceleration."
        elif ram_gb >= 16:
            rec = "CPU/RAM local host: start with a 3–7B quantized model."
        elif ram_gb >= 8:
            rec = "LIGHT local host: start with a 1–3B quantized model."
        else:
            rec = "VERY LIGHT host: use a tiny local model or keep the first experiment manual."
    else:
        rec = "Hardware class uncertain: begin with a small model and measure memory/latency before scaling."

    if gpus and max_vram is None:
        notes.append(
            "GPU VRAM could not be measured reliably. Integrated/AMD/Intel acceleration may still be available."
        )
    if any(gpu.get("source") == "Windows CIM" for gpu in gpus):
        notes.append(
            "Windows AdapterRAM can be unreliable for some modern GPUs; treat reported VRAM as approximate."
        )

    notes.append(
        "This recommendation is intentionally conservative. The first MVCG experiment needs consistency, not the largest possible model."
    )
    return rec, notes


def collect_report() -> HostReport:
    ram = total_ram_gb()
    gpus = detect_gpus()
    ollama_cli, ollama_version, ollama_service, ollama_models = ollama_status()
    recommendation, notes = recommend(ram, gpus)

    if not ollama_cli:
        notes.append("Ollama CLI was not found on PATH.")
    elif not ollama_service:
        notes.append("Ollama CLI is installed, but the local API did not answer at 127.0.0.1:11434.")
    elif not ollama_models:
        notes.append("Ollama is running, but no installed models were reported.")

    return HostReport(
        os=platform.system(),
        os_release=platform.release(),
        architecture=platform.machine(),
        python=platform.python_version(),
        cpu=platform.processor() or platform.machine() or "Unknown",
        logical_cpus=os.cpu_count(),
        ram_gb=ram,
        gpu=gpus,
        ollama_cli=ollama_cli,
        ollama_version=ollama_version,
        ollama_service=ollama_service,
        ollama_models=ollama_models,
        recommendation=recommendation,
        notes=notes,
    )


def print_report(report: HostReport) -> None:
    print()
    print("LUCIAN HOST CHECK")
    print("=" * 52)
    print(f"OS:            {report.os} {report.os_release} ({report.architecture})")
    print(f"Python:        {report.python}")
    print(f"CPU:           {report.cpu}")
    print(f"Logical CPUs:  {report.logical_cpus if report.logical_cpus is not None else 'Unknown'}")
    print(f"RAM:           {report.ram_gb if report.ram_gb is not None else 'Unknown'} GB")
    print()

    print("GPU")
    if report.gpu:
        for index, gpu in enumerate(report.gpu, start=1):
            vram = gpu.get("vram_gb")
            vram_text = f"{vram} GB" if vram is not None else "unknown"
            print(f"  {index}. {gpu.get('name', 'Unknown')} | VRAM: {vram_text} | source: {gpu.get('source')}")
    else:
        print("  No GPU information detected.")
    print()

    print("OLLAMA")
    print(f"  CLI:      {'found' if report.ollama_cli else 'not found'}")
    if report.ollama_cli:
        print(f"  Path:     {report.ollama_cli}")
    if report.ollama_version:
        print(f"  Version:  {report.ollama_version}")
    print(f"  Service:  {'running' if report.ollama_service else 'not detected'}")
    print("  Models:")
    if report.ollama_models:
        for model in report.ollama_models:
            print(f"    - {model}")
    else:
        print("    - none detected")
    print()

    print("RECOMMENDED STARTING CLASS")
    print(f"  {report.recommendation}")
    print()

    print("NOTES")
    for note in report.notes:
        print(f"  - {note}")
    print()
    print("Paste this output back into the Lucian OS project.")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect the local host for the Lucian Continuity/Ollama experiment."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the human-readable report.",
    )
    args = parser.parse_args()

    report = collect_report()
    if args.json:
        print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
