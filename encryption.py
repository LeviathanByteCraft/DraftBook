from cryptography.fernet import Fernet
import os

class EncryptionManager:
    def __init__(self, key_file):
        self.key_file = key_file
        self.key = self.load_key()
        self.cipher = Fernet(self.key)

    def load_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
        else:
            with open(self.key_file, "rb") as f:
                key = f.read()
        return key

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)
