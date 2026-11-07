param([ValidateSet('half','balanced','double','summary')][string]$Family,[string]$Phase,[ValidateSet('qualify.py','budget.py','summarize.py')][string]$Script)
$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$root=Join-Path $stage $Family
if($Phase -notmatch '^[a-z0-9-]+$'){throw 'explicit phase'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T20:25:00Z')){throw 'launch cutoff'}
if(Test-Path -LiteralPath "$stage/STOP-REQUESTED"){throw 'stage hold'}
if(Test-Path -LiteralPath "$root/STOP-REQUESTED"){throw 'family hold'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned worker active'}
if(-not(Test-Path -LiteralPath $root)){New-Item -ItemType Directory -Path $root|Out-Null}
if(Test-Path -LiteralPath "$root/$Phase.start.json"){throw 'existing attempt; inspect'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $stage $Script
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote $Family" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/$Phase.stdout.log" -RedirectStandardError "$root/$Phase.stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path $Family";source_path=$path;source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Phase.start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Phase.end.json"
 Get-Content -LiteralPath "$root/$Phase.stdout.log" -Tail 8
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/$Phase.stderr.log";throw 'failed gate; inspect, no automatic retry'}
}finally{$child.Dispose()}
