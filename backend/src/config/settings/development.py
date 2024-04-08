from src.config.settings.base import BackendBaseSettings
from src.config.settings.environment import Environment


class BackendDevSettings(BackendBaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    BACKEND_SERVER_HOST: str
    BACKEND_SERVER_PORT: int
    BACKEND_SERVER_WORKERS: int
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_SCHEMA: str
    POSTGRES_USERNAME: str
    POSTGRES_HOST: str
    POSTGRES_URI: str
    ETCD_AUTO_COMPACTION_MODE: str
    ETCD_AUTO_COMPACTION_RETENTION: str
    ETCD_QUOTA_BACKEND_BYTES: str