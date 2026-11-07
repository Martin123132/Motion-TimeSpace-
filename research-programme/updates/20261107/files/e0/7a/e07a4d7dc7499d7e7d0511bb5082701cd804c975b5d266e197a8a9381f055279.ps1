$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 368 -or $validation.mean_forward_qualified){throw 'validation'}
foreach($manifest in 'preflight-inputs.json','preflight-v2-inputs.json','coefficient-inputs.json','forward-inputs.json'){
 $frozen=Get-Content -Raw -LiteralPath "$root/$manifest"|ConvertFrom-Json
 foreach($entry in $frozen.sources.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed source $($entry.Name)"}}
}
$diagnostic=Get-Content -Raw -LiteralPath "$root/projection-diagnostic.json"|ConvertFrom-Json
foreach($entry in $diagnostic.source_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "changed diagnostic input $($entry.Name)"}}
$forward=Get-Content -Raw -LiteralPath "$root/forward-result.json"|ConvertFrom-Json
if($forward.state -ne 'complete' -or $forward.passed -or -not $diagnostic.passed){throw 'scientific outcomes'}
foreach($family in $forward.reports){foreach($row in $family.rows){if(-not $row.status.success -or (Hash-Path $row.packet) -ne $row.sha256){throw 'forward evidence'}}}
$parent=Join-Path $post 'mts-correlated-action-mean-20261107/closeout.json'
if((Hash-Path $parent) -ne '22fcbb30b6c999401a783a7492f43158c0f1dcb96864a3427a6d7fcfe0b390bd'){throw 'parent seal'}
$parentSeal=Get-Content -Raw -LiteralPath $parent|ConvertFrom-Json
foreach($artifact in $parentSeal.artifacts){if((Hash-Path $artifact.path) -ne $artifact.sha256){throw "changed parent $($artifact.path)"}}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($label in 'preflight-01','preflight-v2-01','coefficients-01','forward-01','diagnostic-01','validation-01'){
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
 if($label -eq 'preflight-01'){$expected=1}
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
$holds=@("$root/STOP-REQUESTED","$bridge/STOP-REQUESTED","$bridge/../STOP-REQUESTED","$bridge/../execution-v3/STOP-REQUEST.json","$bridge/final-epoch-kinematic-bank/STOP-REQUESTED")
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$doc=Join-Path $post 'MTS-NATIVE-REST-ACTION-FEEDBACK.md'
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|ForEach-Object {@{path=$_.FullName;sha256=(Hash-Path $_.FullName)}})
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$seal=@{
 state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
 preceding_goal_turn_classification='progress';current_goal_turn_classification='progress'
 parent_closeout_sha256=(Hash-Path $parent);validation_sha256=(Hash-Path "$root/validation.json")
 forward_sha256=(Hash-Path "$root/forward-result.json");diagnostic_sha256=(Hash-Path "$root/projection-diagnostic.json")
 artifacts=$artifacts;mutable_resume_bookmarks=@($bookmarks|ForEach-Object {@{path=$_;sha256=(Hash-Path $_)}})
 validation_checks=368;new_evolutions=4;preflight_families=6;prospective_families=2
 remaining_task_workers=0;worker_receipts=$receipts;failed_adapter_attempts=1;failed_forward_integrations=0
 inspected_regime_adapter_correction=$true;blind_numerical_retry=$false
 full_coupled_controls_pass=$true;mean_forward_qualified=$false;cold_identity_pass=$true
 dropped_action_contribution_identified=$true;complete_coupled_inverse_bound_proved=$false
 full_corrector_derivative_derived=$false;corrected_forward_solution_qualified=$false
 no_processes_killed=$true;no_compiler_browser_server_started=$true;no_github_or_galaxy_action=$true
 owner_holds_observed=@($holds|Where-Object {Test-Path -LiteralPath $_})
 scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
 next_target='Assemble the derived nonzero-phase coupled corrector in native state units, bound I+U inverse, derive its full coefficient derivative and both rest couplings, then freeze and forward-test a stated-order reduction with matched initial data against the passing full/cold controls. Preserve the failed first mean; do not change gates or expand wavelengths before qualification.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($seal|ConvertTo-Json -Depth 32))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state='verified_closed';artifacts=$artifacts.Count;remaining_task_workers=0;mean_forward_qualified=$false;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

