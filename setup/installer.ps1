# PowerShell script to set up the environment, install dependencies, and run the Python script

# Ensure Python is installed and accessible in the PATH
$pythonPath = (Get-Command python).Source
if (-not $pythonPath) {
    Write-Host "Python is not installed or not found in PATH. Please install Python and try again."
    exit 1
}

# Create a virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& "venv\Scripts\Activate"

# Install the dependencies
Write-Host "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install pyautogui keyboard sounddevice numpy pypiwin32

# Start the Python script
Write-Host "Starting the Python script..."
python "..\main.py"

# Keep the PowerShell window open
Read-Host "Press Enter to exit..."
