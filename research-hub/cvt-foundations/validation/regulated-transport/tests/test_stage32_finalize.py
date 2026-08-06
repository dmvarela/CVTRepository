import hashlib
import json
from pathlib import Path

from src.stage32_finalize import finalize


def test_finalize_replaces_nonfinite_json_and_rehashes_lock(tmp_path: Path) -> None:
    selection_path = tmp_path / "selection.json"
    lock_path = tmp_path / "model_lock_manifest.json"
    selection_path.write_text('{"rate": NaN, "nested": [Infinity, -Infinity]}')
    lock_path.write_text('{"selection_sha256": "old"}')

    finalize(tmp_path)

    selection_text = selection_path.read_text()
    assert "NaN" not in selection_text
    assert "Infinity" not in selection_text
    assert json.loads(selection_text) == {"rate": None, "nested": [None, None]}

    lock = json.loads(lock_path.read_text())
    expected = hashlib.sha256(selection_path.read_bytes()).hexdigest()
    assert lock["selection_sha256"] == expected
