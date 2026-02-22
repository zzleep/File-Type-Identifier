@echo off
REM Build Script for File Type Identifier GUI
REM This script creates a standalone executable for Windows

echo ========================================
echo File Type Identifier - Build Script
echo ========================================
echo.

REM Check if PyInstaller is installed
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1

if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Failed to install PyInstaller!
        pause
        exit /b 1
    )
    echo PyInstaller installed successfully!
) else (
    echo PyInstaller is already installed.
)

echo.
echo Building executable...
echo.

REM Build the executable
pyinstaller --name=FileTypeIdentifier --onefile --windowed --icon=NONE --add-data="default_signatures.json;." --add-data="src;src" --clean gui.py

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Build completed successfully!
    echo ========================================
    echo.
    echo Executable location: .\dist\FileTypeIdentifier.exe
    echo.
    echo You can now run the application by double-clicking:
    echo   .\dist\FileTypeIdentifier.exe
    echo.
) else (
    echo.
    echo Build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

pause
