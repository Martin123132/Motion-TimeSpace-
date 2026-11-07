$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($upper in @('.04','.02')){
    if(Test-Path -LiteralPath './PAUSE-REQUESTED'){exit 0}
    & $python -B build_initial_operators.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Initial operator bank failed'}
}
foreach($model in @('heavy','cold')){
    foreach($upper in @('.04','.02')){
        if(Test-Path -LiteralPath './PAUSE-REQUESTED'){exit 0}
        & $python -B evaluate_initial_transient.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Initial source test failed'}
    }
}
Write-Output 'Both backgrounds and windows complete'
