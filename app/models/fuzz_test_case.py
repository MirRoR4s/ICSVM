from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, id_key


class FuzzTestCase(Base):
    """
    模糊测试用例表原型，包含 id、name、desc、suite_id、template_id 列。
    """
    __tablename__ = "sys_fuzz_test_cases"
    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment="模糊测试用例名称")
    description: Mapped[str] = mapped_column(String(100), comment="模糊测试用例描述")
    suite_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_fuzz_test_suites.id", ondelete="SET NULL"), default=None, comment="用例所属套件的id"
    )
    # 用例和套件之间是多对一的关系
    suite: Mapped[Union['FuzzTestSuite', None]] = relationship(init=False, back_populates='cases')
    # 模糊测试用例和模糊测试字段之间是一对多的关系
    fields: Mapped[Union['FuzzTestField', None]] = relationship(init=False, back_populates='case')
    
    
    
    # template_id: Mapped[int | None] = mapped_column(
    #     ForeignKey("sys_fuzz_test_suite_templates.id", ondelete="SET NULL"), default=None, comment="用例所属模板的id"
    # )
    
    
    # template: Mapped[Union['FuzzTestCaseTemplate', None]] = relationship(init=False, back_populates='cases')
    
    # blocks: Mapped[list['Block']] = relationship(init=False, back_populates="case")
    # primitives: Mapped[list['Primitive']] = relationship(init=False, back_populates="case")
    
    # statics: Mapped[list['StaticPrimitive']] = relationship(init=False, back_populates="case")
    # simples: Mapped[list['SimplePrimitive']] = relationship(init=False, back_populates="case")
    # bytes: Mapped[list['BytePrimitive']] = relationship(init=False, back_populates="case")
    # delims: Mapped[list['DelimPrimitive']] = relationship(init=False, back_populates="case")