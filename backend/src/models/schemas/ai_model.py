from src.models.schemas.base import BaseSchemaModel


class AiModel(BaseSchemaModel):
    id: int
    name: str
    des: str


class AiModelInResponse(BaseSchemaModel):
    id: int
    name: str
    des: str


class AiModelInUpdate(BaseSchemaModel):
    name: str | None
    des: str | None


class AiModelChooseResponse(BaseSchemaModel):
    name: str
    msg: str
