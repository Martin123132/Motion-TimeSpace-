$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
function Invoke-Packet {
    param([string]$Script, [string]$Packet, [string[]]$ScriptArguments)
    if (-not (Test-Path -LiteralPath (Join-Path $root "$Packet/COMPLETE"))) {
        & $python -B (Join-Path $root $Script) @ScriptArguments 2>&1 |
            Tee-Object -FilePath (Join-Path $root 'precise-run.log') -Append
        if ($LASTEXITCODE -ne 0) { throw "$Script failed with exit code $LASTEXITCODE" }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $root "$Packet/COMPLETE"))) {
        throw "$Script stopped safely without a complete packet; do not continue."
    }
}
foreach ($tag in @('anchor', 'plus', 'minus', 'plus_half', 'minus_half')) {
    if (-not (Test-Path -LiteralPath (Join-Path $root "events/$tag/COMPLETE"))) {
        throw "Original stencil is incomplete: $tag"
    }
}
Invoke-Packet -Script 'repair_state_bank.py' -Packet 'results/state-overlays'
Invoke-Packet -Script 'freeze_predictions_repaired.py' -Packet 'results/frozen'
Invoke-Packet -Script 'evaluate_events_precise.py' -Packet 'events/target' -ScriptArguments @('target')
Invoke-Packet -Script 'test_predictions.py' -Packet 'results/prediction-test'
Invoke-Packet -Script 'analyse_tangent_repaired.py' -Packet 'results/tangent-interpretation'
Invoke-Packet -Script 'diagnose_prediction.py' -Packet 'results/error-decomposition'
Invoke-Packet -Script 'validate_batch_precise.py' -Packet 'results/batch-validation'
Invoke-Packet -Script 'validate_stage170.py' -Packet 'results/validation'
Write-Output 'Experiment and validation completed. Results report, final seal and resume bookmarks remain.'
