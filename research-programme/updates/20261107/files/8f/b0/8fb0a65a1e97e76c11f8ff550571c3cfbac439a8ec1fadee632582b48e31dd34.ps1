$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
& $python -B test_inner_counterpart.py
if($LASTEXITCODE -ne 0){throw 'Exact inner identities failed'}
& $python -B test_inner_dispersion.py
if($LASTEXITCODE -ne 0){throw 'Inner symbol calculation failed'}
foreach($model in @('heavy','cold')){
    foreach($upper in @('0.04','0.02')){
        & $python -B evaluate_spatial_defect.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Feedback failed'}
    }
}
