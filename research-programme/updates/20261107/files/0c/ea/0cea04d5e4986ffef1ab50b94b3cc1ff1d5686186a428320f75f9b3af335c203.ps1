$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path) {
 if(-not (Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing evidence: $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path) {
 Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
}
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'Existing closeout; inspect rather than overwrite'}
$summary=ReadJson "$root/summary/comparison-summary.json"
$validation=ReadJson "$root/summary/validation.json"
if(-not $summary.passed -or -not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'Unqualified aggregate'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-metric-time-primitive-20261107/closeout.json'
if((Hash $parent) -ne '287e3bc01d13d195e70137e417bc8aa5906506145ccc85e982a008bb07cf99a5'){throw 'Parent seal changed'}
foreach($artifact in (ReadJson $parent).artifacts){
 if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent artifact changed: $($artifact.path)"}
}
foreach($source in (ReadJson "$root/source-provenance.json")){
 if((Hash $source.path) -ne $source.sha256 -or (Hash $source.owner) -ne $source.owner_sha256){throw 'Retained algorithm source or owner changed'}
}
foreach($entry in $summary.evidence_hashes.PSObject.Properties){
 if((Hash $entry.Name) -ne $entry.Value){throw "Aggregate evidence changed: $($entry.Name)"}
}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
$required=@('syntax-01','preflight-01','evolution-v2-01','evolution-validation-01','build-01','adjoint-01','adjoint-validation-01','primitive-01','primitive-validation-01','volume-01')
foreach($family in @('half','double','summary')){
 $phases=if($family -eq 'summary'){@('summary-01')}else{$required}
 if($family -eq 'half'){$phases+=@('evolution-01')}
 $starts=@(Get-ChildItem -LiteralPath "$root/$family" -File -Filter '*.start.json')
 if($starts.Count -ne $phases.Count){throw "Unexpected launch count: $family"}
 foreach($phase in $phases){
  $start=ReadJson "$root/$family/$phase.start.json"
  $end=ReadJson "$root/$family/$phase.end.json"
  if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw "Process identity receipt: $family/$phase"}
  if((Hash $start.source_path) -ne $start.source_sha256){throw "Launched source changed: $family/$phase"}
  $expected=if($family -eq 'half' -and $phase -eq 'evolution-01'){1}else{0}
  if($end.exit_code -ne $expected){throw "Unexpected exit: $family/$phase"}
  if($expected -eq 1 -and (Get-Content -LiteralPath "$root/half/evolution-01.stderr.log" -Raw) -notmatch "NameError: name 'np' is not defined"){throw 'Inspected setup failure no longer matches'}
  $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
  if($same.Count){throw "Task process still present: $family/$phase"}
  $receipts+=[ordered]@{family=$family;phase=$phase;pid=$start.pid;created=$start.created;command=$start.command;source_sha256=$start.source_sha256;exit_code=$end.exit_code;finished=$end.finished;same_process_still_present=$false}
 }
}
$workerMatches=@($running|Where-Object {$_.Name -eq 'python.exe' -and $_.CommandLine -like '*mts-newton-wavelength-bounds-20261107*'})
if($workerMatches.Count){throw 'Stage worker still active'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering coverage changed'}
foreach($family in @('half','double')){
 foreach($manifest in @('preflight-v2/frozen-inputs.json','evolution-v2-inputs.json','frozen-inputs.json','response-v2/adjoint-inputs.json','primitive/frozen-inputs.json')){
  if(-not (ReadJson "$root/$family/$manifest").sources){throw "Missing frozen-source map: $family/$manifest"}
  foreach($source in (ReadJson "$root/$family/$manifest").sources.PSObject.Properties){
   if((Hash $source.Name) -ne $source.Value){throw "Frozen source changed: $($source.Name)"}
  }
 }
 $volume=ReadJson "$root/$family/volume/volume-inputs.json"
 if((Hash $volume.source) -ne $volume.sha256){throw "Volume source changed: $family"}
}
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File | Sort-Object FullName | ForEach-Object {
 [ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Hash $_.FullName)}
})
$closeout=[ordered]@{
 state='verified_closed'
 completed_utc=[DateTimeOffset]::UtcNow.ToString('o')
 all_numerical_checks_passed=$true
 parent_seal=(Hash $parent)
 scope='Two additional retained k values; independent GR and truncation controls, terminal adjoints, exact metric-time primitive, density-volume dictionary'
 new_forward_solves=12
 new_backward_solves=16
 balanced_control_reused=$true
 failed_setup_preserved='half/evolution-01: missing explicit NumPy import, before any ODE; repaired in evolve_v2.py'
 immutable_bank_grids_tolerances=$true
 no_fits=$true
 no_new_physical_parameters=$true
 no_continuum_or_uniform_limit_certificate=$true
 aggregate_checks=$validation.count
 cleanup=[ordered]@{workers=$receipts;live_stage_python_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering_coverage=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$closeout|ConvertTo-Json -Depth 12|Set-Content -LiteralPath $destination -Encoding utf8
Write-Output ("verified closeout: "+$artifacts.Count+" artifacts; "+$receipts.Count+" exited worker receipts")
Write-Output ("closeout SHA256: "+(Hash $destination))

