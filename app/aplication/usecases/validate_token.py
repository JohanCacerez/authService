from app.aplication.ports.token_service import TokenService
from app.infrastructure.cahce.redis_token_repository import RedisTokenRepository

class ValidateTokenUseCase:
    def __init__(self, token_service: TokenService, redis_repo: RedisTokenRepository):
        self.token_service = token_service
        self.redis_repo = redis_repo

    def execute(self, token: str):
        if not token:
            raise ValueError("El token es obligatorio")
        
        user_id = self.redis_repo.get_user_id_by_token(token)
        if not user_id:
            raise ValueError("Token inválido o expirado")
        
        validated_user_id = self.token_service.validate_token(token)
        if not validated_user_id:
            raise ValueError("Token inválido")
        
        return validated_user_id