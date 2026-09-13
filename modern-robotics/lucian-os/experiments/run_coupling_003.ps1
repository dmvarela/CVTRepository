$ErrorActionPreference = "Stop"

Write-Host "COUPLING_003 — scorer self-test"
python .\coupling_003_scorer.py --self-test
if ($LASTEXITCODE -ne 0) {
    throw "Scorer self-test failed. Aborting before any model call."
}

$stamp = Get-Date -Format "yyyyMMddTHHmmss"
$trace = "coupling_003_${stamp}.jsonl"
$summary = "coupling_003_${stamp}.summary.json"
$scores = "coupling_003_${stamp}_scores.txt"

Write-Host "COUPLING_003 — running frozen C0-C3 probe matrix on local Ollama"
python .\coupling_003_runner.py --shuffle --output $trace
if ($LASTEXITCODE -ne 0) {
    throw "Runner failed. Preserve any partial trace and stop."
}

Write-Host "COUPLING_003 — deterministic invariant scoring"
python .\coupling_003_scorer.py $trace --events | Tee-Object -FilePath $scores
if ($LASTEXITCODE -ne 0) {
    throw "Scoring failed. Preserve the trace unchanged."
}

Write-Host ""
Write-Host "Run complete. Preserve these files unchanged:"
Write-Host "  $trace"
Write-Host "  $summary"
Write-Host "  $scores"
Write-Host ""
Write-Host "Do not reinterpret or edit failed cases before review."
