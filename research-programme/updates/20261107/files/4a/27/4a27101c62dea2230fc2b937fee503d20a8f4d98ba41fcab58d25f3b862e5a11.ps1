$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$theta = (4.596201578526332e-5 * [Math]::Pow(10.0, 7.5/8.0)).ToString('R', [Globalization.CultureInfo]::InvariantCulture)
foreach ($variant in @(
    @{Name='midpoint16'; Events=6; Quadrature=300},
    @{Name='midpoint16-event8'; Events=8; Quadrature=300},
    @{Name='midpoint16-quadrature420'; Events=8; Quadrature=420}
)) {
    $name = $variant.Name
    & $python -B './build_stable_kernel.py' --name $name --count 16 --theta $theta --event-order $variant.Events --quadrature $variant.Quadrature *> "./$name.log"
    if ($LASTEXITCODE -ne 0) { throw "$name failed" }
    Write-Output "$name complete"
}
foreach ($script in @('verify_temperature_interpolation', 'verify_expanding_background', 'mixed_pair_jacobian', 'acquire_primary_source')) {
    & $python -B "./$script.py" *> "./$script.log"
    if ($LASTEXITCODE -ne 0) { throw "$script failed" }
    Get-Content -LiteralPath "./$script.log" -Tail 1
}
