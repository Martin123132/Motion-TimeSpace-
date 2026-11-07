$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
foreach($model in @('heavy','cold')) {
    foreach($upper in @('0.02','0.04')) {
        & $python -B attribute_carried_source.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
