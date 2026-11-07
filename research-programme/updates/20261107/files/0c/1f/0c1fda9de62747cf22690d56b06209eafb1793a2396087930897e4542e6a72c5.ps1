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
foreach($model in @('heavy','cold')) {
    $cpu=2+2*$index
    $env:MTS_CPU=[string]$cpu
    $arguments=@('-B',"`"$root/replay_reference.py`"",'--model',$model)
    $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/replay-$model.log" -RedirectStandardError "$root/replay-$model.err"
    $active+=@{process=$process;model=$model}
    $records+=@{model=$model;pid=$process.Id;cpu=$cpu;started_utc=[DateTime]::UtcNow.ToString('o');state='running'}
    $index+=1
}
$records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/replay-worker-launch.json" -Encoding utf8
foreach($entry in $active) {
    $entry.process.WaitForExit()
    $code=$entry.process.ExitCode
    ($records | Where-Object {$_.pid -eq $entry.process.Id}).state=if($code -eq 0){'complete'}elseif($code -eq 75){'paused_at_saved_node'}else{'failed'}
    ($records | Where-Object {$_.pid -eq $entry.process.Id}).exit_code=$code
}
$records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/replay-worker-launch.json" -Encoding utf8
if(@($records | Where-Object {$_.state -ne 'complete'}).Count){exit 75}
