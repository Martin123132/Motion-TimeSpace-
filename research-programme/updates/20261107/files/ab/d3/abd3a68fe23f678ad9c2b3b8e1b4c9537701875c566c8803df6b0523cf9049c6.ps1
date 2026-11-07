$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$post=Split-Path -Parent $root
$doc=Join-Path $post 'MTS-SCALAR-CYCLE-AVERAGING-DERIVATION.md'
$bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102'
$destination=Join-Path $root 'closeout.json'
if(Test-Path -LiteralPath $destination){throw 'Already sealed'}
function Hash-Path([string]$path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()}
$validation=Get-Content -Raw -LiteralPath "$root/validation-provenance-result.json"|ConvertFrom-Json
if(-not $validation.passed -or $validation.count -ne 591){throw 'Validation gate'}
foreach($entry in $validation.source_hashes.PSObject.Properties){if((Hash-Path $entry.Name) -ne $entry.Value){throw "Changed source $($entry.Name)"}}
if((Hash-Path "$root/result-common.json") -ne $validation.result_sha256){throw 'Changed result'}
if((Hash-Path "$root/averaging-summary-verified.csv") -ne $validation.csv_sha256){throw 'Changed summary'}
$reconciliation=Get-Content -Raw -LiteralPath "$root/provenance-reconciliation.json"|ConvertFrom-Json
if(-not $reconciliation.passed -or $reconciliation.result_sha256 -ne $validation.result_sha256){throw 'Provenance gate'}
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
    $receipts+=@{path=$endPath;receipt=$end;same_process_running=$same;current_command=$currentCommand}
}
if($receipts.Count -ne 4){throw 'Unexpected receipt count'}
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
    preceding_goal_turn_classification='progress';new_evolutions=0;saved_histories=12;paired_families=6
    cycles=@(1,2,4,8);centers=17;symbolic_identities=4;validation_checks=591
    validation_sha256=(Hash-Path "$root/validation-provenance-result.json")
    result_sha256=(Hash-Path "$root/result-common.json");reconciliation_sha256=(Hash-Path "$root/provenance-reconciliation.json")
    previous_closeout_sha256=(Hash-Path "$post/mts-derived-wavelength-test-20261107/closeout.json")
    remaining_task_processes=0;receipts=$receipts;artifacts=$artifacts;mutable_resume_bookmarks=$bookmarkHashes
    no_new_compilers_browsers_or_servers=$true;no_unrelated_process_action=$true
    scattering_coverage=39;scattering_total=128;next_unstarted_directions=@(39,40)
    finite_window_stress_identity_verified=$true;autonomous_pressure_closure_claimed=$false
    failed_analysis_and_validation_preserved=$true;no_numerical_retry=$true
    next_target='Derive exact co-rotating envelope equations from the retained canonical parent, verify on saved histories, then bound phase/window and discarded nonresonant terms to predict slow endpoint stress before a reduced Newton evolution.'
}
$bytes=[Text.Encoding]::UTF8.GetBytes(($result|ConvertTo-Json -Depth 30))
$stream=[IO.File]::Open($destination,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write)
try{$stream.Write($bytes,0,$bytes.Length)}finally{$stream.Dispose()}
@{state=$result.state;artifacts=$artifacts.Count;owned_workers=0;closeout_sha256=(Hash-Path $destination)}|ConvertTo-Json

