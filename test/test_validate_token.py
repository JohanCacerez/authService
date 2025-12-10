import pytest

from app.aplication.usecases.validate_token import ValidateTokenUseCase

class FakeTokenService:
    def __init__(self, valid=True):
        self.valid = valid

    def validate_token(self, token):
        return "123" if self.valid else None
    
class FakeRedisRepo:
    def __init__(self, token_active=True):
        self.token_active = token_active
    
    def get_user_id(self, token):
        return "123" if self.token_active else None

def test_validate_token_success():
    token_service = FakeTokenService(valid = True)
    redis_repo = FakeRedisRepo(token_active = True)
    usecase = ValidateTokenUseCase(token_service, redis_repo)
    user_id = usecase.execute("token123")
    assert user_id == "123"

def test_validate_token_not_in_redis():
    token_resvice = FakeTokenService(valid = True)
    redis_repo = FakeRedisRepo(token_active = False)
    usecase = ValidateTokenUseCase(token_resvice, redis_repo)

    with pytest.raises(ValueError):
        usecase.execute("token123")

def test_validate_token_invalid_jwt():
    token_service = FakeTokenService(valid = False)
    redis_repo = FakeRedisRepo(token_active = True)
    usecase = ValidateTokenUseCase(token_service, redis_repo)

    with pytest.raises(ValueError):
        usecase.execute("token123")

def test_validate_not_token():
    token_service = FakeTokenService(valid = True)
    redis_repo = FakeRedisRepo(token_active = True)
    usecase = ValidateTokenUseCase(token_service, redis_repo)
    
    with pytest.raises(ValueError):
        usecase.execute("")