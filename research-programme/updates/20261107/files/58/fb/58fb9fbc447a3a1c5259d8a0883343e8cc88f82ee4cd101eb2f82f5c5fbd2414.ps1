$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$records=@()
$active=@()
$index=0
foreach($endpoint in @('start','end')) {
    $cpu=2+2*$index
    $env:MTS_CPU=[string]$cpu
    $arguments=@('-B',"`"$root/repair_soft_events.py`"",'--endpoint',$endpoint,'--stop-at','2026-10-19T06:45:00+00:00')
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/$endpoint.log" -RedirectStandardError "$root/$endpoint.err"
    $active+=@{process=$process;endpoint=$endpoint}
    $records+=@{endpoint=$endpoint;pid=$process.Id;cpu=$cpu;started_utc=[DateTime]::UtcNow.ToString('o');state='running'}
    $index+=1
}
$records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/worker-launch.json" -Encoding utf8
foreach($entry in $active) {
    $entry.process.WaitForExit()
    $code=$entry.process.ExitCode
    ($records | Where-Object {$_.pid -eq $entry.process.Id}).state=if($code -eq 0){'complete'}elseif($code -eq 75){'paused_at_saved_node'}else{'failed'}
    ($records | Where-Object {$_.pid -eq $entry.process.Id}).exit_code=$code
}
$records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/worker-launch.json" -Encoding utf8
if(@($records | Where-Object {$_.state -ne 'complete'}).Count){exit 75}
