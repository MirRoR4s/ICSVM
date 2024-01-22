from fastapi import APIRouter
from app.core.conf import settings
from .v1.auth.auth import router as auth_router
from .v1.user_api import router as user_router

v1 = APIRouter(prefix=settings.API_V1_STR)
v1.include_router(auth_router, prefix='/auth', tags=['认证'])
v1.include_router(user_router, prefix='/users', tags=['用户管理'])