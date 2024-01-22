
from typing import Sequence

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from models import SystemCaseGroup


class CRUDSystemCaseGroup:
    
    async def read_groups(self, db: AsyncSession) -> Sequence[SystemCaseGroup] | None:
        """
        Read all system case groups from the database.

        :param db: The database session.
        :return: A sequence of SystemCaseGroup objects or None if no groups are found.
        """
        # 读取系统内置的所有模糊测试用例组
        system_groups = await db.execute(select(SystemCaseGroup).order_by(asc(SystemCaseGroup.id)))
        return system_groups.scalars().all()

SYSTEMCASEGROUPDAO = CRUDSystemCaseGroup()
