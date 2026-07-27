[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$source = Join-Path $sourceRootPath "source-intake\functional_rg\5176"
$destination = Join-Path $repositoryRoot "research-programme\protocols\1192"

if (-not (Test-Path -LiteralPath $source -PathType Container)) {
    throw "Checkpoint-5176 source directory does not exist: $source"
}

$branch = (& git -C $repositoryRoot branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($branch)) {
    throw "Unable to determine the current Git branch."
}
if ($branch -in @("main", "master")) {
    throw "Refusing to publish from protected branch '$branch'."
}

$topLevelNames = @(
    "ensemble_protocol.json",
    "paired_ensemble_results.json",
    "paired_ensemble_statistics.csv",
    "paired_seed_scores.csv",
    "predeclared_seed_schedule.csv",
    "route_decision.csv",
    "runner_freeze.json",
    "seed_execution_status.csv",
    "source_provenance.csv"
)
$seedLevelNames = @(
    "COMPLETE.marker",
    "forward_scores.csv",
    "phase_diagnostics.csv",
    "seed_result.json",
    "status.json"
)

$publicationRows = [System.Collections.Generic.List[object]]::new()
foreach ($name in $topLevelNames) {
    $sourcePath = Join-Path $source $name
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Missing top-level snapshot source: $sourcePath"
    }
    $publicationRows.Add([pscustomobject]@{
        Kind = "aggregate"
        Source = $sourcePath
        Destination = Join-Path $destination $name
        Length = (Get-Item -LiteralPath $sourcePath).Length
    })
}

$seedDirectories = @(
    Get-ChildItem -LiteralPath (Join-Path $source "seeds") -Directory |
        Where-Object { $_.Name -match "^seed_\d{2}_\d+$" } |
        Sort-Object Name
)
if ($seedDirectories.Count -ne 12) {
    throw "Expected 12 completed seed directories, found $($seedDirectories.Count)."
}

foreach ($seedDirectory in $seedDirectories) {
    foreach ($name in $seedLevelNames) {
        $sourcePath = Join-Path $seedDirectory.FullName $name
        if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
            throw "Missing compact seed snapshot source: $sourcePath"
        }
        $publicationRows.Add([pscustomobject]@{
            Kind = "seed"
            Source = $sourcePath
            Destination = Join-Path (Join-Path $destination "seeds\$($seedDirectory.Name)") $name
            Length = (Get-Item -LiteralPath $sourcePath).Length
        })
    }
}

$oversized = @($publicationRows | Where-Object Length -gt 5MB)
if ($oversized.Count -gt 0) {
    throw "A compact snapshot artifact exceeds 5 MiB: $($oversized[0].Source)"
}

$publicationRows |
    Group-Object Kind |
    Sort-Object Name |
    ForEach-Object {
        [pscustomobject]@{
            Kind = $_.Name
            Files = $_.Count
            KiB = [math]::Round((($_.Group | Measure-Object Length -Sum).Sum / 1KB), 3)
        }
    } |
    Format-Table -AutoSize

"TOTAL_FILES=$($publicationRows.Count)"
"TOTAL_KIB=$([math]::Round((($publicationRows | Measure-Object Length -Sum).Sum / 1KB), 3))"
"BRANCH=$branch"
"MODE=$(if ($Apply) { 'APPLY' } else { 'DRY_RUN' })"

if (-not $Apply) {
    return
}

foreach ($row in $publicationRows) {
    $parent = Split-Path -Parent $row.Destination
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item -LiteralPath $row.Source -Destination $row.Destination -Force
}

$hashFailures = [System.Collections.Generic.List[string]]::new()
foreach ($row in $publicationRows) {
    $sourceHash = (Get-FileHash -LiteralPath $row.Source -Algorithm SHA256).Hash
    $destinationHash = (Get-FileHash -LiteralPath $row.Destination -Algorithm SHA256).Hash
    if ($sourceHash -ne $destinationHash) {
        $hashFailures.Add($row.Destination)
    }
}
if ($hashFailures.Count -gt 0) {
    throw "Hash verification failed for $($hashFailures.Count) snapshot files."
}

"HASH_VERIFIED=$($publicationRows.Count)"
