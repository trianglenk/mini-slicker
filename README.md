# 💰 mini-slicker

A stylish and lightweight Python clicker. Click the button, earn coins, and purchase upgrades! The game is designed with eye care in a modern "Dark Mode" design.

## 🚀 Features
* **Autosave**: All progress (coins, clicks, upgrades) is securely stored in `save.json`.
* **Progression system**: Purchase bonuses to increase your earnings with every click.
* **Visual Feedback**: Animated button and visual feedback with every click.
* **Cross-platform**: Works equally well on Windows and popular Linux distributions.

---

## 🛠 Installation and Run

### 🟦 For Windows Users (Step-by-Step)

1. **Installing Python**:
* Download the installer from the [official python.org website](https://python.org).
* **IMPORTANT:** When running the installer, be sure to check the **"Add Python to PATH"** box at the bottom of the window. This will allow the system to see Python commands.
* Select `Install Now`.
2. **Running the Game**:
* Download this repository (**Code** -> **Download ZIP** button) and unzip the archive.
* Simply double-click the `main.py` file.
* *Tip: If the console window is getting in the way, rename `main.py` to `main.pyw`.*

### 🐧 For Linux users (various distributions)

On Linux, the `Tkinter` graphics library is often not installed by default. Install it with one command:

* **Ubuntu / Debian / Mint**:
```bash
sudo apt update && sudo apt install python3-tk -y
```
* **Arch Linux / Manjaro**:
```bash
sudo pacman -S tk --noconfirm
```
* **Fedora**:
```bash
sudo dnf install python3-tkinter -y
```

**Launch**: Navigate to the project folder in the terminal and enter:
```bash
python3 main.py
```

---

## 📂 Project Structure
* `main.py` — The game core (interface, logic, and visual effects).
* `launcher.py` — Launcher for easy launching and file verification.
* `save.json` — Save file (created automatically after the first launch).

## 🎨 Screenshots
<p align="center">
  <img src="icons/launcher_scn.png" width="500" alt="Launcher">
  <img src="icons/main.png" width="230" alt="Game Interface">
</p>




## 🏗 Future Updates
- [ ] **Auto-clickers**: Item shop for passive coin income.
- [ ] **Particles**: Pop-up "+1" text at the click location.
- [ ] **Sounds**: Juicy click and purchase effects.
- [ ] **Mobile version**: Porting to Android/iOS via the Flet library.

---

## 📜 License
Distributed under the MIT License. You are free to use, modify, and distribute this code.

Developed with ❤️ in Python.
