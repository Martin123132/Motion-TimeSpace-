$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:MTS_DEADLINE_UTC='2026-10-14T15:18:00+00:00'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
foreach($model in @('heavy','cold')) {
    foreach($variant in @('control','cubic')) {
        & $python -B replay_cubic_inner.py --model $model --variant $variant
        if($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
foreach($upper in @('0.02','0.04')) {
    & $python -B build_cubic_weak.py --upper $upper
    if($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
