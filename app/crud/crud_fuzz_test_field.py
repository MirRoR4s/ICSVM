
from typing import Sequence
from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from ..models import FuzzTestField
from ..schemas.fuzz_test_field_schema import CreateFieldSchema

class CRUDFuzzTestField(CRUDBase[FuzzTestField, CreateFieldSchema, CreateFieldSchema]):
    """
    TODO
    """
    async def create_field(
        self, db: AsyncSession, case_id: int, name, field_type, attribute: dict
    ) -> None:
        """TODO"""
        primitive = FuzzTestField(attribute=attribute, name=name, type=field_type, case_id=case_id)
        db.add(primitive)

    async def read_field(self, db: AsyncSession, case_id, name: str) -> FuzzTestField | None:
        """TODO"""
        primitive = await db.execute(
            select(self.model).where(self.model.name == name and self.model.case_id == case_id)
        )
        return primitive.scalars().first()

    async def read_fields(self, db: AsyncSession, case_id) -> Sequence[FuzzTestField]:
        fields = await db.execute(
            select(self.model).where(self.model.case_id == case_id)
        )
        return fields.scalars().all()
    
    async def read_variable(self, db: AsyncSession, case_id, variable_name: str) -> FuzzTestField | None:
            primitive = await db.execute(
                select(self.model).where(self.model.name == variable_name and self.model.case_id == case_id)
            )
            return primitive.scalars().first()

    async def update_field(self, db: AsyncSession, case_id, old_name, new_name, new_type, new_attribute) -> int:
        result = await db.execute(
            update(FuzzTestField).where(and_(FuzzTestField.name == old_name, FuzzTestField.case_id == case_id)).values(
                attribute=new_attribute, name=new_name, type=new_type
            )
        )
        return result.rowcount

    async def delete_field(self, db: AsyncSession, case_id, field_name) -> int:
        result = await db.execute(
            delete(FuzzTestField).where(and_(FuzzTestField.name == field_name, FuzzTestField.case_id == case_id))
        )
        return result.rowcount
    
    async def delete_field_by_case_id(self, db: AsyncSession, case_id) -> int:
        result = await db.execute(
            delete(self.model).where(self.model.case_id == case_id)
        )
        return result.rowcount

FUZZTESTFIELDDAO = CRUDFuzzTestField(FuzzTestField)
