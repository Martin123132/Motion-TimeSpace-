param([string[]]$Suffixes = @('256', '384'))
$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
function Run-Checked {
    param([string]$Label, [string]$Packet, [string[]]$Arguments)
    if (Test-Path -LiteralPath $Packet) {
        $saved = Get-Content -Raw -LiteralPath $Packet | ConvertFrom-Json
        if ($saved.state -eq 'complete' -and $saved.all_checks_passed) {
            Write-Output "Retained completed $Label"
            return
        }
        throw "Nonaccepted packet $Packet; inspect before continuing"
    }
    & $python -B @Arguments *> (Join-Path $PSScriptRoot "diagnostics/$Label.log")
    if ($LASTEXITCODE -ne 0) { throw "Failed $Label; inspect log" }
    $saved = Get-Content -Raw -LiteralPath $Packet | ConvertFrom-Json
    if ($saved.state -ne 'complete' -or -not $saved.all_checks_passed) { throw "Acceptance failed $Label" }
    Write-Output "Completed $Label"
}
foreach ($suffix in $Suffixes) {
    $bank = "split-$suffix"
    Run-Checked "bank-$bank" "banks/$bank/status.json" @('build_partitioned_bank.py', '--name', $bank, '--points', $suffix)
    Run-Checked "elastic-$bank" "banks/$bank-elastic/status.json" @('cold_control.py', '--bank', $bank)
    foreach ($model in @('heavy', 'cold')) {
        Run-Checked "$model-$bank" "runs/$model-$bank/status.json" @('evolve_bank.py', '--bank', $bank, '--name', "$model-$bank", '--model', $model)
        Run-Checked "$model-$bank-elastic" "runs/$model-$bank-elastic/status.json" @('evolve_bank.py', '--bank', "$bank-elastic", '--name', "$model-$bank-elastic", '--model', $model)
    }
    Run-Checked "synthetic-$bank" "runs/synthetic-$bank/status.json" @('evolve_bank.py', '--bank', $bank, '--name', "synthetic-$bank", '--fixture', 'synthetic')
}
