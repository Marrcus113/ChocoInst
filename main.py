import subprocess
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import json
import ctypes

# ========== ПРОВЕРКА ПРАВ АДМИНА ==========
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# ========== УПРАВЛЕНИЕ ТЕМАМИ ==========
class ThemeManager:
    THEMES = {
        "dark": {
            "bg": "#1a1a1a",
            "fg": "#00ff80",
            "entry_bg": "#262626",
            "entry_fg": "#00ff80",
            "button_bg": "#00aa55",
            "button_fg": "black",
            "text_bg": "#262626",
            "text_fg": "#00ff80",
            "status_bg": "#262626",
            "status_fg": "#00ff80",
            "name": "Тёмная"
        },
        "light": {
            "bg": "#f0f0f0",
            "fg": "#006633",
            "entry_bg": "white",
            "entry_fg": "#006633",
            "button_bg": "#4CAF50",
            "button_fg": "white",
            "text_bg": "white",
            "text_fg": "#006633",
            "status_bg": "#e0e0e0",
            "status_fg": "#006633",
            "name": "Светлая"
        },
        "blue": {
            "bg": "#001a33",
            "fg": "#00ccff",
            "entry_bg": "#002b4d",
            "entry_fg": "#00ccff",
            "button_bg": "#0066cc",
            "button_fg": "white",
            "text_bg": "#002b4d",
            "text_fg": "#00ccff",
            "status_bg": "#002b4d",
            "status_fg": "#00ccff",
            "name": "Синяя"
        },
        "matrix": {
            "bg": "black",
            "fg": "#00ff00",
            "entry_bg": "#0a0a0a",
            "entry_fg": "#00ff00",
            "button_bg": "#003300",
            "button_fg": "#00ff00",
            "text_bg": "#0a0a0a",
            "text_fg": "#00ff00",
            "status_bg": "#0a0a0a",
            "status_fg": "#00ff00",
            "name": "Матрица"
        },
        "white_blue": {
            "bg": "#f0f8ff",
            "fg": "#0066cc",
            "entry_bg": "white",
            "entry_fg": "#0066cc",
            "button_bg": "#3399ff",
            "button_fg": "white",
            "text_bg": "white",
            "text_fg": "#0066cc",
            "status_bg": "#e6f0ff",
            "status_fg": "#0066cc",
            "name": "Бело-голубая"
        }
    }
    
    def __init__(self, config_file="theme_config.json"):
        self.config_file = config_file
        self.current_theme = "dark"
        self.load()
        
    def load(self):
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.current_theme = data.get('theme', 'dark')
        except:
            self.current_theme = "dark"
            
    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump({'theme': self.current_theme}, f)
            
    def get(self):
        return self.THEMES.get(self.current_theme, self.THEMES["dark"])
    
    def __init__(self, config_file="theme_config.json"):
        self.config_file = config_file
        self.current_theme = "dark"
        self.load()
        
    def load(self):
        try:
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.current_theme = data.get('theme', 'dark')
        except:
            self.current_theme = "dark"
            
    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump({'theme': self.current_theme}, f)
            
    def get(self):
        return self.THEMES.get(self.current_theme, self.THEMES["dark"])

# ========== ОСНОВНОЙ КЛАСС ==========
class ChocoInst:
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.root = tk.Tk()
        self.root.title("ChocoInst")
        self.root.geometry("700x550")
        
        # ========== УСТАНОВКА ИКОНКИ ==========
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                pass  # если иконка кривая — игнорим
        
        self.center_window()
        self.choco_path = self.find_choco()
        self.setup_menu()
        self.setup_ui()
        self.apply_theme()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 700) // 2
        y = (self.root.winfo_screenheight() - 550) // 2
        self.root.geometry(f"700x550+{x}+{y}")
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню тем
        theme_menu = tk.Menu(menubar, tearoff=0)
        for theme_id, theme_data in ThemeManager.THEMES.items():
            theme_menu.add_command(
                label=theme_data['name'],
                command=lambda t=theme_id: self.change_theme(t)
            )
        menubar.add_cascade(label="🎨 Тема", menu=theme_menu)
        
        # Меню справки
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="ℹ️", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def change_theme(self, theme_id):
        self.theme_manager.current_theme = theme_id
        self.theme_manager.save()
        self.apply_theme()
        
    def apply_theme(self):
        theme = self.theme_manager.get()
        self.root.configure(bg=theme['bg'])
        
        for widget in self.root.winfo_children():
            self._apply_theme_to_widget(widget, theme)
            
        if hasattr(self, 'status_label'):
            self.status_label.config(
                bg=theme['status_bg'],
                fg=theme['status_fg']
            )
        
    def _apply_theme_to_widget(self, widget, theme):
        try:
            if isinstance(widget, tk.Frame):
                widget.configure(bg=theme['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=theme['bg'], fg=theme['fg'])
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=theme['entry_bg'],
                    fg=theme['entry_fg'],
                    insertbackground=theme['entry_fg']
                )
            elif isinstance(widget, tk.Button):
                widget.configure(
                    bg=theme['button_bg'],
                    fg=theme['button_fg']
                )
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=theme['text_bg'],
                    fg=theme['text_fg'],
                    insertbackground=theme['text_fg']
                )
        except:
            pass
            
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, theme)
        
    def find_choco(self):
        paths = [
            r"C:\ProgramData\chocolatey\bin\choco.exe",
            r"C:\Program Files\chocolatey\bin\choco.exe",
        ]
        
        for path in paths:
            if os.path.exists(path):
                return path
        
        try:
            result = subprocess.run(['where', 'choco'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
            
        return None
        
    def setup_ui(self):
        theme = self.theme_manager.get()
        
        # Заголовок
        self.title_label = tk.Label(self.root, text="🍫 ChocoInst", 
                                    font=("Arial", 28, "bold"))
        self.title_label.pack(pady=20)
        
        # Статус Chocolatey
        if self.choco_path:
            status_text = f"✅ Chocolatey найден"
        else:
            status_text = "❌ Chocolatey не найден"
            
        self.status_label = tk.Label(self.root, text=status_text, 
                                     font=("Arial", 10))
        self.status_label.pack(pady=5)
        
        # Поле ввода
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        
        tk.Label(frame, text="Пакет:", font=("Arial", 12)).pack(side="left", padx=5)
        
        self.entry = tk.Entry(frame, width=30, font=("Arial", 12))
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda e: self.install())
        
        # Кнопка установки
        self.btn = tk.Button(self.root, text="📦 Установить", 
                            font=("Arial", 12, "bold"),
                            command=self.install)
        self.btn.pack(pady=10)
        
        # Прогресс
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=400)
        
        # Текстовое поле для вывода
        self.output = tk.Text(self.root, height=12, width=80,
                             font=("Consolas", 9))
        self.output.pack(pady=10, padx=10)
        
        # Скролл
        scroll = tk.Scrollbar(self.output)
        scroll.pack(side="right", fill="y")
        self.output.config(yscrollcommand=scroll.set)
        scroll.config(command=self.output.yview)
        
        # Если choco не найден
        if not self.choco_path:
            self.btn.config(state="disabled")
            self.output.insert("1.0", "❌ Chocolatey не установлен!\n")
            self.output.insert("end", "Установи: https://chocolatey.org/install")
        
        self.apply_theme()
        
    def log(self, text):
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.root.update()
        
    def install(self):
        package = self.entry.get().strip()
        if not package:
            messagebox.showwarning("Ошибка", "Введите название пакета!")
            return
            
        if not self.choco_path:
            messagebox.showerror("Ошибка", "Chocolatey не найден!")
            return
            
        def run():
            self.btn.config(state="disabled")
            self.progress.pack(pady=5)
            self.progress.start(10)
            
            self.log(f"\n🚀 Устанавливаю: {package}")
            
            try:
                cmd = [self.choco_path, 'install', package, '-y']
                self.log(f"💻 Команда: {' '.join(cmd)}")
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    shell=True
                )
                
                while True:
                    line = process.stdout.readline()
                    if not line:
                        break
                    self.log(line.strip())
                    
                returncode = process.wait()
                
                if returncode == 0:
                    self.log(f"✅ {package} установлен!")
                    messagebox.showinfo("Успех", f"{package} установлен!")
                else:
                    error = process.stderr.read()
                    self.log(f"❌ Ошибка: {error}")
                    
            except Exception as e:
                self.log(f"❌ Исключение: {str(e)}")
                
            finally:
                self.progress.stop()
                self.progress.pack_forget()
                self.btn.config(state="normal")
                self.entry.delete(0, tk.END)
                
        threading.Thread(target=run, daemon=True).start()
        
    def show_about(self):
        messagebox.showinfo("О программе", 
                           "🍫 ChocoInst\n"
                           "Версия 1.0\n"
                           "Автор: Марк\n\n"
                           "Программа для установки пакетов через Chocolatey")
        
    def run(self):
        self.root.mainloop()

# ========== ЗАПУСК ==========
if __name__ == "__main__":
    app = ChocoInst()
    app.run()