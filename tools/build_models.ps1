#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Rebuilds every ModernTech 3D model, texture and thumbnail with Blender.
.DESCRIPTION
    Runs tools/build_models.py headlessly. Finds Blender automatically:
      1. -BlenderPath parameter
      2. BLENDER_EXE environment variable
      3. blender.exe on PATH
      4. the usual install locations, preferring 5.2.x (the version the
         committed assets in this repo were built with)
.EXAMPLE
    pwsh -File tools/build_models.ps1
.EXAMPLE
    powershell -NoProfile -ExecutionPolicy Bypass -File tools\build_models.ps1
.EXAMPLE
    pwsh -File tools/build_models.ps1 -BlenderPath 'C:\Program Files\Blender Foundation\Blender 4.5\blender.exe'
#>
[CmdletBinding()]
param(
    [string] $BlenderPath
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$script = Join-Path $root 'tools\build_models.py'

function Find-Blender {
    if ($BlenderPath) {
        if (-not (Test-Path -LiteralPath $BlenderPath)) { throw "No Blender at '$BlenderPath'." }
        return (Resolve-Path -LiteralPath $BlenderPath).Path
    }
    if ($env:BLENDER_EXE -and (Test-Path -LiteralPath $env:BLENDER_EXE)) {
        return $env:BLENDER_EXE
    }
    $onPath = Get-Command blender -ErrorAction SilentlyContinue
    if ($onPath) { return $onPath.Source }

    $candidates = @()
    foreach ($pattern in @(
            (Join-Path $env:ProgramFiles 'Blender Foundation\Blender*\blender.exe'),
            (Join-Path $env:USERPROFILE 'Blender\blender-*\blender.exe'),
            (Join-Path $env:LOCALAPPDATA 'Programs\Blender Foundation\Blender*\blender.exe'))) {
        $candidates += Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue -File
    }
    $candidates = @($candidates | Sort-Object FullName -Unique)
    if ($candidates.Count -eq 0) {
        throw 'Blender not found. Install it, put blender.exe on PATH, or pass -BlenderPath.'
    }
    $preferred = $candidates | Where-Object { $_.FullName -match 'blender[-_ ]?5\.2' } | Select-Object -Last 1
    if ($preferred) { return $preferred.FullName }
    return ($candidates | Select-Object -Last 1).FullName
}

$blender = Find-Blender
Write-Host "Using $blender" -ForegroundColor Cyan

Push-Location $root
try {
    & $blender -b -P $script
    $code = $LASTEXITCODE
}
finally {
    Pop-Location
}

if ($code -ne 0) {
    throw "Blender exited with code $code; models were not rebuilt."
}

Write-Host ''
Write-Host 'Models rebuilt. Check the diff:' -ForegroundColor Green
Write-Host '  git status --short'
