from cryptography.fernet import Fernet
import base64
import hashlib

# This must be fixed across sessions!
SECRET = 'My$ecureP@ssKey123'

def generate_key():
    key = hashlib.sha256(SECRET.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_data(data):
    f = Fernet(generate_key())
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data):
    f = Fernet(generate_key())
    return f.decrypt(encrypted_data).decode()
