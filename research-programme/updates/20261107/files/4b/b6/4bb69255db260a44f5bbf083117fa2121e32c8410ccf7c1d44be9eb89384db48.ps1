$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
$worker=Join-Path $root 'evaluate_colder_events.py'
$receipt=Join-Path $root 'worker-launch.json'
if(Test-Path -LiteralPath $receipt){throw 'Receipt exists; inspect workers before restarting.'}
if(-not (Test-Path -LiteralPath (Join-Path $root 'results\preflight\COMPLETE'))){throw 'Preflight incomplete.'}
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$jobs=@()
foreach($entry in @(@{part='expensive';cpu='2'},@{part='control';cpu='4'})){
    $env:MTS_CPU=$entry.cpu
    $stdout=Join-Path $root ($entry.part+'-events.log')
    $stderr=Join-Path $root ($entry.part+'-events.err')
    $arguments=@('-B',('"'+$worker+'"'),'--epoch','colder','--part',$entry.part,'--max-seconds','10500')
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    $jobs+=@{part=$entry.part;pid=$process.Id;cpu=$entry.cpu;script=$worker;started_utc=[DateTime]::UtcNow.ToString('o');stdout=$stdout;stderr=$stderr}
}
@{jobs=$jobs;maximum_workers=2;no_subagents=$true;checkpoint_stop_before_utc='2026-10-16T05:30:00Z'}|ConvertTo-Json -Depth 5|Set-Content -LiteralPath $receipt -Encoding UTF8
$jobs|ConvertTo-Json -Depth 5
