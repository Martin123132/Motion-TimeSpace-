$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$workers = @(
    @{Id=17304; Label='annular-C0-integral-reference-attempt01'; Script='scripts/integrate_annular_C0_20260930.py'; Earliest='2026-09-30T14:13:00Z'; Latest='2026-09-30T14:13:15Z'; Mode='third-low'},
    @{Id=24080; Label='annular-C0-integral-MTS-attempt02'; Script='scripts/integrate_annular_C0_v2_20260930.py'; Earliest='2026-09-30T14:49:35Z'; Latest='2026-09-30T14:49:50Z'; Mode='fine-complete'}
)
$finished = @{}
while ($finished.Count -lt $workers.Count) {
    if ([datetime]::UtcNow -gt ([datetime]'2026-09-30T17:55:00Z').ToUniversalTime()) { throw 'Safe-boundary watcher deadline reached; no unconditional stop issued' }
    foreach ($worker in $workers) {
        if ($finished.ContainsKey($worker.Label)) { continue }
        $process = Get-CimInstance Win32_Process -Filter "ProcessId = $($worker.Id)"
        if (-not $process) { $finished[$worker.Label]='already exited'; Write-Output ($worker.Label+': already exited'); continue }
        if ($process.Name -ne 'python.exe' -or $process.CommandLine -notlike "*$($worker.Script)*" -or $process.CommandLine -notlike "*--label $($worker.Label) *") { throw 'Worker identity mismatch' }
        $created = $process.CreationDate.ToUniversalTime()
        if ($created -lt ([datetime]$worker.Earliest).ToUniversalTime() -or $created -gt ([datetime]$worker.Latest).ToUniversalTime()) { throw 'Worker creation mismatch' }
        $folder = [IO.Path]::GetFullPath((Join-Path $root ('source-intake/navier-stokes/20260914/'+$worker.Label)))
        if (-not $folder.StartsWith($root+[IO.Path]::DirectorySeparatorChar)) { throw 'Out-of-scope target' }
        $statusPath = Join-Path $folder 'status.json'
        try { $raw=[IO.File]::ReadAllText($statusPath); $status=$raw|ConvertFrom-Json -AsHashtable } catch { Start-Sleep -Milliseconds 300; continue }
        if ($status.state -ne 'running') { $finished[$worker.Label]=$status.state; continue }
        $fine = @($status.cases|Where-Object {$_.summary.level -eq 'fine' -and $_.summary.complete_integral_constructed})
        $low = @($status.rule_outputs|Where-Object {$_.level -eq 'third' -and $_.component -eq 'wave' -and $_.order -eq 24})
        $ready = $fine.Count -eq 1
        if ($worker.Mode -eq 'third-low') { $ready = $ready -and $low.Count -eq 1 -and $status.progress.stage -like 'third:C0-volume-32/36:*' }
        else { $ready = $ready -and $status.progress.stage -like 'third:*' }
        if (-not $ready) { continue }
        if (@($status.checks|Where-Object {-not $_.passed}).Count) { throw 'Scientific check failure cannot be relabelled as a safe stop' }
        foreach ($relative in $status.outputs.Keys) {
            $outputPath = [IO.Path]::GetFullPath((Join-Path $root $relative))
            if (-not $outputPath.StartsWith($root+[IO.Path]::DirectorySeparatorChar)) { throw 'Out-of-scope output' }
            if ((Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $status.outputs[$relative]) { throw 'Incomplete output at boundary' }
        }
        $snapshot = Join-Path $folder 'status-running-at-C0-safe-boundary.json'
        if (Test-Path -LiteralPath $snapshot) { throw 'Boundary snapshot already exists' }
        [IO.File]::WriteAllText($snapshot, $raw, [Text.UTF8Encoding]::new($false))
        $owned = Get-Process -Id $worker.Id
        Stop-Process -Id $worker.Id -Force
        if (-not $owned.WaitForExit(10000)) { throw 'Owned worker did not exit' }
        $status.state='failed'
        $status.error='External safe boundary: completed C0 components preserved before another long rule. Continue in a new evidence run.'
        $status.external_safe_boundary_stop=$true
        $status.numerical_failure=$false
        $status.stopped_at=[datetime]::UtcNow.ToString('o')
        $status.stopped_worker=@{pid=$worker.Id; created_utc=$created.ToString('o'); command_line=$process.CommandLine}
        $relative=[IO.Path]::GetRelativePath($root,$snapshot)
        $status.outputs[$relative]=(Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash.ToLowerInvariant()
        $relative=[IO.Path]::GetRelativePath($root,$PSCommandPath)
        $status.inputs[$relative]=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
        [IO.File]::WriteAllText($statusPath,($status|ConvertTo-Json -Depth 100)+"`n",[Text.UTF8Encoding]::new($false))
        $finished[$worker.Label]='safe saved stop'
        Write-Output ($worker.Label+': saved completed outputs and stopped owned worker '+$worker.Id+' at '+[datetime]::UtcNow.ToString('o'))
    }
    if ($finished.Count -lt $workers.Count) { Start-Sleep -Seconds 5 }
}
