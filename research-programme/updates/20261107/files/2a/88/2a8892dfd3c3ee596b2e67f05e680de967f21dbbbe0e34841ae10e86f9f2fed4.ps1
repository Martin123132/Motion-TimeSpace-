$ErrorActionPreference='Stop'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$jobs=@()
foreach ($index in @(0,1)) {
    $output=Join-Path $PSScriptRoot ("worker-"+$index+".log")
    $errors=Join-Path $PSScriptRoot ("worker-"+$index+".err.log")
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) {throw 'Inspect saved worker before restarting'}
    $worker=Start-Process -FilePath $python -ArgumentList @('-B','bridge215.py','run','--worker',$index,'--seconds','10500') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $worker.PriorityClass='BelowNormal'
    $jobs += [pscustomobject]@{Index=$index;Process=$worker}
}
$jobs | ForEach-Object {@{worker=$_.Index;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')}} | ConvertTo-Json | Set-Content -LiteralPath workers-started.json -Encoding utf8
foreach ($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ('Worker '+$job.Index+' exited '+$job.Process.ExitCode)
}
if (@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
$count=@(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'events') -Recurse -Filter 'event-*.npz').Count
if ($count -ne 108) {Write-Output ("Safe partial: "+$count+"/108");exit 0}
& $python -B .\bridge215.py freeze
exit $LASTEXITCODE
