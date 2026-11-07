$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
function Invoke-Stage {
    param([string]$Script, [string[]]$ScriptArguments)
    & $python -B (Join-Path $root $Script) @ScriptArguments 2>&1 |
        Tee-Object -FilePath (Join-Path $root 'run.log') -Append
    if ($LASTEXITCODE -ne 0) { throw "$Script failed with exit code $LASTEXITCODE" }
}
Invoke-Stage -Script 'evaluate_events.py' -ScriptArguments @('stencil')
foreach ($tag in @('anchor', 'plus', 'minus', 'plus_half', 'minus_half')) {
    if (-not (Test-Path -LiteralPath (Join-Path $root "events/$tag/COMPLETE"))) {
        Write-Output 'Stopped safely at the event deadline; stencil incomplete.'
        exit 0
    }
}
if (-not (Test-Path -LiteralPath (Join-Path $root 'results/frozen/COMPLETE'))) {
    Invoke-Stage -Script 'freeze_predictions.py'
}
Invoke-Stage -Script 'evaluate_events.py' -ScriptArguments @('target')
if (-not (Test-Path -LiteralPath (Join-Path $root 'events/target/COMPLETE'))) {
    Write-Output 'Stopped safely at the event deadline; target incomplete.'
    exit 0
}
if (-not (Test-Path -LiteralPath (Join-Path $root 'results/prediction-test/COMPLETE'))) {
    Invoke-Stage -Script 'test_predictions.py'
}
if (-not (Test-Path -LiteralPath (Join-Path $root 'results/tangent-interpretation/COMPLETE'))) {
    Invoke-Stage -Script 'analyse_tangent.py'
}
Write-Output 'Microscopic prediction experiment finished; validation and sealing still required.'
