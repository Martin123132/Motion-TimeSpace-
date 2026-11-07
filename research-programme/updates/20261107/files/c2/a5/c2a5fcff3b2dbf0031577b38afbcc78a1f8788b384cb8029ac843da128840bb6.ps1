$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
& $python -B verify_isotropic_reduction.py *> isotropic-reduction.log
if ($LASTEXITCODE -ne 0) { throw 'Angular reduction process failed.' }
$packet = Get-Content -LiteralPath 'results/isotropic-reduction/status.json' -Raw | ConvertFrom-Json
if (-not $packet.all_checks_passed) { throw 'Angular reduction check failed.' }
foreach ($model in @('heavy', 'cold')) {
    foreach ($specification in @(
        @{suffix='24-1600'; count=24; steps=1600; stride=1},
        @{suffix='24-3200'; count=24; steps=3200; stride=1},
        @{suffix='16-3200'; count=16; steps=3200; stride=1},
        @{suffix='24-coarse-3200'; count=24; steps=3200; stride=2}
    )) {
        $name = $model + $specification.suffix
        & $python -B run_mixed_waves.py --name $name --model $model --count $specification.count --steps $specification.steps --stride $specification.stride *> "$name.log"
        if ($LASTEXITCODE -ne 0) { throw "Wave process failed: $name" }
        $packet = Get-Content -LiteralPath "waves/$name/status.json" -Raw | ConvertFrom-Json
        if (-not $packet.all_checks_passed) { throw "Wave validation failed: $name" }
        Write-Output "Finished $name"
    }
}
& $python -B compare_mixed_waves.py --name initial-refinements --fine 24-3200 --coarse 24-1600 16-3200 24-coarse-3200 *> initial-refinements.log
if ($LASTEXITCODE -ne 0) { throw 'Comparison process failed.' }
