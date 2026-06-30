"""
system_actions.py - System-level stuff: time, date, screenshots, volume, lock, shutdown.
"""

import os  # used for expanding the home directory path when saving screenshots
import subprocess  # used to run PowerShell and Windows CLI commands
import datetime  # used for getting the current time and date
from utils.logger import logger  # shared logger for the project


def get_time() -> str:  # return the current local time as a human-readable string
    now = datetime.datetime.now()  # grab the current datetime object
    time_str = now.strftime("%I:%M %p").lstrip("0")  # format as 12-hour clock, strip the leading zero (e.g. "09:30 AM" → "9:30 AM")
    logger.info(f"Time: {time_str}")  # log what we're returning
    return f"It's {time_str}."  # spoken response


def get_date() -> str:  # return today's date as a human-readable string
    now = datetime.datetime.now()  # grab the current datetime object
    date_str = now.strftime("%A, %B %d, %Y")  # format as "Monday, January 01, 2024"
    logger.info(f"Date: {date_str}")  # log what we're returning
    return f"Today is {date_str}."  # spoken response


def take_screenshot() -> str:  # capture the primary screen and save it as a PNG on the desktop
    try:  # everything is in a try block because this depends on PowerShell and .NET
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # unique timestamp to avoid overwriting previous screenshots
        save_path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{timestamp}.png")  # save to the user's actual Desktop folder

        # Capture the screen using .NET System.Drawing via PowerShell
        ps_script = f"""
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
            $bitmap.Save("{save_path}")
            $graphics.Dispose()
            $bitmap.Dispose()
        """  # loads .NET drawing libraries, creates a bitmap the size of the screen, copies pixels, saves as PNG, then disposes the objects

        subprocess.run(  # run the PowerShell script and wait for it to finish
            ["powershell", "-NoProfile", "-Command", ps_script],  # -NoProfile skips loading the user profile for faster startup
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL  # suppress output — errors are caught by the except block
        )

        logger.info(f"Screenshot saved: {save_path}")  # log the full path so it's easy to find
        return "Screenshot saved to your Desktop."  # spoken confirmation

    except Exception as e:  # catch any PowerShell or .NET errors
        logger.error(f"Screenshot failed: {e}")  # log what went wrong
        return "Couldn't take the screenshot."  # spoken fallback


def set_volume(level: int) -> str:  # set the system volume to a given percentage using keyboard simulation
    try:  # volume control via SendKeys is fragile — wrap it
        level = max(0, min(100, int(level)))  # clamp to valid range — reject anything below 0 or above 100

        # First mute by pressing volume down 50 times, then raise to the target level.
        # Hacky but works without needing any extra packages.
        ps_script = f"""
            $wshShell = new-object -com wscript.shell
            1..50 | ForEach-Object {{ $wshShell.SendKeys([char]174) }}
            $steps = [math]::Round({level} / 100 * 50)
            1..$steps | ForEach-Object {{ $wshShell.SendKeys([char]175) }}
        """  # char 174 = volume down key, char 175 = volume up key — press down 50 times to mute, then up proportionally

        subprocess.run(  # run the script silently
            ["powershell", "-NoProfile", "-Command", ps_script],  # -NoProfile for faster launch
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL  # suppress all output
        )

        logger.info(f"Volume set to {level}%")  # log the target level
        return f"Volume set to {level} percent."  # spoken confirmation

    except Exception as e:  # catch any errors from the subprocess or value conversion
        logger.error(f"Volume control failed: {e}")  # log what went wrong
        return "Couldn't change the volume."  # spoken fallback


def lock_screen() -> str:  # lock the Windows workstation using the built-in rundll32 command
    try:  # wrap it in case something goes wrong with the subprocess call
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])  # standard Windows lock command — no delay, locks immediately
        logger.info("Screen locked")  # log the action
        return "Locking your screen."  # spoken confirmation
    except Exception as e:  # catch any subprocess errors
        logger.error(f"Lock screen failed: {e}")  # log the error
        return "Couldn't lock the screen."  # spoken fallback


def shutdown_system() -> str:  # schedule a Windows shutdown in 10 seconds
    try:  # wrap it — a failed shutdown should be logged, not crash the assistant
        subprocess.run(["shutdown", "/s", "/t", "10"])  # /s = shutdown, /t 10 = wait 10 seconds before executing
        logger.info("Shutdown initiated")  # log that the command was sent
        return "Shutting down in 10 seconds. Run 'shutdown /a' to cancel."  # spoken response including how to abort
    except Exception as e:  # catch any subprocess errors
        logger.error(f"Shutdown failed: {e}")  # log what went wrong
        return "Couldn't initiate shutdown."  # spoken fallback


def restart_system() -> str:  # schedule a Windows restart in 10 seconds
    try:  # wrap it just like shutdown
        subprocess.run(["shutdown", "/r", "/t", "10"])  # /r = restart, /t 10 = 10-second delay
        logger.info("Restart initiated")  # log that the command was sent
        return "Restarting in 10 seconds. Run 'shutdown /a' to cancel."  # spoken response including the abort command
    except Exception as e:  # catch any subprocess errors
        logger.error(f"Restart failed: {e}")  # log what went wrong
        return "Couldn't initiate restart."  # spoken fallback
