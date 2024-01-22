from typing import Union

from sqlalchemy import ForeignKey, String, JSON, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, id_key


class FuzzTestSuite(Base):
    """
    模糊测试套件表原型，包含 id、name、desc、is_system 列。
    - 模糊测试套件和模糊测试用例是一对多的关系
    - 当套件是被用户选择保存的套件时，需要记录下和该套件关联的模糊测试用例名称
    - 后续可能还会添加一些参数字段
    """
    __tablename__ = "sys_fuzz_test_suites"
    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment="模糊测试套件名称")
    description: Mapped[str] = mapped_column(String(100), comment="模糊测试套件描述")
    is_system: Mapped[bool | None] = mapped_column(Boolean, default=True, comment="是否为系统套件")
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_user.id", ondelete="SET NULL"), default=None, comment="用例所属套件的id"
    )
    is_user_saved: Mapped[bool | None] = mapped_column(
        Boolean, default=False, comment="是否是用户选择保存的套件"
    )
    # cases_name: Mapped[list[str] | None] = mapped_column(JSON(), default=None, comment="该套件关联的模糊测试用例名称列表")
    
    # 测试套件和用户之间是多对一的关系
    user: Mapped[Union['User', None]] = relationship(init=False, back_populates='suites')
    # 测试套件和测试用例之间是一对多的关系
    cases: Mapped[list['FuzzTestCase']] = relationship(init=False, back_populates='suite')

    # name和user id唯一确认一个测试套件
    __table_args__ = (
        UniqueConstraint("name", "user_id", name="name_user_id"),
    )