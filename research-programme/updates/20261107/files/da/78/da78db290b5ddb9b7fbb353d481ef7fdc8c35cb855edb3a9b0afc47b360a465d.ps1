$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
if (Test-Path -LiteralPath (Join-Path $root 'worker-launch.json')) { throw 'Launch exists; inspect workers before resuming.' }
& $python -B (Join-Path $root 'evaluate_holdout_events.py') --epoch holdout --dry-run
if ($LASTEXITCODE -ne 0) { throw 'Dry run failed.' }
$records=@()
$cpu=2
foreach ($part in @('expensive','control')) {
    $env:MTS_CPU="$cpu"
    $arguments=@('-B',('"{0}"' -f (Join-Path $root 'evaluate_holdout_events.py')),'--epoch','holdout','--part',$part)
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput (Join-Path $root "$part-events.log") -RedirectStandardError (Join-Path $root "$part-events.err") -PassThru
    $process.PriorityClass='BelowNormal'
    $process.ProcessorAffinity=[IntPtr](1 -shl $cpu)
    $records+=@{part=$part;pid=$process.Id;cpu=$cpu;started_utc=[DateTime]::UtcNow.ToString('o')}
    $cpu++
}
$records | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $root 'worker-launch.json') -Encoding utf8
$records | ConvertTo-Json

