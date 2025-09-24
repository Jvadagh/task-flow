from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database.postgres import get_db


async def task_service_factory(session: Annotated[AsyncSession, Depends(get_db)], ):
    from app.services.task_service import TaskService
    return TaskService(session)
