param(
 [ValidateSet('half','double','summary')][string]$Family,
 [string]$Label,
 [string]$Script
)
$ErrorActionPreference='Stop'
$stage=$PSScriptRoot
$root=Join-Path $stage $Family
$allowed=@('syntax.py','preflight.py','evolve_v2.py','validate_evolution_v2.py','build.py','adjoint.py','validate_adjoint.py','primitive.py','validate_primitive.py','volume_dictionary.py','summarize.py')
if($Label -notmatch '^[a-z0-9-]+$' -or $Script -notin $allowed){throw 'explicit phase contract'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T17:34:00Z')){throw 'launch deadline'}
if(-not (Test-Path -LiteralPath $root)){New-Item -ItemType Directory -Path $root|Out-Null}
if(Test-Path -LiteralPath "$root/$Label.start.json"){throw 'existing attempt'}
if(Test-Path -LiteralPath "$stage/STOP-REQUESTED"){throw 'stage hold'}
if(Test-Path -LiteralPath "$root/STOP-REQUESTED"){throw 'family hold'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned worker active'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path=Join-Path $stage $Script
$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote $Family" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/$Label.stdout.log" -RedirectStandardError "$root/$Label.stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path $Family";family=$Family;source_path=$path;source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/$Label.end.json"
 Get-Content -LiteralPath "$root/$Label.stdout.log" -Tail 3
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/$Label.stderr.log";throw 'failed; preserve and inspect'}
}finally{$child.Dispose()}
