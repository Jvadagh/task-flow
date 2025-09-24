from fastapi import APIRouter
from app.api.endpoints.task_endpoints import task_endpoints

api_router = APIRouter()
api_router.include_router(task_endpoints, prefix='/tasks')
