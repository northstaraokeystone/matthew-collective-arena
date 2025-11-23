# run.ps1 — Cruella's One-Click Carnage Launcher
# Double-click or run .\run.ps1
# The coat starts filling the second you hit Enter.

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "`n🧥🧥🧥🧥 CRUELLA MATTHEW AWAKENS 🧥🧥🧥`n" -ForegroundColor Red

# Activate or create venv
if (-Not (Test-Path "venv")) {
    Write-Host "No virtual coat found. Sewing one from scratch, darling..." -ForegroundColor Cyan
    python -m venv venv
}

& ".\venv\Scripts\Activate.ps1"

# Install requirements if Streamlit is missing
python -c "import streamlit" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Streamlit is not dressed in rags. Upgrading the wardrobe..." -ForegroundColor Yellow
    pip install -r requirements.txt --upgrade
}

# Launch dashboard in a new window
Write-Host "Opening Cruella's viewing lounge..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit -Command", "Set-Location '$ScriptDir'; streamlit run dashboard.py --server.port=8501" -WindowStyle Normal

Start-Sleep -Seconds 4
Write-Host "Dashboard live at http://localhost:8501`n" -ForegroundColor Cyan

Write-Host "Releasing the 101 puppies into the arena...`n" -ForegroundColor Red

# Run the arena — this is where the screaming happens
python arena.py

Write-Host "`n`nThe coat is finished... or you ran away.`nEither way, I look divine. 🧥🚬" -ForegroundColor Red

Read-Host "Press Enter to close the slaughterhouse window"