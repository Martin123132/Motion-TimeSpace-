$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$post=Split-Path -Parent $stage
$destination=Join-Path $stage 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$stage/response-v2/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 416 -or @($validation.checks|Where-Object {-not $_.passed}).Count){throw 'validation'}
$parent=Join-Path $post 'mts-independent-poisson-evolution-20261107/closeout.json'
if((Hash-Path $parent) -ne 'ef83002ed38f0b3b940067968e41ac9bdb971a7c211fa51304677f47feb89ef9'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
foreach($manifest in 'frozen-inputs.json','adjoint-inputs.json','response-v2/adjoint-inputs.json'){
 $frozen=Get-Content -Raw -LiteralPath "$stage/$manifest"|ConvertFrom-Json
 foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
$build=Get-Content -Raw -LiteralPath "$stage/build-result.json"|ConvertFrom-Json
foreach($model in $build.reports){
 if(-not $model.passed -or (Hash-Path $model.packet) -ne $model.sha256){throw 'coefficient evidence'}
 foreach($chunk in $model.chunks){if((Hash-Path $chunk.path) -ne $chunk.sha256){throw 'coefficient chunk'}}
}
$result=Get-Content -Raw -LiteralPath "$stage/response-v2/adjoint-result.json"|ConvertFrom-Json
if(-not $result.passed){throw 'adjoint evidence'}
$newSolves=0
$reused=0
foreach($model in $result.reports){foreach($branch in $model.reports){
 if(-not $branch.passed){throw 'branch failed'}
 foreach($case in $branch.cases){
  if(-not $case.status.success -or (Hash-Path $case.packet) -ne $case.sha256){throw 'adjoint packet'}
  if($case.status.reused_existing_solution){$reused++}else{$newSolves++}
 }
}}
if($newSolves -ne 6 -or $reused -ne 2){throw 'solve accounting'}
$failed=Get-Content -Raw -LiteralPath "$stage/adjoints/heavy-poisson-spatial-result.json"|ConvertFrom-Json
if($failed.passed -or $failed.refinement.quadrature_budget -lt 2e-5){throw 'original failure not preserved'}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
$scripts=@{'build-01'='build.py';'adjoint-01'='adjoint.py';'adjoint-v2-01'='adjoint_v2.py';'validation-01'='validate_v2.py'}
foreach($label in 'build-01','adjoint-01','adjoint-v2-01','validation-01'){
 $start=Get-Content -Raw -LiteralPath "$stage/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$stage/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 if((Hash-Path (Join-Path $stage $scripts[$label])) -ne $end.source_sha256){throw 'changed worker code'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
 if($same){throw "task worker remains $($end.pid)"}
 if($label -eq 'adjoint-01'){
  if($end.exit_code -ne 1 -or (Get-Content -Raw -LiteralPath "$stage/$label.stderr.log") -notmatch 'inspect adjoint/budget discrepancy'){throw 'unexpected first failure'}
 }elseif($end.exit_code -ne 0){throw 'failed worker'}
 $receipts+=@{label=$label;receipt=$end;same_process_running=$same;inspected_quadrature_failure=($label -eq 'adjoint-01')}
}
$absoluteRoot=[IO.Path]::GetFullPath($stage)
$unreceipted=@($processes|Where-Object {$_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot)})
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $stage -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-NEWTON-FEEDBACK-ADJOINT.md'
$artifacts=@(Get-ChildItem -LiteralPath $stage -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$stage/response-v2/validation.json")
 response_sha256=(Hash-Path "$stage/response-v2/adjoint-result.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 validation_checks=416;backward_integrations_total=8;reused_after_repair=2;new_after_repair=6
 remaining_task_workers=0;worker_receipts=$receipts;failed_attempts=1
 inspected_failure='power-basis triangle budget partition dependence; unchanged-gate Bernstein repair; two finished adjoints reused without rerun'
 all_numerical_checks_passed=$true;balanced_only=$true
 feedback_closed_without_unknown_DeltaD=$true;terminal_reference_conditioned_scope=$true
 new_parameters_fitted=$false;rigorous_continuum_certificate=$false;uniform_limit_theorem_claimed=$false
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Derive a phase-aware bound for the oscillatory Poisson-spatial metric-time response using the retained coupled phase law, including the adjoint phase in the full derivative. Preserve actual cancellation without fitting or assuming slow variation; freeze that remainder before the two other saved wavenumber tests with matched cold controls.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;validation_checks=416;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

