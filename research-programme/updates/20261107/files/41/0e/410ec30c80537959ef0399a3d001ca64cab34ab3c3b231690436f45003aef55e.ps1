$ErrorActionPreference = 'Stop'
$python = 'C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
$stopAt = [DateTimeOffset]::Parse('2026-10-25T00:30:00+00:00')
Set-Location -LiteralPath $PSScriptRoot
foreach ($phase in @('prediction', 'actual')) {
    $seconds = [Math]::Max(0, ($stopAt - [DateTimeOffset]::UtcNow).TotalSeconds)
    if ($seconds -lt 300) {
        Write-Output 'Safe deadline reached before another numerical phase.'
        exit 0
    }
    & $python -B .\source207.py $phase --seconds $seconds 2>&1 | Tee-Object -FilePath .\execution.log -Append
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $progress = Get-Content -LiteralPath .\progress.json -Raw | ConvertFrom-Json
    if ($progress.state -ne ($phase + '_complete')) {
        Write-Output 'Saved at an event boundary; resume rather than restart completed events.'
        exit 0
    }
    if ($phase -eq 'prediction') {
        & $python -B .\source207.py freeze 2>&1 | Tee-Object -FilePath .\execution.log -Append
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
& $python -B .\assess207.py assess 2>&1 | Tee-Object -FilePath .\execution.log -Append
exit $LASTEXITCODE
