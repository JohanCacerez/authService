from app.aplication.ports.user_repository import UserRepository
from app.aplication.ports.token_service import TokenService
from app.infrastructure.security.password_hasher import PasswordHasher
from app.infrastructure.cahce.redis_token_repository import RedisTokenRepository

class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, token_service: TokenService, redis_repo: RedisTokenRepository):
        self.user_repo = user_repo
        self.token_service = token_service
        self.redis_repo = redis_repo

    def execute(self, email: str, password: str):
        if not email or not password:
            raise ValueError("Correo y contraseña son requeridos")
        
        user = self.user_repo.get_by_email(email)
        if not user:
            raise ValueError("El usuario no existe")
        
        if not PasswordHasher.verify_password(password, user.password_hash):
            raise ValueError("Contraseña incorrecta")
        
        token, expire_in = self.token_service.generate_token(user.id)
        self.redis_repo.save_token(token, user.id)

        return token, expire_in
