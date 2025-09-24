from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.schemas.task_schemas import (
    TaskViewModel,
    UpdateTaskCommand,
    PartialUpdateTaskCommand,
    TaskListViewModel,
    TaskCreationCommand,
    GetListOfTasksParams,
)
from app.db.models import TaskModel
from app.services.factory import task_service_factory
from app.services.task_service import TaskService

task_endpoints = APIRouter(tags=["Tasks"])


@task_endpoints.post(path="/", status_code=HTTPStatus.CREATED, response_model=TaskViewModel)
async def create_task(
        command: TaskCreationCommand,
        task_service: Annotated[TaskService, Depends(task_service_factory)],
) -> TaskModel:
    return await task_service.create_task(command=command)


@task_endpoints.get(path="/", response_model=TaskListViewModel, status_code=HTTPStatus.OK)
async def get_list_of_tasks(
        task_service: Annotated[TaskService, Depends(task_service_factory)],
        query_params: GetListOfTasksParams = Depends(),
) -> TaskListViewModel:
    tasks = await task_service.get_list_of_tasks(
        pagination_param=query_params.pagination, status=query_params.status, search=query_params.search
    )
    return TaskListViewModel(results=tasks)


@task_endpoints.get(path="/{id}", response_model=TaskViewModel, status_code=HTTPStatus.OK)
async def retrieve_task(
        id: int,
        task_service: Annotated[TaskService, Depends(task_service_factory)],
) -> TaskModel:
    return await task_service.retrieve_task(id=id)


@task_endpoints.put(path="/{id}", status_code=HTTPStatus.OK, response_model=TaskViewModel)
async def update_task(
        id: int,
        command: UpdateTaskCommand,
        task_service: Annotated[TaskService, Depends(task_service_factory)],
) -> TaskModel:
    return await task_service.update_task(id=id, command=command)


@task_endpoints.patch(path="/{id}", status_code=HTTPStatus.OK, response_model=TaskViewModel)
async def partial_update_task(
        id: int,
        command: PartialUpdateTaskCommand,
        task_service: Annotated[TaskService, Depends(task_service_factory)],
) -> TaskModel:
    return await task_service.partial_update_task(id=id, command=command)


@task_endpoints.delete(path="/{id}", status_code=HTTPStatus.OK)
async def delete_task(
        id: int,
        task_service: Annotated[TaskService, Depends(task_service_factory)],
) -> None:
    await task_service.delete_task(id=id)
