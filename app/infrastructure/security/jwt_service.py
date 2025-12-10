import jwt
import datetime

from app.aplication.ports.token_service import TokenService
from app.infrastructure.config.settings import JWT_SECRET, JWT_EXPIRE_SECONDS

class JWTService(TokenService):

    def generate_token(self, user_id: str):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRE_SECONDS)
        payload = {
            "user_id": user_id,
            "exp": expiration
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return token, JWT_EXPIRE_SECONDS
    
    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None