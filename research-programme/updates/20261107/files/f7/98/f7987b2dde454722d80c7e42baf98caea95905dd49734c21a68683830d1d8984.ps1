$ErrorActionPreference = 'Stop'
$env:MTS_CPU = '2'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot

function Invoke-StageScript {
    param([string]$Script, [string[]]$Arguments)
    & $python -B $Script @Arguments
    if ($LASTEXITCODE -ne 0) { throw "$Script exited with $LASTEXITCODE" }
}

Invoke-StageScript 'compare_repaired_inner.py' @()
foreach ($upper in @('0.04', '0.02')) {
    Invoke-StageScript 'build_dc_cache.py' @('--upper', $upper)
}
foreach ($upper in @('0.04', '0.02')) {
    $order = if ($upper -eq '0.04') { '8' } else { '6' }
    $window = if ($upper -eq '0.04') { '40' } else { '20' }
    foreach ($case in @(@('fine','4','5120'), @('fine','4','10240'), @('space','4','5120'), @('fine','6','5120'))) {
        $variant, $points, $steps = $case
        Invoke-StageScript 'build_repaired_sources.py' @('--upper',$upper,'--event-order',$order,'--variant',$variant,'--points',$points,'--inner-steps',$steps)
        $source = "sources-$variant-p$points-n$steps-o$order-q32-m$window"
        Invoke-StageScript 'propagate_repaired_feedback.py' @('--source',$source,'--steps','2048')
        if ($variant -eq 'fine' -and $points -eq '4' -and $steps -eq '5120') {
            Invoke-StageScript 'propagate_repaired_feedback.py' @('--source',$source,'--steps','1024')
        }
    }
}
Invoke-StageScript 'build_repaired_sources.py' @('--upper','0.04','--event-order','6')
Invoke-StageScript 'propagate_repaired_feedback.py' @('--source','sources-fine-p4-n5120-o6-q32-m40','--steps','2048')
Invoke-StageScript 'compare_repaired_feedback.py' @()
