
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
if(Test-Path -LiteralPath (Join-Path $root 'response-launch.json')){throw 'Inspect response workers first'}
foreach($part in @(0,1)){if(-not(Test-Path -LiteralPath (Join-Path $root "runs/part$part/COMPLETE"))){throw 'Events incomplete'}}
$records=@()
$cpu=2
foreach($model in @('heavy','cold')){
    $env:MTS_CPU="$cpu"
    $arguments=@('-B',('"{0}"' -f (Join-Path $root 'propagate_order6.py')),'--model',$model)
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root "$model-response.log") -RedirectStandardError (Join-Path $root "$model-response.err") -PassThru
    $process.PriorityClass='BelowNormal'
    $process.ProcessorAffinity=[IntPtr](1 -shl $cpu)
    $records+=@{model=$model;pid=$process.Id;cpu=$cpu;started_utc=[DateTime]::UtcNow.ToString('o')}
    $cpu++
}
$records | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'response-launch.json') -Encoding utf8
$records | ConvertTo-Json
