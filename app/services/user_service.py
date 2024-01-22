import random
from fastapi import Request, HTTPException, status

# from sqlalchemy import Select
# from app.common.exception import errors
# from app.common.redis import redis_client
# from app.core.conf import settings
# from app.crud.crud_dept import DeptDao
# from app.crud.crud_role import RoleDao
from app.crud.crud_user import USERDAO
from app.database.db_mysql import async_db_session
from app.models import User
from passlib.context import CryptContext
from asgiref.sync import sync_to_async
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema
from app.common.redis import redis_client
from app.core.conf import settings
from app.utils.timezone import timezone
from app.utils.auth_helper import create_token, hash_password, password_verify
from app.services.login_log_service import LoginLogService


class UserService:
    @staticmethod
    async def register(register_data: UserRegisterSchema) -> None:
        async with async_db_session.begin() as db:
            user = await USERDAO.get_user_by_name(db, register_data.username)
            if user:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "用户已注册")
            nickname = await USERDAO.get_user_by_nickname(db, register_data.nickname)
            if nickname:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "昵称已存在")
            register_data.password = hash_password(register_data.password)
            await USERDAO.create(db, **register_data.model_dump())

    @staticmethod
    async def login(request: Request, login_data: UserLoginSchema) -> str:
        async with async_db_session.begin() as db:
            # 获取对应用户名的 User 对象并与用户传入的账号、密码进行比对，并在比对通过后校验用户账户状态
            user = await USERDAO.get_user_by_name(db, login_data.username)
            if not user:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "用户不存在")
            if not password_verify(login_data.password + user.salt, user.password):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "密码错误")
            if not user.status:
                raise HTTPException(status.HTTP_423_LOCKED, "用户已锁定, 登陆失败")
            # 从 redis 获取验证码并与用户输入的验证码比较
            captcha_code = await redis_client.get(
                f"{settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}"
            )
            if not captcha_code:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "验证码失效，请重新获取")
            if captcha_code.lower() != login_data.captcha:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "验证码错误")
            # 登陆成功，更新登录时间
            await USERDAO.update_login_time(db, login_data.username, timezone.now())
            user_id, is_multi_login = user.id, user.is_multi_login
        return await create_token(user_id, multi_login=is_multi_login)


    @staticmethod
    async def get_user_by_id(user_id: int) -> User:
        """
        获取指定 user_id 的用户
        :param user_id:
        :return:
        """
        async with async_db_session.begin() as db:
            user = await USERDAO.get_with_relation(db, user_id=user_id)
            if not user.status:
                raise HTTPException(status.HTTP_423_LOCKED, "用户已锁定")
            if user.dept_id:
                if not user.dept.status:
                    raise HTTPException(status.HTTP_423_LOCKED, "用户所属部门已锁定")
                if user.dept.del_flag:
                    raise HTTPException(status.HTTP_423_LOCKED, "用户所属部门已删除")
            if user.roles:
                role_status = [role.status for role in user.roles]
                if all(statu == 0 for statu in role_status):
                    raise HTTPException(status.HTTP_423_LOCKED, "用户所属角色已锁定")
            return user

    @staticmethod
    async def is_valid(username, password) -> bool:
        async with async_db_session.begin() as db:
            user = await USERDAO.get_user_by_name(db, username)
            if not user:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "用户不存在")
            elif not password_verify(password + user.salt, user.password):
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "密码错误")
            elif not user.status:
                raise HTTPException(status.HTTP_423_LOCKED, "用户已锁定, 登陆失败")
        return True
