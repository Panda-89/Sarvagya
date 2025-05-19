import platform
import subprocess
import os

def check_disk_encryption():
    if platform.system() == 'Windows':
        output = subprocess.getoutput("manage-bde -status")
        return "Percentage Encrypted: 100%" in output
    elif platform.system() == 'Darwin':
        output = subprocess.getoutput("fdesetup status")
        return "FileVault is On" in output
    elif platform.system() == 'Linux':
        return os.path.exists('/etc/crypttab')
    return False

def check_os_updates():
    return True  # Simulated for now

def check_antivirus():
    if platform.system() == 'Windows':
        output = subprocess.getoutput("powershell Get-MpComputerStatus")
        return "AMServiceEnabled" in output
    elif platform.system() == 'Linux':
        return "clamav" in subprocess.getoutput("ps aux")
    return False

def check_sleep_settings():
    return True  # Simulated for now

def run_all_checks():
    return {
        "disk_encryption": check_disk_encryption(),
        "os_updates": check_os_updates(),
        "antivirus": check_antivirus(),
        "sleep_settings": check_sleep_settings(),
    }