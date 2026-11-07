$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path){Get-Content -LiteralPath $path -Raw|ConvertFrom-Json}
if(Test-Path -LiteralPath "$root/closeout.json"){throw 'Existing closeout; inspect'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-species-stress-suppression-20261107/closeout.json'
if((Hash $parent) -ne '7ac046615b99c5d3f86bd2431cf11bd70d63cc31bec6b1ce31585cf352c39999'){throw 'Parent seal'}
foreach($artifact in (ReadJson $parent).artifacts){if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent changed: $($artifact.path)"}}
$summary=ReadJson "$root/summary/summary.json"
$validation=ReadJson "$root/summary/validation.json"
if(-not $summary.passed -or -not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'Aggregate failed'}
if($summary.locations -ne 582 -or $summary.native_branch_evaluations -ne 3492 -or $summary.distinct_coefficient_cases -ne 240){throw 'Coverage'}
foreach($source in $summary.evidence_hashes.PSObject.Properties){if((Hash $source.Name) -ne $source.Value){throw "Evidence changed: $($source.Name)"}}
foreach($family in 'half','balanced','double'){
 $report=ReadJson "$root/$family/result.json"
 if(-not $report.passed){throw 'Incomplete family'}
 foreach($source in (ReadJson "$root/$family/inputs.json").sources.PSObject.Properties){if((Hash $source.Name) -ne $source.Value){throw "Frozen source changed: $($source.Name)"}}
 foreach($case in $report.reports){
  if(-not $case.passed -or $case.rows.Count -ne 97){throw 'Missing native case'}
  foreach($error in $case.errors.PSObject.Properties){if($error.Value -ge 0.00002){throw 'Numerical gate'}}
  foreach($error in $case.algebra.PSObject.Properties){if($error.Value -ge 0.0000000001){throw 'Algebra gate'}}
  if((Hash $case.coefficient_input.path) -ne $case.coefficient_input.sha256){throw 'Input changed'}
 }
}
$rows=@(Import-Csv -LiteralPath "$root/summary/comparisons.csv")
if($rows.Count -ne 6 -or @($rows|Where-Object {-not $_.family -or -not $_.model -or $_.continuous_supremum_certified -ne 'False'}).Count){throw 'CSV scope'}
foreach($source in @('../mts-independent-poisson-evolution-20261107/poisson_driver.py','../mts-derived-wavelength-test-20261107/build-full-momentum/camb_python.f90','../condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/equations.f90','../mts-coupled-energy-envelope-20261107/physical_energy_map.py','../mts-metric-channel-factorization-20261107/metric_channels.py','../mts-metric-channel-factorization-20261107/DERIVATION.md','../mts-explicit-current-shear-forcing-20261107/forcing_math.py','../mts-explicit-current-shear-forcing-20261107/DERIVATION.md','../mts-species-stress-suppression-20261107/DERIVATION.md','../mts-species-stress-suppression-20261107/PRECONDITIONS.md')){
 if(-not(Test-Path -LiteralPath (Join-Path $root $source) -PathType Leaf)){throw "Cited source missing: $source"}
}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($file in Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.start.json'){
 $start=ReadJson $file.FullName
 $end=ReadJson ($file.FullName -replace '\.start\.json$','.end.json')
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command -or $end.exit_code -ne 0){throw "Receipt identity or failure: $($file.FullName)"}
 if((Hash $start.source_path) -ne $start.source_sha256){throw 'Launched source changed'}
 $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
 if($same.Count){throw 'Task worker still running'}
 $receipts+=[ordered]@{phase=([IO.Path]::GetRelativePath($root,$file.FullName));pid=$start.pid;created=$start.created;command=$start.command;finished=$end.finished;exit_code=$end.exit_code;same_process_still_present=$false}
}
if($receipts.Count -ne 4){throw 'Missing worker receipt'}
$active=@($running|Where-Object {$_.ProcessId -ne $PID -and $_.Name -in @('python.exe','pwsh.exe','powershell.exe') -and $_.CommandLine -like '*mts-cold-adapted-metric-gain-20261107*'})
if($active.Count){$active|Select-Object ProcessId,CreationDate,CommandLine|ConvertTo-Json;throw 'Task-owned supervisor remains'}
$coverage='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102/final-stable-real-batch-rays037-038/common-coverage.json'
if((Hash $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering changed'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected bytecode cache'}
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|Sort-Object FullName|ForEach-Object{[ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Hash $_.FullName)}})
$record=[ordered]@{
 state='verified_closed'
 completed_utc=[DateTimeOffset]::UtcNow.ToString('o')
 all_numerical_checks_passed=$true
 parent_seal=(Hash $parent)
 new_physical_ode_solves=0
 aggregate_checks=$validation.count
 off_node_locations=582
 native_branch_evaluations=3492
 distinct_algebra_coefficient_cases=240
 derived_result='Composite cold-adapted norm; physical current and GR metric channels; explicit GR-reference and Poisson gains; conditional observable convergence with no minimum-speed assumption'
 scope='Retained minimal constant-mass linear equations and explicit regime/preparation conditions; weighted observable limit, not raw-multipole equivalence at zero speed; sampled qualifications are not continuum supremum certificates'
 previous_tighter_error_estimates_preserved=$true
 cleanup=[ordered]@{workers=$receipts;live_stage_worker_or_supervisor_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$record|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$root/closeout.json" -Encoding utf8
Write-Output ("verified "+$artifacts.Count+" artifacts; all"+$receipts.Count+" workers exited")
Write-Output ("closeout SHA256 "+(Hash "$root/closeout.json"))
