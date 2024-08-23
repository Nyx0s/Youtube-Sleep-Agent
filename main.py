# AUTHOR: Maximilian Jonas
# DATE: 2021-09-30
# DESCRIPTION: This script monitors the full-screen applications on the system and performs actions based on the detected application. Specifically, it checks if the YouTube application is running in full-screen mode and monitors its activity. If there is no activity for a specified timeout period, it exits the full-screen mode. Additionally, it provides options to lock the workstation or shut down the system based on certain conditions.

from ctypes import windll
import win32gui 
import time
import pyautogui 
import keyboard 
import os
import sounddevice as sd 
import numpy as np 
import configparser


# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Configs
INACTIVITY_TIMEOUT = config.getint('settings', 'INACTIVITY_TIMEOUT')  # Time in seconds to wait for inactivity before exiting full-screen mode
ISRUNNING = config.getboolean('settings', 'ISRUNNING')  # Set to False to stop the actions of the script
KILLFULLSCREEN = config.getboolean('settings', 'KILLFULLSCREEN')  # Set to False to disable exiting full-screen mode
LOCKWORKSTATION = config.getboolean('settings', 'LOCKWORKSTATION') # Set to True to enable locking the workstation
SHUTDOWN =  config.getboolean('settings', 'SHUTDOWN') # Set to True to enable shutting down the workstation
KEEPRUNNING = config.getboolean('settings', 'KEEPRUNNING') # Set to False to stop the script after the first iteration
AUDIO_THRESHOLD = config.getint('settings', 'AUDIO_THRESHOLD')  # Threshold for detecting if sound is playing (adjust based on environment)

def clear_terminal():
    """
    Clears the terminal screen.

    This function clears the terminal screen by executing the appropriate command based on the operating system.
    On Windows, it uses the 'cls' command, and on other systems, it uses the 'clear' command.

    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_full_screen_rect():
    """
    Retrieves the full-screen resolution.

    This function obtains the full-screen dimensions using the Windows API. It sets the DPI awareness to ensure
    accurate pixel values are returned, and then it retrieves the screen width and height.

    Returns:
        tuple: A tuple containing the coordinates of the full screen (left, top, right, bottom).
    """
    user32 = windll.user32
    user32.SetProcessDPIAware()
    return (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


def is_window_full_screen(hWnd):
    """
    Checks if a specific window is in full-screen mode.

    This function compares the dimensions of the specified window with the full-screen dimensions.
    If the window occupies the entire screen, it is considered to be in full-screen mode.

    Args:
        hWnd (int): Handle to the window.

    Returns:
        bool: True if the window is in full-screen mode, False otherwise.
    """
    full_screen_rect = get_full_screen_rect()
    rect = win32gui.GetWindowRect(hWnd)
    return rect == full_screen_rect


def check_full_screen_applications():
    """
    Enumerates all top-level windows and checks for full-screen applications.

    This function iterates through all visible top-level windows and identifies those that are in full-screen mode.

    Returns:
        list: A list of handles to windows that are in full-screen mode.
    """
    full_screen_windows = []

    def callback(hWnd, _):
        if win32gui.IsWindowVisible(hWnd):
            if is_window_full_screen(hWnd):
                full_screen_windows.append(hWnd)

    win32gui.EnumWindows(callback, None)
    return full_screen_windows


def is_fullscreen_running():
    """
    Checks if the full-screen content is static or changing.

    This function takes two consecutive screenshots and compares them to determine if the screen content
    is changing (indicating activity) or static (indicating inactivity).

    Returns:
        bool: True if the screen content is changing (indicating activity), False otherwise.
    """
    try:
        screen1 = pyautogui.screenshot()
        time.sleep(1)
        screen2 = pyautogui.screenshot()
        return screen1 != screen2
    except Exception as e:
        print(f"Error checking fullscreen: {e}")
        return False


def is_sound_playing():
    """
    Checks if sound is playing on the system.

    This function records a short audio clip and analyzes its volume to determine if sound is being played.
    If the volume exceeds a set threshold, it is assumed that sound is playing.

    Returns:
        bool: True if sound is detected, False otherwise.
    """
    try:
        duration = 1  # seconds
        fs = 44100  # Sample rate
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()  # Wait until recording is finished
        volume = np.linalg.norm(audio_data) * 10
        return volume > AUDIO_THRESHOLD
    except Exception as e:
        print(f"Error checking sound: {e}")
        return False


def exit_fullscreen():
    """
    Exits full-screen mode by sending the "Esc" key.

    This function simulates a keypress of the "Esc" key to exit full-screen mode in an application.

    Returns:
        None
    """
    keyboard.press_and_release('esc')


def lock_workstation():
    """
    Locks the workstation.

    This function uses the Windows API to lock the workstation, requiring the user to enter their credentials to unlock it.

    Returns:
        None
    """
    windll.user32.LockWorkStation()


def shutdown_workstation():
    """
    Shuts down the workstation.

    This function initiates a shutdown of the workstation by executing the `shutdown` command with the `/s` flag to
    shut down the system and the `/t 1` flag to set a delay of 1 second before the shutdown.

    Returns:
        None
    """
    os.system("shutdown /s /t 1")


def monitor_video():
    """
    Monitors the video playback in full-screen mode and performs actions based on the activity status.

    This function continuously checks for full-screen applications and specifically monitors YouTube in full-screen mode.
    If YouTube is detected in full-screen mode, it checks for inactivity and exits full-screen mode if no activity is detected
    for a specified timeout period. The function also provides options to lock the workstation or shut down the system
    based on user preferences.

    Returns:
        None
    """
    while ISRUNNING:
        full_screen_windows = check_full_screen_applications()
        if full_screen_windows:
            full_screen_windows_context = [win32gui.GetWindowText(hWnd) for hWnd in full_screen_windows]
            if "YouTube" in str(full_screen_windows_context):
                time_in_fullscreen = 0
                while time_in_fullscreen < INACTIVITY_TIMEOUT:
                    clear_terminal()
                    print("YouTube is in full-screen mode and running.")

                    if not is_fullscreen_running() and not is_sound_playing():
                        time_in_fullscreen += 1
                        clear_terminal()
                        print(f"YouTube is in full-screen mode but inactive for {time_in_fullscreen} seconds.")
                        time.sleep(1)  # Wait for 1 second before checking again
                        continue
                    else:
                        # Reset inactivity timer if activity is detected
                        time_in_fullscreen = 0
                        break

                if time_in_fullscreen >= INACTIVITY_TIMEOUT:
                    print("No activity detected. Exiting fullscreen mode...")
                    if KILLFULLSCREEN:
                        exit_fullscreen()
            else:
                clear_terminal()
                print("No YouTube full-screen mode detected.")
        else:
            clear_terminal()
            print("No full-screen applications found.")
            if not KEEPRUNNING:
                break

        if LOCKWORKSTATION:
            lock_workstation()
            print("Locking Workstation...")
            os._exit(0)

        if SHUTDOWN:
            print("Shutting down the system...")
            shutdown_workstation()

        time.sleep(1)  # Add a small delay before the next check


if __name__ == "__main__":
    monitor_video()
