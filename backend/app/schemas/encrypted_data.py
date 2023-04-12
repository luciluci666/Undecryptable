from pydantic import BaseModel


class EncryptedData(BaseModel):
    application: str
    username: str 
    password: str
