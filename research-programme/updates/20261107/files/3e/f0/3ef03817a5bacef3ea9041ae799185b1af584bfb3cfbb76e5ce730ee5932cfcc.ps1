$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
if(Test-Path -LiteralPath "$stage/closeout.json"){throw 'Already sealed'}
$validation=Get-Content -LiteralPath "$stage/final-validation/result.json" -Raw|ConvertFrom-Json
if(-not $validation.passed){throw 'Final candidate validation absent'}
$workers=@()
foreach($startPath in Get-ChildItem -LiteralPath $stage -Filter '*.start.json'){
 $start=Get-Content -LiteralPath $startPath.FullName -Raw|ConvertFrom-Json
 $endPath=$startPath.FullName.Replace('.start.json','.end.json')
 if(-not(Test-Path -LiteralPath $endPath)){throw "Unfinished worker $($start.pid)"}
 $end=Get-Content -LiteralPath $endPath -Raw|ConvertFrom-Json
 if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'Process receipt identity mismatch'}
 if((Get-FileHash -LiteralPath $start.source_path).Hash.ToLowerInvariant() -ne $start.source_sha256){throw 'Worker source changed'}
 $active=Get-CimInstance Win32_Process -Filter "ProcessId=$($start.pid)"
 $status='exited'
 if($null -ne $active){
  $difference=[Math]::Abs(($active.CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($start.created)).UtcDateTime).TotalSeconds)
  if($difference -lt 1 -and $active.CommandLine -like "*$($start.source_path)*"){throw 'Owned worker still active'}
  $status='pid_reused_by_unrelated_process_preserved'
 }
 $expected=if($startPath.BaseName -in @('inventory-01.start','validation-01.start')){1}else{0}
 if($end.exit_code -ne $expected){throw 'Unexpected exit status'}
 $workers+=[ordered]@{pid=$start.pid;created=$start.created;command=$start.command;exit_code=$end.exit_code;finished=$end.finished;cleanup_status=$status;process_killed=$false}
}
if($workers.Count -ne 8){throw 'Unexpected stage worker inventory'}
$remaining=@(Get-CimInstance Win32_Process | Where-Object {$_.ProcessId -ne $PID -and $_.Name -match '^(python|pwsh|powershell)\.exe$' -and $_.CommandLine -like "*$stage*"})
if($remaining.Count -gt 0){$remaining|Select-Object ProcessId,CreationDate,CommandLine|Format-List;throw 'Owned launcher or worker remains'}
if(Get-ChildItem -LiteralPath $stage -Directory -Filter '__pycache__' -Recurse){throw 'Unexpected bytecode cache; inspect'}
$coverage='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102/final-stable-real-batch-rays037-038/common-coverage.json'
$coverageHash=(Get-FileHash -LiteralPath $coverage).Hash.ToLowerInvariant()
if($coverageHash -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering coverage changed'}
$artifacts=@(Get-ChildItem -LiteralPath $stage -File -Recurse | Sort-Object FullName | ForEach-Object {[ordered]@{path=$_.FullName;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}})
$receipt=[ordered]@{state='verified_closed';created_utc=[DateTimeOffset]::UtcNow.ToString('o');scope='qualified same-action cold background with analytic phase-uncertainty tube and numerical validation';final_validation_sha256=(Get-FileHash -LiteralPath "$stage/final-validation/result.json").Hash.ToLowerInvariant();parent_seal='cd29bc225d756592906efe5c3eb8316c937af9150865fffa9a7b361e43920b5e';workers=$workers;artifact_count=$artifacts.Count;artifacts=$artifacts;failed_attempts_preserved=@('inventory-01','validation-01');automatic_relaunches=0;source_diagnosed_separate_repairs=@('direct defining thermal integral','analytic comparison-envelope breakpoint');all_task_workers_exited=$true;processes_killed=0;other_chats_untouched=$true;subagents=0;github_actions=0;new_observational_fits=0;late_exact_scalar_phase_available=$false;formal_interval_certificate=$false;scattering_coverage_path=$coverage;scattering_coverage_sha256=$coverageHash;music_lab='Tonight reservation released by owner; actual holds preserved';next='Derive bounded late perturbation micromotion/averaging and initial-mode ownership before the frozen cold GR/Poisson benchmark.'}
$receipt|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$stage/closeout.json"
Write-Output ('Sealed artifacts='+$artifacts.Count+' workers='+$workers.Count)
Get-FileHash -LiteralPath "$stage/closeout.json"
