import grpc
from concurrent import futures
import logging

from app.infrastructure.grpc import auth_pb2, auth_pb2_grpc


class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    def __init__(self, register_uc, login_uc, validate_uc, logout_uc):
        self.register_uc = register_uc
        self.login_uc = login_uc
        self.validate_uc = validate_uc
        self.logout_uc = logout_uc

    def Register(self, request, context):
        result = self.register_uc.execute(request.email, request.password)
        return auth_pb2.RegisterResponse(
            user_id=result["user_id"],
            created_at=result["created_at"]
        )

    def Login(self, request, context):
        result = self.login_uc.execute(request.email, request.password)
        return auth_pb2.LoginResponse(
            access_token=result["access_token"],
            expires_in=result["expires_in"]
        )

    def ValidateToken(self, request, context):
        result = self.validate_uc.execute(request.token)
        return auth_pb2.ValidateTokenResponse(
            is_valid=result["is_valid"],
            user_id=result.get("user_id", "")
        )

    def Logout(self, request, context):
        result = self.logout_uc.execute(request.token)
        return auth_pb2.LogoutResponse(status=result["status"])


def serve(host, port, register_uc, login_uc, validate_uc, logout_uc):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthServiceServicer(register_uc, login_uc, validate_uc, logout_uc),
        server
    )
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logging.info(f"Auth gRPC server started on {host}:{port}")
    server.wait_for_termination()
