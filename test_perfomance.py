import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def benchmark_aes_performance(data_size_mb):
    # Generate random key and IV for AES-256
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)   # 128-bit IV
    
    # Generate random plaintext data
    plaintext = os.urandom(data_size_mb * 1024 * 1024)  # Convert MB to bytes
    
    # AES setup
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    
    # Padding setup
    padder = padding.PKCS7(128).padder()
    unpadder = padding.PKCS7(128).unpadder()
    
    # Encryption
    start_encrypt_time = time.time()
    encryptor = cipher.encryptor()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    end_encrypt_time = time.time()
    
    # Decryption
    start_decrypt_time = time.time()
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    end_decrypt_time = time.time()
    
    # Verify correctness
    assert decrypted_data == plaintext, "Decryption failed: Data mismatch!"

    # Calculate performance metrics
    encrypt_time = end_encrypt_time - start_encrypt_time
    decrypt_time = end_decrypt_time - start_decrypt_time
    total_data_size = data_size_mb * 1024 * 1024  # In bytes

    print(f"Data Size: {data_size_mb} MB")
    print(f"Encryption Time: {encrypt_time:.4f} seconds ({total_data_size / encrypt_time / 1024 / 1024:.2f} MB/s)")
    print(f"Decryption Time: {decrypt_time:.4f} seconds ({total_data_size / decrypt_time / 1024 / 1024:.2f} MB/s)")

# Run the benchmark
if __name__ == "__main__":
    print("Testing AES Encryption Performance on Windows...")
    benchmark_aes_performance(1)  # Test with 1 MB data
    benchmark_aes_performance(10) # Test with 10 MB data
    benchmark_aes_performance(100) # Test with 100 MB data
