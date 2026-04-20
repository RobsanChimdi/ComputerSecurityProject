from ecc import generate_keys, get_shared_secret, derive_key, encrypt, decrypt
import time
import os

def benchmark():
    print("=" * 60)
    print("ECC PERFORMANCE BENCHMARK")
    print("=" * 60)

    start = time.time()
    for i in range(100):
        priv, pub = generate_keys()
    keygen_time = time.time() - start
    print(f"\n[KEY GENERATION] 100 pairs: {keygen_time:.3f} seconds")

    alice_priv, alice_pub = generate_keys()
    bob_priv, bob_pub = generate_keys()

    start = time.time()
    for i in range(1000):
        secret = get_shared_secret(alice_priv, bob_pub)
    ecdh_time = time.time() - start
    print(f"[ECDH EXCHANGE] 1000 operations: {ecdh_time:.3f} seconds")

    shared = get_shared_secret(alice_priv, bob_pub)
    salt = os.urandom(16)

    start = time.time()
    for i in range(1000):
        key = derive_key(shared, salt)
    kdf_time = time.time() - start
    print(f"[KEY DERIVATION] 1000 operations: {kdf_time:.3f} seconds")

    aes_key = derive_key(shared, salt)
    message = "x" * 1024

    start = time.time()
    for i in range(1000):
        ct, iv, tag = encrypt(aes_key, message)
    encrypt_time = time.time() - start
    print(f"[AES ENCRYPTION] 1000 * 1KB: {encrypt_time:.3f} seconds")

    ct, iv, tag = encrypt(aes_key, message)
    start = time.time()
    for i in range(1000):
        decrypt(aes_key, ct, iv, tag)
    decrypt_time = time.time() - start
    print(f"[AES DECRYPTION] 1000 * 1KB: {decrypt_time:.3f} seconds")

    print(f"\n[TOTAL THROUGHPUT] {1000 / encrypt_time:.0f} KB/sec encryption")
    print(f"[TOTAL THROUGHPUT] {1000 / decrypt_time:.0f} KB/sec decryption")

if __name__ == "__main__":
    benchmark()