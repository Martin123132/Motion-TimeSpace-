param([ValidateSet('half','double','summary')][string]$Family,[string]$Label,[string]$Script)
$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$root=Join-Path $stage $Family
if($Label -notmatch '^[a-z0-9-]+$'){throw 'label'}
if($Script -notin @('assemble.py','evolve.py','validate.py')){throw 'script'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T15:46:00Z')){throw 'deadline'}
if(Test-Path "$root/$Label.start.json"){throw 'existing attempt'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned worker active'}
if(-not(Test-Path -LiteralPath $root)){New-Item -ItemType Directory -Path $root|Out-Null}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $stage $Script
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote $Family" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/$Label.stdout.log" -RedirectStandardError "$root/$Label.stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path $Family";source_path=$path;family=$Family;source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.end.json"
 Get-Content -LiteralPath "$root/$Label.stdout.log"
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/$Label.stderr.log";throw 'failed; preserve and inspect'}
}finally{$child.Dispose()}

