$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path){Get-Content -LiteralPath $path -Raw|ConvertFrom-Json}
if(Test-Path -LiteralPath "$root/closeout.json"){throw 'Existing closeout; inspect'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-newton-source-gain-20261107/closeout.json'
if((Hash $parent) -ne '69818d1fedf624d443ee985f9776f5472de8902cde7d4ca5a9c57a8ab3d34687'){throw 'Parent seal'}
foreach($artifact in (ReadJson $parent).artifacts){
 if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent changed: $($artifact.path)"}
}
$summary=ReadJson "$root/summary/summary.json"
$validation=ReadJson "$root/summary/validation.json"
if(-not $summary.passed -or -not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'Aggregate failure'}
foreach($source in $summary.evidence_hashes.PSObject.Properties){
 if((Hash $source.Name) -ne $source.Value){throw "Aggregate evidence changed: $($source.Name)"}
}
foreach($family in 'half','balanced','double'){
 $bound=ReadJson "$root/$family/bound/result.json"
 $verified=ReadJson "$root/$family/bound/validation.json"
 if(-not $bound.passed -or -not $verified.passed -or @($verified.checks|Where-Object {-not $_.passed}).Count){throw "Family failure: $family"}
 foreach($report in $bound.reports){
  if((Hash $report.packet) -ne $report.sha256){throw 'Envelope changed'}
  foreach($chunk in $report.chunks){
   if((Hash $chunk.path) -ne $chunk.sha256){throw 'Transformed node chunk changed'}
  }
 }
 foreach($manifest in Get-ChildItem -LiteralPath "$root/$family" -Recurse -File -Filter '*inputs.json'){
  $inputRecord=ReadJson $manifest.FullName
  foreach($source in $inputRecord.sources.PSObject.Properties){
   if((Hash $source.Name) -ne $source.Value){throw "Frozen source changed: $($source.Name)"}
  }
 }
}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
$expectedFailureCount=0
foreach($file in Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.start.json'){
 $start=ReadJson $file.FullName
 $endPath=$file.FullName -replace '\.start\.json$','.end.json'
 $end=ReadJson $endPath
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw "Receipt identity: $($file.FullName)"}
 if((Hash $start.source_path) -ne $start.source_sha256){throw "Launched source changed: $($file.FullName)"}
 $relative=[IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/')
 $expectedFailure=($relative -eq 'balanced/probe-01.start.json')
 if($expectedFailure){
  if($end.exit_code -ne 1 -or -not((Get-Content -LiteralPath "$root/balanced/probe-01.stderr.log" -Raw).Contains('FileNotFoundError'))){throw 'Historical failure receipt'}
  $expectedFailureCount++
 }elseif($end.exit_code -ne 0){throw "Unresolved phase failure: $relative"}
 $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
 if($same.Count){throw "Worker still present: $relative"}
 $receipts+=[ordered]@{phase=$relative;pid=$start.pid;created=$start.created;command=$start.command;finished=$end.finished;exit_code=$end.exit_code;historical_setup_failure=$expectedFailure;same_process_still_present=$false}
}
if($expectedFailureCount -ne 1){throw 'Historical failed attempt missing'}
$active=@($running|Where-Object {$_.ProcessId -ne $PID -and $_.Name -in @('python.exe','pwsh.exe','powershell.exe') -and $_.CommandLine -like '*mts-coupled-energy-envelope-20261107*'})
if($active.Count){$active|Select-Object ProcessId,CreationDate,CommandLine|ConvertTo-Json;throw 'Task-owned worker or supervisor still present'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering changed'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected bytecode cache'}
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|Sort-Object FullName|ForEach-Object{
 [ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Hash $_.FullName)}
})
$record=[ordered]@{
 state='verified_closed'
 completed_utc=[DateTimeOffset]::UtcNow.ToString('o')
 all_numerical_checks_passed=$true
 historical_failed_setup_preserved=$true
 parent_seal=(Hash $parent)
 new_physical_ode_solves=0
 independent_checks=$summary.independent_check_count
 aggregate_checks=$validation.count
 derived_result='Positive physical-weighted comparison norm and closed two-way heavy/rest feedback bound, including physical forcing and primitive boundaries'
 scope=$summary.scope
 tighter_prior_error_estimates_preserved=$true
 native_continuum_certificate=$false
 uniform_parameter_limit_proved=$false
 cleanup=[ordered]@{workers=$receipts;live_stage_worker_or_supervisor_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$record|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$root/closeout.json" -Encoding utf8
Write-Output ("verified "+$artifacts.Count+" artifacts; all"+$receipts.Count+" workers exited; one historical setup failure preserved")
Write-Output ("closeout SHA256 "+(Hash "$root/closeout.json"))
