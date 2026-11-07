$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$post=Split-Path -Parent $stage
$destination=Join-Path $stage 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$stage/summary/validation.json"|ConvertFrom-Json
if(-not $validation.passed){throw 'validation'}
foreach($entry in $validation.evidence_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed result $($entry.Name)"}}
$parent=Join-Path $post 'mts-coupled-phase-corrector-20261107/closeout.json'
if((Hash-Path $parent) -ne '93ce2cd7595bbf6b575964b6a4d7dd59b67e8a63915741b4c92ea11fa2551a95'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($family in 'half','double','summary'){
 $root=Join-Path $stage $family
 $labels=@('assemble-01','channel-01','evolution-01')
 if($family -eq 'summary'){$labels=@('validation-01')}
 else{
  foreach($manifest in 'frozen-inputs.json','channel-inputs.json','evolution-inputs.json'){
   $frozen=Get-Content -Raw -LiteralPath "$root/$manifest"|ConvertFrom-Json
   foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
  }
  $result=Get-Content -Raw -LiteralPath "$root/evolution-result.json"|ConvertFrom-Json
  foreach($model in $result.reports){foreach($row in $model.rows){if(-not $row.status.success -or (Hash-Path $row.packet) -ne $row.sha256){throw 'forward evidence'}}}
 }
 foreach($label in $labels){
  $start=Get-Content -Raw -LiteralPath "$root/$label.start.json"|ConvertFrom-Json
  $end=Get-Content -Raw -LiteralPath "$root/$label.end.json"|ConvertFrom-Json
  if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command -or $end.family -ne $family){throw 'identity receipt'}
  if((Hash-Path $end.source_path) -ne $end.source_sha256){throw 'changed worker code'}
  $current=@($processes|Where-Object ProcessId -eq $end.pid)
  $same=$false
  if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
  if($same){throw "task worker remains $($end.pid)"}
  if($end.exit_code -ne 0){throw 'failed worker'}
  $receipts+=@{family=$family;label=$label;receipt=$end;same_process_running=$same}
 }
}
$absoluteRoot=[IO.Path]::GetFullPath($stage)
$unreceipted=@($processes|Where-Object {$_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot)})
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $stage -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-COUPLED-WAVELENGTH-CONTROLS.md'
$artifacts=@(Get-ChildItem -LiteralPath $stage -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$stage/summary/validation.json")
 comparison_sha256=(Hash-Path "$stage/summary/comparison-summary.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 validation_checks=$validation.count;new_evolutions=10;new_prospective_families=4
 remaining_task_workers=0;worker_receipts=$receipts;failed_attempts=0;no_numerical_retry=$true
 all_three_wavelengths_qualified=$validation.both_new_wavelengths_qualified
 actual_native_regimes_tested=@('half massless full hierarchy','balanced/double native high-k-tau branch')
 new_parameters_fitted=$false;original_mean_failure_preserved=$true;uniform_limit_theorem_claimed=$false
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Derive a genuinely independent Newtonian weak-field/slow-motion system from the retained action and fixed source normalization, retaining and bounding the pressure, shear, expansion and phase terms discarded in that limit. Establish the valid comparison regime and use matched baseline/MTS controls; do not relabel a GR trajectory or refit a coupling to force agreement.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;all_three_wavelengths_qualified=$validation.both_new_wavelengths_qualified;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

