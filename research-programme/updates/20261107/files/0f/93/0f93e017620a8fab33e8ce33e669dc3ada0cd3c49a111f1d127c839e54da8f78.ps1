$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'run_partitioned_refinements.ps1') -Suffixes @()
Run-Checked 'quadrature-repair' 'results/quadrature-repair/status.json' @('verify_partitioned_quadrature.py')
Run-Checked 'bank-split-384-refined' 'banks/split-384-refined/status.json' @('build_partitioned_bank.py', '--name', 'split-384-refined', '--points', '384', '--order', '10', '--cell-order', '6')
Run-Checked 'bank-split-448-band' 'banks/split-448-band/status.json' @('build_partitioned_bank.py', '--name', 'split-448-band', '--points', '448', '--order', '10', '--cell-order', '6', '--minimum', '1e-6', '--maximum-frequency', '80')
foreach ($bank in @('split-384-refined', 'split-448-band')) {
    Run-Checked "elastic-$bank" "banks/$bank-elastic/status.json" @('cold_control.py', '--bank', $bank)
    foreach ($model in @('heavy', 'cold')) {
        Run-Checked "$model-$bank" "runs/$model-$bank/status.json" @('evolve_bank.py', '--bank', $bank, '--name', "$model-$bank", '--model', $model)
        Run-Checked "$model-$bank-elastic" "runs/$model-$bank-elastic/status.json" @('evolve_bank.py', '--bank', "$bank-elastic", '--name', "$model-$bank-elastic", '--model', $model)
    }
    Run-Checked "synthetic-$bank" "runs/synthetic-$bank/status.json" @('evolve_bank.py', '--bank', $bank, '--name', "synthetic-$bank", '--fixture', 'synthetic')
}
Run-Checked 'split-events' 'results/split-events/status.json' @('compare_partitioned.py', '--first', 'split-384', '--second', 'split-384-refined', '--name', 'split-events')
Run-Checked 'split-band' 'results/split-band/status.json' @('compare_partitioned.py', '--first', 'split-384-refined', '--second', 'split-448-band', '--name', 'split-band')
