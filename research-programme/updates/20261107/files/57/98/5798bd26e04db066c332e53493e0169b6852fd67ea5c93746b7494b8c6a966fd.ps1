param([ValidateSet('half','balanced','double','summary')][string]$Family)
$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$root=Join-Path $stage $Family
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T18:45:00Z')){throw 'launch cutoff'}
if(Test-Path -LiteralPath "$stage/STOP-REQUESTED"){throw 'stage hold'}
if(Test-Path -LiteralPath "$root/STOP-REQUESTED"){throw 'family hold'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned numerical worker active'}
if(-not(Test-Path -LiteralPath $root)){New-Item -ItemType Directory -Path $root|Out-Null}
if(Test-Path -LiteralPath "$root/start.json"){throw 'existing attempt; inspect'}
$script=if($Family -eq 'summary'){'summarize.py'}else{'run.py'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $stage $script
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote $Family" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/stdout.log" -RedirectStandardError "$root/stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path $Family";source_path=$path;source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/end.json"
 Get-Content -LiteralPath "$root/stdout.log" -Tail 8
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/stderr.log";throw 'failed gate; no automatic retry'}
}finally{$child.Dispose()}

