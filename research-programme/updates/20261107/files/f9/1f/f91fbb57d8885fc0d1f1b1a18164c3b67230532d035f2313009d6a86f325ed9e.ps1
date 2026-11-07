$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation.json"|ConvertFrom-Json
if(-not $validation.passed){throw 'validation'}
foreach($pair in @(@('evolution-result.json','evolution_sha256'),@('representation-v2-result.json','representation_sha256'))){
 if((Hash-Path "$root/$($pair[0])") -ne $validation.($pair[1])){throw 'changed result'}
}
foreach($manifest in 'frozen-inputs.json','representation-v2-inputs.json','evolution-inputs.json'){
 $frozen=Get-Content -Raw -LiteralPath "$root/$manifest"|ConvertFrom-Json
 foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
$evolution=Get-Content -Raw -LiteralPath "$root/evolution-result.json"|ConvertFrom-Json
$representation=Get-Content -Raw -LiteralPath "$root/representation-v2-result.json"|ConvertFrom-Json
if($evolution.state -ne 'complete' -or -not $representation.passed -or $evolution.passed -ne $validation.corrected_forward_qualified){throw 'outcomes'}
foreach($family in $evolution.reports){foreach($row in $family.rows){if(-not $row.status.success -or (Hash-Path $row.packet) -ne $row.sha256){throw 'forward evidence'}}}
$parent=Join-Path $post 'mts-native-rest-action-feedback-20261107/closeout.json'
if((Hash-Path $parent) -ne 'f7fded5e04d4a9a958948ed5183fa95c81b9e5d2e306366b3e8727bb672bda75'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($label in 'assemble-01','representation-v2-01','evolution-01','validation-01'){
 $start=Get-Content -Raw -LiteralPath "$root/$label.start.json"|ConvertFrom-Json
 $end=Get-Content -Raw -LiteralPath "$root/$label.end.json"|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'identity receipt'}
 $source=($end.command -split ' -B ',2)[1]
 if((Hash-Path $source) -ne $end.source_sha256){throw 'changed worker code'}
 $current=@($processes|Where-Object ProcessId -eq $end.pid)
 $same=$false
 if($current.Count){$same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02}
 if($same){throw "task worker remains $($end.pid)"}
 $expected=0
 if($label -eq 'assemble-01'){$expected=1}
 if($end.exit_code -ne $expected){throw 'unexpected worker result'}
 $receipts+=@{label=$label;receipt=$end;same_process_running=$same;expected_exit_code=$expected}
}
$absoluteRoot=[IO.Path]::GetFullPath($root)
$unreceipted=@($processes|Where-Object {$_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot)})
if($unreceipted.Count){throw 'outstanding stage worker'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'unexpected bytecode'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-COUPLED-PHASE-CORRECTOR.md'
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$root/validation.json")
 evolution_sha256=(Hash-Path "$root/evolution-result.json");representation_sha256=(Hash-Path "$root/representation-v2-result.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 validation_checks=$validation.count;new_evolutions=4;prospective_families=2
 remaining_task_workers=0;worker_receipts=$receipts;failed_representation_attempts=1;failed_forward_integrations=0
 inspected_same_node_interpolation_repair=$true;blind_numerical_retry=$false
 original_mean_failure_preserved=$true;corrected_forward_qualified=$evolution.passed
 full_derivative_numerically_represented_and_checked=$true;continuous_time_inverse_certificate=$false
 exact_map_is_only_a_control=$true;first_generator_remainder_derived=$true
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Use the private report/resume next target. Retain the first corrected generator and explicit remainder; extend only after its same-gate balanced control has qualified, without refitting or changing the physical bank.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;corrected_forward_qualified=$evolution.passed;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

