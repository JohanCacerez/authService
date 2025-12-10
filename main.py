import logging

from app.infrastructure.persistence.mongo_user_repository import MongoUserRepository
from app.infrastructure.security.jwt_service import JWTService
from app.infrastructure.cache.redis_token_repository import RedisTokenRepository

from app.aplication.usecases.register_user import RegisterUserUseCase
from app.aplication.usecases.login_user import LoginUserUseCase
from app.aplication.usecases.validate_token import ValidateTokenUseCase
from app.aplication.usecases.logout_user import LogoutUserUseCase

from app.infrastructure.grpc.auth_server import serve



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Repos / Adapters reales
    user_repo = MongoUserRepository()
    token_service = JWTService()
    redis_repo = RedisTokenRepository()

    # Casos de uso
    register_uc = RegisterUserUseCase(user_repo)
    login_uc = LoginUserUseCase(user_repo, token_service, redis_repo)
    validate_uc = ValidateTokenUseCase(token_service, redis_repo)
    logout_uc = LogoutUserUseCase(redis_repo)

    # Iniciar servidor gRPC
    serve(
        host="0.0.0.0",
        port=50051,
        register_uc=register_uc,
        login_uc=login_uc,
        validate_uc=validate_uc,
        logout_uc=logout_uc
    )
