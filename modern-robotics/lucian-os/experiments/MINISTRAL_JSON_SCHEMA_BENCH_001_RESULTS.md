# MINISTRAL-JSON-SCHEMA-BENCH-001 — Result

**Status:** PASS  
**Model:** `ministral-3:3b-instruct-2512-q4_K_M`  
**Observed digest:** `f04aa1c738f64e13c625b82ae92504fc0260fa6723b509ed1ece0fa188179b1d`  
**Manifest SHA256:** `2537158596c964bf42ef465fd123d59a94cb5846cc6a8996413450ba76f191f0`

The technical bench was run before RVT-INTERP-003 was frozen. It contained no K17 facts, no correction-history manipulation, and no 003 condition language.

Results:

- total calls: 12
- parseable JSON objects: 12/12
- exact schema-conforming objects: 12/12
- selective retries: none
- failures: none

The frozen pass rule required every call to satisfy exact required keys, no extra keys, enum constraints, integer confidence, and the 0–100 confidence range.

Therefore strict Ollama JSON Schema is eligible as the response interface for RVT-INTERP-003 under this locked local model/runtime.

This bench does not establish that schema conformance will be perfect on the experimental task. RVT-INTERP-003 must still preserve every raw response and must not selectively retry failures.
