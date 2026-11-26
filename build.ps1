# Build the site and capture the latest CMS snapshot for deployment
$ErrorActionPreference = "Stop"

Write-Host "Building site and creating CMS snapshot..." -ForegroundColor Cyan
Set-Location (Join-Path $PSScriptRoot "frontend")
npm run build
Write-Host "Build complete! Snapshot updated in frontend/src/data/cms-snapshot.json." -ForegroundColor Green
