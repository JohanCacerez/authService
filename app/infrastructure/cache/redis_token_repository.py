import redis
from app.infrastructure.config.settings import REDIS_HOST, REDIS_PORT, JWT_EXPIRE_SECONDS

class RedisTokenRepository:

    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def save_token(self, token: str, user_id: str):
        self.client.setex(token, JWT_EXPIRE_SECONDS, user_id)

    def get_user_id_by_token(self, token: str):
        return self.client.get(token)
    
    def delete_token(self, token: str):
        self.client.delete(token)