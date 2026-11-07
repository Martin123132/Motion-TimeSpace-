$ErrorActionPreference='Stop'
$env:MTS_CPU='2'
$python='C:/Users/ollet/AppData/Local/Programs/Python/Python313/python.exe'
Set-Location -LiteralPath $PSScriptRoot
foreach($upper in @('.04','.02')){
    & $python -B refine_response.py --upper $upper --dry-run
    if($LASTEXITCODE -ne 0){throw 'Preflight failed'}
}
foreach($upper in @('.04','.02')){
    & $python -B refine_response.py --upper $upper
    if($LASTEXITCODE -ne 0){throw 'Response calculation failed'}
}
& $python -B compare_response_time.py
if($LASTEXITCODE -ne 0){throw 'Response comparison failed'}
& $python -B audit_response_equations.py
if($LASTEXITCODE -ne 0){throw 'Physical equation audit failed'}
