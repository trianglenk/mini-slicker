import tkinter as tk
import json
import os

SAVE_FILE = "save.json"

class SimpleClicker:
    def __init__(self):
        self.root = tk.Tk()
        
        # Загрузка иконки (убедитесь, что путь правильный)
        try:
            photo = tk.PhotoImage(file='icons/5902290e65cb615bb0706051.png')
            self.root.iconphoto(False, photo)
        except:
            pass # Если иконка не найдена, программа просто продолжит работу
            
        self.root.title("Mini-Clicker")
        self.root.geometry("350x480")
        self.root.resizable(False, False)
        
        # --- COLOR PALETTE ---
        self.bg_color = "#2c2c2e"      
        self.text_color = "#ffffff"    
        self.accent_color = "#4cd964"  
        
        self.root.configure(bg=self.bg_color)

        self.score = 0
        self.load_game()

        # 1. Score Label
        self.label = tk.Label(
            self.root, 
            text=f"Score: {self.score}", 
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.label.pack(pady=40)

        # 2. CLICK Button
        self.btn_click = tk.Button(
            self.root, 
            text="🪙 CLICK ME", 
            command=self.add_point, 
            font=("Helvetica", 14, "bold"),
            width=15, height=2, 
            bg=self.accent_color,
            fg="black",
            activebackground="#3dbb56",
            relief="flat",
            cursor="hand2"
        )
        self.btn_click.pack(pady=10)

        # 3. Reset Button
        self.btn_reset = tk.Button(
            self.root, 
            text="Reset Progress", 
            command=self.reset_game,
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg="#ff3b30",
            bd=0,
            activebackground=self.bg_color,
            activeforeground="#b02a22",
            cursor="hand2"
        )
        self.btn_reset.pack(side="bottom", pady=20)

        self.root.mainloop()

    def add_point(self):
        self.score += 1
        self.update_ui()
        self.save_game()

    def update_ui(self):
        self.label.config(text=f"Score: {self.score}")

    def save_game(self):
        data = {"score": self.score}
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                self.score = data.get("score", 0)

    def reset_game(self):
        self.score = 0
        self.update_ui()
        self.save_game()

if __name__ == "__main__":
    SimpleClicker()
