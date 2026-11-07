param([string]$StopAt='2026-10-26T10:10:00+00:00',[ValidatePattern('^[A-Za-z0-9_-]{1,40}$')][string]$Attempt='initial')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$deadline=[DateTimeOffset]::Parse($StopAt).ToUniversalTime()
if ($deadline -le [DateTimeOffset]::UtcNow -or $deadline -gt [DateTimeOffset]::UtcNow.AddHours(3.75)) {throw 'Use a future deadline inside the turn limit'}
$live=@(Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object {$_.CommandLine -match 'response221\.py.*\bgenerate\b'})
if($live.Count) {throw 'Stage221 generator is already live; observe it'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
foreach($model in @('heavy','cold')) {
    foreach($suffix in @('.log','.err.log')) {
        if(Test-Path -LiteralPath (Join-Path $PSScriptRoot ($Attempt+'-'+$model+$suffix))) {throw 'Attempt logs exist; inspect before resuming'}
    }
}
$jobs=@()
foreach($model in @('heavy','cold')) {
    $worker=Start-Process -FilePath $python -ArgumentList @('-B','response221.py','generate','--model',$model,'--stop-at',$deadline.ToString('o')) -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput ($Attempt+'-'+$model+'.log') -RedirectStandardError ($Attempt+'-'+$model+'.err.log') -PassThru
    $worker.PriorityClass='BelowNormal'
    $jobs += [pscustomobject]@{Model=$model;Process=$worker}
}
$jobs | ForEach-Object {@{model=$_.Model;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o');stop_at=$deadline.ToString('o')}} | ConvertTo-Json | Set-Content -LiteralPath ($Attempt+'-workers.json') -Encoding utf8
foreach($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ($job.Model+' worker exited '+$job.Process.ExitCode)
}
if(@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
Write-Output ('Saved source points: '+@(Get-ChildItem -LiteralPath 'sources' -Filter 'result.json' -Recurse).Count+'/128')
exit 0
