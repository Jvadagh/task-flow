from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import api_router
from app.core.config import settings
from app.middlewares.exception_handler import (
    GeneralException,
    exception_handler,
    integrity_error_exception_handler,
    no_result_found_exception_handler,
    validation_exception_handler
)

app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"]
)

if settings.ENVIRONMENT != "DEVELOPMENT":
    app.exception_handler(ValueError)(validation_exception_handler)
    app.exception_handler(NoResultFound)(no_result_found_exception_handler)
    app.exception_handler(GeneralException)(exception_handler)
    app.exception_handler(IntegrityError)(integrity_error_exception_handler)

app.include_router(api_router, prefix='/api')
