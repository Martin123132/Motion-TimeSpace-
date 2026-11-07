$ErrorActionPreference = 'Stop'
$python = 'C:\Users\ollet\AppData\Local\Programs\Python\Python313\python.exe'
Set-Location -LiteralPath $PSScriptRoot
$diagnostics = Join-Path $PSScriptRoot 'diagnostics'
New-Item -ItemType Directory -Path $diagnostics -Force | Out-Null
$cases = @(
    @{ Tag='base'; Points=96; Polar=10; Step=0.01 },
    @{ Tag='time'; Points=96; Polar=10; Step=0.005 },
    @{ Tag='frequency'; Points=144; Polar=10; Step=0.005 },
    @{ Tag='fine'; Points=192; Polar=10; Step=0.005 },
    @{ Tag='angular'; Points=192; Polar=12; Step=0.005 }
)
foreach ($model in @('heavy', 'cold')) {
    foreach ($case in $cases) {
        foreach ($type in @('warm', 'elastic')) {
            $name = "$model-$type-$($case.Tag)"
            $statusPath = Join-Path $PSScriptRoot "runs\$name\status.json"
            if (Test-Path -LiteralPath $statusPath) {
                $status = Get-Content -LiteralPath $statusPath -Raw | ConvertFrom-Json
                if ($status.state -ne 'complete' -or -not $status.all_checks_passed) {
                    throw "Existing run is not accepted and will not be restarted: $name"
                }
                Write-Output "Already complete: $name"
                continue
            }
            $arguments = @('-B','evolve_defect.py','--model',$model,'--name',$name,
                '--points',"$($case.Points)",'--polar',"$($case.Polar)",'--step',"$($case.Step)")
            if ($type -eq 'elastic') { $arguments += '--cold' }
            & $python @arguments *>&1 | Tee-Object -FilePath (Join-Path $diagnostics "$name.log") | Select-Object -Last 1
            if ($LASTEXITCODE -ne 0) { throw "Run failed: $name" }
        }
    }
}
