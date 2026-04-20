from ecc import generate_keys, get_shared_secret, derive_key, encrypt, decrypt
import os

print("=" * 60)
print("ELLIPTIC CURVE CRYPTOGRAPHY - ECDH + AES-256-GCM")
print("=" * 60)

alice_priv, alice_pub = generate_keys()
bob_priv, bob_pub = generate_keys()

alice_secret = get_shared_secret(alice_priv, bob_pub)
bob_secret = get_shared_secret(bob_priv, alice_pub)

assert alice_secret == bob_secret

salt = os.urandom(16)
aes_key = derive_key(alice_secret, salt)

message = "Confidential: The meeting is at 3PM in Room 4B."

ciphertext, iv, tag = encrypt(aes_key, message)

decrypted = decrypt(aes_key, ciphertext, iv, tag)

print(f"\n[ALICE] Original: {message}")
print(f"\n[ALICE] Encrypted (hex): {ciphertext.hex()[:80]}...")
print(f"[ALICE] IV: {iv.hex()}")
print(f"[ALICE] Auth Tag: {tag.hex()}")

print(f"\n[BOB] Decrypted: {decrypted}")

if message == decrypted:
    print("\n[SUCCESS] ECDH key exchange and AES encryption working correctly!")
else:
    print("\n[FAILURE] Decryption mismatch!")

print(f"\n[KEYS] ECC Key Size: 256 bits")
print(f"[KEYS] AES Key Size: {len(aes_key) * 8} bits")
print(f"[KEYS] Shared Secret: {alice_secret[:16].hex()}...")