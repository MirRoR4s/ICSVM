#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from fast_captcha import text_captcha
from sqlalchemy import and_, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from .base import CRUDBase
from ..models import Role, User
from ..schemas.user_schema import Avatar, UserRegisterSchema, UpdateUser, UpdateUserRole


class CRUDUser(CRUDBase[User, UserRegisterSchema, UpdateUser]):
    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        """
        Retrieve a user by their ID.

        :param db: The database session.
        :param user_id: The ID of the user to retrieve.
        :return: The user object if found, otherwise None.
        """
        return await self.get_(db, primary_key=user_id)

    async def get_user_by_name(self, db: AsyncSession, username: str) -> User | None:
        """
        Get a user by their username.

        :param db: The database session.
        :param username: The username of the user to retrieve.
        :return: The user object if found, otherwise None.
        """
        user = await db.execute(
            select(self.model).where(self.model.username == username)
        )
        return user.scalars().first()

    async def get_user_by_nickname(
        self, db: AsyncSession, nickname: str
    ) -> User | None:
        user = await db.execute(
            select(self.model).where(self.model.nickname == nickname)
        )
        return user.scalars().first()

    async def update_login_time(
        self, db: AsyncSession, username: str, login_time: datetime
    ) -> int:
        """
        Update the last login time for a user.

        :param db: The database session.
        :param username: The username of the user.
        :param login_time: The login time to be updated.
        :return: The number of rows affected.
        """
        user = await db.execute(
            update(self.model)
            .where(self.model.username == username)
            .values(last_login_time=login_time)
        )
        await db.commit()
        return await user.rowcount

    async def create(self, db: AsyncSession, regitster_data: dict) -> None:
        salt = text_captcha(5)
        regitster_data.update({"salt": salt})
        new_user = self.model(**regitster_data)
        db.add(new_user)

    # async def add(self, db: AsyncSession, obj: AddUser) -> None:
    #     salt = text_captcha(5)
    #     obj.password = await jwt.hash_password(obj.password + salt)
    #     dict_obj = obj.dict(exclude={'roles'})
    #     dict_obj.update({'salt': salt})
    #     new_user = self.model(**dict_obj)
    #     role_list = []
    #     for role_id in obj.roles:
    #         role_list.append(await db.get(Role, role_id))
    #     new_user.roles.extend(role_list)
    #     db.add(new_user)
    #
    # async def update_userinfo(self, db: AsyncSession, input_user: User, obj: UpdateUser) -> int:
    #     user = await db.execute(update(self.model).where(self.model.id == input_user.id).values(**obj.dict()))
    #     return user.rowcount
    #
    # @staticmethod
    # async def update_role(db: AsyncSession, input_user: User, obj: UpdateUserRole) -> None:
    #     # 删除用户所有角色
    #     for i in list(input_user.roles):
    #         input_user.roles.remove(i)
    #     # 添加用户角色
    #     role_list = []
    #     for role_id in obj.roles:
    #         role_list.append(await db.get(Role, role_id))
    #     input_user.roles.extend(role_list)
    #
    # async def update_avatar(self, db: AsyncSession, current_user: User, avatar: Avatar) -> int:
    #     user = await db.execute(update(self.model).where(self.model.id == current_user.id).values(avatar=avatar.url))
    #     return user.rowcount
    #
    # async def delete(self, db: AsyncSession, user_id: int) -> int:
    #     return await self.delete_(db, user_id)
    #
    # async def check_email(self, db: AsyncSession, email: str) -> User | None:
    #     mail = await db.execute(select(self.model).where(self.model.email == email))
    #     return mail.scalars().first()
    #
    # async def reset_password(self, db: AsyncSession, pk: int, password: str, salt: str) -> int:
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == pk).values(password=await jwt.hash_password(password + salt))
    #     )
    #     return user.rowcount
    #
    # async def get_all(self, dept: int = None, username: str = None, phone: str = None, status: int = None) -> Select:
    #     se = (
    #         select(self.model)
    #         .options(selectinload(self.model.dept))
    #         .options(selectinload(self.model.roles).selectinload(Role.menus))
    #         .order_by(desc(self.model.join_time))
    #     )
    #     where_list = []
    #     if dept:
    #         where_list.append(self.model.dept_id == dept)
    #     if username:
    #         where_list.append(self.model.username.like(f'%{username}%'))
    #     if phone:
    #         where_list.append(self.model.phone.like(f'%{phone}%'))
    #     if status is not None:
    #         where_list.append(self.model.status == status)
    #     if where_list:
    #         se = se.where(and_(*where_list))
    #     return se
    #
    # async def get_super(self, db: AsyncSession, user_id: int) -> bool:
    #     user = await self.get_user_by_id(db, user_id)
    #     return user.is_superuser
    #
    # async def get_staff(self, db: AsyncSession, user_id: int) -> bool:
    #     user = await self.get_user_by_id(db, user_id)
    #     return user.is_staff
    #
    # async def get_status(self, db: AsyncSession, user_id: int) -> bool:
    #     user = await self.get_user_by_id(db, user_id)
    #     return user.status
    #
    # async def get_multi_login(self, db: AsyncSession, user_id: int) -> bool:
    #     user = await self.get_user_by_id(db, user_id)
    #     return user.is_multi_login
    #
    # async def set_super(self, db: AsyncSession, user_id: int) -> int:
    #     super_status = await self.get_super(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_superuser=False if super_status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_staff(self, db: AsyncSession, user_id: int) -> int:
    #     staff_status = await self.get_staff(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_staff=False if staff_status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_status(self, db: AsyncSession, user_id: int) -> int:
    #     status = await self.get_status(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(status=False if status else True)
    #     )
    #     return user.rowcount
    #
    # async def set_multi_login(self, db: AsyncSession, user_id: int) -> int:
    #     multi_login = await self.get_multi_login(db, user_id)
    #     user = await db.execute(
    #         update(self.model).where(self.model.id == user_id).values(is_multi_login=False if multi_login else True)
    #     )
    #     return user.rowcount

    async def get_with_relation(
        self, db: AsyncSession, user_id: int = None, username: str = None
    ) -> User | None:
        where = []
        if user_id:
            where.append(self.model.id == user_id)
        if username:
            where.append(self.model.username == username)
        user = await db.execute(
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).joinedload(Role.menus))
            .where(*where)
        )
        return user.scalars().first()


USERDAO: CRUDUser = CRUDUser(User)
