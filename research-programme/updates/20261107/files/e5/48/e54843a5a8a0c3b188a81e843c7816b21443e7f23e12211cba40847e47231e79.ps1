param([Parameter(Mandatory=$true)][ValidateSet(2048,4096)][int]$Count)
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
$live=@(Get-CimInstance Win32_Process -Filter "name='python.exe'" | Where-Object {$_.CommandLine -match '(evolve221|response221)\.py.*\b(run|generate|evolve)\b'})
if($live.Count) {throw 'A Stage221 numerical worker is live; observe it'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
foreach($model in @('heavy','cold')) {
    foreach($suffix in @('.log','.err.log')) {
        if(Test-Path -LiteralPath ('response-'+$model+'-'+$Count+$suffix)) {throw 'Response logs exist; inspect them first'}
    }
}
$jobs=@()
foreach($model in @('heavy','cold')) {
    $worker=Start-Process -FilePath $python -ArgumentList @('-B','evolve221.py','run','--model',$model,'--count',$Count) -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput ('response-'+$model+'-'+$Count+'.log') -RedirectStandardError ('response-'+$model+'-'+$Count+'.err.log') -PassThru
    $worker.PriorityClass='BelowNormal'
    $jobs += [pscustomobject]@{Model=$model;Process=$worker}
}
$jobs | ForEach-Object {@{model=$_.Model;count=$Count;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')}} | ConvertTo-Json | Set-Content -LiteralPath ('response-'+$Count+'-workers.json') -Encoding utf8
foreach($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ($job.Model+' response exited '+$job.Process.ExitCode)
}
if(@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
exit 0
