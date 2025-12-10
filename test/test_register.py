# tests/test_register.py
import pytest
from app.aplication.usecases.register_user import RegisterUserUseCase
from app.domain.entities.user import User

class FakeUserRepo:
    def __init__(self):
        self.users = {}

    def get_by_email(self, email: str):
        return self.users.get(email)

    def create(self, user: User):
        user.id = "123"
        self.users[user.email] = user
        return user


def test_register_success():
    repo = FakeUserRepo()
    usecase = RegisterUserUseCase(repo)

    user = usecase.execute("test@mail.com", "password123")

    assert user.email == "test@mail.com"
    assert user.id == "123"
    assert user.password_hash != "password123"


def test_register_existing_email():
    repo = FakeUserRepo()
    usecase = RegisterUserUseCase(repo)

    # usuario ya existente
    repo.users["test@mail.com"] = User(
        id="1",
        email="test@mail.com",
        password_hash="xx",
        created_at="2023-01-01T00:00:00Z",
    )

    with pytest.raises(ValueError):
        usecase.execute("test@mail.com", "password123")


def test_register_invalid_fields():
    repo = FakeUserRepo()
    usecase = RegisterUserUseCase(repo)

    with pytest.raises(ValueError):
        usecase.execute("", "pass")

    with pytest.raises(ValueError):
        usecase.execute("email", "")
