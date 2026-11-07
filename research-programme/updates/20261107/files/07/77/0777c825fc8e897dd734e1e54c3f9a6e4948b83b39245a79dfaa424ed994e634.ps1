param([string]$Phase,[ValidateSet('inventory.py','extend.py','summarize.py')][string]$Script)
$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
if($Phase -notmatch '^[a-z0-9-]+$'){throw 'explicit phase'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T21:30:00Z')){throw 'launch cutoff'}
if(Test-Path -LiteralPath "$stage/STOP-REQUESTED"){throw 'stage hold'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned worker active'}
if(Test-Path -LiteralPath "$stage/$Phase.start.json"){throw 'existing attempt; inspect'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $stage $Script
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$stage/$Phase.stdout.log" -RedirectStandardError "$stage/$Phase.stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path";source_path=$path;source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$stage/$Phase.start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$stage/$Phase.end.json"
 Get-Content -LiteralPath "$stage/$Phase.stdout.log" -Tail 10
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$stage/$Phase.stderr.log";throw 'failed gate; inspect, no automatic retry'}
}finally{$child.Dispose()}
