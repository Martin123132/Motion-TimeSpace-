param(
    [Parameter(Mandatory=$true)][int]$OwnedPid,
    [Parameter(Mandatory=$true)][long]$CreationTicksUtc,
    [int]$CompletedCases = 3
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$Intake = Join-Path $Root 'source-intake/navier-stokes/20260914'
$RunFolder = Join-Path $Intake 'annular-position-reaction-diagnostic-attempt02'
$StatusPath = Join-Path $RunFolder 'status.json'
$ControlFolder = Join-Path $Intake 'annular-position-reaction-boundary-workflow'
$ExpectedScript = 'scripts/diagnose_annular_position_reaction_solve_v2_20260929.py'
if (Test-Path -LiteralPath $ControlFolder) { throw 'Controller output already exists' }
[IO.Directory]::CreateDirectory($ControlFolder) | Out-Null
$Control = [ordered]@{state='waiting'; owned_pid=$OwnedPid; creation_ticks_utc=$CreationTicksUtc; completed_case_target=$CompletedCases; scientific_files_modified=$false; unrelated_processes_touched=$false}
$ControlPath = Join-Path $ControlFolder 'status.json'
function Save-Control {
    [IO.File]::WriteAllText($ControlPath, ($Control | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
}
function Assert-Owned {
    $Process = Get-CimInstance Win32_Process -Filter "ProcessId=$OwnedPid"
    if (-not $Process) { throw 'Owned worker no longer exists' }
    if ($Process.CreationDate.ToUniversalTime().Ticks -ne $CreationTicksUtc) { throw 'PID creation-time mismatch' }
    if ($Process.CommandLine -notlike "*$ExpectedScript*--max-seconds 8000*") { throw 'Worker command mismatch' }
    if ($Process.ExecutablePath -ne 'C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe') { throw 'Worker executable mismatch' }
}
try {
    Assert-Owned
    Save-Control
    $Deadline = [DateTime]::UtcNow.AddHours(2.5)
    while ([DateTime]::UtcNow -lt $Deadline) {
        $Status = Get-Content -LiteralPath $StatusPath -Raw | ConvertFrom-Json
        if ($Status.state -ne 'running') {
            $Control.state='complete'
            $Control.result='worker_finished_without_external_stop'
            $Control.worker_state=$Status.state
            Save-Control
            exit 0
        }
        if ($Status.cases.Count -ge $CompletedCases) {
            $Verified = 0
            foreach ($Case in $Status.cases) {
                foreach ($Entry in $Case.paths.PSObject.Properties) {
                    $Relative = [string]$Entry.Value
                    $Full = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
                    if (-not $Full.StartsWith($Root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Case path outside workspace' }
                    $Expected = $Status.outputs.PSObject.Properties[$Relative].Value
                    if (-not $Expected) { $Expected = $Status.inputs.PSObject.Properties[$Relative].Value }
                    if (-not $Expected) { throw "Unowned completed case file: $Relative" }
                    if ((Get-FileHash -LiteralPath $Full -Algorithm SHA256).Hash.ToLowerInvariant() -ne $Expected) { throw "Changed completed case file: $Relative" }
                    $Verified++
                }
            }
            Assert-Owned
            $SnapshotPath = Join-Path $RunFolder 'running-status-at-safe-boundary.json'
            $Stream = [IO.File]::Open($SnapshotPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
            try {
                $Bytes = [Text.Encoding]::UTF8.GetBytes(($Status | ConvertTo-Json -Depth 100))
                $Stream.Write($Bytes, 0, $Bytes.Length)
            } finally { $Stream.Dispose() }
            Stop-Process -Id $OwnedPid -ErrorAction Stop
            for ($Attempt=0; $Attempt -lt 20; $Attempt++) {
                if (-not (Get-Process -Id $OwnedPid -ErrorAction SilentlyContinue)) { break }
                Start-Sleep -Milliseconds 250
            }
            if (Get-Process -Id $OwnedPid -ErrorAction SilentlyContinue) { throw 'Owned worker did not exit' }
            $Final = Get-Content -LiteralPath $StatusPath -Raw | ConvertFrom-Json
            $Final.state='failed'
            $Final | Add-Member -NotePropertyName external_safe_boundary_stop -NotePropertyValue $true -Force
            $Final | Add-Member -NotePropertyName numerical_failure -NotePropertyValue $false -Force
            $Final | Add-Member -NotePropertyName error -NotePropertyValue 'Controlled stop after three completed diagnostic controls; last refined MTS control deferred to a fresh bounded run.' -Force
            $Final | Add-Member -NotePropertyName stopped_at -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
            [IO.File]::WriteAllText($StatusPath, ($Final | ConvertTo-Json -Depth 100), [Text.UTF8Encoding]::new($false))
            $Control.state='complete'
            $Control.result='owned_worker_stopped_at_saved_case_boundary'
            $Control.completed_cases=$Final.cases.Count
            $Control.completed_case_files_verified=$Verified
            Save-Control
            exit 0
        }
        Start-Sleep -Seconds 5
    }
    throw 'Controller deadline reached without stopping any process'
} catch {
    $Control.state='failed'
    $Control.error=$_.Exception.Message
    Save-Control
    throw
}
