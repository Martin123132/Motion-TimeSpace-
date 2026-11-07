$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-ACTION-AND-SOURCE-PULLBACK.md'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/verified/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 1091){throw 'validation'}
foreach($entry in $validation.compiled_sources.PSObject.Properties){
 if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}
}
foreach($entry in $validation.authority_sources.PSObject.Properties){
 if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed authority $($entry.Name)"}
}
if((Hash-Path "$root/verified/result.json") -ne $validation.result_sha256){throw 'result'}
if((Hash-Path "$root/verified/summary.csv") -ne $validation.csv_sha256){throw 'csv'}
$result=Get-Content -Raw -LiteralPath "$root/verified/result.json"|ConvertFrom-Json
foreach($entry in $result.source_hashes.PSObject.Properties){
 if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed frozen input $($entry.Name)"}
}
$parent=Join-Path $post 'mts-second-micromotion-20261107/closeout.json'
if((Hash-Path $parent) -ne '3213844114a78015ee286d2782d0d2017ddc0262e308cfa5af65a0604c4a4f99'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){
 if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}
}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($label in 'action-01','action-02','validation-01'){
 $start=Get-Content -Raw -LiteralPath "$root/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$root/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){
  $same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02
 }
 if($same){throw "task worker remains $($end.pid)"}
 if($label -eq 'action-01'){
  if($end.exit_code -ne 1 -or -not(Test-Path "$root/CHECKER-REPAIR.md")){throw 'failure provenance'}
 }elseif($end.exit_code -ne 0){throw 'failed accepted worker'}
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
$closeout=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='no progress';current_goal_turn_classification='progress'
 histories_reused=42;new_evolutions=0;paired_families=6;symbolic_identities=16;validation_checks=1091
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$root/verified/validation.json")
 result_sha256=(Hash-Path "$root/verified/result.json");source_reconstruction_max=1.7516141497458e-15
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 remaining_task_workers=0;worker_receipts=$receipts;failed_checker_receipt_preserved=$true
 no_numerical_evolution_retry=$true;no_processes_killed=$true;no_compiler_browser_server_started=$true
 no_github_or_galaxy_action=$true;scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 exact_scalar_action_pullback_derived=$true;full_truncated_covariant_action_claimed=$false;independent_newtonian_evolution_completed=$false
 next_target='Derive a retained-order action/Hamiltonian and its induced spectator/metric sources before variation; compare its generated equations with saved full and second-micromotion trajectories, then independently evolve the Newtonian comparison with retained relativistic force budgets.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($closeout|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

