from app.aplication.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.security.password_hasher import PasswordHasher

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, email: str, password: str) -> User:
        if not email or not password:
            raise ValueError("Email y contraseña son requeridos")
        
        existing = self.user_repo.get_by_email(email)

        if existing:
            raise ValueError("El usaurio ya existe")
        
        password_hash = PasswordHasher.generate_password_hash(password).decode()

        user = User.create_new(email=email, password_hash=password_hash)

        save_user =self.user_repo.create(user)

        return save_user 