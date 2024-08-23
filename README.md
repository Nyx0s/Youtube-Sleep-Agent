# Full-Screen Application Monitor

## Overview
This script monitors full-screen applications on your system, specifically targeting YouTube in a web browser (e.g., Brave). It detects inactivity based on the screen content and audio playback, and can take actions such as exiting full-screen mode, locking the workstation, or shutting down the system.

## Features
- Monitors YouTube in full-screen mode for inactivity.
- Exits full-screen mode after a specified timeout if no activity is detected.
- Optionally locks the workstation or shuts down the system after inactivity.
- Configurable through an external `config.ini` file.

## Requirements
- Python 3.x
- Windows OS

## Installation

### 1. Clone the Repository or Download the Script
Download the script and `config.ini` file from this repository.

### 2. Install Dependencies
Before running the script, install the required Python packages. This can be done automatically by running the setup script or manually via pip.

#### Using the Setup Script (Windows)
- **Batch Script**: Create a batch script to install dependencies, setup the environment, and run the script.
- **PowerShell Script**: Alternatively, use a PowerShell script:

 

### 3. Configure the Script
All configuration settings are stored in a `config.ini` file, which allows you to customize the script's behavior without modifying the code.

#### `config.ini` Example:

```ini
[settings]
INACTIVITY_TIMEOUT = 5           # Time in seconds to wait for inactivity before exiting full-screen mode
ISRUNNING = True                 # Set to False to stop the actions of the script
KILLFULLSCREEN = True            # Set to False to disable exiting full-screen mode
LOCKWORKSTATION = False          # Set to True to enable locking the workstation
SHUTDOWN = False                 # Set to True to enable shutting down the workstation
KEEPRUNNING = True               # Set to False to stop the script after the first iteration
AUDIO_THRESHOLD = 100            # Threshold for detecting if sound is playing (adjust based on environment)
```

### 4. Run the Script
- **Via Command Line**: Activate the virtual environment and run the script:

    ```bash
    venv\Scripts\activate
    python main.py
    ```

- **Using the Setup Script**: Simply double-click the batch or PowerShell script to set up the environment and run the Python script.

### 5. Create an Executable (Optional)
You can bundle the script into a standalone executable using `PyInstaller`, so it can run on any Windows machine without requiring Python.

#### Install `PyInstaller`:

```bash
pip install pyinstaller
```

#### Create the Executable:

Run the following command:

```bash
pyinstaller --onefile --add-data "config.ini;." --icon=your_icon.ico --windowed "main.py"
```

- `--onefile`: Packages everything into a single executable.
- `--add-data "config.ini;."`: Ensures the `config.ini` file is included.
- `--icon=your_icon.ico`: Optionally specify an icon for the executable.
- `--windowed`: Prevents the command prompt window from appearing (useful for GUI applications; omit for CLI).

#### Place the Executable on the Desktop:

After running `PyInstaller`, navigate to the `dist` directory and copy the `.exe` file to your desktop.

## Usage

1. **Modify Configurations**: Adjust the settings in `config.ini` to suit your needs.
2. **Run**: Double-click the executable or run the script via command line or the setup script.
3. **Monitor**: The script will now monitor YouTube or other specified applications in full-screen mode and take actions based on the configured settings.

## Contributing
Feel free to submit issues or pull requests if you find bugs or want to add new features.

## License
This project is licensed under the MIT License.

---

This `README.md` provides all the necessary information to set up, configure, and run your Python script, as well as instructions for creating a standalone executable.