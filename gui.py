import tkinter as tk
from tkinter import messagebox
import time
import os  

class GUI:
    def __init__(self, root, encryption_manager, file_path):
        self.root = root
        self.encryption_manager = encryption_manager
        self.file_path = file_path

        screen_width = root.winfo_screenwidth()
        window_width = 600
        window_height = 50
        x_position = screen_width // 2 + 200
        y_position = 0  

        self.root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
        self.root.overrideredirect(True)
        self.root.configure(bg='#607D8B')
        self.font = ("Arial", 16)

        self.offset_x = 0
        self.offset_y = 0
        self.is_expanded = False
        self.is_fixed = False
        self.original_height = 50
        self.expanded_height = 400

        self.root.bind('<Button-1>', self.click_window)
        self.root.bind('<B1-Motion>', self.drag_window)

        self.time_label = tk.Label(self.root, bg='#607D8B', fg='white', font=self.font)
        self.time_label.pack(side=tk.LEFT, padx=20)
        self.root.after(1000, self.update_clock)

        button_frame = tk.Frame(self.root, bg='#607D8B')
        button_frame.pack(side=tk.RIGHT, padx=10)

        self.fix_button = tk.Button(button_frame, text="📌", command=self.toggle_fix, bg='#607D8B', fg='#000000', borderwidth=0, font=self.font, highlightthickness=0)
        self.fix_button.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(button_frame, text="✖", command=self.close_app, bg='#607D8B', fg='#000000', borderwidth=0, font=self.font, highlightthickness=0)
        close_button.pack(side=tk.LEFT, padx=5)

        self.expand_button = tk.Button(button_frame, text="⮟", command=self.toggle_expand, bg='#607D8B', fg='#000000', borderwidth=0, font=self.font, highlightthickness=0)
        self.expand_button.pack(side=tk.LEFT, padx=5)

        self.text_field = tk.Text(self.root, font=("Arial", 14), wrap=tk.WORD, bg='#EAE0C8')
        self.text_field.pack_forget()

        self.load_notes()

    def click_window(self, event):
        if not self.is_fixed:
            self.offset_x = event.x
            self.offset_y = event.y

    def drag_window(self, event):
        if not self.is_fixed:
            x = self.root.winfo_pointerx() - self.offset_x
            y = self.root.winfo_pointery() - self.offset_y
            self.root.geometry(f'+{x}+{y}')

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.time_label.configure(text=now)
        self.root.after(1000, self.update_clock)

    def close_app(self):
        self.save_notes()
        self.root.destroy()

    def toggle_expand(self):
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()

        if self.is_expanded:
            self.text_field.pack_forget()
            self.root.geometry(f'600x{self.original_height}+{current_x}+{current_y}')
            self.time_label.pack(side=tk.LEFT, padx=20)
            self.expand_button.config(text="⮟")
        else:
            self.time_label.pack_forget()
            self.root.geometry(f'600x{self.expanded_height}+{current_x}+{current_y}')
            self.text_field.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            self.expand_button.config(text="⮝")

        self.is_expanded = not self.is_expanded

    def toggle_fix(self):
        self.is_fixed = not self.is_fixed
        
        if self.is_fixed:
            self.fix_button.config(text="🔒")  
        else:
            self.fix_button.config(text="📌")  

    def save_notes(self):
        try:
            text = self.text_field.get("1.0", tk.END).encode()
            encrypted_text = self.encryption_manager.encrypt(text)
            with open(self.file_path, "wb") as file:
                file.write(encrypted_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving: {e}")

    def load_notes(self):
        if os.path.exists(self.file_path): 
            try:
                with open(self.file_path, "rb") as file:
                    encrypted_text = file.read()
                    decrypted_text = self.encryption_manager.decrypt(encrypted_text).decode()
                    self.text_field.insert(tk.END, decrypted_text)
            except Exception as e:
                messagebox.showerror("Error", f"The saved notes could not be loaded: {e}")
