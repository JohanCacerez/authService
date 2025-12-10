from app.infrastructure.cache.redis_token_repository import RedisTokenRepository

class LogoutUserUseCase:
    def __init__(self, redis_repo: RedisTokenRepository):
        self.redis_repo = redis_repo
    
    def execute(self, token: str):
        if not token:
            raise ValueError("El token es requerido para cerrar sesión.")
        
        self.redis_repo.delete_token(token)

        return {"status": "logout_success"}