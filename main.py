import tkinter as tk
from gui import GUI
from encryption import EncryptionManager
import os


user_directory = os.path.expanduser("~")
draft_book_dir = os.path.join(user_directory, ".DraftBook")


if not os.path.exists(draft_book_dir):
    os.makedirs(draft_book_dir)


note_file_path = os.path.join(draft_book_dir, "notiz.txt")
key_file_path = os.path.join(draft_book_dir, "secret.key")

if __name__ == "__main__":
    root = tk.Tk()
    encryption_manager = EncryptionManager(key_file_path)
    app = GUI(root, encryption_manager, note_file_path)
    root.mainloop()
