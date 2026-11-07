param([string]$Label='action-01')
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
if($Label -notmatch '^[a-z0-9-]+$'){throw 'invalid label'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T13:35:00Z')){throw 'deadline'}
if((Test-Path "$root/$Label.start.json") -or (Test-Path "$root/$Label.end.json")){throw 'existing attempt'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'another owned worker'}
foreach($var in 'OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'){[Environment]::SetEnvironmentVariable($var,'1','Process')}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $root 'test_action_sources.py'
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/$Label.stdout.log" -RedirectStandardError "$root/$Label.stderr.log"
try{
    $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path";source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
    $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.start.json"
    $child.WaitForExit();$child.Refresh()
    $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
    $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.end.json"
    Get-Content -LiteralPath "$root/$Label.stdout.log"
    if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/$Label.stderr.log";throw 'failed; preserve and inspect'}
}finally{$child.Dispose()}

