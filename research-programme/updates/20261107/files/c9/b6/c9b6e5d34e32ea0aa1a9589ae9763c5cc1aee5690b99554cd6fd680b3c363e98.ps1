$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$jobs=@()
foreach ($index in @(0,1)) {
    $output=Join-Path $PSScriptRoot ("worker-"+$index+".log")
    $errors=Join-Path $PSScriptRoot ("worker-"+$index+".err.log")
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) {throw 'Inspect previous worker before restarting'}
    $worker=Start-Process -FilePath $python -ArgumentList @('-B','batch219.py','run','--worker',$index,'--seconds','11600','--stop-at','2026-10-26T03:55:00+00:00') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $worker.PriorityClass='BelowNormal'
    $jobs += [pscustomobject]@{Index=$index;Process=$worker}
}
$jobs | ForEach-Object {@{worker=$_.Index;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')}} | ConvertTo-Json | Set-Content -LiteralPath workers-started.json -Encoding utf8
foreach ($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ('Worker '+$job.Index+' exited '+$job.Process.ExitCode)
}
if (@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
$count=@(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'events') -Filter 'event-*.json' -Recurse).Count
Write-Output ("Saved completed events: "+$count+"/216")
exit 0
