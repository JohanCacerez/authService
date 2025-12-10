import bycrypt
from typing import Union


class PasswordHasher:
    @staticmethod
    def generate_passwordhash(password: Union[str, bytes], rounds: int = 12) -> bytes:
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = bycrypt.gensalt(rounds=rounds)
        hashed = bycrypt.hashpw(password, salt)
        return hashed
    
    @staticmethod
    def verify_password(password: Union[str, bytes], passwordHash: bytes[bytes, str]) -> bool:
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(passwordHash, str):
            hashed = passwordHash.encode('utf-8')
        try:
            return bycrypt.checkpw(password, hashed)
        except ValueError:
            return False