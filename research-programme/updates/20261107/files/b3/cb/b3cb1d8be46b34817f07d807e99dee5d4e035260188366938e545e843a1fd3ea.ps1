$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($upper in @('0.04','0.02')){
    & $python -B compare_weak_actions.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Weak-action comparison failed'}
}
& $python -B test_finite_adjoint.py
if($LASTEXITCODE -ne 0){throw 'Finite adjoint identity failed'}
foreach($model in @('heavy','cold')){
    foreach($upper in @('0.04','0.02')){
        & $python -B evaluate_source_pairing.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Paired feedback failed'}
    }
}
