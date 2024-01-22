from typing import Sequence
from sqlalchemy import and_, asc, or_, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from ..models import FuzzTestSuite

from ..schemas.fuzz_test_suite_schema import UpdateSuiteSchema, SuiteSchema


class CRUDFuzzTestSuite(CRUDBase[FuzzTestSuite, SuiteSchema, UpdateSuiteSchema]):
    """
    增删改查模糊测试用例组。

    :param CRUDBase: CRUD基类。
    """
    async def read_suite(self, db: AsyncSession, user_id: int, suite_name: str) -> FuzzTestSuite | None:
            suite = await db.execute(
                select(FuzzTestSuite).where(
                    FuzzTestSuite.name == suite_name and FuzzTestSuite.user_id == user_id
                )
            )
            return suite.scalars().first()
    
    async def read_user_suites(self, db: AsyncSession, user_id) -> Sequence[FuzzTestSuite]:
        groups = await db.execute(
            select(FuzzTestSuite).where(FuzzTestSuite.user_id == user_id).order_by(asc(FuzzTestSuite.id))
        )
        return groups.scalars().all()
        
    async def read_system_suites(self, db: AsyncSession) -> Sequence[FuzzTestSuite]:
        groups = await db.execute(
                select(FuzzTestSuite).where(FuzzTestSuite.is_system == True).order_by(asc(FuzzTestSuite.id))
            )
        return groups.scalars().all()

    async def create_suite(
        self, db, user_id, name, desc=None, is_user_saved=False, is_system=False
        ):
        """TODO"""
        suite = FuzzTestSuite(
            user_id=user_id, name=name, description=desc, is_user_saved=is_user_saved, is_system=is_system
        )
        db.add(suite)
    
    async def update_suite(self, db, user_id, old_name, new_name, new_desc=None) -> int:
        """TODO"""
        suite = await db.execute(
            update(FuzzTestSuite).where(
                FuzzTestSuite.name == old_name and FuzzTestSuite.user_id == user_id).values(
                    name=new_name, description=new_desc
            )
        )
        return suite.rowcount

    async def delete_suite(self, db: AsyncSession, user_id: int, name: str) -> int:
        """TODO"""
        result_proxy = await db.execute(
            delete(FuzzTestSuite).where(and_(FuzzTestSuite.user_id == user_id, FuzzTestSuite.name == name))
        )
        await db.commit()
        return result_proxy.rowcount


FUZZTESTSUITEDAO = CRUDFuzzTestSuite(FuzzTestSuite)
