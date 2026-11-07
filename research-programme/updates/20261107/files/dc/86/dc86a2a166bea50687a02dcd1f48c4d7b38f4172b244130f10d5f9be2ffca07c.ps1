$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-JOINT-GRAVITY-HAMILTONIAN-AND-CANONICAL-MEAN.md'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 577){throw 'validation'}
foreach($group in @($validation.compiled_sources,$validation.authority_sources)){
 foreach($entry in $group.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
foreach($pair in @(@('result.json','result_sha256'),@('canonical/result.json','canonical_sha256'),@('summary.csv','csv_sha256'),@('symbolic-result.json','symbolic_sha256'))){
 if((Hash-Path "$root/$($pair[0])") -ne $validation.($pair[1])){throw "changed evidence $($pair[0])"}
}
$result=Get-Content -Raw -LiteralPath "$root/result.json"|ConvertFrom-Json
$canonical=Get-Content -Raw -LiteralPath "$root/canonical/result.json"|ConvertFrom-Json
foreach($owner in @($result,$canonical)){
 foreach($entry in $owner.source_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "frozen input $($entry.Name)"}}
}
$parent=Join-Path $post 'mts-action-source-pullback-20261107/closeout.json'
if((Hash-Path $parent) -ne '150d0101357dc178c231c168e178a8bb9d9964706129b9dd7b578352a95aca4d'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($label in 'joint-01','canonical-01','validation-01'){
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
 histories_reused=42;new_evolutions=0;paired_families=6;symbolic_identities=13;validation_checks=577
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$root/validation.json")
 result_sha256=(Hash-Path "$root/result.json");canonical_sha256=(Hash-Path "$root/canonical/result.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 remaining_task_workers=0;worker_receipts=$receipts;failed_attempts=0;no_numerical_retry=$true
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 joint_scalar_gravity_hamiltonian_constructed=$true;frozen_phase_mean_derived=$true;canonical_frozen_map_verified=$true
 actual_background_coefficient_derivative_completed=$false;new_averaged_forward_qualification_claimed=$false
 independent_newtonian_evolution_completed=$false
 next_target='Compute the full background-only generating-matrix derivative, including coefficient/phase-frequency micromotion, and the matrix-exponential Frechet time derivative. Transform sources and constraints, reproduce the exact full flow, then prospectively qualify the retained-order action with matched initial data before the independent Newtonian comparison.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

