import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)


import grpc
from app.infrastructure.grpc import auth_pb2, auth_pb2_grpc


def test_register():
    channel = grpc.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    print("=== Register ===")
    response = stub.Register(auth_pb2.RegisterRequest(
        email="test3@mail.com",
        password="123456"
    ))
    print(response)
    return response


def test_login():
    channel = grpc.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    print("=== Login ===")
    response = stub.Login(auth_pb2.LoginRequest(
        email="test3@mail.com",
        password="123456"
    ))
    print(response)
    return response.access_token


def test_validate(token):
    channel = grpc.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    print("=== ValidateToken ===")
    response = stub.ValidateToken(auth_pb2.ValidateTokenRequest(
        token=token
    ))
    print(response)
    return response


def test_logout(token):
    channel = grpc.insecure_channel("localhost:50051")
    stub = auth_pb2_grpc.AuthServiceStub(channel)

    print("=== Logout ===")
    response = stub.Logout(auth_pb2.LogoutRequest(
        token=token
    ))
    print(response)
    return response


if __name__ == "__main__":
    reg = test_register()
    token = test_login()
    test_validate(token)
    test_logout(token)
