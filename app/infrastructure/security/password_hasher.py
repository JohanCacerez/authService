import bcrypt
from typing import Union


class PasswordHasher:
    @staticmethod
    def generate_password_hash(password: Union[str, bytes], rounds: int = 12) -> bytes:
        if isinstance(password, str):
            password = password.encode('utf-8')
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password, salt)
        return hashed
    
    @staticmethod
    def verify_password(password: Union[str, bytes], password_hash: Union[bytes, str]) -> bool:
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(password_hash, str):
            password_hash = password_hash.encode('utf-8')
        try:
            return bcrypt.checkpw(password, password_hash)
        except ValueError:
            return False