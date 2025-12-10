import pytest
from app.aplication.usecases.login_user import LoginUserUseCase
from app.domain.entities.user import User
from app.infrastructure.security.password_hasher import PasswordHasher

class FakeUserRepo:
    def __init__(self):
        self.users = {}

    def get_by_email(self, email):
        return self.users.get(email)
    
    def create(self, user):
        self.users[user.email] = user
        return user
    
class FakeTokenService:
    def generate_token(self, user_id):
        return "fake_token", 3600
    
    def valdiate_token(self, token):
        return "123"
    
class FakeRedisRepo:
    def __init__(self):
        self.storage = {}

    def save_token(self, token, user_id):
        self.storage[token] = user_id
    
def test_login_success():
    repo = FakeUserRepo()
    token_service = FakeTokenService()
    redis_repo = FakeRedisRepo()

    password_hash = PasswordHasher.generate_password_hash("contrasenia").decode()
    user = User(id="123", email="email@test.com", password_hash=password_hash, created_at="2025")
    repo.users["email@test.com"] = user

    usecase = LoginUserUseCase(repo, token_service, redis_repo)
    token, expires = usecase.execute("email@test.com", "contrasenia")

    assert token == "fake_token"
    assert redis_repo.storage[token] == "123"

def test_login_wrong_password():
    repo = FakeUserRepo()
    token_service = FakeTokenService()
    redis_repo = FakeRedisRepo()

    repo.users["email@test.com"] = User(
        id="123",
        email="email@test.com",
        password_hash=PasswordHasher.generate_password_hash("contrasenia").decode(),
        created_at="2025"
    )

    usecase = LoginUserUseCase(repo, token_service, redis_repo)

    with pytest.raises(ValueError):
        usecase.execute("email@test.com", "contrasenia_incorrecta")

def test_login_no_user():
    repo = FakeUserRepo()
    token_service = FakeTokenService()
    redis_repo = FakeRedisRepo()

    usecase = LoginUserUseCase(repo, token_service, redis_repo)

    with pytest.raises(ValueError):
        usecase.execute("noemail@test.com", "contrasenia")