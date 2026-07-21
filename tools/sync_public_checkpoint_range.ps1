[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [int]$StartPrivate = 4501,
    [int]$EndPrivate = 5175,
    [int]$PublicOffset = 3984,
    [switch]$Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$sourceRootPath = (Resolve-Path -LiteralPath $SourceRoot).Path
$checkpointSource = $sourceRootPath
$scriptSource = Join-Path $sourceRootPath "scripts"
$residualSource = Join-Path $sourceRootPath "source-intake\mts_residuals"

$checkpointDestination = Join-Path $repositoryRoot "research-programme\checkpoints"
$scriptDestination = Join-Path $repositoryRoot "research-programme\scripts"
$residualDestination = Join-Path $repositoryRoot "research-programme\source-intake\mts_residuals"

if ($StartPrivate -gt $EndPrivate) {
    throw "StartPrivate must not exceed EndPrivate."
}

if (($StartPrivate - $PublicOffset) -lt 0) {
    throw "PublicOffset produces a negative public checkpoint number."
}

foreach ($requiredPath in @($checkpointSource, $scriptSource, $residualSource)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Container)) {
        throw "Required source directory does not exist: $requiredPath"
    }
}

$branch = (& git -C $repositoryRoot branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($branch)) {
    throw "Unable to determine the current Git branch."
}

if ($branch -in @("main", "master")) {
    throw "Refusing to publish from protected branch '$branch'."
}

function Test-CheckpointIdInRange {
    param([string]$Name)

    foreach ($match in [regex]::Matches($Name, "(?<!\d)(\d{4})(?!\d)")) {
        $checkpointId = [int]$match.Groups[1].Value
        if ($checkpointId -ge $StartPrivate -and $checkpointId -le $EndPrivate) {
            return $true
        }
    }

    return $false
}

$publicationRows = [System.Collections.Generic.List[object]]::new()

Get-ChildItem -LiteralPath $checkpointSource -File -Filter "*.md" |
    Where-Object {
        $_.Name -match "^(\d+)([A-Za-z]*)-(.+)$" -and
        [int]$Matches[1] -ge $StartPrivate -and
        [int]$Matches[1] -le $EndPrivate
    } |
    ForEach-Object {
        if ($_.Name -notmatch "^(\d+)([A-Za-z]*)-(.+)$") {
            throw "Unable to parse checkpoint filename: $($_.Name)"
        }

        $privateId = [int]$Matches[1]
        $suffix = $Matches[2]
        $remainder = $Matches[3]
        $publicId = $privateId - $PublicOffset
        $destinationName = "$publicId$suffix-$remainder"

        $publicationRows.Add([pscustomobject]@{
            Kind = "checkpoint"
            PrivateId = $privateId
            Source = $_.FullName
            Destination = Join-Path $checkpointDestination $destinationName
            Length = $_.Length
        })
    }

Get-ChildItem -LiteralPath $scriptSource -File -Filter "*.py" |
    Where-Object { Test-CheckpointIdInRange $_.Name } |
    ForEach-Object {
        $publicationRows.Add([pscustomobject]@{
            Kind = "script"
            PrivateId = $null
            Source = $_.FullName
            Destination = Join-Path $scriptDestination $_.Name
            Length = $_.Length
        })
    }

Get-ChildItem -LiteralPath $residualSource -File |
    Where-Object {
        $_.Extension -in @(".csv", ".json") -and
        (Test-CheckpointIdInRange $_.Name)
    } |
    ForEach-Object {
        if ($_.Length -gt 5MB) {
            throw "Residual artifact exceeds the 5 MiB publication ceiling: $($_.FullName)"
        }

        $publicationRows.Add([pscustomobject]@{
            Kind = "residual"
            PrivateId = $null
            Source = $_.FullName
            Destination = Join-Path $residualDestination $_.Name
            Length = $_.Length
        })
    }

$collisions = $publicationRows | Group-Object Destination | Where-Object Count -gt 1
if ($collisions) {
    $collisionNames = ($collisions.Name -join [Environment]::NewLine)
    throw "Destination collisions detected:$([Environment]::NewLine)$collisionNames"
}

$summary = $publicationRows |
    Group-Object Kind |
    Sort-Object Name |
    ForEach-Object {
        [pscustomobject]@{
            Kind = $_.Name
            Files = $_.Count
            MiB = [math]::Round((($_.Group | Measure-Object Length -Sum).Sum / 1MB), 3)
        }
    }

$summary | Format-Table -AutoSize
"TOTAL_FILES=$($publicationRows.Count)"
"TOTAL_MIB=$([math]::Round((($publicationRows | Measure-Object Length -Sum).Sum / 1MB), 3))"
"BRANCH=$branch"
"MODE=$(if ($Apply) { 'APPLY' } else { 'DRY_RUN' })"

if (-not $Apply) {
    return
}

foreach ($directory in @($checkpointDestination, $scriptDestination, $residualDestination)) {
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
}

foreach ($row in $publicationRows) {
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
    throw "Hash verification failed for $($hashFailures.Count) published files."
}

"HASH_VERIFIED=$($publicationRows.Count)"
