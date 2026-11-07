$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($upper in @('.04','.02')){
    if(Test-Path -LiteralPath './PAUSE-REQUESTED'){Write-Output 'Safe pause before next operator bank';exit 0}
    $label=[int]([double]$upper*1000)
    if(-not (Test-Path -LiteralPath "./results/operator-m$label/COMPLETE")){
        & $python -B build_intermediate_operators.py --upper $upper
        if($LASTEXITCODE -ne 0){throw 'Fresh operator bank failed'}
    }
}
foreach($model in @('heavy','cold')){
    foreach($upper in @('.04','.02')){
        if(Test-Path -LiteralPath './PAUSE-REQUESTED'){Write-Output 'Safe pause before next source probe';exit 0}
        $label=[int]([double]$upper*1000)
        if(-not (Test-Path -LiteralPath "./results/probe-$model-m$label/COMPLETE")){
            & $python -B evaluate_source_probes.py --model $model --upper $upper
            if($LASTEXITCODE -ne 0){throw 'Source probe failed'}
        }
    }
}
Write-Output 'Source operators and both-background probes complete.'
