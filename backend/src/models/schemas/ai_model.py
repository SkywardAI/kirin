from typing import Optional
from src.models.schemas.base import BaseSchemaModel


class AiModelCreate(BaseSchemaModel):
    # id: int | None
    name: str
    des: str

class AiModelCreateResponse(BaseSchemaModel):
    id: int
    name: str
    des: str
    msg: Optional[str] = None

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
