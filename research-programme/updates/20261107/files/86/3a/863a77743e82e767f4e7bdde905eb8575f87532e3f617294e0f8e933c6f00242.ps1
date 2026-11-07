$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path){Get-Content -LiteralPath $path -Raw|ConvertFrom-Json}
if(Test-Path -LiteralPath "$root/closeout.json"){throw 'Existing closeout; inspect'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-metric-channel-factorization-20261107/closeout.json'
if((Hash $parent) -ne 'a16e7c9764cebbadc43dbf729b5f8f86310aea63a5e6b83ab8afc082717f0ed0'){throw 'Parent seal'}
foreach($artifact in (ReadJson $parent).artifacts){
 if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent changed: $($artifact.path)"}
}
$summary=ReadJson "$root/summary/summary.json"
$validation=ReadJson "$root/summary/validation.json"
if(-not $summary.passed -or -not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'Aggregate failed'}
foreach($source in $summary.evidence_hashes.PSObject.Properties){
 if((Hash $source.Name) -ne $source.Value){throw "Aggregate evidence changed: $($source.Name)"}
}
foreach($family in 'half','balanced','double'){
 $qualification=ReadJson "$root/$family/qualification.json"
 $budget=ReadJson "$root/$family/budget/result.json"
 if(-not $qualification.passed -or -not $budget.passed){throw 'Incomplete family'}
 foreach($report in $qualification.reports){
  if(-not $report.passed){throw 'Failed qualification'}
  foreach($value in $report.errors.PSObject.Properties){if($value.Value -ge 0.00002){throw 'Numerical gate'}}
  foreach($value in $report.algebra.PSObject.Properties){if($value.Value -ge 0.0000000001){throw 'Algebra gate'}}
 }
 foreach($report in $budget.reports){
  if(-not $report.passed){throw 'Failed budget'}
  if((Hash $report.source_packet) -ne $report.source_sha256 -or (Hash $report.parent_interval_packet) -ne $report.parent_interval_sha256){throw 'Changed numerical packet'}
  foreach($source in $report.input_hashes.PSObject.Properties){
   if((Hash $source.Name) -ne $source.Value){throw "Input changed: $($source.Name)"}
  }
 }
 foreach($manifest in @("$root/$family/qualification-inputs.json","$root/$family/budget/inputs.json")){
  foreach($source in (ReadJson $manifest).sources.PSObject.Properties){
   if((Hash $source.Name) -ne $source.Value){throw "Frozen source changed: $($source.Name)"}
  }
 }
}
$csv=@(Import-Csv -LiteralPath "$root/summary/observable-budgets.csv")
if($csv.Count -ne 12 -or @($csv|Where-Object {-not $_.family -or -not $_.model -or -not $_.observable -or -not $_.total_percent}).Count){throw 'CSV shape'}
foreach($source in @('../mts-metric-channel-factorization-20261107/metric_channels.py','../mts-metric-channel-factorization-20261107/DERIVATION.md','../mts-coupled-energy-envelope-20261107/physical_energy_map.py','../mts-coupled-energy-envelope-20261107/comparison_math.py','../mts-newton-wavelength-bounds-20261107/primitive_math.py','../mts-independent-poisson-evolution-20261107/poisson_driver.py','../mts-metric-time-primitive-20261107/VOLUME-DICTIONARY.md','../condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/equations.f90')){
 if(-not(Test-Path -LiteralPath (Join-Path $root $source) -PathType Leaf)){throw "Cited source missing: $source"}
}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
$expectedFailures=0
foreach($file in Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.start.json'){
 $start=ReadJson $file.FullName
 $end=ReadJson ($file.FullName -replace '\.start\.json$','.end.json')
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw "Receipt identity: $($file.FullName)"}
 if((Hash $start.source_path) -ne $start.source_sha256){throw "Launched source changed: $($file.FullName)"}
 $relative=[IO.Path]::GetRelativePath($root,$file.FullName).Replace('\','/')
 $expectedFailure=($relative -eq 'summary/summary-01.start.json')
 if($expectedFailure){
  if($end.exit_code -ne 1 -or -not((Get-Content -LiteralPath "$root/summary/summary-01.stderr.log" -Raw).Contains("bad operand type for abs(): 'list'"))){throw 'Historical verifier failure'}
  $expectedFailures++
 }elseif($end.exit_code -ne 0){throw "Unresolved failed phase: $relative"}
 $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
 if($same.Count){throw "Worker remains: $relative"}
 $receipts+=[ordered]@{phase=$relative;pid=$start.pid;created=$start.created;command=$start.command;finished=$end.finished;exit_code=$end.exit_code;historical_verifier_type_error=$expectedFailure;same_process_still_present=$false}
}
if($receipts.Count -ne 8 -or $expectedFailures -ne 1){throw 'Missing phase receipts'}
$active=@($running|Where-Object {$_.ProcessId -ne $PID -and $_.Name -in @('python.exe','pwsh.exe','powershell.exe') -and $_.CommandLine -like '*mts-explicit-current-shear-forcing-20261107*'})
if($active.Count){$active|Select-Object ProcessId,CreationDate,CommandLine|ConvertTo-Json;throw 'Task-owned process remains'}
$coverage='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102/final-stable-real-batch-rays037-038/common-coverage.json'
if((Hash $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering changed'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected bytecode cache'}
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|Sort-Object FullName|ForEach-Object{
 [ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Hash $_.FullName)}
})
$record=[ordered]@{
 state='verified_closed'
 completed_utc=[DateTimeOffset]::UtcNow.ToString('o')
 all_numerical_checks_passed=$true
 historical_verifier_failure_preserved=$true
 parent_seal=(Hash $parent)
 new_physical_ode_solves=0
 aggregate_checks=$validation.count
 off_node_qualification_locations=582
 derived_result='Derivative-free physical current/shear forcing; explicit source/preparation/readout budget; conditional finite-interval linear GR-to-spatial-Poisson observable convergence criterion'
 scope='Retained constant-mass linear branch; hypotheses and all physical projection factors in DERIVATION.md; numerical budget preserves parent quintic scope with explicit representation residual'
 uniform_nonlinear_or_local_vacuum_limit_claimed=$false
 previous_tighter_error_estimates_preserved=$true
 cleanup=[ordered]@{workers=$receipts;live_stage_worker_or_supervisor_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$record|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$root/closeout.json" -Encoding utf8
Write-Output ("verified "+$artifacts.Count+" artifacts; all"+$receipts.Count+" workers exited; verifier type error preserved")
Write-Output ("closeout SHA256 "+(Hash "$root/closeout.json"))
