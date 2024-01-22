"""
FastAPI 中间件，详情参看：

- https://fastapi.tiangolo.com/zh/tutorial/middleware/
- https://fastapi.tiangolo.com/zh/advanced/middleware/
- https://www.starlette.io/authentication/

"""
from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
)
from app.services.user_service import UserService
from app.core.conf import settings

class JWTAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    def __init__(self, secret_key: str, algorithm: str, excluded_routers: list[str]):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.excluded_routers = excluded_routers

    async def authenticate(self, request: Request):
        """
        TODO
        """
        if request.url.path in settings.TOKEN_EXCLUDE:
            print("白名单路径")
            return

        auth = request.headers.get("Authorization")
        if not auth:
            return

        scheme, token = auth.split()
        if scheme.lower() != "bearer":
            return

        # 代码来自：https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # {'exp': 1705656122, 'sub': '1'}
            user_id = jwt.decode(token, self.secret_key, self.algorithm).get("sub")
            user = UserService.get_user_by_id(user_id)
        except JWTError:
            raise credentials_exception
        return AuthCredentials(["authenticated"]), user
