"""Lucian OS read-only computational proprioception probe v0.01.

Prints a host snapshot to stdout. It does not write files, change permissions,
probe the public network, load/unload models, or actuate devices.

Optional --include-runtime-status executes `ollama ps` if Ollama is available.
That command is read-only and is used only to report whether the local runtime
responds and how many models are currently loaded; model names are not emitted.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def memory_snapshot() -> dict[str, int | str | None]:
    try:
        import psutil  # type: ignore
        vm = psutil.virtual_memory()
        return {"source": "psutil", "total_mb": int(vm.total / (1024 * 1024)), "available_mb": int(vm.available / (1024 * 1024)), "used_mb": int(vm.used / (1024 * 1024))}
    except Exception:
        pass

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
        state = MEMORYSTATUSEX()
        state.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        ok = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state))
        if ok:
            total = int(state.ullTotalPhys / (1024 * 1024))
            available = int(state.ullAvailPhys / (1024 * 1024))
            return {"source": "windows_GlobalMemoryStatusEx", "total_mb": total, "available_mb": available, "used_mb": total - available}

    try:
        page = os.sysconf("SC_PAGE_SIZE")
        total_pages = os.sysconf("SC_PHYS_PAGES")
        avail_pages = os.sysconf("SC_AVPHYS_PAGES")
        total = int(page * total_pages / (1024 * 1024))
        available = int(page * avail_pages / (1024 * 1024))
        return {"source": "os.sysconf", "total_mb": total, "available_mb": available, "used_mb": total - available}
    except Exception:
        return {"source": "unavailable", "total_mb": None, "available_mb": None, "used_mb": None}


def disk_snapshot() -> dict[str, int | str | None]:
    try:
        probe_path = Path.cwd().anchor or str(Path.cwd())
        usage = shutil.disk_usage(probe_path)
        return {"source": "shutil.disk_usage", "total_mb": int(usage.total / (1024 * 1024)), "free_mb": int(usage.free / (1024 * 1024)), "used_mb": int(usage.used / (1024 * 1024))}
    except Exception:
        return {"source": "unavailable", "total_mb": None, "free_mb": None, "used_mb": None}


def runtime_availability() -> dict[str, bool]:
    return {
        "python": shutil.which("python") is not None or shutil.which("py") is not None,
        "git": shutil.which("git") is not None,
        "ollama": shutil.which("ollama") is not None,
        "powershell": shutil.which("powershell") is not None or shutil.which("pwsh") is not None,
    }


def ollama_status(enabled: bool) -> dict[str, Any]:
    if not enabled:
        return {"checked": False}
    if shutil.which("ollama") is None:
        return {"checked": True, "available": False, "responding": False, "loaded_model_count": None}
    try:
        proc = subprocess.run(["ollama", "ps"], capture_output=True, text=True, timeout=8, check=False)
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        count = max(0, len(lines) - 1) if proc.returncode == 0 else None
        return {"checked": True, "available": True, "responding": proc.returncode == 0, "loaded_model_count": count, "return_code": proc.returncode}
    except Exception as exc:
        return {"checked": True, "available": True, "responding": False, "loaded_model_count": None, "error_type": type(exc).__name__}


def collect(host_id: str, include_runtime_status: bool) -> dict[str, Any]:
    return {
        "schema_version": "0.01",
        "mode": "READ_ONLY_OBSERVATION",
        "host_id": host_id,
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "static": {
            "os": platform.system(),
            "os_release": platform.release(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "logical_cpu_count": os.cpu_count(),
        },
        "dynamic": {"memory": memory_snapshot(), "disk": disk_snapshot()},
        "runtime_availability": runtime_availability(),
        "ollama_status": ollama_status(include_runtime_status),
        "privacy": {
            "hostname_collected": False,
            "username_collected": False,
            "serial_number_collected": False,
            "network_address_collected": False,
            "executable_paths_collected": False,
            "model_names_collected": False,
        },
        "side_effect_contract": {
            "file_writes": False,
            "permission_changes": False,
            "network_probe": False,
            "model_load_unload": False,
            "device_actuation": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host-id", default="unassigned-local-host", help="Caller-supplied non-secret host label; hardware identifiers are not collected.")
    parser.add_argument("--include-runtime-status", action="store_true", help="Also run read-only `ollama ps`; no model names are emitted.")
    args = parser.parse_args()
    print(json.dumps(collect(args.host_id, args.include_runtime_status), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
