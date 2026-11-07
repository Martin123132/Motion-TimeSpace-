$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-DERIVED-WAVELENGTH-AND-NEWTON-TEST.md'
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'Already sealed; inspect, do not overwrite'}
$holds=@("$root/STOP-REQUESTED","$bridge/STOP-REQUESTED","$bridge/../STOP-REQUESTED","$bridge/../execution-v3/STOP-REQUEST.json","$bridge/final-epoch-kinematic-bank/STOP-REQUESTED")
foreach($hold in $holds){if(Test-Path -LiteralPath $hold){throw "Owner hold $hold"}}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation-result.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 1287){throw 'Validation gate'}
foreach($entry in $validation.source_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "Changed validated source $($entry.Name)"}}
$comparison=Get-Content -Raw -LiteralPath "$root/comparison-roundtrip-result.json"|ConvertFrom-Json
$prediction=Get-Content -Raw -LiteralPath "$root/prediction-bound-result.json"|ConvertFrom-Json
if(-not $comparison.passed -or $prediction.state -ne 'complete'){throw 'Incomplete outputs'}
if((Hash-Path "$root/comparison-roundtrip-result.json") -ne $validation.comparison_sha256){throw 'Changed comparison'}
if((Hash-Path "$root/prediction-bound-result.json") -ne $validation.prediction_sha256){throw 'Changed trajectories manifest'}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($startFile in Get-ChildItem -LiteralPath $root -Filter '*.start.json' -File){
    $start=Get-Content -Raw -LiteralPath $startFile.FullName|ConvertFrom-Json
    $endPath=$startFile.FullName.Replace('.start.json','.end.json')
    if(-not(Test-Path -LiteralPath $endPath)){throw "Outstanding start $($startFile.Name)"}
    $end=Get-Content -Raw -LiteralPath $endPath|ConvertFrom-Json
    if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'Receipt identity changed'}
    $current=@($processes|Where-Object ProcessId -eq $end.pid)
    $same=$false
    $currentCommand=$null
    if($current.Count){
        $currentCommand=$current[0].CommandLine
        $same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02
    }
    if($same){throw "Owned worker still running $($end.pid)"}
    $receipts+=@{path=$endPath;receipt=$end;same_process_running=$same;current_command=$currentCommand}
}
$compilerReceipts=@()
foreach($folder in @('build','build-full-momentum')){
    $build=Get-Content -Raw -LiteralPath "$root/$folder/build-result.json"|ConvertFrom-Json
    foreach($parent in $build.processes){
        if($parent.exit_code -ne 0){throw 'Compiler failed'}
        foreach($owned in @($parent)+@($parent.children)){
            if($null -eq $owned){continue}
            $current=@($processes|Where-Object ProcessId -eq $owned.pid)
            $same=$false
            $currentCommand=$null
            if($current.Count){
                $currentCommand=$current[0].CommandLine
                $epoch=([DateTimeOffset]$current[0].CreationDate).ToUnixTimeMilliseconds()/1000.0
                $same=[math]::Abs($epoch-[double]$owned.created) -lt .02
            }
            if($same){throw "Owned compiler child still running $($owned.pid)"}
            $compilerReceipts+=@{pid=$owned.pid;created=$owned.created;command=$owned.command;same_process_running=$same;current_command=$currentCommand}
        }
    }
}
$absoluteRoot=[IO.Path]::GetFullPath($root)
$unreceipted=@($processes|Where-Object { $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot) })
if($unreceipted.Count){throw 'Unclosed numerical process under this stage'}
foreach($drive in @('R:/','S:/','T:/')){if(Test-Path -LiteralPath $drive){throw "Temporary mapping remains $drive"}}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected bytecode'}
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Scattering coverage changed'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$bookmarkHashes=@($bookmarks|ForEach-Object { @{path=$_;sha256=(Hash-Path $_)} })
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|ForEach-Object { @{path=$_.FullName;sha256=(Hash-Path $_.FullName)} })
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$result=@{
    state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
    preceding_goal_turn_classification='progress';coupled_cases=48;paired_wave_families=6
    validation_checks=1287;validation_sha256=(Hash-Path "$root/validation-result.json")
    prediction_sha256=(Hash-Path "$root/prediction-bound-result.json")
    comparison_sha256=(Hash-Path "$root/comparison-roundtrip-result.json")
    previous_closeout_sha256=(Hash-Path "$post/mts-repaired-coupled-evolution-20261107/closeout.json")
    remaining_task_processes=0;receipts=$receipts;compiler_process_cleanup=$compilerReceipts
    artifacts=$artifacts;mutable_resume_bookmarks=$bookmarkHashes
    scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
    source_conditioned_force_bounds_pass=$true;raw_conservation_and_metric_checks_pass=$true
    failed_preflight_and_partial_analysis_preserved=$true;no_numerical_retry=$true
    no_unrelated_process_action=$true;temporary_mappings_removed=$true
    next_target='Derive finite-window scalar-stress averaging from saved canonical trajectories with endpoint, expansion, metric and gauge terms; compare cold control and exact force budget before independently evolving a reduced Newton system.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($result|ConvertTo-Json -Depth 30))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state=$result.state;artifacts=$artifacts.Count;owned_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

