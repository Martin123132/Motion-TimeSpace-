$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($model in @('heavy','cold')){
    foreach($step in @(0,5120,10240,15360,20480,25600,30720,35840)){
        if(Test-Path -LiteralPath './PAUSE-REQUESTED'){Write-Output 'Safe pause between replay packets';exit 0}
        $label='{0:D5}' -f $step
        if(-not (Test-Path -LiteralPath "./results/replay-$model-s$label/COMPLETE")){
            & $python -B replay_source_intervals.py --model $model --restart-step $step
            if($LASTEXITCODE -ne 0){throw 'Replay failed'}
        }
    }
}
Write-Output 'Both background replays complete.'
