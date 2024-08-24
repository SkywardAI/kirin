# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import pathlib

import decouple
import pydantic
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(BaseSettings):
    TITLE: str = "Kirin Aggregator"
    BACKEND_SERVER_VERSION: str = decouple.config("BACKEND_SERVER_VERSION", cast=str)
    TIMEZONE: str = decouple.config("TIMEZONE", cast=str)
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    BACKEND_SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    BACKEND_SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    BACKEND_SERVER_WORKERS: int = decouple.config("BACKEND_SERVER_WORKERS", cast=int)  # type: ignore
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    # POSTGRES_HOST: str = decouple.config("POSTGRES_HOST", cast=str)  # type: ignore
    # DB_MAX_POOL_CON: int = decouple.config("DB_MAX_POOL_CON", cast=int)  # type: ignore
    # POSTGRES_DB: str = decouple.config("POSTGRES_DB", cast=str)  # type: ignore
    # POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)  # type: ignore
    # DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int)  # type: ignore
    # DB_POOL_OVERFLOW: int = decouple.config("DB_POOL_OVERFLOW", cast=int)  # type: ignore
    # POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)  # type: ignore
    # POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str)  # type: ignore
    # DB_TIMEOUT: int = decouple.config("DB_TIMEOUT", cast=int)  # type: ignore
    # POSTGRES_USERNAME: str = decouple.config("POSTGRES_USERNAME", cast=str)  # type: ignore

    # IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool)  # type: ignore
    # IS_DB_FORCE_ROLLBACK: bool = decouple.config("IS_DB_FORCE_ROLLBACK", cast=bool)  # type: ignore
    # IS_DB_EXPIRE_ON_COMMIT: bool = decouple.config("IS_DB_EXPIRE_ON_COMMIT", cast=bool)  # type: ignore

    API_TOKEN: str = decouple.config("API_TOKEN", cast=str)  # type: ignore
    AUTH_TOKEN: str = decouple.config("AUTH_TOKEN", cast=str)  # type: ignore
    JWT_TOKEN_PREFIX: str = decouple.config("JWT_TOKEN_PREFIX", cast=str)  # type: ignore
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)  # type: ignore
    JWT_SUBJECT: str = decouple.config("JWT_SUBJECT", cast=str)  # type: ignore
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int)  # type: ignore
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int)  # type: ignore
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int)  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",  # React default port
        "http://0.0.0.0:3000",
        "http://127.0.0.1:3000",  # React docker port
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Qwik default port
        "http://0.0.0.0:5173",
        "http://127.0.0.1:5173",  # Qwik docker port
        "http://127.0.0.1:5174",
    ]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    HASHING_ALGORITHM_LAYER_1: str = decouple.config("HASHING_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = decouple.config("HASHING_ALGORITHM_LAYER_2", cast=str)  # type: ignore
    HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str)  # type: ignore
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # type: ignore

    INFERENCE_ENG: str = decouple.config("INFERENCE_ENG", cast=str)  # type: ignore
    INFERENCE_ENG_PORT: int = decouple.config("INFERENCE_ENG_PORT", cast=int)  # type: ignore
    INFERENCE_ENG_VERSION: str = decouple.config("INFERENCE_ENG_VERSION", cast=str)  # type: ignore

    # Configurations for language model
    LANGUAGE_MODEL_NAME: str = decouple.config("LANGUAGE_MODEL_NAME", cast=str)  # type: ignore
    EMBEDDING_MODEL_NAME: str = decouple.config("EMBEDDING_MODEL_NAME", cast=str)  # type: ignore

    # Admin setting
    ADMIN_USERNAME: str = decouple.config("ADMIN_USERNAME", cast=str)  # type: ignore
    ADMIN_EMAIL: str = decouple.config("ADMIN_EMAIL", cast=str)  # type: ignore
    ADMIN_PASS: str = decouple.config("ADMIN_PASS", cast=str)  # type: ignore

    # Configurations for language model
    INSTRUCTION: str = decouple.config("INSTRUCTION", cast=str)  # type: ignore

    NUM_CPU_CORES: float = decouple.config("NUM_CPU_CORES", cast=float)  # type: ignore

    EMBEDDING_ENG: str = decouple.config("EMBEDDING_ENG", cast=str)  # type: ignore
    EMBEDDING_ENG_PORT: int = decouple.config("EMBEDDING_ENG_PORT", cast=int)  # type: ignore
    NUM_CPU_CORES_EMBEDDING: int = decouple.config("NUM_CPU_CORES_EMBEDDING", cast=str)  # type: ignore

    METRICS_PATHS: str = decouple.config("METRICS_PATHS", cast=str)  # type: ignore
    DEFAULT_RAG_DS_NAME: str = decouple.config("DEFAULT_RAG_DS_NAME", cast=str)  # type: ignore

    class Config(pydantic.ConfigDict):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True
        # https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.extra
        # TODO: We need to make sure pydanic is really useful
        # extra='allow'

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.BACKEND_SERVER_VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
