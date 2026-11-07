$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path){Get-Content -LiteralPath $path -Raw|ConvertFrom-Json}
if(Test-Path -LiteralPath "$root/closeout.json"){throw 'Existing closeout; inspect'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-coupled-energy-envelope-20261107/closeout.json'
if((Hash $parent) -ne 'a7d059d619106fe290c941a1bdcab9691ce9156bdaf502f71bb4b479bf438a29'){throw 'Parent seal'}
foreach($artifact in (ReadJson $parent).artifacts){
 if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent changed: $($artifact.path)"}
}
$summary=ReadJson "$root/summary/summary.json"
$validation=ReadJson "$root/summary/validation.json"
if(-not $summary.passed -or -not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'Aggregate failed'}
foreach($source in $summary.evidence_hashes.PSObject.Properties){
 if((Hash $source.Name) -ne $source.Value){throw "Aggregate evidence changed: $($source.Name)"}
}
$restChecks=0
$restEvidence=@()
foreach($family in 'half','balanced','double'){
 foreach($kind in 'result.json','rest-result.json'){
  $result=ReadJson "$root/$family/$kind"
  if(-not $result.passed){throw "Failed result: $family/$kind"}
  foreach($report in $result.reports){
   if(-not $report.passed){throw 'Failed model'}
   foreach($errorValue in $report.errors.PSObject.Properties){if($errorValue.Value -ge 0.00002){throw 'Numerical tolerance'}}
   if($kind -eq 'rest-result.json'){
    if(@($report.checks|Where-Object {-not $_.passed}).Count){throw 'Rest inequality'}
    $restChecks+=$report.checks.Count
   }else{
    foreach($errorValue in $report.algebra.PSObject.Properties){if($errorValue.Value -ge 0.0000000001){throw 'Algebra tolerance'}}
   }
  }
  $restEvidence+=[ordered]@{path="$root/$family/$kind";sha256=(Hash "$root/$family/$kind")}
 }
 foreach($manifest in Get-ChildItem -LiteralPath "$root/$family" -File -Filter '*inputs.json'){
  $inputRecord=ReadJson $manifest.FullName
  foreach($source in $inputRecord.sources.PSObject.Properties){
   if((Hash $source.Name) -ne $source.Value){throw "Frozen source changed: $($source.Name)"}
  }
 }
}
if($restChecks -ne 441){throw 'Incomplete additional comparisons'}
$csv=@(Import-Csv -LiteralPath "$root/summary/couplings.csv")
if($csv.Count -ne 6 -or @($csv|Where-Object {-not $_.family -or -not $_.model -or -not $_.k}).Count){throw 'CSV shape'}
foreach($source in @('../mts-independent-poisson-evolution-20261107/poisson_driver.py','../mts-derived-wavelength-test-20261107/build-full-momentum/camb_python.f90','../condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/equations.f90','../mts-coupled-energy-envelope-20261107/physical_energy_map.py','../mts-newton-wavelength-bounds-20261107/primitive_math.py')){
 if(-not(Test-Path -LiteralPath (Join-Path $root $source) -PathType Leaf)){throw "Cited source missing: $source"}
}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($file in Get-ChildItem -LiteralPath $root -Recurse -File -Filter '*.start.json'){
 $start=ReadJson $file.FullName
 $end=ReadJson ($file.FullName -replace '\.start\.json$','.end.json')
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command -or $end.exit_code -ne 0){throw "Receipt identity: $($file.FullName)"}
 if((Hash $start.source_path) -ne $start.source_sha256){throw "Launched source changed: $($file.FullName)"}
 $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
 if($same.Count){throw "Worker remains: $($file.FullName)"}
 $receipts+=[ordered]@{phase=[IO.Path]::GetRelativePath($root,$file.FullName);pid=$start.pid;created=$start.created;command=$start.command;finished=$end.finished;exit_code=$end.exit_code;same_process_still_present=$false}
}
if($receipts.Count -ne 7){throw 'Missing phase receipts'}
$active=@($running|Where-Object {$_.ProcessId -ne $PID -and $_.Name -in @('python.exe','pwsh.exe','powershell.exe') -and $_.CommandLine -like '*mts-metric-channel-factorization-20261107*'})
if($active.Count){$active|Select-Object ProcessId,CreationDate,CommandLine|ConvertTo-Json;throw 'Task-owned worker or supervisor remains'}
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
 parent_seal=(Hash $parent)
 new_physical_ode_solves=0
 primary_aggregate_checks=$validation.count
 additional_rest_checks=$restChecks
 primary_off_node_locations=582
 additional_off_node_locations=294
 derived_result='Explicit rank-two metric-mediated scalar/rest feedback; physical stress/current dictionary including enthalpy defect; explicit rest growth bound and conditional balanced uniform response estimate'
 derived_regime='Bounded physical background/pressure/weight quantities and kappa_Omega=H*sqrt(k^2+(am)^2)/k^2; see DERIVATION.md'
 sampled_qualification_not_continuum_certificate=$true
 previous_observable_errors_and_budgets_unchanged=$true
 uniform_small_observable_error_proved=$false
 additional_evidence=$restEvidence
 cleanup=[ordered]@{workers=$receipts;live_stage_worker_or_supervisor_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$record|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$root/closeout.json" -Encoding utf8
Write-Output ("verified "+$artifacts.Count+" artifacts; all"+$receipts.Count+" workers exited")
Write-Output ("closeout SHA256 "+(Hash "$root/closeout.json"))
