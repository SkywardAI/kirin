from src.models.schemas.base import BaseSchemaModel


class AiModel(BaseSchemaModel):
    name: str
    des: str | None


class AiModelInResponse(BaseSchemaModel):
    id: int
    available_models: AiModel


class AiModelInUpdate(BaseSchemaModel):
    name: str | None
    des: str | None
