$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
if(-not $env:MTS_DEADLINE_UTC){$env:MTS_DEADLINE_UTC='2026-10-14T07:34:26+00:00'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($variant in @('stable','event1','event2','frequency1','frequency2','joint')){
    foreach($upper in @('.04','.02')){
        & $python -B build_operator_bank.py --variant $variant --upper $upper
        if($LASTEXITCODE -eq 75){Write-Output 'Saved a safe bank boundary; remaining work is pending';exit 0}
        if($LASTEXITCODE -ne 0){throw 'Operator bank failed'}
    }
}
Write-Output 'All operator banks complete'
