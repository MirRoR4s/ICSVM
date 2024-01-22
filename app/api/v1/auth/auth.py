"""认证接口,包括用户登陆 登出 获取登陆验证码 创建 token 表单登陆等功能"""
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.token import GetSwaggerToken
from app.schemas.user_schema import UserLoginSchema
from app.schemas.response_schema import  response_base
from app.utils.auth_helper import DependsJwtAuth
from app.services.auth_service import AuthService


router = APIRouter()


@router.post('/swagger_login', summary='swagger 表单登录')
async def swagger_login(form_data: OAuth2PasswordRequestForm = Depends()) -> GetSwaggerToken:
    token, user = await AuthService().swagger_login(form_data=form_data)
    return GetSwaggerToken(access_token=token, user=user)  # type: ignore


@router.post('/login', summary='用户登录')
async def login(request: Request, login_data: UserLoginSchema, background_tasks: BackgroundTasks):
    pass

@router.post('/new_token', summary='创建新 token',dependencies=[DependsJwtAuth])
async def create_new_token(request: Request, refresh_token: str):
    pass

@router.post('/logout', summary='用户登出',dependencies=[DependsJwtAuth])
async def logout(request: Request):
    await AuthService.logout(request=request)
    return await response_base.success()