$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
if(-not (Test-Path -LiteralPath './results/inner-cold-n40960/COMPLETE')){
    if(Test-Path -LiteralPath './results/inner-cold-n40960/checkpoints'){
        & $python -B refine_inner_again.py --model cold --resume
    } else {
        & $python -B refine_inner_again.py --model cold
    }
    if($LASTEXITCODE -ne 0){throw 'Inner integration failed'}
    if(-not (Test-Path -LiteralPath './results/inner-cold-n40960/COMPLETE')){Write-Output 'Stopped at a safe restart checkpoint'; exit 0}
}
foreach($upper in @('.04','.02')){
    $label=[int]([double]$upper*1000)
    if(-not (Test-Path -LiteralPath "./results/feedback-m$label-n40960/COMPLETE")){
        & $python -B recompute_feedback.py --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Feedback failed'}
    }
}
if(-not (Test-Path -LiteralPath './results/inner-contraction/COMPLETE')){
    & $python -B compare_inner_contraction.py
    if($LASTEXITCODE -ne 0){throw 'Contraction comparison failed'}
}
Write-Output 'Cold-background computation complete; paired comparison includes sealed heavy data.'
