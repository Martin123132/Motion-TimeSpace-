param([Parameter(Mandatory=$true)][int]$WorkerId,
      [Parameter(Mandatory=$true)][string]$Label)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
if ($Label -notmatch '^annular-wave-flux-events-(reference|MTS)-third-attempt01$') { throw 'Unexpected evidence label' }
$folder = [IO.Path]::GetFullPath((Join-Path $root "source-intake/navier-stokes/20260914/$Label"))
if (-not $folder.StartsWith($root + [IO.Path]::DirectorySeparatorChar)) { throw 'Out-of-scope evidence' }
$statusPath = Join-Path $folder 'status.json'
$raw = [IO.File]::ReadAllText($statusPath)
$status = $raw | ConvertFrom-Json -AsHashtable
if ($status.state -ne 'running' -or $status.cases.Count -ne 2 -or $status.progress.stage -notlike 'volume-32/36:*') { throw 'Not at the complete two-rule boundary' }
if (@($status.checks | Where-Object { -not $_.passed }).Count) { throw 'Prior checks failed' }
$process = Get-CimInstance Win32_Process -Filter "ProcessId = $WorkerId"
if (-not $process -or $process.Name -ne 'python.exe' -or $process.CommandLine -notlike '*scripts/diagnose_annular_wave_flux_third_20260930.py*' -or $process.CommandLine -notlike "*--label $Label *") { throw 'Worker identity mismatch' }
$created = $process.CreationDate.ToUniversalTime()
if ($created -lt [datetime]'2026-09-29T23:53:30Z' -or $created -gt [datetime]'2026-09-29T23:54:00Z') { throw 'Worker creation time mismatch' }
$snapshot = Join-Path $folder 'status-running-at-two-rule-boundary.json'
if (Test-Path -LiteralPath $snapshot) { throw 'Boundary already recorded' }
[IO.File]::WriteAllText($snapshot, $raw, [Text.UTF8Encoding]::new($false))
$owned = Get-Process -Id $WorkerId
Stop-Process -Id $WorkerId -Force
if (-not $owned.WaitForExit(10000)) { throw 'Owned worker did not exit' }
$status.state = 'failed'
$status.error = 'External safe boundary: completed two rules preserved; final rule continues in a new evidence run with its own time guard.'
$status.external_safe_boundary_stop = $true
$status.numerical_failure = $false
$status.stopped_at = [datetime]::UtcNow.ToString('o')
$status.stopped_worker = @{pid=$WorkerId; created_utc=$created.ToString('o'); command_line=$process.CommandLine}
$snapshotRelative = [IO.Path]::GetRelativePath($root, $snapshot)
$scriptRelative = [IO.Path]::GetRelativePath($root, $PSCommandPath)
$status.outputs[$snapshotRelative] = (Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash.ToLowerInvariant()
$status.inputs[$scriptRelative] = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText($statusPath, ($status | ConvertTo-Json -Depth 100) + "`n", [Text.UTF8Encoding]::new($false))
Write-Output "Saved two complete rules and stopped only owned worker $WorkerId ($Label)."
