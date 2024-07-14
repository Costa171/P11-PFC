from Crypto.Cipher import AES, Blowfish, ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA256
import hashlib, secrets
from tinyec import registry

# Function to encrypt data using XChaCha20
def xchacha20_encrypt(data, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.encrypt(data)

# Function to decrypt data using XChaCha20
def xchacha20_decrypt(encrypted_data, key, nonce):
    cipher = ChaCha20.new(key=key, nonce=nonce)
    return cipher.decrypt(encrypted_data)

# Function to encrypt data using HMAC-SHA-256
def hmac_encrypt(data, key):
    hmac_hash = HMAC.new(key, data, digestmod=SHA256)
    return hmac_hash.digest() + data

# Function to decrypt data using HMAC-SHA-256
def hmac_decrypt(encrypted_data, key):
    hmac_digest = encrypted_data[:32]  # Extract HMAC digest
    data = encrypted_data[32:]  # Extract data without HMAC digest
    hmac_hash = HMAC.new(key, data, digestmod=SHA256)
    if hmac_hash.digest() == hmac_digest:
        return data
    else:
        return b'HMAC verification failed'

# Function to encrypt data using ChaCha20
def chacha20_encrypt(data, key):
    cipher = ChaCha20.new(key=key)
    return cipher.encrypt(data)

# Function to decrypt data using ChaCha20
def chacha20_decrypt(encrypted_data, key):
    cipher = ChaCha20.new(key=key)
    return cipher.decrypt(encrypted_data)

# Function to encrypt data using AES-CTR
def aes_ctr_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_CTR)
    return cipher.encrypt(data)

# Function to decrypt data using AES-CTR
def aes_ctr_decrypt(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_CTR)
    return cipher.decrypt(encrypted_data)

# Function to encrypt data using AES-256
def aes_256_encrypt(data, key):
    iv = get_random_bytes(AES.block_size)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = _pad(data)
    encrypted_data = cipher.encrypt(padded_data)
    return iv + encrypted_data

# Function to decrypt data using AES-256
def aes_256_decrypt(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:])
    return _unpad(decrypted_data)

# Helper functions to pad data to be a multiple of AES block size
def _pad(data):
    block_size = AES.block_size
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length]) * padding_length
    return data + padding

def _unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

