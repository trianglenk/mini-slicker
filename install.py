# install.py
import subprocess
import sys
import os
import platform


def log(msg):
    print(f"⚙️  {msg}")


def run(cmd):
    log("Running: " + " ".join(cmd))
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    log("Auto‑installer for mini‑slicker")

    # 1. Установка customtkinter
    log("Installing required Python packages...")
    if not run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]):
        log("Failed to install packages!")
        return

    # 2. Подготовка для линукса (если нужно)
    if platform.system() == "Linux":
        log("Linux detected, you may need to install tkinter separately:")
        log("Try: sudo apt install python3-tk   (Ubuntu/Debian)")
        log("Or:  sudo pacman -S tk             (Arch/Manjaro)")
        log("Or:  sudo dnf install python3-tkinter (Fedora)")

    # 3. Запуск лэйнчера после установки
    log("Installation done. Starting Launcher...")
    run([sys.executable, "Launcher.py"])


if __name__ == "__main__":
    main()