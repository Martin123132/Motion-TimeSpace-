param([ValidateSet('half','double')][string]$Family,[switch]$ResumeSetupRepair)
$ErrorActionPreference='Stop'
$steps=@()
if($ResumeSetupRepair){
 if($Family -ne 'half'){throw 'only inspected half-k setup failure'}
 $root=Join-Path $PSScriptRoot $Family
 $prior=Get-Content -Raw -LiteralPath "$root/evolution-01.end.json"|ConvertFrom-Json
 $preflight=Get-Content -Raw -LiteralPath "$root/preflight-v2/preflight-result.json"|ConvertFrom-Json
 if($prior.exit_code -ne 1 -or -not $preflight.passed -or (Get-Content -Raw -LiteralPath "$root/evolution-01.stderr.log") -notmatch "NameError: name 'np' is not defined"){throw 'repair contract'}
}else{
 $steps+=,@('syntax-01','syntax.py')
 $steps+=,@('preflight-01','preflight.py')
}
$steps+=,@('evolution-v2-01','evolve_v2.py')
$steps+=,@('evolution-validation-01','validate_evolution_v2.py')
$steps+=,@('build-01','build.py')
$steps+=,@('adjoint-01','adjoint.py')
$steps+=,@('adjoint-validation-01','validate_adjoint.py')
$steps+=,@('primitive-01','primitive.py')
$steps+=,@('primitive-validation-01','validate_primitive.py')
$steps+=,@('volume-01','volume_dictionary.py')
foreach($step in $steps){
 Write-Output "$Family starting $($step[0])"
 & "$PSScriptRoot/run_phase_v2.ps1" -Family $Family -Label $step[0] -Script $step[1]
}
Write-Output "$Family all frozen phases complete"

