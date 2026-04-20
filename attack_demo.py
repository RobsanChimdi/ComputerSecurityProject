from ecc import generate_keys, get_shared_secret, derive_key, encrypt, decrypt
import os

print("=" * 60)
print("MAN-IN-THE-MIDDLE ATTACK DEMONSTRATION")
print("Showing why authentication is needed with ECDH")
print("=" * 60)

alice_priv, alice_pub = generate_keys()
bob_priv, bob_pub = generate_keys()

mallory_priv, mallory_pub = generate_keys()

print("\n[NORMAL ECDH - NO ATTACKER]")
alice_to_mallory = get_shared_secret(alice_priv, mallory_pub)
mallory_to_alice = get_shared_secret(mallory_priv, alice_pub)
assert alice_to_mallory == mallory_to_alice
print("[!] Alice thinks she's talking to Bob, but she's talking to Mallory!")

mallory_to_bob = get_shared_secret(mallory_priv, bob_pub)
bob_to_mallory = get_shared_secret(bob_priv, mallory_pub)
assert mallory_to_bob == bob_to_mallory
print("[!] Bob thinks he's talking to Alice, but he's talking to Mallory!")

salt = os.urandom(16)
alice_key = derive_key(alice_to_mallory, salt)
bob_key = derive_key(bob_to_mallory, salt)

message = "My password is hunter2"

ciphertext, iv, tag = encrypt(alice_key, message)

mallory_decrypted = decrypt(alice_key, ciphertext, iv, tag)

mallory_new_msg = "Send $1000 to Mallory"
new_ciphertext, new_iv, new_tag = encrypt(bob_key, mallory_new_msg)

print(f"\n[ALICE] Sends: {message}")
print(f"[MALLORY] Intercepts and reads: {mallory_decrypted}")
print(f"[MALLORY] Modifies and forwards: {mallory_new_msg}")

bob_receives = decrypt(bob_key, new_ciphertext, new_iv, new_tag)
print(f"[BOB] Receives: {bob_receives}")

print("\n[CONCLUSION] ECDH alone is vulnerable to MITM attacks!")
print("[SOLUTION] Use digital signatures or certificates to authenticate public keys.")