# Start both backend CMS (FastAPI) and frontend site (Astro) for local development
$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Starting Portfolio Backend & Frontend " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Start Backend in a separate window
$backendDir = Join-Path $PSScriptRoot "backend"
$runBackendScript = Join-Path $backendDir "run.ps1"

Write-Host "Launching Content Backend at http://127.0.0.1:8000/back ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", "`"$runBackendScript`""

# 2. Wait a moment for backend to initialize
Start-Sleep -Seconds 3

# 3. Launch Frontend in another window
$frontendDir = Join-Path $PSScriptRoot "frontend"
Write-Host "Launching Astro Frontend at http://localhost:4321 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd `"$frontendDir`"; npm run dev"

Write-Host ""
Write-Host "Done! Two development windows have been opened:" -ForegroundColor Yellow
Write-Host "  * Admin Panel: http://127.0.0.1:8000/back" -ForegroundColor Cyan
Write-Host "  * Website:     http://localhost:4321" -ForegroundColor Cyan
Write-Host ""
