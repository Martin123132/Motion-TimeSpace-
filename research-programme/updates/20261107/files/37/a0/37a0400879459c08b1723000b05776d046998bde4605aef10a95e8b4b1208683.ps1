$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$jobs = @()
foreach ($worker in @(0, 1)) {
    $output = Join-Path $PSScriptRoot ('worker-' + $worker + '.log')
    $errors = Join-Path $PSScriptRoot ('worker-' + $worker + '.err.log')
    if ((Test-Path -LiteralPath $output) -or (Test-Path -LiteralPath $errors)) { throw 'Worker log already exists; inspect and resume explicitly.' }
    $process = Start-Process -FilePath $python -ArgumentList @('-B', 'connection208.py', 'run', '--worker', $worker, '--seconds', '5400', '--central-only') -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -RedirectStandardOutput $output -RedirectStandardError $errors -PassThru
    $process.PriorityClass = 'BelowNormal'
    $jobs += [pscustomobject]@{ Worker = $worker; Process = $process }
}
$jobs | ForEach-Object { @{worker=$_.Worker;pid=$_.Process.Id;started_at=$_.Process.StartTime.ToUniversalTime().ToString('o')} } | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'workers-started.json') -Encoding utf8
foreach ($job in $jobs) {
    $job.Process.WaitForExit()
    Write-Output ('Worker ' + $job.Worker + ' exited ' + $job.Process.ExitCode)
}
if (@($jobs | Where-Object { $_.Process.ExitCode -ne 0 }).Count) { exit 1 }
$count = @(Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'events/frequency-3') -Filter 'event-*.npz').Count
if ($count -ne 36) { Write-Output ('Saved partial node: ' + $count + '/36'); exit 0 }
& $python -B .\assess208.py 2>&1 | Tee-Object -FilePath .\assessment.log -Append
exit $LASTEXITCODE
