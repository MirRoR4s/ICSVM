from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models import FuzzTestCase
from ..schemas.fuzz_test_case_schema import UpdateCaseSchema, CreateCaseSchema


class CRUDFuzzTestCase(CRUDBase[CreateCaseSchema, CreateCaseSchema, UpdateCaseSchema]):

    async def create_case(
        self, db: AsyncSession, suite_id: int, name: str, desc: str = None
    ) -> None:
        """
        TODO
        """
        case = FuzzTestCase(suite_id=suite_id, name=name, description=desc)
        db.add(case)

    async def read_case(self, db: AsyncSession, case_name: str, suite_id):
        """
        TODO
        """
        case = await db.execute(select(FuzzTestCase).where(
            and_(FuzzTestCase.name == case_name, FuzzTestCase.suite_id == suite_id)
        ))
        return case.scalars().first()
    
    async def read_cases(sel, db: AsyncSession, suite_id: int) -> list[FuzzTestCase]:
        cases = await db.execute(select(FuzzTestCase).where(FuzzTestCase.suite_id == suite_id))
        return cases.scalars().all()
        
    async def update_case(
        self, db: AsyncSession, suite_id: int, old_name: str, new_name: str, new_desc: str = None
    ) -> int:
        """
        TODO
        """
        result = await db.execute(
            update(FuzzTestCase).where(and_(FuzzTestCase.suite_id == suite_id, FuzzTestCase.name == old_name))
            .values(name=new_name, description=new_desc)
        )
        return result.rowcount

    async def delete_case(self, db: AsyncSession, suite_id:int, name: str) -> int:
        """
        TODO
        """

        result = await db.execute(delete(FuzzTestCase).where(
            and_(FuzzTestCase.name == name and FuzzTestCase.suite_id == suite_id)
        ))
        return result.rowcount

FUZZTESTCASEDAO = CRUDFuzzTestCase(CreateCaseSchema)
