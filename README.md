# Auth Service (gRPC + Python)

## Descripción

Este microservicio implementa un sistema de autenticación basado en
**gRPC**, utilizando:

- **MongoDB** como base de datos para usuarios\
- **Redis** para invalidación de tokens\
- **JWT** para autenticación\
- Contenedores Docker y `docker-compose`

El servicio ofrece las operaciones:

- **Register**
- **Login**
- **ValidateToken**
- **Logout**

---

## Estructura del Proyecto

    app/
     ├── infrastructure/
     │    ├── grpc/
     │    │     ├── auth_pb2.py
     │    │     ├── auth_pb2_grpc.py
     │    │     └── auth_server.py
     │    ├── config/
     │    │     ├── settings.py
     │    ├── security/
     │    │     ├── password_hasher.py
     │    │     └── jwt_service.py
     │    └── persistence/
     │          └── mongo_user_repository.py
     ├── domain/
     |     └── emtities/
     |            └── user.py
     ├── application/
     │    └── ports/
     |          ├── token_service.py
     |          └──user_repository.py
     |    └──usecases/
     |          ├── login_user.py
     |          ├── logout_user.py
     |          ├── register_user.py
     |          └── validate_token.py
     └── main.py

    scripts/
     └── grpc_client_test.py

    docker-compose.yml
    Dockerfile
    requirements.txt
    auth.proto

---

## Ejecutar el proyecto con Docker

### 1. Crear archivo `.env`

    MONGO_URI=mongodb://mongo:27017/auth_db
    REDIS_HOST=redis
    JWT_SECRET=supersecret
    JWT_EXPIRE_SECONDS=3600

### 2. Levantar el entorno

    docker compose up --build

Esto levanta:

- `auth-service` → gRPC en **0.0.0.0:50051**
- `mongo`
- `redis`

---

## Probar el microservicio

Ejecutar el cliente incluido:

    python scripts/grpc_client_test.py

NOTA: si requiere hacer mas pruebas, debera cambiar el correo dentro del archivo

Este script prueba:

- Registro\
- Login\
- Validación de token\
- Logout

Output esperado:

    === Register ===
    user_id: "..."
    created_at: "..."

    === Login ===
    access_token: "..."
    expires_in: 3600

    === ValidateToken ===
    is_valid: true

    === Logout ===
    status: "logout_success"

---

## auth.proto

```proto
service AuthService {
  rpc Register (RegisterRequest) returns (RegisterResponse);
  rpc Login (LoginRequest) returns (LoginResponse);
  rpc ValidateToken (ValidateTokenRequest) returns (ValidateTokenResponse);
  rpc Logout (LogoutRequest) returns (LogoutResponse);
}
```

---

## Detalles técnicos

### Password hashing

Usa `bcrypt`.

### JWT

- HS256\
- Incluye user_id y expiración\
- Validación/decodificación segura

### Redis

- Almacena tokens invalidados\
- Soporta logout persistente

### Mongo

Colección: `users`\
Campos: `_id`, `email`, `password_hash`, `created_at`.

---

## Requisitos

- Python 3.11\
- Docker / Docker Compose\
- grpcio\
- pymongo\
- redis\
- bcrypt

---

## Detener contenedores

    docker compose down
