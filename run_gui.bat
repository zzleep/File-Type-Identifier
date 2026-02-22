@echo off
REM Quick launcher for the GUI application
REM Double-click this file to run the GUI from source

echo Starting File Type Identifier GUI...
python gui.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Failed to start the GUI.
    echo Make sure Python is installed and all files are present.
    pause
)
