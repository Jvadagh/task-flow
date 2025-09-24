from datetime import date, datetime
from typing import Optional, List
from fastapi import Depends
from pydantic import BaseModel, ConfigDict, Field

from app.api.dependencies.base import PaginationParam, pagination_param
from app.db.models.task_model import Status


class TaskCreationCommand(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None


class UpdateTaskCommand(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None


class PartialUpdateTaskCommand(BaseModel):
    status: Status


class TaskViewModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, )
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Status
    create_time: datetime
    update_time: Optional[datetime] = None


class TaskListViewModel(BaseModel):
    results: List[TaskViewModel]


class GetListOfTasksParams(BaseModel):
    pagination: PaginationParam = Depends(pagination_param)
    status: Optional[Status] = None
    search: Optional[str] = Field(None, max_length=30)
