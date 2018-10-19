import sys
from simplecrypt import decrypt
from base64 import b64encode, b64decode

def desencripta(key, encoded_cipher):
    cipher = b64decode(encoded_cipher)
    return decrypt(key, cipher)