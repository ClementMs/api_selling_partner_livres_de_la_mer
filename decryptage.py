from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand
# Charger la clé privée
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
# Lire le fichier chiffré
with open("message_encrypted.bin", "rb") as f:
    encrypted_data = f.read()
# Extraire les parties chiffrées
encrypted_aes_key = encrypted_data[:256]  # Taille de la clé RSA-2048 chiffrée
iv = encrypted_data[256:268]  # 12 octets pour IV
tag = encrypted_data[268:284]  # 16 octets pour le tag GCM
ciphertext = encrypted_data[284:]  # Le reste est le texte chiffré
# Déchiffrer la clé AES avec RSA
aes_key = private_key.decrypt(
    encrypted_aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
# Déchiffrer le fichier avec AES-GCM
cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag))
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()
# Sauvegarde du fichier déchiffré
with open("message_decrypted.txt", "wb") as f:
    f.write(plaintext)
print("✅ Fichier déchiffré avec succès !")
