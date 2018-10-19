import sys
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
from getpass import getpass

def decrypt(key, encoded_cipher)
    cipher = b64decode(encoded_cipher)
    return = decrypt(password, cipher)