import tkinter as tk
from gui import GUI
from encryption import EncryptionManager
import os


user_directory = os.path.expanduser("~")
simple_note_dir = os.path.join(user_directory, ".DraftBook")


if not os.path.exists(simple_note_dir):
    os.makedirs(simple_note_dir)


note_file_path = os.path.join(simple_note_dir, "notiz.txt")
key_file_path = os.path.join(simple_note_dir, "secret.key")

if __name__ == "__main__":
    root = tk.Tk()
    encryption_manager = EncryptionManager(key_file_path)
    app = GUI(root, encryption_manager, note_file_path)
    root.mainloop()
