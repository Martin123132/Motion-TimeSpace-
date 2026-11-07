$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
if(Test-Path -LiteralPath (Join-Path $root 'worker-launch.json')){throw 'Inspect saved workers before resuming.'}
foreach($anchor in @('warm','centre')){
    & $python -B (Join-Path $root 'evaluate_anchor.py') --anchor $anchor --dry-run
    if($LASTEXITCODE -ne 0){throw 'Dry run failed'}
}
$records=@()
$cpu=2
foreach($anchor in @('warm','centre')){
    $env:MTS_CPU="$cpu"
    $arguments=@('-B',('"{0}"' -f (Join-Path $root 'evaluate_anchor.py')),'--anchor',"$anchor")
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root "$anchor.log") -RedirectStandardError (Join-Path $root "$anchor.err") -PassThru
    $process.PriorityClass='BelowNormal'
    $process.ProcessorAffinity=[IntPtr](1 -shl $cpu)
    $records+=@{anchor=$anchor;pid=$process.Id;cpu=$cpu;started_utc=[DateTime]::UtcNow.ToString('o')}
    $cpu++
}
$records | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'worker-launch.json') -Encoding utf8
$records | ConvertTo-Json
