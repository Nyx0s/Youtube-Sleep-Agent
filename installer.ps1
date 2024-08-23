# PowerShell script to set up the environment, install dependencies, and run the Python script

# Ensure Python is installed and accessible in the PATH
$pythonPath = (Get-Command python).Source
if (-not $pythonPath) {
    Write-Host "Python is not installed or not found in PATH. Please install Python and try again."
    exit 1
}

# Create a new directory 'App'
$targetDir = "App"
if (-not (Test-Path -Path $targetDir)) {
    Write-Host "Creating directory 'App'..."
    New-Item -ItemType Directory -Path $targetDir
}

# Copy all necessary files to the 'App' directory
Write-Host "Copying files to 'App' directory..."
Copy-Item -Path "main.py", "requirements.txt", "config.ini" -Destination $targetDir

# Change to the 'App' directory
Set-Location -Path $targetDir

# Create a virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& "venv\Scripts\Activate"

# Upgrade pip and install distutils
Write-Host "Upgrading pip and installing distutils..."
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
python -m pip install --upgrade pywin32
python -m pip install --upgrade pyautogui
python -m pip install --upgrade keyboard
python -m pip install --upgrade sounddevice
python -m pip install --upgrade numpy
python -m pip install --upgrade configparser
python -m pip install --upgrade bootstrap-py
python -m pip install --upgrade wheel   
python -m pip install --upgrade pyinstaller


# Ensure config.ini exists
if (-not (Test-Path -Path "config.ini")) {
    Write-Host "config.ini not found. Creating a default config.ini..."
    @"
[settings]
INACTIVITY_TIMEOUT = 5
ISRUNNING = True
KILLFULLSCREEN = True
LOCKWORKSTATION = False
SHUTDOWN = False
KEEPRUNNING = True
AUDIO_THRESHOLD = 100
"@ | Out-File -FilePath "config.ini" -Encoding utf8
}

# Install pyinstaller
Write-Host "Installing pyinstaller..."
python -m pip install pyinstaller

# Bundle the script into an executable using PyInstaller
Write-Host "Bundling the script into an executable..."
pyinstaller --onefile --add-data "venv/;venv/." --add-data "config.ini/;config.ini/." --icon=your_icon.ico --windowed ".\main.py"

# Start the Python script
Write-Host "Starting the Python script..."
python ".\main.py"

# Keep the PowerShell window open
Read-Host "Press Enter to exit..."