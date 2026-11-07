$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach ($model in @('heavy', 'cold')) {
    foreach ($residual in @($false, $true)) {
        $name = $model + '24-event8-3200'
        $extra = @()
        if ($residual) { $name += '-residual'; $extra += '--include-residual' }
        & $python -B run_mixed_waves.py --name $name --model $model --bank event8 --steps 3200 @extra *> "$name.log"
        if ($LASTEXITCODE -ne 0) { throw "Wave process failed: $name" }
        $packet = Get-Content -LiteralPath "waves/$name/status.json" -Raw | ConvertFrom-Json
        if (-not $packet.all_checks_passed) { throw "Wave validation failed: $name" }
        Write-Output "Finished $name"
    }
}
& $python -B compare_mixed_waves.py --name event-and-background-source-refinement --fine 24-event8-3200 --coarse 24-3200 24-event8-3200-residual --bank event8 *> event-and-background-source-refinement.log
if ($LASTEXITCODE -ne 0) { throw 'Event comparison process failed.' }
& $python -B interpret_response.py --name response-interpretation --suffix 24-event8-3200 --bank event8 *> response-interpretation.log
if ($LASTEXITCODE -ne 0) { throw 'Response interpretation process failed.' }
