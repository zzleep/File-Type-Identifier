# Build Script for File Type Identifier GUI
# This script creates a standalone executable for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "File Type Identifier - Build Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
Write-Host "Checking for PyInstaller..." -ForegroundColor Yellow
$pyinstallerCheck = & python -m pip list | Select-String "pyinstaller"

if (-not $pyinstallerCheck) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    & python -m pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install PyInstaller!" -ForegroundColor Red
        exit 1
    }
    Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
} else {
    Write-Host "PyInstaller is already installed." -ForegroundColor Green
}

Write-Host ""
Write-Host "Building executable..." -ForegroundColor Yellow
Write-Host ""

# Build the executable
& pyinstaller `
    --name="FileTypeIdentifier" `
    --onefile `
    --windowed `
    --icon=NONE `
    --add-data="default_signatures.json;." `
    --add-data="src;src" `
    --clean `
    gui.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: .\dist\FileTypeIdentifier.exe" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run the application by double-clicking:" -ForegroundColor Yellow
    Write-Host "  .\dist\FileTypeIdentifier.exe" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
    exit 1
}
