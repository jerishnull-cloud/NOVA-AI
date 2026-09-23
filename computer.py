import os
import subprocess


def computer_command(command):

    command = command.lower().strip()

    # ==========================================
    # OPEN CHROME
    # ==========================================

    if "open chrome" in command:

        subprocess.Popen(
            "start chrome",
            shell=True
        )

        return "Opening Chrome, sir."


    # ==========================================
    # OPEN VS CODE
    # ==========================================

    if (
        "open vs code" in command
        or "open visual studio code" in command
    ):

        subprocess.Popen(
            "code",
            shell=True
        )

        return "Opening Visual Studio Code, sir."


    # ==========================================
    # OPEN DOWNLOADS
    # ==========================================

    if "open downloads" in command:

        downloads = os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        )

        os.startfile(downloads)

        return "Opening your Downloads folder, sir."


    # ==========================================
    # OPEN FILE EXPLORER
    # ==========================================

    if (
        "open file explorer" in command
        or "open explorer" in command
    ):

        subprocess.Popen("explorer")

        return "Opening File Explorer, sir."


    # ==========================================
    # OPEN CALCULATOR
    # ==========================================

    if "open calculator" in command:

        subprocess.Popen("calc.exe")

        return "Opening Calculator, sir."


    # ==========================================
    # TAKE SCREENSHOT
    # ==========================================

    if (
        "take a screenshot" in command
        or "take screenshot" in command
        or "screenshot" in command
    ):

        try:

            desktop = os.path.join(
                os.path.expanduser("~"),
                "Desktop"
            )

            os.makedirs(
                desktop,
                exist_ok=True
            )

            filename = os.path.join(
                desktop,
                "nova_screenshot.png"
            )

            # Windows native screenshot using PowerShell
            powershell_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screen = [System.Windows.Forms.Screen]::PrimaryScreen

$bitmap = New-Object System.Drawing.Bitmap(
    $screen.Bounds.Width,
    $screen.Bounds.Height
)

$graphics = [System.Drawing.Graphics]::FromImage($bitmap)

$graphics.CopyFromScreen(
    $screen.Bounds.X,
    $screen.Bounds.Y,
    0,
    0,
    $bitmap.Size
)

$bitmap.Save("{filename}")

$graphics.Dispose()
$bitmap.Dispose()
'''

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    powershell_script
                ],
                check=True
            )

            print(
                f"📸 Screenshot saved to: {filename}"
            )

            return (
                "Screenshot captured and saved "
                "to your Desktop, sir."
            )

        except Exception as error:

            print(
                f"Screenshot error: {error}"
            )

            return (
                "Sorry sir, I couldn't take "
                "the screenshot."
            )


    # ==========================================
    # LOCK COMPUTER
    # ==========================================

    if (
        "lock my computer" in command
        or "lock the computer" in command
    ):

        subprocess.run(
            [
                "rundll32.exe",
                "user32.dll,LockWorkStation"
            ]
        )

        return "Locking the computer, sir."


    # ==========================================
    # NO COMPUTER COMMAND
    # ==========================================

    return None