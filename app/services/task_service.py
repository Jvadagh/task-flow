from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.base import PaginationParam, SortParam
from app.api.schemas.task_schemas import TaskCreationCommand, UpdateTaskCommand, PartialUpdateTaskCommand
from app.db.models.task_model import Status, TaskModel
from app.db.repository.base import (
    get_entity_by_filters,
    delete_entity,
    update_entity,
    get_list_of_entities,
    create_entity,
)


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, command: TaskCreationCommand) -> TaskModel:
        return await create_entity(
            session=self.session,
            entity=TaskModel(title=command.title, description=command.description, due_date=command.due_date)
        )

    async def retrieve_task(self, id: int) -> TaskModel:
        return await get_entity_by_filters(
            session=self.session,
            entity_type=TaskModel,
            filters=[and_(TaskModel.id == id)]
        )

    async def get_list_of_tasks(
            self,
            status: Status,
            pagination_param: PaginationParam,
            search: str = None,
    ) -> list[TaskModel]:
        filters = []
        if search:
            filters.append(or_(
                TaskModel.title.ilike(f"%{search}%"),
                TaskModel.description.ilike(f"%{search}%")
            ))
        if status:
            filters.append(TaskModel.status == status)

        return await get_list_of_entities(
            session=self.session,
            entity_type=TaskModel,
            filters=filters,
            sort=SortParam(by=[TaskModel.create_time], order="desc"),
            pagination=pagination_param,
        )

    async def delete_task(self, id: int) -> None:
        await delete_entity(session=self.session, entity_type=TaskModel, filters=[and_(TaskModel.id == id)])

    async def update_task(self, id: int, command: UpdateTaskCommand) -> TaskModel:
        return await update_entity(
            session=self.session,
            entity_type=TaskModel,
            filters=[and_(TaskModel.id == id)],
            to_update=command.model_dump(exclude_unset=True)
        )

    async def partial_update_task(self, id: int, command: PartialUpdateTaskCommand) -> TaskModel:
        return await update_entity(
            session=self.session,
            entity_type=TaskModel,
            filters=[and_(TaskModel.id == id)],
            to_update=command.model_dump(exclude_unset=True),
            update_time=False
        )
