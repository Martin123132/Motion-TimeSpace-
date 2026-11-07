$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$records=@()
foreach($band in @(3,4)) {
    $active=@()
    foreach($part in @(0,1)) {
        $env:MTS_CPU=[string](2+$part)
        $arguments=@('-B',"`"$root/evaluate_bands.py`"",'--band',[string]$band,'--part',[string]$part,'--stop-at','2026-10-18T20:00:00+00:00')
        $process=Start-Process -FilePath $python -ArgumentList $arguments -WorkingDirectory $root -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/band$band-part$part.log" -RedirectStandardError "$root/band$band-part$part.err"
        $active+=@{process=$process;band=$band;part=$part}
        $records+=@{band=$band;part=$part;pid=$process.Id;cpu=(2+$part);started_utc=[DateTime]::UtcNow.ToString('o');state='running'}
    }
    $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/worker-launch.json" -Encoding utf8
    foreach($entry in $active) {
        $entry.process.WaitForExit()
        $code=$entry.process.ExitCode
        ($records | Where-Object {$_.pid -eq $entry.process.Id}).state=if($code -eq 0){'complete'}elseif($code -eq 75){'paused_at_saved_node'}else{'failed'}
        ($records | Where-Object {$_.pid -eq $entry.process.Id}).exit_code=$code
    }
    $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$root/worker-launch.json" -Encoding utf8
    $failed=@($records | Where-Object {$_.state -ne 'complete'})
    if($failed.Count) {
        $records | ConvertTo-Json -Depth 5
        exit 75
    }
    Write-Output "Band $band complete at $([DateTime]::UtcNow.ToString('o'))"
}
$records | ConvertTo-Json -Depth 5
