from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from scipy.stats import entropy
import numpy as np
import os

def test_ciphertext_entropy():
    # Setup AES Encryption
    key = os.urandom(32)  # AES-256
    iv = os.urandom(16)
    plaintext = os.urandom(1024 * 1024)  # 1 MB random data
    
    # Encrypt data
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    # Calculate entropy
    ciphertext_bytes = bytearray(ciphertext)
    values, counts = np.unique(ciphertext_bytes, return_counts=True)
    shannon_entropy = entropy(counts, base=2)
    
    print(f"Entropy of Ciphertext: {shannon_entropy:.4f} bits/byte")
    if shannon_entropy >= 7.9:
        print("Strong randomness: Encryption is secure.")
    else:
        print("Low randomness: Possible weakness in encryption.")

test_ciphertext_entropy()
