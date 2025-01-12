# Viper: An Advanced Multi-Platform Data Extraction Virus

## Overview
Viper is a sophisticated multi-platform malware developed for educational and penetration testing purposes as part of UWA's CITS3006 course. Designed to operate across Windows, Linux, and macOS, Viper showcases various malware techniques such as operating system detection, virus-like behaviour, mutation for evasion, data exfiltration, and anti-debugging mechanisms.

**Disclaimer:** This project is for educational purposes only.

---

## Features
- Cross-platform compatibility (Windows, Linux, macOS)
- OS detection and customised behaviour
- Virus-like replication and mutation
- Stealthy data exfiltration to a remote server
- Anti-debugging measures
- Minimal user disruption to maintain stealth

---


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/viper.git
   cd viper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How It Works
### 1. OS Detection
Viper detects the target operating system using Python's `platform` module and adapts its behaviour accordingly:
- **Windows**: Uses `ctypes` for pop-up messages and anti-debugging mechanisms.
- **Linux**: Utilises `Zenity` or `Tkinter` for displaying infection alerts.
- **macOS**: Uses `osascript` to display pop-ups via AppleScript.

### 2. Replication and Mutation
Viper replicates itself across Python files in the current directory and subdirectories. It employs a simple mutation mechanism to modify its genetic sequence, changing its hash with each replication to evade detection by antivirus software.

### 3. Data Exfiltration
Viper stealthily collects files from the following directories:
- **Windows**: `Documents`, `Desktop`, `Downloads`
- **Linux/macOS**: `~/Documents`, `~/Desktop`, `~/Downloads`

The files are then sent to a remote server via an obfuscated URL using the `requests` library.

### 4. Anti-Debugging
On Windows, Viper includes anti-debugging measures that terminate the malware if a debugger is detected. It also implements a time-based exit to prevent extended analysis using tools like GDB.

---

## Usage
Run the malware using Python:
```bash
python viper.py
```
Ensure you have the necessary permissions to execute the script, especially on Linux/macOS systems:
```bash
chmod +x viper.py
```



