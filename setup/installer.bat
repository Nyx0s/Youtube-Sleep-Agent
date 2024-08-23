@echo off
REM Ensure Python is installed and accessible in the PATH
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not found in PATH. Please install Python and try again.
    exit /b 1
)

REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install the dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pyautogui keyboard sounddevice numpy pypiwin32

REM Start the Python script
echo Starting the Python script...
python "your_script.py"

REM Keep the command prompt open
pause
