"""
system_actions.py - System-level stuff: time, date, screenshots, volume, lock, shutdown.
"""

import os
import subprocess
import datetime
from utils.logger import logger


def get_time() -> str:
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p").lstrip("0")
    logger.info(f"Time: {time_str}")
    return f"It's {time_str}."


def get_date() -> str:
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    logger.info(f"Date: {date_str}")
    return f"Today is {date_str}."


def take_screenshot() -> str:
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = os.path.join(os.path.expanduser("~"), "Desktop", f"screenshot_{timestamp}.png")

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
        """

        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        logger.info(f"Screenshot saved: {save_path}")
        return "Screenshot saved to your Desktop."

    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return "Couldn't take the screenshot."


def set_volume(level: int) -> str:
    try:
        level = max(0, min(100, int(level)))

        # First mute by pressing volume down 50 times, then raise to the target level.
        # Hacky but works without needing any extra packages.
        ps_script = f"""
            $wshShell = new-object -com wscript.shell
            1..50 | ForEach-Object {{ $wshShell.SendKeys([char]174) }}
            $steps = [math]::Round({level} / 100 * 50)
            1..$steps | ForEach-Object {{ $wshShell.SendKeys([char]175) }}
        """

        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        logger.info(f"Volume set to {level}%")
        return f"Volume set to {level} percent."

    except Exception as e:
        logger.error(f"Volume control failed: {e}")
        return "Couldn't change the volume."


def lock_screen() -> str:
    try:
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        logger.info("Screen locked")
        return "Locking your screen."
    except Exception as e:
        logger.error(f"Lock screen failed: {e}")
        return "Couldn't lock the screen."


def shutdown_system() -> str:
    try:
        subprocess.run(["shutdown", "/s", "/t", "10"])
        logger.info("Shutdown initiated")
        return "Shutting down in 10 seconds. Run 'shutdown /a' to cancel."
    except Exception as e:
        logger.error(f"Shutdown failed: {e}")
        return "Couldn't initiate shutdown."


def restart_system() -> str:
    try:
        subprocess.run(["shutdown", "/r", "/t", "10"])
        logger.info("Restart initiated")
        return "Restarting in 10 seconds. Run 'shutdown /a' to cancel."
    except Exception as e:
        logger.error(f"Restart failed: {e}")
        return "Couldn't initiate restart."
