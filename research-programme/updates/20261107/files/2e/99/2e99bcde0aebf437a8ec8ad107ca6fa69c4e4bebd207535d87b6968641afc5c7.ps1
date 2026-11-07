param([ValidateSet('half','double')][string]$Family)
$ErrorActionPreference='Stop'
$steps=@(
 @('syntax-01','syntax.py'),
 @('preflight-01','preflight.py'),
 @('evolution-01','evolve.py'),
 @('evolution-validation-01','validate_evolution.py'),
 @('build-01','build.py'),
 @('adjoint-01','adjoint.py'),
 @('adjoint-validation-01','validate_adjoint.py'),
 @('primitive-01','primitive.py'),
 @('primitive-validation-01','validate_primitive.py'),
 @('volume-01','volume_dictionary.py')
)
foreach($step in $steps){
 Write-Output "$Family starting $($step[0])"
 & "$PSScriptRoot/run_phase.ps1" -Family $Family -Label $step[0] -Script $step[1]
}
Write-Output "$Family all frozen phases complete"

