import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess

# ============================================================
# SETTINGS
# ============================================================
GAME_SCRIPT = "./main.py"  # Path to the game script relative to the launcher
# ============================================================

class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Launcher")
        self.geometry("480x300")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")
        
        self._build_ui()
        self.check_game_exists()

    def _build_ui(self):
        tk.Label(
            self, text="🎮 MY GAME",
            font=("Segoe UI", 22, "bold"),
            bg="#1a1a2e", fg="#e94560"
        ).pack(pady=(50, 10))

        self.status_label = tk.Label(
            self, text="Checking status...",
            font=("Segoe UI", 10),
            bg="#1a1a2e", fg="#a8a8b3"
        )
        self.status_label.pack()

        # Play Button
        self.play_btn = tk.Button(
            self, text="▶  PLAY",
            font=("Segoe UI", 13, "bold"),
            bg="#e94560", fg="white",
            activebackground="#c73652",
            activeforeground="white",
            relief="flat", bd=0,
            padx=40, pady=10,
            cursor="hand2",
            state="disabled", # Disabled by default
            command=self.launch_game
        )
        self.play_btn.pack(pady=30)

    def check_game_exists(self):
        """Checks if the game script exists"""
        if os.path.exists(GAME_SCRIPT):
            self.play_btn.config(state="normal")
            self.status_label.config(text="Game found. Press 'PLAY' to start", fg="#4cd964")
        else:
            self.status_label.config(text=f"Error: {GAME_SCRIPT} not found!", fg="#ff3b30")
            messagebox.showerror("Error", f"Could not find the game file at:\n{GAME_SCRIPT}")

    def launch_game(self):
        try:
            # Launch the game
            subprocess.Popen(["python", GAME_SCRIPT])
            # Close the launcher
            self.destroy()
        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to start the game:\n{e}")

if __name__ == "__main__":
    app = Launcher()
    app.mainloop()
