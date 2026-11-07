$ErrorActionPreference = 'Stop'
$env:OMP_NUM_THREADS = '1'
$env:OPENBLAS_NUM_THREADS = '1'
$env:MKL_NUM_THREADS = '1'
$env:NUMEXPR_NUM_THREADS = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'

function Run-Checked {
    param([string[]]$Arguments)
    & $python -B @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Worker exited with code $LASTEXITCODE" }
}

Run-Checked -Arguments @('verify_dense_derivative.py')
Run-Checked -Arguments @('verify_br_jacobian.py')
foreach ($model in @('heavy', 'cold')) {
    Run-Checked -Arguments @('verify_emitting_geometry_v3.py', '--model', $model, '--background', "$model-ir96-integrated-6400", '--name', "$model-emitting-geometry-v3")
    foreach ($suffix in @('q1000', 'e8', 'lowcut', 't17')) {
        Run-Checked -Arguments @('evolve_integrated_background.py', '--bank', "infrared96-$suffix", '--model', $model, '--steps', '6400', '--name', "$model-ir96-$suffix-6400")
        Run-Checked -Arguments @('compare_backgrounds_v2.py', '--fine', "$model-ir96-$suffix-6400", '--coarse', "$model-ir96-integrated-6400", '--name', "$model-integrated-$suffix-refinement")
    }
    Run-Checked -Arguments @('evolve_integrated_background.py', '--bank', 'infrared96-q700', '--model', $model, '--steps', '6400', '--quadrature', '1400', '--temperature-knots', '161', '--name', "$model-ir96-emissionfine-6400")
    Run-Checked -Arguments @('compare_backgrounds_v2.py', '--fine', "$model-ir96-emissionfine-6400", '--coarse', "$model-ir96-integrated-6400", '--name', "$model-integrated-emission-refinement")
    foreach ($count in @(88, 96)) {
        Run-Checked -Arguments @('evolve_infrared_background.py', '--bank', "infrared$count-q700", '--model', $model, '--steps', '3200', '--name', "$model-ir$count-polynomialdc-3200")
    }
    Run-Checked -Arguments @('compare_backgrounds_v2.py', '--fine', "$model-ir96-polynomialdc-3200", '--coarse', "$model-ir88-polynomialdc-3200", '--name', "$model-polynomialdc-infrared96-over88")
    foreach ($control in @('none', 'dc')) {
        Run-Checked -Arguments @('evolve_integrated_background.py', '--bank', 'infrared88-q700', '--model', $model, '--steps', '6400', '--emission', $control, '--name', "$model-ir88-$control-6400")
        Run-Checked -Arguments @('compare_backgrounds_v2.py', '--fine', "$model-ir96-$control-6400", '--coarse', "$model-ir88-$control-6400", '--name', "$model-integrated$control-infrared96-over88")
    }
}
Run-Checked -Arguments @('compare_geometry_coordinates.py')
