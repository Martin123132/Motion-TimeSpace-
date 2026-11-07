$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
$null = New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot 'diagnostics') -Force
function Run-StageCommand {
    param([string]$Label, [string]$Packet, [string[]]$Arguments)
    if (Test-Path -LiteralPath $Packet) {
        $saved = Get-Content -Raw -LiteralPath $Packet | ConvertFrom-Json
        if ($saved.state -eq 'complete' -and $saved.all_checks_passed) {
            Write-Output "Retained completed $Label"
            return
        }
        throw "Existing nonaccepted packet $Packet; inspect rather than restart"
    }
    & $python -B @Arguments *> (Join-Path $PSScriptRoot "diagnostics/$Label.log")
    if ($LASTEXITCODE -ne 0) { throw "Failed $Label; inspect saved log" }
    $saved = Get-Content -Raw -LiteralPath $Packet | ConvertFrom-Json
    if ($saved.state -ne 'complete' -or -not $saved.all_checks_passed) { throw "Acceptance failed $Label" }
    Write-Output "Completed $Label"
}
Run-StageCommand 'bank-192-refined' 'banks/main-192-refined/status.json' @('build_bank.py','--name','main-192-refined','--points','192','--order','8','--cell-order','6')
Run-StageCommand 'bank-224-band' 'banks/main-224-band/status.json' @('build_bank.py','--name','main-224-band','--points','224','--order','8','--cell-order','6','--minimum','.0003','--maximum-frequency','40')
foreach ($suffix in @('96','144','192','192-refined','224-band')) {
    $bank = "main-$suffix"
    Run-StageCommand "elastic-$suffix" "banks/$bank-elastic/status.json" @('cold_control.py','--bank',$bank)
    foreach ($model in @('heavy','cold')) {
        Run-StageCommand "$model-$suffix" "runs/$model-$suffix/status.json" @('evolve_bank.py','--bank',$bank,'--name',"$model-$suffix",'--model',$model)
        Run-StageCommand "$model-$suffix-elastic" "runs/$model-$suffix-elastic/status.json" @('evolve_bank.py','--bank',"$bank-elastic",'--name',"$model-$suffix-elastic",'--model',$model)
    }
    Run-StageCommand "synthetic-$suffix" "runs/synthetic-$suffix/status.json" @('evolve_bank.py','--bank',$bank,'--name',"synthetic-$suffix",'--fixture','synthetic')
}
