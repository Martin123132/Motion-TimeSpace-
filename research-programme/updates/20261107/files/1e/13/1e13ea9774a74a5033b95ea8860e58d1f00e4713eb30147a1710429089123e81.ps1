$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($model in @('heavy','cold')){
    if(Test-Path -LiteralPath "./results/inner-$model-n20480/checkpoints"){
        & $python -B refine_inner_again.py --model $model --resume
    } else {
        & $python -B refine_inner_again.py --model $model
    }
    if($LASTEXITCODE -ne 0){throw 'Inner integration failed'}
    if(-not (Test-Path -LiteralPath "./results/inner-$model-n20480/COMPLETE")){Write-Output 'Stopped at a safe restart checkpoint'; exit 0}
}
foreach($upper in @('.04','.02')){
    & $python -B recompute_feedback.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Feedback failed'}
}
& $python -B compare_inner_contraction.py
if($LASTEXITCODE -ne 0){throw 'Contraction comparison failed'}
