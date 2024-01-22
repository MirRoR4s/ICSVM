"""一些辅助身份认证的函数"""
from datetime import datetime, timedelta
from jose import jwt
from asgiref.sync import sync_to_async
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends, Request
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.conf import settings
from app.common.redis import redis_client
from app.models import User
from .timezone import timezone
from ..crud.crud_user import USERDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_SWAGGER)


@sync_to_async
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@sync_to_async
def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    :return: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_token(
    sub: str, expires_delta: timedelta | None = None, multi_login=False
) -> str:
    """
    生成一个加密 token

    代码来自：https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/

    :param sub: The subject/userid of the JWT
    :param expires_delta: token 的时效，默认为 86400 秒
    :param multi_login: 多点登录标志，默认为 False 表示不允许多点登录。
    :return: A tuple containing the generated token and its expiration datetime
    """
    if expires_delta:
        expire = timezone.now() + expires_delta
        expire_seconds = int(expires_delta.total_seconds())
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_EXPIRE_SECONDS
    to_encode = {"exp": expire, "sub": sub}
    token = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)
    if multi_login is False:
        prefix = f"{settings.TOKEN_REDIS_PREFIX}:{sub}:"
        await redis_client.delete_prefix(prefix)
    key = f"{settings.TOKEN_REDIS_PREFIX}:{sub}:{token}"
    await redis_client.setex(key, expire_seconds, token)
    return token


async def create_refresh_token(
    sub: str, expire_time: datetime | None = None, **kwargs
) -> tuple[str, datetime]:
    """
    Generate encryption refresh token, only used to create a new token

    :param sub: The subject/userid of the JWT
    :param expire_time: expiry time
    :return:
    """
    if expire_time:
        expire = expire_time + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
        expire_datetime = timezone.f_datetime(expire_time)
        current_datetime = timezone.now()
        if expire_datetime < current_datetime:
            raise HTTPException(detail="Refresh Token 过期时间无效")
        expire_seconds = int((expire_datetime - current_datetime).total_seconds())
    else:
        expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
        expire_seconds = settings.TOKEN_REFRESH_EXPIRE_SECONDS

    multi_login = kwargs.pop("multi_login", None)
    to_encode = {"exp": expire, "sub": sub, **kwargs}
    refresh_token = jwt.encode(
        to_encode, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM
    )
    if multi_login is False:
        prefix = f"{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:"
        await redis_client.delete_prefix(prefix)
    key = f"{settings.TOKEN_REFRESH_REDIS_PREFIX}:{sub}:{refresh_token}"
    await redis_client.setex(key, expire_seconds, refresh_token)
    return refresh_token, expire


@sync_to_async
def jwt_decode(token: str) -> int:
    """
    解码 JWT token 并返回用户 id
    :param token: JWT token
    :return: 用户 id
    """
    try:
        user_id = int(
            (
                jwt.decode(token, settings.TOKEN_SECRET_KEY, [settings.TOKEN_ALGORITHM])
            ).get("sub")
        )
        if not user_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token 无效！")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token 已过期！")
    except (jwt.JWTError, Exception):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token 无效！")
    return user_id


async def get_user_id_by_token(token: str) -> int:
    """
    返回 token 中包含的用户 id。
    :param token: JWT token
    :return: 用户 id。
    """
    user_id = await jwt_decode(token)
    key = f"{settings.TOKEN_REDIS_PREFIX}:{user_id}:{token}"
    if not await redis_client.get(key):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "token 已过期")
    return user_id


def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> (str, str):
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


async def get_current_user(db: AsyncSession, user_id: int) -> User:
    """
    获取指定 user_id 的用户
    """
    user = await USERDAO.get_with_relation(db, user_id=user_id)
    if not user.status:
        raise HTTPException(detail="用户已锁定")
    if user.dept_id:
        if not user.dept.status:
            raise HTTPException(detail="用户所属部门已锁定")
        if user.dept.del_flag:
            raise HTTPException(detail="用户所属部门已删除")
    if user.roles:
        role_status = [role.status for role in user.roles]
        if all(status == 0 for status in role_status):
            raise HTTPException(detail="用户所属角色已锁定")
    return user


@sync_to_async
def get_token(request: Request) -> str:
    """
    Get token for request header

    :return:
    """
    authorization = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise HTTPException(detail="Token 无效")
    return token


# JWT authorizes dependency injection, which can be used if the interface only
# needs to provide a token instead of RBAC permission control
DependsJwtAuth = Depends(oauth2_schema)
