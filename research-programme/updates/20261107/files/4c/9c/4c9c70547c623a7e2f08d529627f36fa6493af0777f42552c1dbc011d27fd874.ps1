$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-CORRELATED-ACTION-ORDER-MEAN.md'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 710){throw 'validation'}
foreach($group in @($validation.compiled_sources,$validation.authority_sources)){
 foreach($entry in $group.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
foreach($pair in @(@('result.json','result_sha256'),@('remainder-bounds.json','bounds_sha256'),@('summary.csv','csv_sha256'))){
 if((Hash-Path "$root/$($pair[0])") -ne $validation.($pair[1])){throw "changed evidence $($pair[0])"}
}
foreach($manifest in 'frozen-inputs.json'){
 $frozen=Get-Content -Raw -LiteralPath "$root/$manifest"|ConvertFrom-Json
 foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "frozen input $($entry.Name)"}}
}
$result=Get-Content -Raw -LiteralPath "$root/result.json"|ConvertFrom-Json
if(-not $result.passed -or $result.histories.Count -ne 42 -or $result.new_trajectories -ne 0){throw 'result'}
$parent=Join-Path $post 'mts-canonical-full-time-chain-20261107/closeout.json'
if((Hash-Path $parent) -ne 'e51918b33753fbb44a6f5093af864b45c0f448f0b0f656d2b413d26a0aa4bc5a'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($label in 'mean-01','bounds-01','validation-01'){
 $start=Get-Content -Raw -LiteralPath "$root/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$root/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
 if($same){throw "task worker remains $($end.pid)"}
 if($end.exit_code -ne 0){throw 'failed worker'}
 $receipts+=@{label=$label;receipt=$end;same_process_running=$same}
}
$absoluteRoot=[IO.Path]::GetFullPath($root)
$unreceipted=@($processes|Where-Object { $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot) })
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 histories_reused=42;new_evolutions=0;paired_families=6;validation_checks=710
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$root/validation.json")
 result_sha256=(Hash-Path "$root/result.json");bounds_sha256=(Hash-Path "$root/remainder-bounds.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 remaining_task_workers=0;worker_receipts=$receipts;failed_attempts=0;no_numerical_retry=$true
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 correlated_action_mean_derived=$true;source_and_constraint_mean_coefficients_derived=$true
 mean_order=2;analytic_truncation_bound_derived=$true;phase_uniform_at_sampled_times=$true;background_probes_per_wavelength=65;continuous_time_bound_claimed=$false
 new_averaged_forward_qualification_claimed=$false;independent_newtonian_evolution_completed=$false
 next_target='Implement the actual native rest-feedback blocks C*S and D alongside J*S^T*B, preserving collision and metric equations. Freeze matched initial data and the complete coupled operator, verify constraint propagation and forward-test against retained full controls without saved future rest forcing. Then proceed to the independent Newtonian comparison.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json
