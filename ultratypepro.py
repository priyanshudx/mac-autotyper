import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import time
from pynput import keyboard
from pynput.keyboard import Controller, Key

class AutoTyperGUI:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Ultra Type Pro ⌨️")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        self.root.configure(bg="#f8f9fa")

        # --- State Management ---
        self.is_typing = False
        self.stop_event = threading.Event()
        self.typing_thread = None
        self.typing_speed = 10  # Default delay in ms between characters
        self.keyboard_controller = Controller()
        self.current_text_section = 1
        
        # For global hotkeys
        self.hotkey_listener = None
        self.current_keys = set()

        self.setup_styles()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        # --- Header ---
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ttk.Label(header_frame, text="Ultra Type Pro", style="Header.TLabel").pack(anchor="center", pady=5)

        # --- Speed Control ---
        settings_frame = ttk.Frame(self.root, style="Settings.TFrame")
        settings_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        settings_frame.columnconfigure(1, weight=1)

        ttk.Label(settings_frame, text="Typing Delay:").grid(row=0, column=0, sticky="w", padx=5)
        self.speed_var = tk.IntVar(value=self.typing_speed)
        self.speed_scale = ttk.Scale(settings_frame, from_=0, to=200, orient=tk.HORIZONTAL, variable=self.speed_var, command=self.on_speed_change)
        self.speed_scale.grid(row=0, column=1, sticky="ew", padx=5)
        self.speed_label = ttk.Label(settings_frame, text=f"{self.typing_speed}ms / char")
        self.speed_label.grid(row=0, column=2, sticky="w", padx=5)

        # --- Notebook (Text Sections) ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

        self.text_areas = []
        hotkey_map = {'X': 1, 'Y': 2, 'Z': 3}
        for key, section_num in hotkey_map.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f"Section {section_num} (Cmd/Ctrl+Shift+{key})")
            
            text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("SF Pro Text", 12), padx=10, pady=10, relief=tk.FLAT, borderwidth=1)
            text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.text_areas.append(text_area)

        default_texts = [
            "This is the sample text for Section 1.",
            "Here you can enter the content for Section 2. The auto typer will reproduce it exactly.",
            "You can use hotkeys to trigger typing for each section. Stop typing with Cmd/Ctrl+Shift+0."
        ]
        for i, text in enumerate(default_texts):
            self.text_areas[i].insert(tk.INSERT, text)

        # --- Control Buttons ---
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        for i in range(4):
            control_frame.columnconfigure(i, weight=1)

        ttk.Button(control_frame, text="Type Section 1", command=lambda: self.start_typing(1), style="Action.TButton").grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(control_frame, text="Type Section 2", command=lambda: self.start_typing(2), style="Action.TButton").grid(row=0, column=1, padx=5, sticky="ew")
        ttk.Button(control_frame, text="Type Section 3", command=lambda: self.start_typing(3), style="Action.TButton").grid(row=0, column=2, padx=5, sticky="ew")
        ttk.Button(control_frame, text="Stop Typing (Esc)", command=self.stop_typing, style="Stop.TButton").grid(row=0, column=3, padx=5, sticky="ew")

        # --- Status Bar ---
        self.status_var = tk.StringVar(value="Ready | Start: Cmd/Ctrl+Shift+<X,Y,Z> | Stop: Esc or Cmd/Ctrl+Shift+0")
        status_bar = ttk.Frame(self.root, style="Status.TFrame")
        status_bar.grid(row=4, column=0, sticky="ew", padx=10, pady=5)
        status_bar.columnconfigure(0, weight=1)
        self.status_label = ttk.Label(status_bar, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.grid(row=0, column=0, sticky="w", padx=5)

        self.progress = ttk.Progressbar(status_bar, mode='indeterminate')
        self.progress.grid(row=0, column=1, sticky="e", padx=5)

        # --- Footer ---
        footer_frame = ttk.Frame(self.root, style="Settings.TFrame")
        footer_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 5))
        ttk.Label(footer_frame, text="Developed by Priyanshu Kashyap", font=('SF Pro Text', 9, 'italic')).pack(anchor="center")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()
        self.setup_global_hotkeys()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#f8f9fa", foreground="#212529")
        style.configure("Header.TFrame", background="#4f6bed")
        style.configure("Header.TLabel", background="#4f6bed", foreground="white", font=('SF Pro Display', 16, 'bold'))
        style.configure("Settings.TFrame", background="#f8f9fa")
        style.configure("TButton", padding=6)
        style.configure("Action.TButton", font=('SF Pro Text', 10, 'bold'), background="#e9ecef", bordercolor="#ced4da")
        style.map("Action.TButton", background=[('active', '#d6dce1')])
        style.configure("Stop.TButton", font=('SF Pro Text', 10, 'bold'), background="#ff6b6b", foreground="white")
        style.map("Stop.TButton", background=[('active', '#e05252')])
        style.configure("Status.TFrame", background="#e9ecef")
        style.configure("Status.TLabel", background="#e9ecef", font=('SF Pro Text', 9))

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def on_speed_change(self, value):
        self.typing_speed = int(float(value))
        self.speed_label.config(text=f"{self.typing_speed}ms / char")

    def start_typing(self, section_number):
        if self.is_typing:
            self.update_status("⚠️ Already typing. Stop the current task first.")
            return
        self.current_text_section = section_number
        self.typing_thread = threading.Thread(target=self.run_typing_logic, daemon=True)
        self.typing_thread.start()

    def stop_typing(self):
        if not self.is_typing:
            self.update_status("Not currently typing.")
            return
        self.update_status("🛑 Stopping...")
        self.stop_event.set()

    def run_typing_logic(self):
        self.is_typing = True
        self.stop_event.clear()
        
        # Ensure we get text from the correct (main) thread
        text_to_type = self.text_areas[self.current_text_section - 1].get("1.0", tk.END).strip()
        
        if not text_to_type:
            self.update_status(f"Section {self.current_text_section} is empty.")
            self.is_typing = False
            return

        self.update_status("Starting in 3s... Switch to your target window.")
        self.root.after(0, self.progress.start)
        
        for i in range(3, 0, -1):
            if self.stop_event.is_set():
                self.is_typing = False
                self.stop_event.clear()
                self.root.after(0, self.progress.stop)
                self.update_status("Cancelled before start.")
                return
            self.update_status(f"Starting in {i}...")
            time.sleep(1)

        self.update_status(f"⌨️ Typing Section {self.current_text_section}...")
        
        # --- Typing happens here ---
        for char in text_to_type:
            if self.stop_event.is_set():
                break
            self.keyboard_controller.type(char)
            if self.typing_speed > 0:
                time.sleep(self.typing_speed / 1000.0)

        if not self.stop_event.is_set():
            self.update_status(f"✅ Section {self.current_text_section} completed!")
        else:
            self.update_status("🛑 Typing stopped by user.")
            
        self.is_typing = False
        self.stop_event.clear()
        self.root.after(0, self.progress.stop)

    def update_status(self, message):
        self.root.after(0, lambda: self.status_var.set(message))

    # --- Global Hotkey Logic ---
    def setup_global_hotkeys(self):
        self.hotkey_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.hotkey_listener.start()

    def on_key_press(self, key):
        # Add a dedicated check for the Escape key to stop typing
        if key == keyboard.Key.esc:
            if self.is_typing:
                self.root.after(0, self.stop_typing)
            return

        self.current_keys.add(key)
        self.check_hotkey_combination()

    def on_key_release(self, key):
        try:
            self.current_keys.remove(key)
        except KeyError:
            pass

    def check_hotkey_combination(self):
        # Using a set for combination check
        # For Mac: {Key.cmd, Key.shift, 'x'}
        # For Win/Linux: {Key.ctrl, Key.shift, 'x'}
        
        is_ctrl_pressed = Key.ctrl_l in self.current_keys or Key.ctrl_r in self.current_keys
        is_cmd_pressed = Key.cmd in self.current_keys
        is_shift_pressed = Key.shift_l in self.current_keys or Key.shift_r in self.current_keys

        if (is_ctrl_pressed or is_cmd_pressed) and is_shift_pressed:
            if keyboard.KeyCode.from_char('x') in self.current_keys:
                self.root.after(0, self.start_typing, 1)
            elif keyboard.KeyCode.from_char('y') in self.current_keys:
                self.root.after(0, self.start_typing, 2)
            elif keyboard.KeyCode.from_char('z') in self.current_keys:
                self.root.after(0, self.start_typing, 3)
            elif keyboard.KeyCode.from_char('0') in self.current_keys:
                self.root.after(0, self.stop_typing)


    def on_closing(self):
        if self.is_typing:
            self.stop_event.set()
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.root.destroy()

if __name__ == "__main__": 
    main_window = tk.Tk()
    app = AutoTyperGUI(main_window)
    main_window.mainloop()
    


 
