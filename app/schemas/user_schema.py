from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator

from app.common.enums import StatusType
from .base import CustomPhoneNumber, SchemaBase
from .dept import GetAllDept
from .role import GetAllRole

class UserSchemaBase(SchemaBase):
    username: str
    password: str

class UserRegisterSchema(UserSchemaBase):
    nickname: str
    email: EmailStr = Field(example="user@example.com")


class UserLoginSchema(UserSchemaBase):
    captcha: str


class _UserInfoBase(SchemaBase):
    dept_id: int | None = None
    username: str
    nickname: str
    email: EmailStr = Field(..., example='user@example.com')
    phone: CustomPhoneNumber | None = None


class UpdateUser(_UserInfoBase):
    pass


class UpdateUserRole(SchemaBase):
    roles: list[int]


class Avatar(SchemaBase):
    url: HttpUrl = Field(..., description='头像 http 地址')


class GetUserInfoNoRelation(_UserInfoBase):
    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = None
    id: int
    uuid: str
    avatar: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    is_staff: bool
    is_multi_login: bool
    join_time: datetime = None
    last_login_time: datetime | None = None


class GetAllUserInfo(GetUserInfoNoRelation):
    model_config = ConfigDict(from_attributes=True)

    dept: GetAllDept | None = None
    roles: list[GetAllRole]


class GetCurrentUserInfo(GetAllUserInfo):
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def handel(self, values):
        """处理部门和角色"""
        dept = self.dept
        if dept:
            self.dept = dept.name  # type: ignore
        roles = self.roles
        if roles:
            self.roles = [role.name for role in roles]  # type: ignore
        return values


class ResetPassword(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str
