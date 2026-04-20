from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def generate_keys():
    private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public = private.public_key()
    return private, public

def sign_message(private_key, message):
    signature = private_key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
    return signature

def verify_signature(public_key, message, signature):
    try:
        public_key.verify(signature, message.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False

def get_shared_secret(private_key, peer_public_key):
    return private_key.exchange(ec.ECDH(), peer_public_key)

def derive_key(shared_secret, salt):
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=salt, info=b'authenticated-channel', backend=default_backend())
    return hkdf.derive(shared_secret)

def encrypt(key, plaintext):
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext, iv, encryptor.tag

def decrypt(key, ciphertext, iv, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()

def main():
    print("=" * 60)
    print("AUTHENTICATED ECC WITH DIGITAL SIGNATURES")
    print("ECDH + ECDSA + AES-256-GCM")
    print("=" * 60)

    alice_priv, alice_pub = generate_keys()
    bob_priv, bob_pub = generate_keys()

    alice_secret = get_shared_secret(alice_priv, bob_pub)
    bob_secret = get_shared_secret(bob_priv, alice_pub)

    assert alice_secret == bob_secret

    salt = os.urandom(16)
    aes_key = derive_key(alice_secret, salt)

    original = "Top secret: Launch codes are 42-87-93"

    ciphertext, iv, tag = encrypt(aes_key, original)

    signature = sign_message(alice_priv, original)

    print(f"\n[SENDER] Original: {original}")
    print(f"[SENDER] Signature: {signature.hex()[:40]}...")

    is_valid = verify_signature(alice_pub, original, signature)
    print(f"[RECEIVER] Signature valid: {is_valid}")

    decrypted = decrypt(aes_key, ciphertext, iv, tag)
    print(f"[RECEIVER] Decrypted: {decrypted}")

    tampered = original + " (modified)"
    is_valid_tampered = verify_signature(alice_pub, tampered, signature)
    print(f"[ATTACKER] Tampered message signature valid: {is_valid_tampered}")

    if is_valid and not is_valid_tampered and original == decrypted:
        print("\n[SUCCESS] Complete authenticated ECC system working!")
        print("- Confidentiality: AES encryption")
        print("- Integrity: GCM authentication")
        print("- Authentication: ECDSA signatures")

if __name__ == "__main__":
    main()