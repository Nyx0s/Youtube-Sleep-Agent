# PowerShell script to set up the environment, install dependencies, and run the Python script

# Function to check if Visual C++ Redistributable is installed
function Test-VisualCPlusPlusInstalled {
    $vcKeys = @(
        "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x86",
        "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
    )
    foreach ($key in $vcKeys) {
        if (Test-Path $key) {
            return $true
        }
    }
    return $false
}

# Download and install the latest Visual C++ Redistributable
if (-not (Test-VisualCPlusPlusInstalled)) {
    Write-Host "Visual C++ Redistributable not found. Downloading and installing the latest version..."

    # Set download URL and destination path
    $vcRedistUrl = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
    $vcRedistInstaller = "vc_redist.x64.exe"

    # Download the installer
    Invoke-WebRequest -Uri $vcRedistUrl -OutFile $vcRedistInstaller

    # Install the Redistributable silently
    Start-Process -FilePath $vcRedistInstaller -ArgumentList "/quiet", "/norestart" -Wait

    # Clean up the installer file
    Remove-Item $vcRedistInstaller

    Write-Host "Visual C++ Redistributable installed successfully."
} else {
    Write-Host "Visual C++ Redistributable is already installed."
}

# Ensure Python is installed and accessible in the PATH
try {
    $pythonPath = (Get-Command python).Source
} catch {
    Write-Host "Python is not installed or not found in PATH. Please install Python and try again."
    exit 1
}

# Create a new directory 'App' if it doesn't exist
$targetDir = "App"
if (-not (Test-Path -Path $targetDir)) {
    Write-Host "Creating directory 'App'..."
    New-Item -ItemType Directory -Path $targetDir
}

# Copy all necessary files to the 'App' directory
Write-Host "Copying files to 'App' directory..."
$filesToCopy = @("main.py", "requirements.txt", "config.ini")
foreach ($file in $filesToCopy) {
    if (Test-Path $file) {
        Copy-Item -Path $file -Destination $targetDir
    } else {
        Write-Host "$file not found."
    }
}

# Change to the 'App' directory
Set-Location -Path $targetDir

# Create a virtual environment
Write-Host "Creating virtual environment..."
python -m venv venv

# Activate the virtual environment
Write-Host "Activating virtual environment..."
& "venv\Scripts\Activate"

# Upgrade pip and install necessary packages
Write-Host "Upgrading pip and installing dependencies..."
$packages = @("pip", "setuptools", "pywin32", "pyautogui", "keyboard", "sounddevice", "numpy", "bootstrap-py", "wheel", "pyinstaller")
foreach ($pkg in $packages) {
    python -m pip install --upgrade $pkg

}


# Bundle the script into an executable using PyInstaller with hidden imports
Write-Host "Bundling the script into an executable..."
$hiddenImports = "setuptools,pywin32,pyautogui,keyboard,sounddevice,numpy,bootstrap-py,wheel,pyinstaller"
pyinstaller --onefile --console --hidden-import $hiddenImports "main.py"

# Run the Python script
Write-Host "Starting the Python script..."
python ".\main.py"

# Keep the PowerShell window open
Read-Host "Press Enter to exit..."
