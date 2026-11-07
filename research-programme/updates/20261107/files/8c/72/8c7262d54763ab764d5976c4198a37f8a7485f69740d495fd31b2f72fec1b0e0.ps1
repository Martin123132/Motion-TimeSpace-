$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
if(-not $env:MTS_DEADLINE_UTC){$env:MTS_DEADLINE_UTC='2026-10-14T13:31:52+00:00'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($variant in @('control','dense','balanced')){
    foreach($model in @('heavy','cold')){
        & $python -B replay_coefficients.py --model $model --variant $variant
        if($LASTEXITCODE -eq 75){Write-Output 'Safe saved replay boundary;remaining work pending';exit 0}
        if($LASTEXITCODE -ne 0){throw 'Replay failed'}
    }
}
