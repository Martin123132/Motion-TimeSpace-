$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-SECOND-MICROMOTION-REDUCTION.md'
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'Already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation-result.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 1325){throw 'Validation gate'}
foreach($entry in $validation.source_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "Changed source $($entry.Name)"}}
if((Hash-Path "$root/comparison-result.json") -ne $validation.comparison_sha256){throw 'Changed result'}
if((Hash-Path "$root/second-micromotion-comparison.csv") -ne $validation.csv_sha256){throw 'Changed summary'}
$comparison=Get-Content -Raw -LiteralPath "$root/comparison-result.json"|ConvertFrom-Json
if(-not $comparison.implementation_valid -or -not $comparison.reduced_all_qualified -or -not $comparison.second_micromotion_candidate){throw 'Qualification mismatch'}
if(@($comparison.reports|Where-Object {-not $_.reduced_candidate_qualified}).Count){throw 'Unqualified bounded family'}
$processes=@(Get-CimInstance Win32_Process)
$receipts=@()
foreach($startFile in Get-ChildItem -LiteralPath $root -Filter '*.start.json' -File){
    $start=Get-Content -Raw -LiteralPath $startFile.FullName|ConvertFrom-Json
    $endPath=$startFile.FullName.Replace('.start.json','.end.json')
    if(-not(Test-Path -LiteralPath $endPath)){throw "Outstanding start $($startFile.Name)"}
    $end=Get-Content -Raw -LiteralPath $endPath|ConvertFrom-Json
    if($start.pid -ne $end.pid -or $start.created -ne $end.created -or $start.command -ne $end.command){throw 'Receipt identity'}
    $current=@($processes|Where-Object ProcessId -eq $end.pid)
    $same=$false
    $currentCommand=$null
    if($current.Count){
        $currentCommand=$current[0].CommandLine
        $same=[math]::Abs(($current[0].CreationDate.ToUniversalTime()-([DateTimeOffset]::Parse($end.created)).UtcDateTime).TotalSeconds) -lt .02
    }
    if($same){throw "Owned worker running $($end.pid)"}
    if($end.exit_code -ne 0){throw 'Unsuccessful owned worker'}
    $receipts+=@{path=$endPath;receipt=$end;same_process_running=$same;current_command=$currentCommand}
}
if($receipts.Count -ne 3){throw 'Unexpected receipt count'}
$absoluteRoot=[IO.Path]::GetFullPath($root)
$unreceipted=@($processes|Where-Object { $_.Name -match '^python(w)?\.exe$' -and $_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($absoluteRoot) })
if($unreceipted.Count){throw 'Unclosed stage worker'}
if(@(Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__').Count){throw 'Unexpected bytecode'}
$coverage="$bridge/final-stable-real-batch-rays037-038/common-coverage.json"
if((Hash-Path $coverage) -ne '95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3'){throw 'Changed scattering'}
$bookmarks=@("$post/CURRENT_LOCAL_RESUME.md","$post/condensate-origin-20261003/RESUME-CURRENT.md","$bridge/../NEXT.md")
$bookmarkHashes=@($bookmarks|ForEach-Object { @{path=$_;sha256=(Hash-Path $_)} })
$artifacts=@(Get-ChildItem -LiteralPath $root -Recurse -File|ForEach-Object { @{path=$_.FullName;sha256=(Hash-Path $_.FullName)} })
$artifacts+=@{path=$doc;sha256=(Hash-Path $doc)}
$result=@{
    state='verified_closed';utc=[DateTimeOffset]::UtcNow.ToString('o')
    preceding_goal_turn_classification='progress';new_evolutions=42;paired_families=6
    cycles=@(1,2,4,8);centers=17;symbolic_identities=14;validation_checks=1325
    validation_sha256=(Hash-Path "$root/validation-result.json")
    comparison_sha256=(Hash-Path "$root/comparison-result.json");prediction_sha256=(Hash-Path "$root/prediction-result.json")
    previous_closeout_sha256=(Hash-Path "$post/mts-mean-retaining-reduction-20261107/closeout.json")
    remaining_task_processes=0;receipts=$receipts;artifacts=$artifacts;mutable_resume_bookmarks=$bookmarkHashes
    no_new_compilers_browsers_or_servers=$true;no_unrelated_process_action=$true
    scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
    exact_second_coordinate_control_verified=$true;bounded_second_micromotion_candidate_qualified=$true;exact_conservation_theorem_claimed=$false;independent_newtonian_evolution_completed=$false;global_error_bound_claimed=$false
    all_worker_receipts_successful=$true;no_numerical_retry=$true
    next_target='Pull back the retained scalar quadratic action/stress into the second coordinate, with variational metric coupling and retained boundary terms; derive effective matter sources before independently evolving the Newtonian approximation.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($result|ConvertTo-Json -Depth 30))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state=$result.state;artifacts=$artifacts.Count;owned_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

