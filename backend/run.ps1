# One-shot start for the content backend.
# Creates the virtualenv and .env on first run, then serves on http://127.0.0.1:8000

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Installing dependencies..." -ForegroundColor Cyan
& ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt --quiet

if (-not (Test-Path ".env")) {
    Write-Host "Creating .env with a generated SECRET_KEY..." -ForegroundColor Cyan
    $secret = -join ((1..48) | ForEach-Object { '{0:x}' -f (Get-Random -Max 16) })
    (Get-Content ".env.example") -replace `
        "^SECRET_KEY=.*", "SECRET_KEY=$secret" | Set-Content ".env" -Encoding utf8
    Write-Host "Default login is admin / change-me - change it at /back/account." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Admin panel:  http://127.0.0.1:8000/back" -ForegroundColor Green
Write-Host "API docs:     http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host ""

& ".venv\Scripts\python.exe" -m uvicorn app.main:app --reload --port 8000
