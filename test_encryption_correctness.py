from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def test_encryption_correctness():
    try:
        # Setup Key and IV
        key = os.urandom(32)  # 256-bit key for AES
        iv = os.urandom(16)   # 128-bit Initialization Vector (IV)

        # Sample plaintext
        plaintext = b"Testing AES encryption on Windows!"

        # Pad the plaintext
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # Encrypt the data
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        print(f"Ciphertext (hex): {ciphertext.hex()}")

        # Decrypt the data
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        # Verify correctness
        if decrypted_data == plaintext:
            print("Encryption and decryption successful!")
        else:
            print("Mismatch: Test failed!")
    
    except Exception as e:
        print(f"Error during encryption/decryption test: {e}")

# Run the test
test_encryption_correctness()
