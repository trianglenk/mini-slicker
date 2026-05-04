import tkinter as tk
from tkinter import messagebox, ttk
import os
import subprocess
import sys
import webbrowser
import platform

# ============================================================
# SETTINGS
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_SCRIPT = os.path.join(BASE_DIR, "main.py")
ICON_PATH = os.path.join(BASE_DIR, 'icons', '5902290e65cb615bb0706051.png')

LINKS = {
    "GitHub": "https://github.com/trianglenk/mini-slicker",
}

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini-Slicker Launcher")
        self.geometry("500x350")
        self.resizable(False, False)
        self.configure(bg="#0f0f1a")

        # 1. Иконка окна
        try:
            self.photo = tk.PhotoImage(file=ICON_PATH)
            self.iconphoto(False, self.photo)
        except Exception:
            self.photo = None

        self._build_ui()
        self.check_game_exists()
        
        # СОЗДАНИЕ ЯРЛЫКА ПРИ СТАРТЕ
        self.create_desktop_shortcut()

    def create_desktop_shortcut(self):
        """Создает ярлык на рабочем столе для Linux и Windows"""
        system = platform.system()
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Проверка локализованных путей Linux (например, "Рабочий стол")
        if system == "Linux" and not os.path.exists(desktop):
            try:
                desktop = subprocess.check_output(["xdg-user-dir", "DESKTOP"]).decode('utf-8').strip()
            except: pass

        shortcut_path_linux = os.path.join(desktop, "Mini-Slicker.desktop")
        shortcut_path_win = os.path.join(desktop, "Mini-Slicker.bat")

        # Определяем путь к Python из venv
        venv_path = "Scripts" if system == "Windows" else "bin"
        python_exe = os.path.join(BASE_DIR, ".venv", venv_path, "python")
        if not os.path.exists(python_exe):
            python_exe = sys.executable

        if system == "Linux":
            if not os.path.exists(shortcut_path_linux):
                content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Mini-Slicker
Comment=Clicker Game by TriangleNk
Exec={python_exe} {os.path.join(BASE_DIR, "Launcher.py")}
Icon={ICON_PATH}
Path={BASE_DIR}
Terminal=false
Categories=Game;
"""
                with open(shortcut_path_linux, "w") as f:
                    f.write(content)
                os.chmod(shortcut_path_linux, 0o755) # Делаем исполняемым

        elif system == "Windows":
            if not os.path.exists(shortcut_path_win):
                # На Windows проще всего создать .bat файл, который запускает игру без консоли
                with open(shortcut_path_win, "w") as f:
                    f.write(f'@echo off\nstart "" "{python_exe}" "{os.path.join(BASE_DIR, "Launcher.py")}"')

    def _build_ui(self):
        header = tk.Frame(self, bg="#1a1a2e", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_container = tk.Frame(header, bg="#1a1a2e")
        title_container.pack(side="left", padx=20)

        try:
            self.header_logo = tk.PhotoImage(file=ICON_PATH).subsample(10, 10)
            tk.Label(title_container, image=self.header_logo, bg="#1a1a2e").pack(side="left", padx=(0, 10))
        except:
            tk.Label(title_container, text="🪙", bg="#1a1a2e", fg="#4cd964", font=("Arial", 18)).pack(side="left", padx=(0, 10))

        tk.Label(title_container, text="MINI-SLICKER", font=("Segoe UI", 18, "bold"), bg="#1a1a2e", fg="#4cd964").pack(side="left")

        content = tk.Frame(self, bg="#0f0f1a")
        content.pack(expand=True, fill="both", pady=20)

        self.play_btn = tk.Button(content, text="LAUNCH GAME", font=("Segoe UI", 14, "bold"), bg="#333", fg="#666", 
                                  activebackground="#4cd964", activeforeground="white", relief="flat", bd=0, 
                                  width=20, pady=12, cursor="hand2", state="disabled", command=self.start_loading)
        self.play_btn.pack(pady=10)

        self.progress = ttk.Progressbar(content, length=300, mode='determinate')
        self.progress.pack_forget()

        self.status_lbl = tk.Label(content, text="System: Waiting for action", font=("Segoe UI", 9), bg="#0f0f1a", fg="#a8a8b3")
        self.status_lbl.pack()

        social_frame = tk.Frame(self, bg="#0f0f1a")
        social_frame.pack(pady=20)

        for name, url in LINKS.items():
            tk.Button(social_frame, text=f"[{name}]", font=("Segoe UI", 9), bg="#0f0f1a", fg="#e94560", 
                      activebackground="#0f0f1a", activeforeground="white", relief="flat", bd=0, 
                      cursor="hand2", command=lambda u=url: webbrowser.open(u)).pack(side="left", padx=10)

    def check_game_exists(self):
        if os.path.exists(GAME_SCRIPT):
            self.play_btn.config(state="normal", bg="#e94560", fg="white")
            self.status_lbl.config(text="● System Ready", fg="#4cd964")
        else:
            self.status_lbl.config(text="● Error: main.py not found", fg="#ff3b30")
            messagebox.showerror("Error", "Game file (main.py) is missing!")

    def start_loading(self):
        self.play_btn.config(state="disabled", text="STARTING...")
        self.progress.pack(pady=5)
        self.animate_progress(0)

    def animate_progress(self, val):
        if val <= 100:
            self.progress["value"] = val
            self.after(15, lambda: self.animate_progress(val + 5))
        else: self.run_game()

    def run_game(self):
        try:
            venv_path = "Scripts" if platform.system() == "Windows" else "bin"
            python_exe = os.path.join(BASE_DIR, ".venv", venv_path, "python")
            if not os.path.exists(python_exe): python_exe = sys.executable

            subprocess.Popen([python_exe, GAME_SCRIPT], creationflags=getattr(subprocess, 'DETACHED_PROCESS', 0), close_fds=True)
            self.destroy()
            sys.exit()
        except Exception as e:
            messagebox.showerror("Launcher Error", f"Failed to start:\n{e}")
            self.play_btn.config(state="normal", text="LAUNCH GAME")
            self.progress.pack_forget()

if __name__ == "__main__":
    app = Launcher()
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TProgressbar", thickness=10, foreground='#4cd964', background='#2c2c2e')
    app.mainloop()
