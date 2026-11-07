$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($upper in @('.04','.02')) {
    & $python -B next_feedback.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Feedback failed'}
}
& $python -B compare_next_grid.py
if($LASTEXITCODE -ne 0){throw 'Grid comparison failed'}
foreach($upper in @('.04','.02')) {
    foreach($model in @('heavy','cold')) {
        foreach($centre in @('baseline','mts')) {
            & $python -B evolve_precision_segment.py --upper $upper --model $model --centre $centre
            if($LASTEXITCODE -ne 0){throw 'Precision evolution failed'}
        }
    }
}
