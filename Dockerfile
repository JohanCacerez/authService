# Dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para bcrypt, compilación y openssl
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Asegurar que los paquetes sean tratables como módulos (si no los creaste aún)
RUN mkdir -p app/infrastructure/grpc || true

# Generar stubs gRPC dentro del paquete (auth_pb2.py / auth_pb2_grpc.py)
RUN python -m grpc_tools.protoc \
    -I . \
    --python_out=. \
    --grpc_python_out=. \
    auth.proto


# Exponer puerto gRPC
EXPOSE 50051

# Comando por defecto
CMD ["python", "main.py"]
