import pytest
from app.aplication.usecases.logout_user import LogoutUserUseCase

class FakeRedisRepo:
    def __init__(self):
        self.storage = {}

    def save_token(self, token, user_id):
        self.storage[token] = user_id

    def delete_token(self, token):
        self.storage.pop(token, None)

    def get_user_id(self, token):
        return self.storage.get(token)
    
def test_logout_success():
    repo = FakeRedisRepo()
    repo.save_token("token123", "usuario1")

    usecase = LogoutUserUseCase(repo)
    result = usecase.excecute("token123")

    assert result == "logout_success"
    assert repo.get_user_id("token123") is None

def test_logout_token_missing():
    repo = FakeRedisRepo()
    usecase = LogoutUserUseCase(repo)

    result = usecase.excecute("token123")
    assert result == "logout_success"
    assert repo.get_user_id("token123") is None

def test_logout_empty_token():
    repo = FakeRedisRepo()
    usecase = LogoutUserUseCase(repo)

    with pytest.raises(ValueError):
        usecase.excecute("")