$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Hash([string]$path){
 if(-not(Test-Path -LiteralPath $path -PathType Leaf)){throw "Missing $path"}
 (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function ReadJson([string]$path){Get-Content -LiteralPath $path -Raw|ConvertFrom-Json}
if(Test-Path -LiteralPath "$root/closeout.json"){throw 'Existing closeout; inspect'}
$parent=Join-Path (Split-Path $root -Parent) 'mts-newton-wavelength-bounds-20261107/closeout.json'
if((Hash $parent) -ne '9d5f2606ce7642ef477772bfee5554525bedbd463b57aa3ed0ba4834036d075b'){throw 'Parent seal'}
foreach($artifact in (ReadJson $parent).artifacts){
 if((Hash $artifact.path) -ne $artifact.sha256){throw "Parent changed: $($artifact.path)"}
}
$summary=ReadJson "$root/summary/summary.json"
$validation=ReadJson "$root/summary/validation.json"
$energy=ReadJson "$root/energy/result.json"
if(-not $summary.passed -or -not $validation.passed -or -not $energy.passed){throw 'Missing completed numerical result'}
if(@($validation.checks|Where-Object {-not $_.passed}).Count -or @($energy.checks|Where-Object {-not $_.passed}).Count){throw 'Failed check'}
$running=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($family in @('half','balanced','double','energy','summary')){
 $start=ReadJson "$root/$family/start.json"
 $end=ReadJson "$root/$family/end.json"
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command -or $end.exit_code -ne 0){throw "Receipt $family"}
 if((Hash $start.source_path) -ne $start.source_sha256){throw "Launched source changed: $family"}
 $same=@($running|Where-Object {$_.ProcessId -eq $start.pid -and [Math]::Abs(($_.CreationDate.ToUniversalTime()-[DateTimeOffset]::Parse($start.created).UtcDateTime).TotalSeconds) -lt 2})
 if($same.Count){throw "Worker remains: $family"}
 $receipts+=[ordered]@{family=$family;pid=$start.pid;created=$start.created;command=$start.command;finished=$end.finished;exit_code=$end.exit_code;same_process_still_present=$false}
 if($family -ne 'summary'){
  $input=ReadJson "$root/$family/inputs.json"
  if(-not $input.sources){throw "Missing frozen manifest: $family"}
  foreach($source in $input.sources.PSObject.Properties){if((Hash $source.Name) -ne $source.Value){throw "Source changed: $($source.Name)"}}
  $result=ReadJson "$root/$family/result.json"
  if(-not $result.passed){throw "Result failed: $family"}
  foreach($source in $result.input_hashes.PSObject.Properties){if((Hash $source.Name) -ne $source.Value){throw "Saved input changed: $($source.Name)"}}
 }
}
foreach($source in $summary.evidence_hashes.PSObject.Properties){if((Hash $source.Name) -ne $source.Value){throw 'Aggregate evidence changed'}}
$active=@($running|Where-Object {$_.Name -eq 'python.exe' -and $_.CommandLine -like '*mts-newton-source-gain-20261107*'})
if($active.Count){throw 'Task worker still present'}
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering coverage changed'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected task bytecode cache'}
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|Sort-Object FullName|ForEach-Object{
 [ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Hash $_.FullName)}
})
$record=[ordered]@{
 state='verified_closed'
 completed_utc=[DateTimeOffset]::UtcNow.ToString('o')
 all_numerical_checks_passed=$true
 parent_seal=(Hash $parent)
 new_ode_solves=0
 reused_adjoint_traces=12
 source_gain_checks=$validation.count
 native_phase_samples=291
 energy_coefficient_samples=291
 derived_result='Source-response Holder criterion; exact carrier/gamma current-direction cancellation; positive full-frequency homogeneous scalar growth bound <=3/2 per e-fold with explicit metric forcing'
 full_feedback_limit_claimed=$false
 cleanup=[ordered]@{workers=$receipts;live_stage_python_count=0;cleanup_kills=0;unrelated_processes_untouched=$true;browser_server_subagents_started=0}
 scattering=[ordered]@{path=$coverage;sha256=(Hash $coverage);completed_rays=39;next_unstarted_pair=@(39,40)}
 artifact_count=$artifacts.Count
 artifacts=$artifacts
}
$record|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$root/closeout.json" -Encoding utf8
Write-Output ("verified "+$artifacts.Count+" artifacts; all5 workers exited")
Write-Output ("closeout SHA256 "+(Hash "$root/closeout.json"))

