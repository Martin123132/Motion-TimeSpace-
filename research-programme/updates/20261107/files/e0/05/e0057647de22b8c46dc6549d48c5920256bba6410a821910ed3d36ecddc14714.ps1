$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($model in @('heavy','cold')){
    foreach($upper in @('.04','.02')){
        & $python -B evaluate_replay_sources.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Feedback failed'}
    }
}
