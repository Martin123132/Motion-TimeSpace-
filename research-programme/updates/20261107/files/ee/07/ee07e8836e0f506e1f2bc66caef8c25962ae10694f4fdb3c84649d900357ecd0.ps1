$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$jobs = @()
foreach ($worker in @(0, 1)) {
    $output = Join-Path $PSScriptRoot ('diagnostic-worker-' + $worker + '.log')
    $errors = Join-Path $PSScriptRoot ('diagnostic-worker-' + $worker + '.err.log')
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) { throw 'Existing log: inspect before resuming.' }
    $process = Start-Process -FilePath $python -ArgumentList @('-B', 'diagnose208.py', 'run', '--worker', $worker, '--seconds', '5400') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $process.PriorityClass = 'BelowNormal'
    $jobs += [pscustomobject]@{Worker=$worker;Process=$process}
}
$jobs | ForEach-Object { @{worker=$_.Worker;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')} } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'diagnostic-workers-started.json') -Encoding utf8
foreach ($job in $jobs) { $job.Process.WaitForExit(); Write-Output ('Diagnostic worker '+$job.Worker+' exited '+$job.Process.ExitCode) }
if (@($jobs | Where-Object {$_.Process.ExitCode -ne 0}).Count) {exit 1}
$count = @(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'diagnostic/events') -Filter 'event-*.npz').Count
if ($count -ne 36) {Write-Output ('Diagnostic saved partial: '+$count+'/36');exit 0}
& $python -B .\diagnose208.py assess 2>&1 | Tee-Object -FilePath .\diagnostic-assessment.log -Append
exit $LASTEXITCODE
