# scripts/test_hasher.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.infrastructure.security.password_hasher import PasswordHasher

def main():
    pw = "MiContraseñaMuySegura123!"
    print("Password:", pw)
    hashed = PasswordHasher.generate_password_hash(pw)
    print("Hash (utf8):", hashed.decode())
    assert PasswordHasher.verify_password(pw, hashed)
    print("Verificado OK")
    assert not PasswordHasher.verify_password("otra", hashed)
    print("Rechaza contraseña incorrecta OK")

if __name__ == "__main__":
    main()
