param(
    [Parameter(Mandatory=$true)][string]$StopAt,
    [ValidateRange(60,13500)][int]$Seconds=12500,
    [ValidatePattern('^[A-Za-z0-9_-]{1,40}$')][string]$Attempt='initial'
)
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$deadline=[DateTimeOffset]::Parse($StopAt).ToUniversalTime()
if ($deadline -le [DateTimeOffset]::UtcNow -or $deadline -gt [DateTimeOffset]::UtcNow.AddHours(3.75)) {throw 'Use a future event deadline inside this turn limit'}
$live=@(Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object {$_.CommandLine -match 'batch220\.py.*\brun\b'})
if ($live.Count) {throw 'A Stage220 worker is live; observe it instead of restarting'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$jobs=@()
foreach ($index in @(0,1)) {
    $output=Join-Path $PSScriptRoot ($Attempt+'-worker-'+$index+'.log')
    $errors=Join-Path $PSScriptRoot ($Attempt+'-worker-'+$index+'.err.log')
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) {throw 'This attempt already has logs; inspect them first'}
}
foreach ($index in @(0,1)) {
    $output=Join-Path $PSScriptRoot ($Attempt+'-worker-'+$index+'.log')
    $errors=Join-Path $PSScriptRoot ($Attempt+'-worker-'+$index+'.err.log')
    $worker=Start-Process -FilePath $python -ArgumentList @('-B','batch220.py','run','--worker',$index,'--seconds',$Seconds,'--stop-at',$deadline.ToString('o')) -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $worker.PriorityClass='BelowNormal'
    $jobs += [pscustomobject]@{Index=$index;Process=$worker}
}
$jobs | ForEach-Object {@{worker=$_.Index;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o');stop_at=$deadline.ToString('o')}} | ConvertTo-Json | Set-Content -LiteralPath ($Attempt+'-workers.json') -Encoding utf8
foreach ($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ('Worker '+$job.Index+' exited '+$job.Process.ExitCode)
}
if (@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
$count=@(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'events') -Filter 'event-*.json' -Recurse).Count
Write-Output ("Saved completed events: "+$count+"/216")
exit 0
