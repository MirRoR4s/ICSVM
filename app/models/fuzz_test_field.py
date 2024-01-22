"""字段表数据库原型"""
from typing import Union
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, JSON, UniqueConstraint
from .base import Base, id_key


class FuzzTestField(Base):
    """TODO"""
    __tablename__ = "sys_fuzz_test_fields"
    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(64), comment="模糊测试用例字段的名称")
    type: Mapped[str] = mapped_column(String(50), comment="字段类型")
    attribute: Mapped[dict | None] = mapped_column(JSON(), default=None, comment="模糊测试用例字段的属性")
    case_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_fuzz_test_cases.id", ondelete="SET NULL"), default=None, comment="字段所属用例的id"
    )
    case: Mapped[Union['FuzzTestCase', None]] = relationship(init=False, back_populates='fields')
    # case id 和 name 唯一确定一个字段
    __table_args__ = (
        UniqueConstraint("case_id", "name", name="case_id_name"),
    )
