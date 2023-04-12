from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
import os
import base64
import hashlib


class Encrypter:
    def __init__(self):
        self.SALT = os.getenv("SALT")

    def base64Encoding(self, input):
        dataBase64 = base64.b64encode(input)
        dataBase64P = dataBase64.decode("UTF-8")
        return dataBase64P

    def base64Decoding(self, input):
        return base64.decodebytes(input.encode("ascii"))

    def hash_secret_key(self, secret_key: str):
        return hashlib.sha256(self.SALT.encode() + secret_key.encode()).hexdigest()

    def encrypt(self, secret_key: str, data_to_encrypt: str):
        passwordBytes = self.hash_secret_key(secret_key).encode("ascii")
        salt = get_random_bytes(32)
        PBKDF2_ITERATIONS = 15000
        encryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
        cipher = AES.new(encryptionKey, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(data_to_encrypt.encode("ascii"), AES.block_size))
        ivBase64 = self.base64Encoding(cipher.iv)
        saltBase64 = self.base64Encoding(salt)
        ciphertextBase64 = self.base64Encoding(ciphertext)
        return f"{saltBase64}:{ivBase64}:{ciphertextBase64}"

    def decrypt(self, secret_key: str, encrypted_data: str):
        passwordBytes = self.hash_secret_key(secret_key).encode("ascii")
        data = encrypted_data.split(":")
        salt = self.base64Decoding(data[0])
        iv = self.base64Decoding(data[1])
        ciphertext = self.base64Decoding(data[2])
        PBKDF2_ITERATIONS = 15000
        decryptionKey = PBKDF2(passwordBytes, salt, 32, count=PBKDF2_ITERATIONS, hmac_hash_module=SHA256)
        cipher = AES.new(decryptionKey, AES.MODE_CBC, iv)
        decryptedtext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        decryptedtextP = decryptedtext.decode("UTF-8")
        return decryptedtextP


# to understand how does it work
if __name__ == "__main__":
    encrypter = Encrypter()
    data = encrypter.encrypt(input("input your secret_key: "), input("input text to encrypt: "))
    print(data)
    while True:
        try:
            decryptedtext = encrypter.decrypt(input("Input your secret_key: "), data)
            print("Correct! Your data is: " + decryptedtext)
            break
        except:
            print("Wrong secret_key, try again.")
