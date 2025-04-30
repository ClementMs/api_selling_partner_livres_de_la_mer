from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
# Charger la clé publique
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())
# Générer une clé AES aléatoire pour le chiffrement du fichier
aes_key = os.urandom(32)  # Clé AES-256
# Chiffrer la clé AES avec RSA
encrypted_aes_key = public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
# Chiffrer le contenu du fichier avec AES-GCM
iv = os.urandom(12)  # Initialisation vector (IV)
cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv))
encryptor = cipher.encryptor()
with open("message.txt", "rb") as f:
    plaintext = f.read()
ciphertext = encryptor.update(plaintext) + encryptor.finalize()
# Sauvegarde du fichier chiffré
with open("message_encrypted.bin", "wb") as f:
    f.write(encrypted_aes_key + iv + encryptor.tag + ciphertext)
print("✅ Fichier chiffré avec succès !")
