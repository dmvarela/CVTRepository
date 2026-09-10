param(
    [Parameter(Mandatory = $true)]
    [string]$Model
)

$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $Here "..\..")).Path
$Benchmark = Join-Path $ProjectRoot "experiments\requirement_extraction_001.json"
$Runner = Join-Path $ProjectRoot "prototype\run_requirement_extraction_v001.py"
$Evaluator = Join-Path $ProjectRoot "prototype\evaluate_requirement_extraction_v001.py"
$ResultsDir = Join-Path $Here "results"

if (-not (Test-Path $Benchmark)) {
    throw "Frozen benchmark not found: $Benchmark"
}
if (-not (Test-Path $Runner)) {
    throw "Runner not found: $Runner"
}
if (-not (Test-Path $Evaluator)) {
    throw "Evaluator not found: $Evaluator"
}

New-Item -ItemType Directory -Force -Path $ResultsDir | Out-Null

$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$SafeModel = ($Model -replace '[^A-Za-z0-9._-]', '_')
$Predictions = Join-Path $ResultsDir "requirement_extraction_001_${SafeModel}_${Stamp}_predictions.json"
$Scores = Join-Path $ResultsDir "requirement_extraction_001_${SafeModel}_${Stamp}_scores.json"

$env:LUCIAN_MODEL = $Model

Write-Host "REQUIREMENT_EXTRACTION_001"
Write-Host "Dedicated run folder: $Here"
Write-Host "Project root: $ProjectRoot"
Write-Host "Model: $Model"
Write-Host "Frozen benchmark: $Benchmark"
Write-Host "Capability menu exposed: False"
Write-Host "Execution: simulation / semantic extraction only"
Write-Host ""

Push-Location $ProjectRoot
try {
    py $Runner `
        --benchmark $Benchmark `
        --output $Predictions

    if ($LASTEXITCODE -ne 0) {
        throw "Requirement extraction runner failed with exit code $LASTEXITCODE"
    }

    py $Evaluator `
        --benchmark $Benchmark `
        --predictions $Predictions `
        --output $Scores

    if ($LASTEXITCODE -ne 0) {
        throw "Requirement extraction evaluator failed with exit code $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Completed REQUIREMENT_EXTRACTION_001 only."
Write-Host "Predictions: $Predictions"
Write-Host "Scores:      $Scores"
