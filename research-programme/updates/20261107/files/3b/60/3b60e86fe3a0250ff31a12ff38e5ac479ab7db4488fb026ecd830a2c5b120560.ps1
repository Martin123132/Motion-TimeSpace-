$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$workerId=24080
$label='annular-C0-integral-MTS-attempt02'
$folder=[IO.Path]::GetFullPath((Join-Path $root ('source-intake/navier-stokes/20260914/'+$label)))
if(-not $folder.StartsWith($root+[IO.Path]::DirectorySeparatorChar)){throw 'Out of scope'}
$path=Join-Path $folder 'status.json'
$raw=[IO.File]::ReadAllText($path)
$status=$raw|ConvertFrom-Json -AsHashtable
if($status.state -ne 'running' -or $status.progress.stage -notlike 'fine:C0-native-events:*'){throw 'Not at native event stage'}
if(@($status.rule_outputs|Where-Object {$_.level -eq 'fine' -and $_.component -eq 'native-and-dust' -and $_.order -eq 64}).Count -ne 1){throw 'Matter64 not saved'}
if(@($status.checks|Where-Object {-not $_.passed}).Count){throw 'Failed scientific checks'}
$process=Get-CimInstance Win32_Process -Filter "ProcessId = $workerId"
if(-not $process -or $process.Name -ne 'python.exe' -or $process.CommandLine -notlike '*scripts/integrate_annular_C0_v2_20260930.py*' -or $process.CommandLine -notlike "*--label $label *"){throw 'Wrong process'}
$created=$process.CreationDate.ToUniversalTime()
if($created -lt ([datetime]'2026-09-30T14:49:35Z').ToUniversalTime() -or $created -gt ([datetime]'2026-09-30T14:49:50Z').ToUniversalTime()){throw 'Creation time mismatch'}
foreach($relative in $status.outputs.Keys){
 $outputPath=[IO.Path]::GetFullPath((Join-Path $root $relative))
 if(-not $outputPath.StartsWith($root+[IO.Path]::DirectorySeparatorChar)){throw 'Out-of-scope output'}
 if((Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $status.outputs[$relative]){throw 'Changed output'}
}
$snapshot=Join-Path $folder 'status-running-before-native-event-restructure.json'
if(Test-Path -LiteralPath $snapshot){throw 'Snapshot exists'}
[IO.File]::WriteAllText($snapshot,$raw,[Text.UTF8Encoding]::new($false))
$owned=Get-Process -Id $workerId
Stop-Process -Id $workerId -Force
if(-not $owned.WaitForExit(10000)){throw 'Process still running'}
$status.state='failed'
$status.external_safe_boundary_stop=$true
$status.numerical_failure=$false
$status.error='External bounded-work restructure: saved wave24/32 and matter48/64 retained; partial unsaved native-event accumulator discarded, not evidence. Replace repeated kernel rebuilds with validated coefficient interpolation.'
$status.unsaved_native_event_partial_discarded=$true
$status.stopped_at=[datetime]::UtcNow.ToString('o')
$status.stopped_worker=@{pid=$workerId;created_utc=$created.ToString('o');command_line=$process.CommandLine}
$relative=[IO.Path]::GetRelativePath($root,$snapshot)
$status.outputs[$relative]=(Get-FileHash -LiteralPath $snapshot -Algorithm SHA256).Hash.ToLowerInvariant()
$relative=[IO.Path]::GetRelativePath($root,$PSCommandPath)
$status.inputs[$relative]=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText($path,($status|ConvertTo-Json -Depth 100)+"`n",[Text.UTF8Encoding]::new($false))
Write-Output ('Stopped only owned MTS worker at saved matter boundary; unsaved event partial explicitly discarded at '+[datetime]::UtcNow.ToString('o'))

