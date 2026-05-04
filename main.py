import customtkinter as ctk
import json
import os
import random


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(BASE_DIR, "save.json")
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


class SimpleClicker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("400x650")
        self.root.resizable(False, False)

        # Конфиг и язык
        self.cfg = {}
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                self.cfg = json.load(f)
        except:
            self.cfg = {"lang": "en"}
        self.lang = self.cfg.get("lang", "en")

        self.texts = {
            "en": {
                "title": "Mini-Clicker",
                "reset": "🗑 Reset",
                "market": "MARKET",
                "upgrades_title": "UPGRADES",
                "upgrades_close": "CLOSE",
                "income": "income: +{} / click, +{} / s",
                "power_label": "Power",
                "auto_label": "Auto",
                "cost": "Cost",
                "per_sec": "/s",
            },
            "ru": {
                "title": "Мини‑кликер",
                "reset": "🗑 Сброс",
                "market": "МАРКЕТ",
                "upgrades_title": "УЛУЧШЕНИЯ",
                "upgrades_close": "ЗАКРЫТЬ",
                "income": "доход: +{} / клик, +{} / с",
                "power_label": "Мощность",
                "auto_label": "Авто",
                "cost": "Цена",
                "per_sec": "/с",
            }
        }

        self.root.title(self.texts[self.lang]["title"])

        # Цвета
        self.color_affordable = "#4cd964"
        self.color_expensive = "#3a3a3c"
        self.color_button_default = "#252529"

        # Данные
        self.score = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.auto_click_level = 0
        self.auto_cost = 50

        self.shop_open = False
        self.is_animating = False
        self.current_y = 1.0

        self.load_game()
        self.setup_ui()
        self.update_auto_click_loop()
        self.save_game()
        self.root.mainloop()

    def setup_ui(self):
        self.bg_frame = ctk.CTkFrame(
            self.root,
            fg_color="#1a1a1c",
            corner_radius=0
        )
        self.bg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Хедер
        self.header = ctk.CTkFrame(
            self.bg_frame,
            fg_color="#252529",
            height=50
        )
        self.header.pack(fill="x")

        self.btn_reset = ctk.CTkButton(
            self.header,
            text=self.texts[self.lang]["reset"],
            font=("Helvetica", 11, "bold"),
            width=70,
            height=28,
            fg_color="#3a3a3c",
            text_color="#e94560",
            hover_color="#503030",
            corner_radius=8,
            command=self.reset_game
        )
        self.btn_reset.place(x=12, y=11)

        # Счёт и доход
        self.score_label = ctk.CTkLabel(
            self.bg_frame,
            text=str(int(self.score)),
            font=("Helvetica", 64, "bold"),
            text_color="#4cd964"
        )
        self.score_label.pack(pady=(50, 0))

        self.income_label = ctk.CTkLabel(
            self.bg_frame,
            text=self.texts[self.lang]["income"].format(
                self.click_power, self.auto_click_level
            ),
            font=("Helvetica", 14, "italic"),
            text_color="#a8a8b3"
        )
        self.income_label.pack(pady=(0, 20))

        # Кнопка клика
        self.btn_click = ctk.CTkButton(
            self.bg_frame,
            text="🪙",
            font=("Helvetica", 70),
            width=170,
            height=170,
            corner_radius=85,
            fg_color="#2c2c2e",
            hover_color="#3a3a3c",
            border_width=4,
            border_color="#4cd964",
            command=self.do_click
        )
        self.btn_click.pack(pady=20)

        # Кнопка магазина
        self.shop_toggle_btn = ctk.CTkButton(
            self.root,
            text=self.texts[self.lang]["upgrades_title"] + " ▲",
            font=("Segoe UI", 13, "bold"),
            fg_color=self.color_button_default,
            hover_color="#2c2c2e",
            height=55,
            corner_radius=0,
            command=self.toggle_shop
        )
        self.shop_toggle_btn.place(relx=0, rely=0.92, relwidth=1)

        # Панель магазина
        self.shop_panel = ctk.CTkFrame(
            self.root,
            fg_color="#252529",
            corner_radius=25,
            border_width=2,
            border_color="#3a3a3c"
        )
        self.shop_panel.place(relx=0, rely=1.0, relwidth=1, relheight=0.5)

        ctk.CTkLabel(
            self.shop_panel,
            text=self.texts[self.lang]["market"],
            font=("Segoe UI", 18, "bold"),
            text_color="#4cd964"
        ).pack(pady=15)

        # Кнопки улучшений
        self.upg_click_btn = ctk.CTkButton(
            self.shop_panel,
            text="",
            command=self.buy_upgrade,
            height=55,
            corner_radius=12
        )
        self.upg_click_btn.pack(fill="x", padx=30, pady=10)

        self.upg_auto_btn = ctk.CTkButton(
            self.shop_panel,
            text="",
            command=self.buy_auto,
            height=55,
            corner_radius=12
        )
        self.upg_auto_btn.pack(fill="x", padx=30, pady=10)

        self.update_ui_text()

    def update_ui_text(self):
        self.score_label.configure(text=str(int(self.score)))
        self.income_label.configure(
            text=self.texts[self.lang]["income"].format(
                self.click_power, self.auto_click_level
            )
        )

        afford_click = self.score >= self.upgrade_cost
        click_text = (
            f"{self.texts[self.lang]['power_label']}: +{self.click_power} | "
            f"{self.texts[self.lang]['cost']}: {self.upgrade_cost}"
        )
        self.upg_click_btn.configure(
            text=click_text,
            fg_color=self.color_affordable if afford_click else self.color_expensive,
            text_color="black" if afford_click else "white",
            hover_color="#3dbb56" if afford_click else "#4a4a4c"
        )

        afford_auto = self.score >= self.auto_cost
        auto_text = (
            f"{self.texts[self.lang]['auto_label']}: {self.auto_click_level}"
            f"{self.texts[self.lang]['per_sec']} | "
            f"{self.texts[self.lang]['cost']}: {self.auto_cost}"
        )
        self.upg_auto_btn.configure(
            text=auto_text,
            fg_color=self.color_affordable if afford_auto else self.color_expensive,
            text_color="black" if afford_auto else "white",
            hover_color="#3dbb56" if afford_auto else "#4a4a4c"
        )

        if (afford_click or afford_auto) and not self.shop_open:
            self.shop_toggle_btn.configure(
                fg_color="#1a5a2a",
                text_color=self.color_affordable
            )
        else:
            self.shop_toggle_btn.configure(
                fg_color=self.color_button_default,
                text_color="white"
            )

    def do_click(self):
        self.btn_click.configure(border_width=2)
        self.root.after(70, lambda: self.btn_click.configure(border_width=4))
        self.score += self.click_power
        self.create_particle()
        self.update_ui_text()
        self.save_game()

    def update_auto_click_loop(self):
        if self.auto_click_level > 0:
            self.score += self.auto_click_level
            self.update_ui_text()
            self.save_game()
        self.root.after(1000, self.update_auto_click_loop)

    def create_particle(self):
        offset_x = random.uniform(-0.15, 0.15)
        p = ctk.CTkLabel(
            self.bg_frame,
            text=f"+{self.click_power}",
            font=("Helvetica", 20, "bold"),
            text_color="#88ff88"
        )
        p.place(relx=0.5 + offset_x, rely=0.45)

        def animate_p(step=0):
            if step < 25:
                p.place(rely=0.45 - (step * 0.012))
                self.root.after(15, lambda: animate_p(step + 1))
            else:
                p.destroy()
        animate_p()

    def toggle_shop(self):
        if self.is_animating:
            return
        self.is_animating = True
        target = 0.55 if not self.shop_open else 1.05
        self.animate_shop(target)

        text = (
            self.texts[self.lang]["upgrades_close"] if not self.shop_open
            else self.texts[self.lang]["upgrades_title"]
        ) + (" ▼" if not self.shop_open else " ▲")
        self.shop_toggle_btn.configure(text=text)

        self.shop_open = not self.shop_open
        self.update_ui_text()

    def animate_shop(self, target_y):
        step = 0.05
        if abs(self.current_y - target_y) > 0.02:
            if self.current_y > target_y:
                self.current_y -= step
            else:
                self.current_y += step
            self.shop_panel.place(rely=self.current_y)
            button_y = self.current_y - 0.08 if self.current_y < 1.0 else 0.92
            self.shop_toggle_btn.place(rely=button_y)
            self.root.after(10, lambda: self.animate_shop(target_y))
        else:
            self.current_y = target_y
            self.shop_panel.place(rely=self.current_y)
            button_y = 0.92 if target_y > 1.0 else target_y - 0.08
            self.shop_toggle_btn.place(rely=button_y)
            self.is_animating = False

    def buy_upgrade(self):
        if self.score >= self.upgrade_cost:
            self.score -= self.upgrade_cost
            self.click_power += 1
            self.upgrade_cost = int(self.upgrade_cost * 1.6)
            self.update_ui_text()
            self.save_game()
        else:
            self.flash_error(self.upg_click_btn)

    def buy_auto(self):
        if self.score >= self.auto_cost:
            self.score -= self.auto_cost
            self.auto_click_level += 1
            self.auto_cost = int(self.auto_cost * 1.8)
            self.update_ui_text()
            self.save_game()
        else:
            self.flash_error(self.upg_auto_btn)

    def flash_error(self, button):
        button.configure(fg_color="#e94560")
        self.root.after(400, self.update_ui_text)

    def reset_game(self):
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        self.score = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.auto_click_level = 0
        self.auto_cost = 50
        self.update_ui_text()
        self.save_game()

    def save_game(self):
        data = {
            "score": self.score,
            "power": self.click_power,
            "cost": self.upgrade_cost,
            "auto_lvl": self.auto_click_level,
            "auto_cost": self.auto_cost
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print("Save error:", e)

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    self.score = d.get("score", 0)
                    self.click_power = d.get("power", 1)
                    self.upgrade_cost = d.get("cost", 10)
                    self.auto_click_level = d.get("auto_lvl", 0)
                    self.auto_cost = d.get("auto_cost", 50)
            except Exception as e:
                print("Load error:", e)


if __name__ == "__main__":
    SimpleClicker()