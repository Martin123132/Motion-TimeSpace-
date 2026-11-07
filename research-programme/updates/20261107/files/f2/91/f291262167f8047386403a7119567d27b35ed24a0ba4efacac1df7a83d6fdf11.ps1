$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$post=Split-Path -Parent $stage
$destination=Join-Path $stage 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$stage/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or @($validation.checks|Where-Object {-not $_.passed}).Count -or $validation.count -ne 334){throw 'validation'}
$parent=Join-Path $post 'mts-coupled-wavelength-controls-20261107/closeout.json'
if((Hash-Path $parent) -ne 'c83781ddf4078655f6c7b20dd9c12b5546a8abb2f0d1b392de97c614cd502da2'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
foreach($manifest in 'frozen-inputs.json','preflight-v2/frozen-inputs.json','evolution-inputs.json'){
 $frozen=Get-Content -Raw -LiteralPath "$stage/$manifest"|ConvertFrom-Json
 foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
$result=Get-Content -Raw -LiteralPath "$stage/evolution-result.json"|ConvertFrom-Json
if(-not $result.passed){throw 'evolution'}
foreach($model in $result.reports){
 foreach($row in $model.rows){
  if(-not $row.status.success -or -not $row.numerical_passed -or (Hash-Path $row.packet) -ne $row.sha256){throw 'forward evidence'}
 }
}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
$scripts=@{'preflight-01'='preflight.py';'preflight-v2-01'='preflight_v2.py';'evolution-01'='evolve.py';'validation-01'='validate.py'}
foreach($label in 'preflight-01','preflight-v2-01','evolution-01','validation-01'){
 $start=Get-Content -Raw -LiteralPath "$stage/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$stage/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 if((Hash-Path (Join-Path $stage $scripts[$label])) -ne $end.source_sha256){throw 'changed worker code'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
 if($same){throw "task worker remains $($end.pid)"}
 if($label -eq 'preflight-01'){
  if($end.exit_code -ne 1 -or (Get-Content -Raw -LiteralPath "$stage/$label.stderr.log") -notmatch "TypeError: bad operand type for abs"){throw 'unexpected first failure'}
 }elseif($end.exit_code -ne 0){throw 'failed worker'}
 $receipts+=@{label=$label;receipt=$end;same_process_running=$same;inspected_reporting_failure=($label -eq 'preflight-01')}
}
$absoluteRoot=[IO.Path]::GetFullPath($stage)
$unreceipted=@($processes|Where-Object {$_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot)})
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $stage -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-INDEPENDENT-POISSON-EVOLUTION.md'
$artifacts=@(Get-ChildItem -LiteralPath $stage -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$stage/validation.json")
 evolution_sha256=(Hash-Path "$stage/evolution-result.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 validation_checks=334;new_evolutions=6;balanced_only=$true;all_numerical_checks_passed=$true
 remaining_task_workers=0;worker_receipts=$receipts;failed_attempts=1
 inspected_failure='list normalization TypeError, original outputs retained; separate preflight-v2 repairs reporting only'
 physical_truncation_is_not_numerical_error=$true;no_future_perturbation_forcing=$true
 gravity_normalization='inherited calibrated Einstein action, no numerical G derivation'
 newton_scope='self-consistent dust-force truncation with live relativistic species; spatial driver is not a physical lensing metric'
 new_parameters_fitted=$false;uniform_limit_theorem_claimed=$false
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Close the finite-time density-feedback remainder from the retained coupled matter operator, retaining phase and metric-time contributions. Use the saved six histories first, then freeze and test the same derived law at the other two saved wavenumbers with matched cold controls and fixed parameters/tolerances.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;validation_checks=334;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

