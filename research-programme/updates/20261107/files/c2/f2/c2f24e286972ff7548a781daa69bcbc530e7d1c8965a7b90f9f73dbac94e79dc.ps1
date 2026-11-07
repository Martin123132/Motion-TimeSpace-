param([string]$Bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102',[string]$Python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe')
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Check-Slot {
    $now=[DateTimeOffset]::UtcNow
    if($now -gt [DateTimeOffset]::Parse('2026-11-07T02:38:00Z') -or $now.Hour -ge 3){throw 'outside this one-time slot'}
    foreach($flag in 'STOP-REQUESTED','../STOP-REQUESTED','../execution-v3/STOP-REQUEST.json','saved-epoch-cell450/STOP-REQUESTED','final-epoch-kinematic-bank/STOP-REQUESTED','final-stable-real-batch-rays037-038/STOP-REQUESTED','final-stable-real-batch-rays035-036/STOP-REQUESTED'){
        if(Test-Path -LiteralPath (Join-Path $Bridge $flag)){throw 'workspace held'}
    }
    $end=Get-Content -LiteralPath "$Bridge/regular-pair-037-038-process-receipts/coverage.end.json" -Raw|ConvertFrom-Json
    $integrity=Get-Content -LiteralPath "$Bridge/final-stable-real-batch-rays037-038/integrity.json" -Raw|ConvertFrom-Json
    $coverage=Get-Content -LiteralPath "$Bridge/final-stable-real-batch-rays037-038/common-coverage.json" -Raw|ConvertFrom-Json
    if($end.actual_exit_code -ne 0 -or !$integrity.passed -or !$coverage.passed -or $coverage.through -ne 38){throw 'pair not verified'}
    if(Get-CimInstance Win32_Process -Filter "Name='python.exe' OR Name='node.exe'"|Where-Object {$_.CommandLine -match 'source-readout-bridge-20261102|mts-wave-state-20261107'}){throw 'existing worker; no relaunch'}
}
function Invoke-Checked([string]$name,[string]$exe,[string]$arguments,[string]$inputText) {
    Check-Slot
    $start=Join-Path $root "$name-start.receipt.json"
    $end=Join-Path $root "$name-end.receipt.json"
    if((Test-Path $start) -or (Test-Path $end)){throw "prior $name attempt; inspect"}
    $info=[Diagnostics.ProcessStartInfo]::new()
    $info.FileName=$exe
    $info.Arguments=$arguments
    $info.WorkingDirectory=$root
    $info.UseShellExecute=$false
    $info.CreateNoWindow=$true
    $info.RedirectStandardInput=$true
    $info.RedirectStandardOutput=$true
    $info.RedirectStandardError=$true
    $process=[Diagnostics.Process]::Start($info)
    try {
        $process.PriorityClass='BelowNormal'
        $process.ProcessorAffinity=[IntPtr]16
        $record=[ordered]@{pid=$process.Id;created_utc=$process.StartTime.ToUniversalTime().ToString('o');exe=$exe;arguments=$arguments;parent=$PID}
        $record|ConvertTo-Json|Set-Content -LiteralPath $start
        $stdout=$process.StandardOutput.ReadToEndAsync()
        $stderr=$process.StandardError.ReadToEndAsync()
        if($inputText){$process.StandardInput.Write($inputText)}
        $process.StandardInput.Close()
        $process.WaitForExit()
        $record.exit_code=$process.ExitCode
        $record.ended_utc=[DateTimeOffset]::UtcNow.ToString('o')
        $record.stderr=$stderr.Result
        $record|ConvertTo-Json|Set-Content -LiteralPath $end
        if($record.exit_code -ne 0){throw "$name failed: $($record.stderr)"}
        return $stdout.Result
    }finally{$process.Dispose()}
}
Check-Slot
$inputData=& "$root/inputs.ps1" -Bridge $Bridge
$node=(Get-Command node.exe).Source
$validation=Invoke-Checked 'wave-replay' $node '--v8-pool-size=1 verify.cjs' $inputData|ConvertFrom-Json
if(!$validation.passed){throw 'validation failed'}
$validation|ConvertTo-Json -Depth 7|Set-Content -LiteralPath "$root/validation.receipt.json"
$grid=Invoke-Checked 'mass-grid' $Python '-B mass_grid.py' ''
Write-Output $grid
