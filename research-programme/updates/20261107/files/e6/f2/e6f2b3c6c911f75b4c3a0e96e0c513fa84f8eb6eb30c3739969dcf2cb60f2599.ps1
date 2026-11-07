$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
$worker=Join-Path $root 'evaluate_adjacent_events.py'
$receipt=Join-Path $root 'worker-launch.json'
if(Test-Path -LiteralPath $receipt){throw 'Launch receipt already exists; inspect saved workers instead of duplicating them.'}
if(-not (Test-Path -LiteralPath (Join-Path $root 'results\preflight\COMPLETE'))){throw 'Preflight is incomplete.'}
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$jobs=@()
foreach($entry in @(@{epoch='centre';cpu='2'},@{epoch='end';cpu='4'})){
    $env:MTS_CPU=$entry.cpu
    $stdout=Join-Path $root ($entry.epoch+'-events.log')
    $stderr=Join-Path $root ($entry.epoch+'-events.err')
    $arguments=@('-B',('`"'+$worker+'`"'),'--epoch',$entry.epoch,'--max-seconds','10500')
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    $jobs+=@{epoch=$entry.epoch;pid=$process.Id;cpu=$entry.cpu;script=$worker;started_utc=[DateTime]::UtcNow.ToString('o');stdout=$stdout;stderr=$stderr}
}
@{jobs=$jobs;maximum_workers=2;no_subagents=$true;checkpoint_stop_before_utc='2026-10-16T00:00:00Z'}|ConvertTo-Json -Depth 5|Set-Content -LiteralPath $receipt -Encoding UTF8
$jobs|ConvertTo-Json -Depth 5
