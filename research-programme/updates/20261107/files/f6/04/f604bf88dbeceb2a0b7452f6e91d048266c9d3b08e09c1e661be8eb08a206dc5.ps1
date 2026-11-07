$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach ($count in @(16,24)) {
    foreach ($index in 1..8) {
        $name = "stable$count-t$index"
        $packet = "banks/$name/status.json"
        if (Test-Path -LiteralPath $packet) {
            $saved = Get-Content -Raw -LiteralPath $packet | ConvertFrom-Json
            if ($saved.state -eq 'complete' -and $saved.all_checks_passed) { continue }
            throw "Existing nonaccepted $name"
        }
        $theta = (4.596201578526332e-5 * [Math]::Pow(10.0,$index/8.0)).ToString('R',[Globalization.CultureInfo]::InvariantCulture)
        & $python -B './build_stable_kernel.py' --name $name --count $count --theta $theta *> "./$name.log"
        if ($LASTEXITCODE -ne 0) { throw "Failed $name" }
        $saved = Get-Content -Raw -LiteralPath $packet | ConvertFrom-Json
        if (-not $saved.all_checks_passed) { throw "Nonaccepted $name" }
        Write-Output "Completed $name"
    }
}
