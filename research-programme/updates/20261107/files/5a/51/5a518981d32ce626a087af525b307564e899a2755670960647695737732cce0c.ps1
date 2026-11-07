param([string]$Bridge='C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102')
$ErrorActionPreference='Stop'
$post=Split-Path -Parent $PSScriptRoot
$root=Join-Path $post 'mts-local-gr-transfer-20261106'
$paths=[ordered]@{
    archive=Join-Path $root 'Rotmod_LTG.zip'
    cohort=Join-Path $Bridge 'plateau-pressure-junction/junction-rows.csv'
    outer=Join-Path $Bridge 'retained-local-galactic-transfer-v2/outermost-one-per-galaxy.csv'
    growth=Join-Path $post 'condensate-origin-20261003/matter-growth-response-20261006/results/scan/status.json'
}
$hashes=@('0a80cc90714828cc28b7dd57923576714d209f2490328c087c4a4ad607faf588','8ccbfde28236ed7d3453e2cf2f9d6c8b02be2595f436635e5a72efa69ffec2c6','444402205662f1807c8a57987e867e1e0ed8841a180ff65c6065398f512624ba','d654f5afaf0afda26ed519f9b95d1ce4a7c3e333722c631e561c298a4743e50a')
$index=0
foreach($path in $paths.Values){
    if((Get-FileHash -LiteralPath $path).Hash -ne $hashes[$index]){throw "Changed input $path"}
    $index++
}
$growth=Get-Content -LiteralPath $paths.growth -Raw | ConvertFrom-Json
$examples=@($growth.rows | Where-Object { $_.model -like '*zero*' -and $_.heavy_fraction -eq .5 -and $_.preparation -eq 'equal' -and $_.mass_over_H0 -gt 6.4196e8 -and $_.mass_over_H0 -lt 6.4197e8 -and $_.accepted })
$mass=@($examples.mass_eV|Select-Object -Unique)
if($mass.Count -ne 1 -or $mass[0] -le 0){throw 'Retained mass selection ambiguous'}
$outer=@{}
foreach($row in (Import-Csv -LiteralPath $paths.outer)){$outer.Add($row.galaxy,$row)}
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip=[IO.Compression.ZipFile]::OpenRead($paths.archive)
try{
    $profiles=@(foreach($row in (Import-Csv -LiteralPath $paths.cohort)){
        $entries=@($zip.Entries|Where-Object Name -eq ($row.galaxy+'_rotmod.dat'))
        if($entries.Count -ne 1){throw "Missing or duplicate profile for $($row.galaxy)"}
        $reader=[IO.StreamReader]::new($entries[0].Open())
        try{$lines=$reader.ReadToEnd().Split([char]10)}finally{$reader.Dispose()}
        $points=@(foreach($line in $lines){
            $line=$line.Trim()
            if(!$line -or $line.StartsWith('#')){continue}
            $parts=$line -split '\s+'
            if($parts.Count -lt 6){throw 'SPARC row truncated'}
            ,([double[]]$parts[0..5])
        })
        if($points.Count -lt 2){throw "Insufficient parsed rows for $($row.galaxy)"}
        $radius=[double]$outer[$row.galaxy].radius_kpc
        if([math]::Abs($radius-[double]$row.radius_kpc) -gt 1e-12*$radius){throw 'Junction radius not the same outer point'}
        [ordered]@{name=$row.galaxy;outerRadius=$radius;flatSpeed=[double]$row.flat_km_s;outerDeficit=[double]$outer[$row.galaxy].observed_squared_minus_baryons;points=$points}
    })
}finally{$zip.Dispose()}
[ordered]@{profiles=$profiles;massEV=[double]$mass[0];inputs=$paths;sha256=$hashes}|ConvertTo-Json -Depth 7 -Compress
