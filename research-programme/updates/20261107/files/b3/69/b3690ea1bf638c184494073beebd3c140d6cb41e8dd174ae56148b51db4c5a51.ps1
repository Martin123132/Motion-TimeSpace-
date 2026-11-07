$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$post=Split-Path -Parent $stage
$destination=Join-Path $stage 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$stage/validation.json"|ConvertFrom-Json
$volume=Get-Content -Raw -LiteralPath "$stage/volume-result.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 275 -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'primary validation'}
if(-not $volume.passed -or $volume.count -ne 24 -or @($volume.checks|Where-Object {-not $_.passed}).Count){throw 'volume validation'}
$parent=Join-Path $post 'mts-newton-feedback-adjoint-20261107/closeout.json'
if((Hash-Path $parent) -ne '2843c90481aa70251f9f8caeedbba2e5cc9d8088619952afee1be56a55548d9a'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$frozen=Get-Content -Raw -LiteralPath "$stage/frozen-inputs.json"|ConvertFrom-Json
foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
$volumeInputs=Get-Content -Raw -LiteralPath "$stage/volume-inputs.json"|ConvertFrom-Json
if((Hash-Path $volumeInputs.source) -ne $volumeInputs.sha256){throw 'volume source'}
$result=Get-Content -Raw -LiteralPath "$stage/primitive-result.json"|ConvertFrom-Json
if(-not $result.passed -or $result.new_ode_solves -ne 0){throw 'primitive evidence'}
$reused=0
foreach($model in $result.reports){foreach($branch in $model.branches){
 if(-not $branch.passed){throw 'branch failed'}
 foreach($case in $branch.cases){
  if((Hash-Path $case.packet) -ne $case.sha256 -or (Hash-Path $case.original_adjoint) -ne $case.original_adjoint_sha256){throw 'response packet'}
  $reused++
 }
}}
if($reused -ne 8){throw 'reuse accounting'}
foreach($row in $volume.summaries){
 if((Hash-Path $row.packet) -ne $row.sha256 -or (Hash-Path $row.source) -ne $row.source_sha256){throw 'volume packet'}
}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
$scripts=@{'primitive-01'='primitive.py';'validation-01'='validate.py';'volume-01'='volume_dictionary.py'}
foreach($label in 'primitive-01','validation-01','volume-01'){
 $start=Get-Content -Raw -LiteralPath "$stage/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$stage/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 if((Hash-Path (Join-Path $stage $scripts[$label])) -ne $end.source_sha256){throw 'changed worker code'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
 if($same){throw "task worker remains $($end.pid)"}
 if($end.exit_code -ne 0){throw 'failed worker'}
 $receipts+=@{label=$label;receipt=$end;same_process_running=$same}
}
$absoluteRoot=[IO.Path]::GetFullPath($stage)
$unreceipted=@($processes|Where-Object {$_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot)})
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $stage -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-METRIC-TIME-PRIMITIVE.md'
$artifacts=@(Get-ChildItem -LiteralPath $stage -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$stage/validation.json")
 volume_sha256=(Hash-Path "$stage/volume-result.json");response_sha256=(Hash-Path "$stage/primitive-result.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 primary_validation_checks=275;volume_validation_checks=24;validation_checks=299;new_ode_solves=0;reused_adjoint_traces=8
 remaining_task_workers=0;worker_receipts=$receipts;failed_numerical_attempts=0
 launcher_correction='stale allowlist stopped before Python launch; corrected before first numerical run'
 all_numerical_checks_passed=$true;balanced_only=$true
 physical_primitive_from_constraint=$true;slow_adjoint_assumed=$false;full_phase_derivative_kept=$true
 physical_density_volume_dictionary_checked=$true;dust_subcase_not_assumed_for_live_mixture=$true
 worsened_dust_bounds_preserved=$true;predeclared_minimum_of_valid_bounds=$true
 new_parameters_fitted=$false;rigorous_continuum_certificate=$false;uniform_limit_theorem_claimed=$false
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Freeze the exact metric-time primitive/full derivative and physical-density dictionary; test them at the other two retained k values with actual native regimes and matched cold controls. Keep physical readouts and initial preparation unchanged. Then close uniform source/gain conditions including current, anisotropic stress and scalar phase rather than fitting or assuming a slow adjoint.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;validation_checks=299;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

