$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($model in @('heavy','cold')) {
    & $python -B refine_inner_time.py --model $model
    if($LASTEXITCODE -ne 0){throw 'Inner time refinement failed'}
}
foreach($upper in @('.04','.02')) {
    & $python -B refine_time_feedback.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Time-refined feedback failed'}
}
& $python -B compare_time_refinement.py
if($LASTEXITCODE -ne 0){throw 'Time comparison failed'}
