$ErrorActionPreference='Stop'
$root=$PSScriptRoot
if(Test-Path -LiteralPath "$root/bounds-01.start.json"){throw 'already attempted'}
if([DateTimeOffset]::UtcNow -ge [DateTimeOffset]::Parse('2026-11-07T14:45:00Z')){throw 'deadline'}
if(Get-CimInstance Win32_Process -Filter "Name='python.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-.*20261107'}){throw 'owned worker active'}
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$path="$root/bound_remainder.py";$quote=[char]34
$child=Start-Process -FilePath $python -ArgumentList "-B $quote$path$quote" -WindowStyle Hidden -PassThru -RedirectStandardOutput "$root/bounds-01.stdout.log" -RedirectStandardError "$root/bounds-01.stderr.log"
try{
 $receipt=[ordered]@{pid=$child.Id;created=$child.StartTime.ToUniversalTime().ToString('o');command="$python -B $path";source_sha256=(Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant()}
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/bounds-01.start.json"
 $child.WaitForExit();$child.Refresh()
 $receipt.exit_code=$child.ExitCode;$receipt.finished=[DateTimeOffset]::UtcNow.ToString('o')
 $receipt|ConvertTo-Json|Set-Content -LiteralPath "$root/bounds-01.end.json"
 Get-Content -LiteralPath "$root/bounds-01.stdout.log"
 if($child.ExitCode -ne 0){Get-Content -LiteralPath "$root/bounds-01.stderr.log";throw 'failed; preserve and inspect'}
}finally{$child.Dispose()}
