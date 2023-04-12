from fastapi import Header

from app.schemas import EncryptedData as EncryptedDataSchema
from app.utils import Encrypter

ENCRYPTER = Encrypter()


class EncryptedData:
    async def encrypt_data(data: EncryptedDataSchema, secret: str = Header(title="Secret")):
        encrypted_password = ENCRYPTER.encrypt(secret, data.password)

        return {"encrypted": encrypted_password}
