#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Builds clean, upload-ready copies of the three ModernTech packages in dist/.
.DESCRIPTION
    Windows port of tools/package.sh. Needs no bash, rsync or make: only Python
    (for tools/check_tyd.py) and PowerShell.

    The in-game Workshop uploader sends a mod's whole folder, so upload the
    copies in dist/, not the development folder (which also holds .git, tools
    and extras).
.EXAMPLE
    pwsh -File tools/package.ps1
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\package.ps1
#>
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root 'dist'

# Package name -> file extensions the Workshop uploader accepts for that mod type
$allowedExtensions = [ordered]@{
    'ModernTech'       = @('txt', 'xml', 'png', 'tyd', 'gltf', 'glb', 'obj')
    'ModernTech PCs'   = @('xml', 'png', 'obj', 'txt', 'tyd')
    'ModernTechDemand' = @('cs', 'jpg', 'jpeg', 'png', 'txt', 'tyd', 'ogg', 'mp3', 'wav', 'obj', 'gltf', 'glb')
}

function Copy-PackageTree {
    param(
        [Parameter(Mandatory)][string] $Source,
        [Parameter(Mandatory)][string] $Target,
        [string[]] $ExcludeDirectories = @(),
        [string[]] $ExcludeFiles = @(),
        [string[]] $ExcludePatterns = @()
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Missing source folder: $Source"
    }
    New-Item -ItemType Directory -Force -Path $Target | Out-Null

    Get-ChildItem -LiteralPath $Source -Recurse -File -Force | ForEach-Object {
        $relative = $_.FullName.Substring($Source.Length).TrimStart('\', '/')
        $segments = $relative -split '[\\/]'
        $leaf = $segments[-1]

        if ($segments | Where-Object { $ExcludeDirectories -contains $_ } | Select-Object -First 1) { return }
        if ($ExcludeFiles -contains $leaf) { return }
        if ($ExcludePatterns | Where-Object { $leaf -like $_ } | Select-Object -First 1) { return }

        $destination = Join-Path $Target $relative
        $directory = Split-Path -Parent $destination
        if (-not (Test-Path -LiteralPath $directory)) {
            New-Item -ItemType Directory -Force -Path $directory | Out-Null
        }
        Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
    }
}

# --- 1. Validate every TyD file before packaging anything -------------------
$python = Get-Command python, python3, py -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $python) {
    throw 'Python was not found on PATH; tools/check_tyd.py needs it.'
}
Write-Host 'Checking TyD files...' -ForegroundColor Cyan
& $python.Source -I (Join-Path $root 'tools\check_tyd.py')
if ($LASTEXITCODE -ne 0) {
    throw "tools/check_tyd.py reported problems (exit $LASTEXITCODE); not packaging."
}

# --- 2. Rebuild dist/ ------------------------------------------------------
if (Test-Path -LiteralPath $dist) {
    Remove-Item -LiteralPath $dist -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $dist | Out-Null

# Data package: everything at the repo root except development-only material
Copy-PackageTree -Source $root -Target (Join-Path $dist 'ModernTech') `
    -ExcludeDirectories @('.git', 'tools', 'extras', 'dist', 'downloads') `
    -ExcludeFiles @('README.md', 'LICENSE') `
    -ExcludePatterns @('.git*')

# Furniture package
Copy-PackageTree -Source (Join-Path $root 'extras\Furniture\ModernTech PCs') `
    -Target (Join-Path $dist 'ModernTech PCs')

# Code package, without Unity's cache leftovers
Copy-PackageTree -Source (Join-Path $root 'extras\DLLMods\ModernTechDemand') `
    -Target (Join-Path $dist 'ModernTechDemand') `
    -ExcludePatterns @('*.dcache', '*H.bin')

# --- 3. License into every package, as package.sh does ---------------------
foreach ($package in $allowedExtensions.Keys) {
    $folder = Join-Path $dist $package
    Copy-Item -LiteralPath (Join-Path $root 'LICENSE') -Destination (Join-Path $folder 'LICENSE.txt') -Force
}

# --- 4. Reject anything the Workshop uploader would refuse ------------------
$problems = @()
foreach ($package in $allowedExtensions.Keys) {
    $allowed = $allowedExtensions[$package]
    Get-ChildItem -LiteralPath (Join-Path $dist $package) -Recurse -File -Force | ForEach-Object {
        $extension = $_.Extension.TrimStart('.').ToLowerInvariant()
        if ($allowed -notcontains $extension) {
            $problems += "$package : $($_.FullName.Substring($dist.Length).TrimStart('\'))"
        }
    }
}
if ($problems.Count -gt 0) {
    Write-Host 'The Workshop uploader would reject these files:' -ForegroundColor Red
    $problems | ForEach-Object { Write-Host "  $_" }
    throw "Packaging failed: $($problems.Count) file(s) not allowed."
}

# --- 5. Downloadable archive for people who cannot use the Workshop --------
$downloads = Join-Path $root 'downloads'
New-Item -ItemType Directory -Force -Path $downloads | Out-Null

$install = @"
ModernTech - manual install
===========================

This zip holds three packages. Copy each one into a different folder of your
Software Inc install (Steam > Software Inc > Manage > Browse local files):

  ModernTech        ->  Mods\ModernTech              (required)
  ModernTech PCs    ->  Furniture\ModernTech PCs     (optional furniture)
  ModernTechDemand  ->  DLLMods\ModernTechDemand     (optional code mod)

Then start the game, open Options > Mods and tick what you copied. The first
time, the game asks you to allow the .cs code mod (ModernTech Demand).

New software types only appear in a new game; existing saves keep their markets.

Source and issues: https://github.com/erisparreshi369-dev/ModernTech
"@
Set-Content -Path (Join-Path $dist 'INSTALL.txt') -Value $install -Encoding ASCII

$archive = Join-Path $downloads 'ModernTech-packages.zip'
if (Test-Path -LiteralPath $archive) { Remove-Item -LiteralPath $archive -Force }
# Python's zipfile writes forward-slash entry names; .NET's Compress-Archive and
# ZipFile both write backslashes, which other tools extract as part of the name.
$archiveBase = $archive -replace '\.zip$', ''
& $python.Source -c "import shutil,sys; shutil.make_archive(sys.argv[1], 'zip', sys.argv[2])" $archiveBase $dist
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $archive)) {
    throw 'Could not build the download archive.'
}

# --- 6. Report -------------------------------------------------------------
Write-Host ''
Write-Host 'Packages in dist/:' -ForegroundColor Green
foreach ($package in $allowedExtensions.Keys) {
    $folder = Get-Item -LiteralPath (Join-Path $dist $package)
    $bytes = (Get-ChildItem -LiteralPath $folder.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $count = (Get-ChildItem -LiteralPath $folder.FullName -Recurse -File | Measure-Object).Count
    Write-Host ('  {0,-18} {1,6:N1} MB  ({2} files)' -f $package, ($bytes / 1MB), $count)
}
$archiveFile = Get-Item -LiteralPath $archive
Write-Host ''
Write-Host ('Download archive: downloads\{0} ({1:N1} MB)' -f $archiveFile.Name, ($archiveFile.Length / 1MB)) -ForegroundColor Green
Write-Host ''
Write-Host 'Upload from dist/ in Options > Mods, then copy the new SteamID'
Write-Host 'values from each meta.tyd back into the repo and commit them.'
