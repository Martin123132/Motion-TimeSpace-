$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($model in @('heavy','cold')){
    if(Test-Path -LiteralPath './PAUSE-REQUESTED'){exit 0}
    & $python -B replay_response_sites.py --model $model --dry-run
    if($LASTEXITCODE -ne 0){throw 'Preflight failed'}
    & $python -B replay_response_sites.py --model $model
    if($LASTEXITCODE -ne 0){throw 'Replay failed'}
}
Write-Output 'Both response-site replays complete'
