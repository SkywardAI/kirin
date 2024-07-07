from src.models.schemas.base import BaseSchemaModel


class ServiceVersionResponse(BaseSchemaModel):
    llamacpp: str | None = None
    milvus : str | None = None
    kirin :str | None = None

