from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request, BackgroundTasks

# from app.common.jwt import DependsJwtAuth
# from app.common.pagination import DependsPagination, paging_data
# from app.common.permission import RequestPermission
# from app.common.rbac import DependsRBAC
from app.common.response.response_schema import ResponseModel, response_base
from app.database.db_mysql import CurrentSession

# from app.schemas.user_schema import (
#     AddUserParam,
#     AvatarParam,
#     GetCurrentUserInfoDetail,
#     GetUserInfoListDetails,
#     RegisterUserParam,
#     ResetPasswordParam,
#     UpdateUserParam,
#     UpdateUserRoleParam,
# )
from fastapi_limiter.depends import RateLimiter
from app.services.user_service import UserService
from app.utils.serializers import select_as_dict
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema

router = APIRouter()


@router.post("/register", summary="用户注册")
async def user_register(register_data: UserRegisterSchema):
    await UserService.register(register_data=register_data)
    return await response_base.success()


@router.post(
    "/login", summary="用户登录", response_model=ResponseModel, dependencies=[Depends(RateLimiter(times=5, minutes=1))]
)
async def user_login(request: Request, login_data: UserLoginSchema, background_tasks: BackgroundTasks):
    (
        access_token,
        refresh_token,
        access_expire,
        refresh_expire,
        user,
    ) = await UserService().login(
        request=request, obj=login_data, background_tasks=background_tasks
    )
    data = GetLoginToken(
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expire_time=access_expire,
        refresh_token_expire_time=refresh_expire,
        user=user,  # type: ignore
    )
    return await response_base.success(data=data)


#
# @router.post('/add', summary='添加用户', dependencies=[DependsRBAC])
# async def add_user(request: Request, obj: AddUserParam):
#     await UserService.add(request=request, obj=obj)
#     current_user = await UserService.get_userinfo(username=obj.username)
#     data = GetUserInfoListDetails(**await select_as_dict(current_user))
#     return await response_base.success(data=data)
#
#
# @router.post('/password/reset', summary='密码重置', dependencies=[DependsJwtAuth])
# async def password_reset(request: Request, obj: ResetPasswordParam):
#     count = await UserService.pwd_reset(request=request, obj=obj)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.get('/me', summary='获取当前用户信息', dependencies=[DependsJwtAuth], response_model_exclude={'password'})
# async def get_current_userinfo(request: Request):
#     data = GetCurrentUserInfoDetail(**await select_as_dict(request.user))
#     return await response_base.success(data=data)
#
#
# @router.get('/{username}', summary='查看用户信息', dependencies=[DependsJwtAuth])
# async def get_user(username: str):
#     current_user = await UserService.get_userinfo(username=username)
#     data = GetUserInfoListDetails(**await select_as_dict(current_user))
#     return await response_base.success(data=data)
#
#
# @router.put('/{username}', summary='更新用户信息', dependencies=[DependsJwtAuth])
# async def update_userinfo(request: Request, username: str, obj: UpdateUserParam):
#     count = await UserService.update(request=request, username=username, obj=obj)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.put(
#     '/{username}/role',
#     summary='更新用户角色',
#     dependencies=[
#         Depends(RequestPermission('sys:user:role:edit')),
#         DependsRBAC,
#     ],
# )
# async def update_user_role(request: Request, username: str, obj: UpdateUserRoleParam):
#     await UserService.update_roles(request=request, username=username, obj=obj)
#     return await response_base.success()
#
#
# @router.put('/{username}/avatar', summary='更新头像', dependencies=[DependsJwtAuth])
# async def update_avatar(request: Request, username: str, avatar: AvatarParam):
#     count = await UserService.update_avatar(request=request, username=username, avatar=avatar)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.get(
#     '',
#     summary='（模糊条件）分页获取所有用户',
#     dependencies=[
#         DependsJwtAuth,
#         DependsPagination,
#     ],
# )
# async def get_all_users(
#     db: CurrentSession,
#     dept: Annotated[int | None, Query()] = None,
#     username: Annotated[str | None, Query()] = None,
#     phone: Annotated[str | None, Query()] = None,
#     status: Annotated[int | None, Query()] = None,
# ):
#     user_select = await UserService.get_select(dept=dept, username=username, phone=phone, status=status)
#     page_data = await paging_data(db, user_select, GetUserInfoListDetails)
#     return await response_base.success(data=page_data)
#
#
# @router.put('/{pk}/super', summary='修改用户超级权限', dependencies=[DependsRBAC])
# async def super_set(request: Request, pk: int):
#     count = await UserService.update_permission(request=request, pk=pk)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.put('/{pk}/staff', summary='修改用户后台登录权限', dependencies=[DependsRBAC])
# async def staff_set(request: Request, pk: int):
#     count = await UserService.update_staff(request=request, pk=pk)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.put('/{pk}/status', summary='修改用户状态', dependencies=[DependsRBAC])
# async def status_set(request: Request, pk: int):
#     count = await UserService.update_status(request=request, pk=pk)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.put('/{pk}/multi', summary='修改用户多点登录状态', dependencies=[DependsRBAC])
# async def multi_set(request: Request, pk: int):
#     count = await UserService.update_multi_login(request=request, pk=pk)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
#
#
# @router.delete(
#     path='/{username}',
#     summary='用户注销',
#     description='用户注销 != 用户登出，注销之后用户将从数据库删除',
#     dependencies=[
#         Depends(RequestPermission('sys:user:del')),
#         DependsRBAC,
#     ],
# )
# async def delete_user(username: str):
#     count = await UserService.delete(username=username)
#     if count > 0:
#         return await response_base.success()
#     return await response_base.fail()
