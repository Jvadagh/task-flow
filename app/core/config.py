from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

PROJECT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    ENVIRONMENT: Literal["PYTEST", "PRODUCTION", "DEVELOPMENT"]

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True
        extra = "allow"


class ProductionEnvironmentSetting(Settings):
    DB_URL: str


class DevelopmentEnvironmentSetting(Settings):
    DB_URL: str
    ALEMBIC_URL: str


base_settings = Settings()

if base_settings.ENVIRONMENT == "DEVELOPMENT":
    settings = DevelopmentEnvironmentSetting()

elif base_settings.ENVIRONMENT == "PRODUCTION":
    settings = ProductionEnvironmentSetting()
