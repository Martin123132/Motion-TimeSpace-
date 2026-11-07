$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:MTS_DEADLINE_UTC='2026-10-14T23:55:00+00:00'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
foreach($upper in @('0.02','0.04')) {
    & $python -B build_half_sources.py --upper $upper
    if($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
foreach($model in @('heavy','cold')) {
    foreach($upper in @('0.02','0.04')) {
        if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse($env:MTS_DEADLINE_UTC)) { exit 75 }
        & $python -B evaluate_half_feedback.py --model $model --upper $upper
        if($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
