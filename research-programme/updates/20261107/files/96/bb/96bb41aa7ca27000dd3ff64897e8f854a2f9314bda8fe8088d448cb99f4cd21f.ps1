param([ValidateSet('anchors','target')][string]$Phase)
$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$jobs = @()
foreach ($worker in @(0,1)) {
    $output = Join-Path $PSScriptRoot ($Phase+'-'+$worker+'.log')
    $errors = Join-Path $PSScriptRoot ($Phase+'-'+$worker+'.err.log')
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) { throw 'Existing logs: inspect actual live workers before resuming.' }
    $process = Start-Process -FilePath $python -ArgumentList @('-B','operator213.py',$Phase,'--worker',$worker,'--seconds','10800') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $process.PriorityClass = 'BelowNormal'
    $jobs += [pscustomobject]@{Worker=$worker;Process=$process}
}
$jobs | ForEach-Object { @{worker=$_.Worker;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')} } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot ($Phase+'-started.json')) -Encoding utf8
foreach ($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ('Worker '+$job.Worker+' exited '+$job.Process.ExitCode)
}
if (@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) { exit 1 }
$count = @(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot $Phase) -Filter 'event-*.npz' -Recurse).Count
$expected = if ($Phase -eq 'anchors') {108} else {36}
if ($count -ne $expected) { Write-Output ('Safe partial '+$Phase+': '+$count+'/'+$expected); exit 0 }
if ($Phase -eq 'anchors') { & $python -B .\operator213.py freeze }
else { & $python -B .\assess213.py }
exit $LASTEXITCODE

